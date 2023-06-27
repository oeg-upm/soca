import os
from distutils.dir_util import copy_tree
import shutil
from bs4 import BeautifulSoup
from datetime import datetime
import json
from somef import __version__ as somef_version

from . import card
from . import scripts
from . import metadata
from ... import base_dir, __version__


def generate(repo_metadata_dir, output, title, favicon):

    copy_assets(output)

    # Load html template
    with open(f"{base_dir}/assets/template.html") as template:
        soup = BeautifulSoup(template.read(), features="html.parser")

    cards_and_failed = card.cards_data_dump(repo_metadata_dir)
    cards_data = cards_and_failed[0]
    failed_cards = cards_and_failed[1]
    # Create json with cards data and metadata
    with open(f"{output}/cards_data.json", "w") as cards_data_json:
        json.dump(cards_data ,fp=cards_data_json, indent=4)
        print(f"✅ A total of {len(cards_data)} cards saved in: {os.path.abspath(output)}/cards_data.json")
        #if there are failed cards:
        if (num_failed:=len(failed_cards))>0:
            print('\033[91m' + f"There has been {num_failed} repositories that have failed while creating a card. Check log file" + '\033[0m')
            try:
                log_file = "failed_repos.log"
                with open(f"{output}/" + log_file, "w") as log:
                    for repo_name in failed_cards:
                        log.write(repo_name + "\n")
                        print(f"✅ Log file saved in: {os.path.abspath(output)}/failed_repos.log")
            except:
                Exception("Failed to write Log file")
        else:
            print("With no failures!")
    # Insert extra scripts
    sc = scripts.scripts()
    soup.body.script.string = sc.function_copy_card() + sc.function_tooltip() + sc.functions_modals()

    # Add filter owners
    owners = list_owners(repo_metadata_dir)
    if len(owners) > 1:
        owner_filter = soup.find(id='owner-filter')
        l = '\n'.join([ f'<option value="{owner}">{owner}</option>' for owner in owners ])
        html_parsed = BeautifulSoup(f"""
        <div data-toggle="tooltip" data-placement="bottom" title="Filter by User/Organization"><img src="repo_icons/owner.svg" class="sort-filter-icon grey-color-svg"/></div>
			<select id="owner" class="owner-dropdown">
				<option value="all">All</option>
                {l}
			</select>
        """, 'html.parser')
        owner_filter.append(html_parsed)

    # Insert last updated date
    add_last_updated_date(soup)

    # Insert title
    add_title(soup, title)

    # Insert favicon
    add_favicon(soup, favicon, output)

    # Save index.html
    with open(f"{output}/index.html", "w") as index:
        index.write(str(soup))
        print(f"✅ Portal saved in: {os.path.abspath(output)}/index.html")

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
    shutil.copy(f"{base_dir}/assets/app.js", output)

    # Copy css files
    shutil.copy(f"{base_dir}/assets/soca-card.css", output)
    shutil.copy(f"{base_dir}/assets/styles.css", output)

    # Copy About page
    shutil.copy(f"{base_dir}/assets/about.html", output)
    


def add_last_updated_date(soup):
    loc = soup.find(id="portal-last-updated")
    loc.string = f"Last updated on {datetime.today().strftime('%d/%m/%Y')}"
    loc = soup.find(id="portal-versions")
    loc.append(BeautifulSoup(f"Created with <a href=\"https://github.com/oeg-upm/soca/\" target=\"_blank\">soca</a> {__version__} and <a href=\"https://github.com/KnowledgeCaptureAndDiscovery/somef\" target=\"_blank\">somef</a> {somef_version}"
        ,'html.parser'))
    

def add_title(soup, title):
    loc = soup.find(id="nav-title")
    loc.string = title

def add_favicon(soup, favicon, output):
    # if is not the default ico copy it
    if favicon != 'soca-logo.ico':
        if os.path.exists(favicon):
            shutil.copy(favicon, f"{output}/img")
        else:
            print(f"ERROR: The favicon '{favicon}' does not exist. Falling back to default one.")
            return
    
    favicon_loc = soup.find("link", rel="icon")
    favicon_loc['href'] = f"/img/{favicon}"

def list_owners(repo_metadata_dir):

    owners = []

    for file in os.listdir(os.fsencode(repo_metadata_dir)):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open(f"{repo_metadata_dir}/{filename}") as json_metadata:
                repo_metadata = json.load(json_metadata)
                md = metadata.metadata(repo_metadata_dir, repo_metadata)
                owner = md.owner()
                if owner not in owners:
                    owners.append(owner)

    return owners

    # repo_full_name = (repo_url[19:]).replace("/", "_").replace(".", "-")
    # today = datetime.date.today().strftime("%Y-%m-%d")
    #
    # for file in os.listdir(os.fsencode(repo_metadata_dir)):
    #     filename = os.fsdecode(file)
    #     if filename.endswith(f"_{today}.json"):
    #         with open(f"{repo_metadata_dir}/{filename}") as json_metadata:
    #             repo_metadata = json.load(json_metadata)
    #             md = metadata.metadata(repo_metadata_dir, repo_metadata)
    #             owner = md.owner()
    #             if owner not in owners:
    #                 owners.append(owner)


