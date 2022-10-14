import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from jobs.parser import Page, Listing, Database
from jobs.helpers import elements


page = Page(area=2, role=96, text='Python', period=1)
links = page.get_links()

for link in links:
    listing = Listing(link, elements)
    data = listing.clean_data()
    database = Database(data)
    database.write_to_db()