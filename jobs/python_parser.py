from .parser import Page, Listing, Database


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


page = Page(area=2, role=96, text='Python', period=1)
links = page.get_links()

for link in links:
    listing = Listing(link, elements)
    data = listing.clean_data()
    database = Database(data)
    database.write_to_db()