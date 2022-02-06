import os
from distutils.dir_util import copy_tree
from bs4 import BeautifulSoup
from datetime import datetime

from . import card
from scc import base_dir


def generate(repo_metadata_dir, output):

    copy_assets(output)

    # Load the template
    with open(f"{base_dir}/assets/template.html") as template:
        soup = BeautifulSoup(template.read(), features="html.parser")

    # Insert cards for each repo
    card.insert_cards(repo_metadata_dir, soup)

    # Insert last updated date
    add_last_updated_date(soup)

    # Save index.html
    with open(f"{output}/index.html", "w") as index:
        index.write(str(soup))

def copy_assets(output):

    # Make output dir
    if not os.path.exists(output):
        os.makedirs(output)

    # Copy all img to destination folder
    copy_tree(f"{base_dir}/assets/img", f"{output}/img")

    # Copy all languague_icons
    copy_tree(f"{base_dir}/assets/language_icons", f"{output}/language_icons")

    # Copy all repo_icons
    copy_tree(f"{base_dir}/assets/repo_icons", f"{output}/repo_icons")

def add_last_updated_date(soup):
    loc = soup.find(id="portal-last-updated")
    loc.string = f"Last updated on {datetime.today().strftime('%d/%m/%Y')}"


