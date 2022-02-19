import os
import json
import htmlmin

from . import metadata
from . import styles
from . import scripts

def cards_data_dump(repo_metadata_dir):

    cards_data = []

    for file in os.listdir(os.fsencode(repo_metadata_dir)):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            with open(f"{repo_metadata_dir}/{filename}") as json_metadata:
                print(f"Creating card for {filename}")
                repo_metadata = json.load(json_metadata)
                md = metadata.metadata(repo_metadata)
                cards_data.append({
                    'id': md.repo_url(),
                    'html_card': html_view(repo_metadata, False),
                    'html_card_embedded': html_view(repo_metadata, True),
                    'title': md.title(),
                    'recently_updated': md.last_update_days(),
                    'stars': md.stars(),
                    'releases': md.n_releases(),
                    'languagues': md.languagues(),
                    'description': md.description(),
                    'license': md.license(),
                    'readme': md.readme(),
                    'notebook': md.notebook(),
                    'citation': md.citations(),
                    'paper': md.paper(),
                    'docker': md.docker(),
                    'installation': md.installation(),
                    'requirements': md.requirements()
                })

    return cards_data


def html_view(repo_metadata, embedded, minify=True):

    s = styles.styles()
    md = metadata.metadata(repo_metadata, embedded)
    sc = scripts.scripts()

    html_card = f"""
    <article class="scc-card" id="{md.repo_url()}">
        <div class="card-row">
            <div class="card-col">
                <div class="flex-horizontal">
                    <a href="{md.repo_url()}" target="_blank" style="text-decoration: none;">
                        <h4 class="title">{md.title()}</h4>
                    </a>
                    {md.copy_btn()}
                </div>
                <p class="description">{md.description()}</p>
            </div>
            <div>
                <a href="{md.repo_url()}" target="_blank" style="text-decoration: none;">
                    <img src="{md.logo()}" alt="repo-logo" class="repo-logo">
                </a>
                <div class="flex-horizontal float-right">
                    {md.recently_updated()}
                </div>
                <div class="flex-horizontal float-right" style="margin-top: 0.3rem;" data-toggle="tooltip" data-placement="right" title="Stars">
                    <b>{md.stars()}</b>
                    <img src="{md.icon_star()}" alt="stars" class="repo-icon">
                </div>
                <div data-toggle="tooltip" data-placement="right" title="Releases">
                    <a href="{md.url_releases()}" target="_blank" class="flex-horizontal float-right" style="text-decoration: none;">
                        <b>{md.n_releases()}</b>
                        <img src="{md.icon_releases()}" alt="releases" class="repo-icon">
                    </a>
                </div>
            </div>
        </div>

        <div class="card-row">
            <div class="card-col">
                <div class="flex-horizontal">
                    {md.html_repo_icons()}
                </div>
            </div>
            <div>
                <div class="flex-horizontal float-right">
                    {md.html_languages()}
                </div>
            </div>
        </div>
    {sc.js_dependencies if embedded else ''}
    {f'<script>{sc.tooltip}</script>' if embedded else ''}
    {f'<script>{sc.copy_card}</script>' if embedded else ''}
    {f'<style>{s.rules}</style>' if embedded else ''}
    </article>
    """
    #return html_card
    return htmlmin.minify(html_card, remove_empty_space=True) if minify else html_card