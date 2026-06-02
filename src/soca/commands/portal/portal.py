import os
from distutils.dir_util import copy_tree
import shutil
from bs4 import BeautifulSoup
from datetime import datetime
import json
from somef import __version__ as somef_version

from . import card
from . import scripts
from .metadata import Metadata
from ... import base_dir, __version__


#######################Embebido de dashboards

#funcion para insertar de env link dashverse
def add_dashverse_link(soup, target=None):
    import os


    DASHBOARD_ORG_PAGE = "dashboard-org.html"
    DASHBOARD_REPO_PAGE = "dashboard-repo.html"
    
    link_org = soup.find(id="dashverse-org-link")
    link_user = soup.find(id="dashverse-user-link")
    
    if link_org and DASHBOARD_ORG_PAGE:
        link_org["href"] = DASHBOARD_ORG_PAGE

    if link_user and DASHBOARD_REPO_PAGE:
        link_user["href"] = DASHBOARD_REPO_PAGE
            
            
# generación e archivos html del portal
from pathlib import Path
import os

def create_embedded_dashboard_pages(portal_output_dir):
    portal_output_dir = Path(portal_output_dir)

    # URL pública que ve el navegador para cargar Superset
    superset_public_url = os.getenv("SUPERSET_PUBLIC_DOMAIN", "http://host.docker.internal:8088")

    org_dashboard_id = os.getenv("DASHBOARD_ORG_EMBED_ID", "")
    repo_dashboard_id = os.getenv("DASHBOARD_REPO_EMBED_ID", "")

    create_dashboard_page(
        output_file=portal_output_dir / "dashboard-org.html",
        title="SQOO Organization Dashboard",
        dashboard_ref=org_dashboard_id,
        superset_domain=superset_public_url,
    )

    create_dashboard_page(
        output_file=portal_output_dir / "dashboard-repo.html",
        title="SQOO Repository Dashboard",
        dashboard_ref=repo_dashboard_id,
        superset_domain=superset_public_url,
    )


def dashboard_url(superset_domain, dashboard_ref):
    dashboard_ref = (dashboard_ref or "").strip()
    if dashboard_ref.startswith("http://") or dashboard_ref.startswith("https://"):
        base_url = dashboard_ref
    else:
        superset_domain = (superset_domain or "http://host.docker.internal:8088").rstrip("/")
        base_url = f"{superset_domain}/superset/dashboard/{dashboard_ref.strip('/')}/"

    separator = "&" if "?" in base_url else "?"
    return f"{base_url}{separator}standalone=2"


def create_dashboard_page(output_file, title, dashboard_ref, superset_domain):
    iframe_src = dashboard_url(superset_domain, dashboard_ref)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>

  <style>
    body {{
      margin: 0;
      background: #f4f4f4;
      font-family: Arial, sans-serif;
    }}

    header {{
      height: 50px;
      display: flex;
      align-items: center;
      padding: 0 20px;
      background: white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
      box-sizing: border-box;
    }}

    header a {{
      text-decoration: none;
      color: #333;
      font-weight: bold;
    }}

    .dashboard-frame {{
      width: 100vw;
      height: calc(100vh - 50px);
      border: none;
      display: block;
    }}
  </style>
</head>

<body>
  <header>
    <a href="index.html">← Back to Software Catalog</a>
  </header>

  <iframe
    class="dashboard-frame"
    src="{iframe_src}"
    title="{title}"
    allowfullscreen>
  </iframe>
</body>
</html>
"""

    output_file.write_text(html, encoding="utf-8")
#####################################################3

def generate(repo_metadata_dir, output, title, favicon):


        
    copy_assets(output)
    portal_cache_version = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")

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
				<option value="all">All orgs</option>
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
    
    # insertar links dashverse
    create_embedded_dashboard_pages(output)
    add_dashverse_link(soup)

    app_script = soup.find("script", src=lambda src: src and src.startswith("app.js"))
    if app_script:
        version_script = soup.new_tag("script")
        version_script.string = f'window.SOCA_PORTAL_VERSION = "{portal_cache_version}";'
        app_script.insert_before(version_script)
        app_script["src"] = f"app.js?v={portal_cache_version}"

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
                md = Metadata(repo_metadata_dir, repo_metadata)
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
    #             md = Metadata(repo_metadata_dir, repo_metadata)
    #             owner = md.owner()
    #             if owner not in owners:
    #                 owners.append(owner)


