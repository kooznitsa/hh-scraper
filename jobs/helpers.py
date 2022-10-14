headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

months = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
    'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
    'сентября': 9, 'октября': 10, 'ноября': 11,
    'декабря': 12
}

elements = {
    'title': ('h1', {'data-qa': 'vacancy-title'}),
    'address': ('span', {'data-qa': 'vacancy-view-raw-address'}),
    'city': ('p', {'data-qa': 'vacancy-view-location'}),
    'salary': ('span', {'data-qa': 'vacancy-salary-compensation-type-net'}),
    'employer': ('div', {'data-qa': 'vacancy-company__details'}),
    'experience': ('span', {'data-qa': 'vacancy-experience'}),
    'employment_modes': ('p', {'data-qa': 'vacancy-view-employment-mode'}),
    'date': ('p', 'vacancy-creation-time-redesigned'),
    'skills': ('span', 'bloko-tag__section_text'),
    'description': ('div', {'data-qa': 'vacancy-description'}),
}