import os
import json
from bs4 import BeautifulSoup
from click import style

from . import metadata
from . import styles

def insert_cards(repo_metadata_dir, soup: BeautifulSoup, embedded = False):

    # Insert CSS rules
    s = styles.styles(embedded)
    soup.style.string += s.get_rules()

    loc = soup.find(id="myCards")
    meta_dir = os.fsencode(repo_metadata_dir)
    
    for file in os.listdir(meta_dir):

        filename = os.fsdecode(file)
        if filename.endswith(".json"): 

            with open(f"{repo_metadata_dir}/{filename}") as json_metadata:
                print(f"Creating card for {filename}")
                repo_metadata = json.load(json_metadata)
                html_component = BeautifulSoup(html_view(repo_metadata, embedded), 'html.parser')
                loc.append(html_component)

def html_view(repo_metadata, embedded):

    s = styles.styles(embedded)
    md = metadata.metadata(repo_metadata, s)

    html_card = f"""
    <article {s.get('card')}>
        <div {s.get('card-row')}>
            <div {s.get('card-col1')}>
                <h4 style="{s.get_global_css()}">{md.title()}</h4>
                <p {s.get('description')}>{md.description()}</p>
            </div>
            <div>
                <img src="{md.logo()}" alt="repo-logo" {s.get('repo-logo')}>
                <div {s.get('recently-updated')} title={md.last_update()}></div>
                <div {s.get(['flex-horizontal','float-right'], custom_css='margin-top: 0.3rem;')} title="Stars">
                    <b>{md.stars()}</b>
                    <img src="repo_icons/star.png" alt="stars" {s.get('repo-icon')}>
                </div>
                <div title="Releases">
                    <a href="{md.url_releases()}" target="_blank" {s.get(['flex-horizontal','float-right'], custom_css='text-decoration: none;')}>
                        <b>{md.n_releases()}</b>
                        <img src="repo_icons/releases.png" alt="releases" {s.get('repo-icon')}>
                    </a>
                </div>
            </div>
        </div>

        <div {s.get('card-row')}>
            <div {s.get('card-col1')}>
                <div {s.get('flex-horizontal')}>
                    {md.html_repo_icons()}
                </div>
            </div>
            <div>
                <div {s.get(['flex-horizontal','float-right','grey-color-svg'])}>
                    {md.html_languages()}
                </div>
            </div>
        </div>
    </article>
    """

    return html_card