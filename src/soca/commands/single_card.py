from soca.commands.portal import card
from somef.somef_cli import cli_get_data
from soca import HiddenPrints
import traceback
import os
from html2image import Html2Image

def create(repo_url, output, save_as):

    try:
        print(f"Extracting metadata from {repo_url}. It may take a while... (depends on repository size).")
        with HiddenPrints():
                metadata = cli_get_data(0.9, False, repo_url)
    except Exception:
        traceback.print_exc()
        print(f"ERROR: Could not extract metadata from {repo_url}")
        exit()
        
    card_view = card.html_view('', metadata, embedded=True)

    if save_as == 'html':
        with open(f'{output}.html', "w+") as index:
            index.write(card_view)

    elif save_as == 'png':
        with HiddenPrints():
            hti = Html2Image()
            hti.screenshot(html_str=card_view, save_as=f'{output}.png',size=(511, 297))
    else:
        print(f"ERROR: The save_as '{save_as}' format is not supported.")
        quit()

    print(f'✅ Card generated correctly and saved in: {os.path.abspath(output)}')