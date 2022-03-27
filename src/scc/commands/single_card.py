from scc.commands.portal import card
from somef.cli import cli_get_data
from scc import HiddenPrints
import traceback
import os

def create(repo_url, output):

    try:
        print(f"Extracting metadata from {repo_url}. It may take a while... (depends on repository size).")
        with HiddenPrints():
                metadata = cli_get_data(0.9, False, repo_url)
    except Exception:
        traceback.print_exc()
        print(f"ERROR: Could not extract metadata from {repo_url}")
        exit()
        
    card_view = card.html_view(metadata, embedded=True)
    with open(f"{output}", "w+") as index:
        index.write(card_view)
    print(f'✅ Card generated correctaly and saved in: {os.path.abspath(output)}')