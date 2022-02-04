from scc.commands.software_catalog_portal import card, portal
from somef.cli import cli_get_data

def create(repo_url, output):

    try:
        print(f"Extracting metadata from {repo_url}. It may take a while... (depends on repository size).")
        metadata = cli_get_data(0.9, False, repo_url)
    except:
        print(f"ERROR: Could not extract metadata from {repo_url[0]}")
        exit()

    #portal.copy_assets(output)
    card_view = card.html_view(metadata, embedded=True)
    with open(f"{output}.html", "w") as index:
        index.write(card_view)