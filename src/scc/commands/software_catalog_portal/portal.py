import os
from distutils.dir_util import copy_tree
from bs4 import BeautifulSoup
from datetime import datetime

from . import card
from . import styles
from . import scripts
from scc import base_dir


def generate(repo_metadata_dir, output):

    copy_assets(output)

    # Load html template
    with open(f"{base_dir}/assets/template.html") as template:
        soup = BeautifulSoup(template.read(), features="html.parser")
        
    # Insert CSS rules
    s = styles.styles()
    soup.style.string += s.rules

    # Insert last updated date
    add_last_updated_date(soup)

    # Create object with cards data and metadata
    cards_data = card.cards_data_dump(repo_metadata_dir)

    # Insert scripts
    sc = scripts.scripts()
    sc.set_card_data(cards_data)
    soup.body.script.string += sc.card_data # let with all cards data
    soup.body.script.string += sc.filtering
    soup.body.script.string += sc.tooltip
    soup.body.script.string += sc.copy_card

    # Save index.html
    with open(f"{output}/index.html", "w") as index:
        index.write(str(soup))
        print(f"Portal saved at {output}/index.html")

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
    
    # Log



def add_last_updated_date(soup):
    loc = soup.find(id="portal-last-updated")
    loc.string = f"Last updated on {datetime.today().strftime('%d/%m/%Y')}"


