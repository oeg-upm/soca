import os
from distutils.dir_util import copy_tree
import shutil
from bs4 import BeautifulSoup
from datetime import datetime
import json

from . import card
from . import scripts
from scc import base_dir


def generate(repo_metadata_dir, output):

    copy_assets(output)

    # Load html template
    with open(f"{base_dir}/assets/template.html") as template:
        soup = BeautifulSoup(template.read(), features="html.parser")

    # Insert last updated date
    add_last_updated_date(soup)

    # Create json with cards data and metadata
    cards_data = card.cards_data_dump(repo_metadata_dir)
    with open(f"{output}/cards_data.json", "w") as cards_data_json:
        json.dump(cards_data ,fp=cards_data_json, indent=4)
        print(f"Cards data saved at {output}/cards_data.json")

    # Insert extra scripts
    sc = scripts.scripts()
    soup.body.script.string = sc.function_copy_card() + sc.function_tooltip()

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

    # Copy app.js
    shutil.copy(f"{base_dir}/assets/app.js", f"{output}")

    # Copy css files
    shutil.copy(f"{base_dir}/assets/scc-card.css", f"{output}")
    shutil.copy(f"{base_dir}/assets/styles.css", f"{output}")
    


def add_last_updated_date(soup):
    loc = soup.find(id="portal-last-updated")
    loc.string = f"Last updated on {datetime.today().strftime('%d/%m/%Y')}"


