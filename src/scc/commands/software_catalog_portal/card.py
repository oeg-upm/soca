import os
import json
from bs4 import BeautifulSoup

from . import metadata

def insert_cards(repo_metadata_dir, soup):

    loc = soup.find(id="myCards")
    meta_dir = os.fsencode(repo_metadata_dir)
    
    for file in os.listdir(meta_dir):

        filename = os.fsdecode(file)
        if filename.endswith(".json"): 

            with open(f"{repo_metadata_dir}/{filename}") as json_metadata:
                print(f"Creating card for {filename}")
                repo_metadata = json.load(json_metadata)
                html_component = BeautifulSoup(html_view(repo_metadata), 'html.parser')
                loc.append(html_component)

def html_view(repo_metadata):

    md = metadata.metadata(repo_metadata)

    html_card = f"""
    <article class="card">

        <div class="card-row">
            <div class="card-col1">
                <h4 class="title">{md.title()}</h4>
                <p class="description">{md.description()}</p>
            </div>
            <div class="card-col2">
                <img src="img/github-default.svg" alt="repo-logo" class="repo-logo">
                <div class="recently-updated" title={md.last_update()}></div>
                <div class="flex-horizontal float-right" style="margin-top: 0.3rem;" title="Stars">
                    <p><b>{md.stars()}</b></p>
                    <img src="repo_icons/star.png" alt="stars" class="repo-icon">
                </div>
                <div class="flex-horizontal float-right" title="Releases">
                    <p><b>{md.releases()}</b></p>
                    <img src="repo_icons/releases.png" alt="releases" class="repo-icon">
                </div>
            </div>
        </div>

        <div class="card-row">
            <div class="card-col1">
                <div class="flex-horizontal">
                    {md.html_repo_icons()}
                </div>
            </div>
            <div class="card-col2">
                <div class="flex-horizontal float-right grey-color-svg">
                    {md.html_languages()}
                </div>
            </div>
        </div>
    
    </article>
"""

    return html_card