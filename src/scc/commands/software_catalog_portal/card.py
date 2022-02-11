import os
import json
from bs4 import BeautifulSoup
import htmlmin

from . import metadata
from . import styles

def insert_cards(repo_metadata_dir, soup: BeautifulSoup, embedded = False):

    # Insert CSS rules
    s = styles.styles()
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

    s = styles.styles()
    md = metadata.metadata(repo_metadata, embedded)
    
    tooltip_script = """
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <script>$(document).ready(function(){$('[data-toggle="tooltip"]').tooltip();});</script>"""

    copy_card_script = """
    <script>
    $("button").click(function() {
        var copy_card = document.getElementById($(this).val());
        navigator.clipboard.writeText(copy_card.outerHTML)    
    });
    </script>"""

    html_card = f"""
    <article class="scc-card" id="{md.repo_url()}">
    {f'<style>{s.get_rules()}</style>'+tooltip_script+copy_card_script if embedded else ''}
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
    </article>
    """

    return html_card if not embedded else htmlmin.minify(html_card, remove_empty_space=True)