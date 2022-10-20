from time import sleep
from celery import shared_task

from jobs.parser import Page, Listing, Database
from jobs.helpers import elements


@shared_task
def scrape_jobs():
    page = Page(area=2, role=96, text='Python', period=1)
    links = page.get_links()

    for link in links:
        listing = Listing(link, elements)
        data = listing.clean_data()
        database = Database(data)
        database.write_to_db()
        sleep(5)

while True:
    scrape_jobs()
    sleep(150)