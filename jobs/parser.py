from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import re
from datetime import date

from confidential import DATABASE_CONNECTION
from helpers import headers, months


class Page(object):
    def __init__(self, area, role, text, period):
        self.area = area
        self.role = role
        self.text = text
        self.period = period

    @property
    def page_urls(self):
        return [f'https://spb.hh.ru/search/vacancy?area={self.area}'
                + f'&professional_role={self.role}'
                + f'&search_field=name&search_field=description'
                + f'&text={self.text}'
                + f'&clusters=true&enable_snippets=true&ored_clusters=true'
                + f'&search_period={self.period}'
                + f'&page={num}&hhtm' for num in range(0, 5)]

    def get_links(self):
        links = []
        for page_url in self.page_urls:
            try:
                req = urlopen(Request(url=page_url, headers=headers))
                soup = BeautifulSoup(req, 'html.parser')
                for link in soup.find_all('a', class_='serp-item__title'):
                    links.append(link['href'])
            except Exception as e: 
                print('ERROR IN get_links:', e)
                continue

        print('NUMBER OF LINKS:', len(links))
        return links


class Listing(object):
    def __init__(self, link, elements):
        self.link = link
        self.elements = elements

    def open_link(self):
        try:
            req = Request(url=self.link, headers=headers)
            return BeautifulSoup(urlopen(req), 'html.parser')
        except: return

    def scrape_data(self):
        soup = self.open_link()
        if soup:
            scraped = {'url': [self.link]}
            for k, v in self.elements.items():
                try:
                    scraped[k] = list(set(i.get_text() for i in soup.find_all(v[0], attrs=v[1])))
                except: scraped[k] = None
            print('DATA SCRAPED:', self.link)
            return scraped

    def convert_date(self, text):
        ints = [months[m] if m in months else m for m in text.rstrip().split(' ')]
        ints = list(map(int, ints))
        return date(ints[2], ints[1], ints[0]).isoformat()    

    def clean_data(self):
        data = self.scrape_data()
        del_hardspace = lambda x: x.replace(u'\xa0', u' ')
        data = {k: list(map(del_hardspace, v)) for k, v in data.items()}
        data = {k: ''.join(v) if len(v) < 2 else v for k, v in data.items()}

        def parse_city():
            if data['city'] == '':
                data['city'] = data['address'].split(',')[0] if data['address'] else None
            return data['city']

        def parse_date():
            data['date'] = data['date'].rsplit('Вакансия опубликована ', 1)[1] \
                                .rsplit('в ', 1)[0] if data['date'] else None
            data['date'] = self.convert_date(data['date'])
            return data['date']

        def parse_employment():
            data['employment_modes'] = data['employment_modes'].lower().split(', ')
            return data['employment_modes']

        def parse_salary():
            split_salary = lambda x, y: int(re.search(r'\d+', x.rsplit(y, 1)[1]).group()) if x else None
            try: data['salary_from'] = split_salary(data['salary'], 'от')
            except: data['salary_from'] = None
            try: data['salary_to'] = split_salary(data['salary'], 'до')
            except: data['salary_to'] = None
            
            stopwords = ['от', 'до', 'руб.']
            filtered = lambda x: x.lower() not in stopwords and not x.isdigit()
            data['salary_mode'] = ' '.join(filter(filtered, data['salary'].split()))

            return data['salary_from'], data['salary_to'], data['salary_mode']

        parse_city()
        parse_date()
        parse_employment()
        parse_salary()

        print('DATA CLEANED:', self.link)

        return data


class Connection(object):  
    def __init__(self):
        self.connection = psycopg2.connect(**DATABASE_CONNECTION)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

        print('CONNECTION ESTABLISHED')

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type and exc_value:
            self.connection.rollback()
        self.cursor.close()
        self.connection.close()
        print('CONNECTION CLOSED')
        return False


class Database(object):
    def __init__(self, data):
        self.data = data

    def write_to_db(self): 
        with Connection() as cursor:
            cursor.execute('SELECT DISTINCT url FROM jobs;')
            old_urls = [i[0].rstrip() for i in cursor.fetchall()]
            
            if self.data['url'] in old_urls:
                print('URL found in the database')
                return
            
            else:
                query1 = """
                    WITH ins1 AS (
                        INSERT INTO cities (city)
                        VALUES (%s)
                        ON CONFLICT (city) DO UPDATE
                        SET city = excluded.city
                        RETURNING id AS city_id
                        ),

                        ins2 AS (
                        INSERT INTO employers (city_id, employer)
                        VALUES ((SELECT city_id FROM ins1), %s)
                        ON CONFLICT (employer) DO UPDATE
                        SET employer = excluded.employer
                        RETURNING id AS employer_id
                        ),

                        ins3 AS (
                        INSERT INTO addresses (city_id, employer_id, address)
                        VALUES ((SELECT city_id FROM ins1), (SELECT employer_id FROM ins2), %s)
                        ON CONFLICT (address) DO UPDATE
                        SET address = excluded.address
                        RETURNING id AS address_id
                        ),

                        ins4 AS (
                        INSERT INTO salary_modes (salary_mode)
                        VALUES (%s)
                        ON CONFLICT (salary_mode) DO UPDATE
                        SET salary_mode = excluded.salary_mode
                        RETURNING id AS salary_mode_id
                        ),

                        ins5 AS (
                        INSERT INTO experiences (experience)
                        VALUES (%s)
                        ON CONFLICT (experience) DO UPDATE
                        SET experience = excluded.experience
                        RETURNING id AS experience_id
                        )

                    INSERT INTO jobs (url, title, salary_from, salary_to, salary_mode_id, address_id, experience_id, employer_id, date, description)
                    VALUES (%s, %s, %s, %s, (SELECT salary_mode_id FROM ins4), (SELECT address_id FROM ins3), (SELECT experience_id FROM ins5), (SELECT employer_id FROM ins2), %s, %s)
                    ON CONFLICT (url) DO NOTHING
                    RETURNING id AS job_id;
                """
                cursor.execute(query1, (
                        self.data['city'], 
                        self.data['employer'], 
                        self.data['address'], 
                        self.data['salary_mode'],
                        self.data['experience'],
                        self.data['url'], 
                        self.data['title'], 
                        self.data['salary_from'], 
                        self.data['salary_to'], 
                        self.data['date'], 
                        self.data['description']))

                listing_id = cursor.fetchone()[0]

                query2 = """
                    WITH ins7 AS (
                        INSERT INTO employment_modes (employment_mode)
                        VALUES (%s)
                        ON CONFLICT (employment_mode) DO UPDATE
                        SET employment_mode = excluded.employment_mode
                        RETURNING id AS employment_mode_id
                        )

                    INSERT INTO job_employment_modes (job_id, employment_mode_id)
                    VALUES (%s, (SELECT employment_mode_id FROM ins7));
                """
                for emp_mode in self.data['employment_modes']:
                    cursor.execute(query2, (emp_mode, listing_id))
                        
                query3 = """
                    WITH ins9 AS (
                        INSERT INTO skills (skill)
                        VALUES (%s)
                        ON CONFLICT (skill) DO UPDATE
                        SET skill = excluded.skill
                        RETURNING id as skill_id
                        )

                    INSERT INTO job_skills (job_id, skill_id)
                    VALUES (%s, (SELECT skill_id FROM ins9));
                """
                for skill in self.data['skills']:
                    cursor.execute(query3, (skill, listing_id))

                print('DATA INSERTED:', self.data['url'])
        return