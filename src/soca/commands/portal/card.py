import os
import json
import htmlmin

from . import metadata
from . import styles
from . import scripts

def cards_data_dump(repo_metadata_dir):

    cards_data = []
#TODO change
    #add possible "final release"
    for file in os.listdir(os.fsencode(repo_metadata_dir)):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open(f"{repo_metadata_dir}/{filename}") as json_metadata:
                print(f"Creating card for '{filename}'")
                repo_metadata = json.load(json_metadata)
                md = metadata.metadata(repo_metadata_dir, repo_metadata)
                citations = md.citations()
                print(md.identifier())
                cards_data.append({
                    'id': md.repo_url(),
                    'html_card': html_view(repo_metadata_dir, repo_metadata, False),
                    'html_card_embedded': html_view(repo_metadata_dir, repo_metadata, True),
                    'name': md.title(),
                    'recently_updated': md.last_update_days(),
                    'stargazersCount': md.stars(),
                    'releases': md.n_releases(),
                    'languages': md.languages(),
                    'description': md.description(),
                    'license': md.license() is not None,
                    'licenseName': md.license()['name'] if md.license() is not None else None,
                    'readmeUrl': md.readme() is not None,
                    'hasExecutableNotebook': md.notebook() is not None,
                    'citation':{
                        'cff': citations['cff'] if 'cff' in citations else None,
                        'bibtex': citations['bibtex'] if 'bibtex' in citations else None,
                        'citation': citations['citation'] if 'citation' in citations else None,
                    } if citations is not None else None,
                    'citationText': citations['citation'] if citations is not None else None,
                    'paper': md.paper() is not None,
                    'hasBuildFile': md.docker() is not None,
                    'installation': md.installation() is not None,
                    'requirement': md.requirements() is not None,
                    'usage': md.usage() is not None,
                    'help': md.help() is not None,
                    'hasDocumentation': md.hasDocumentation() is not None,
                    'hasIdentifier': md.identifier() is not None,
                    'identifierLink': md.identifier() if md.identifier() is not None else None,
                    'repoStatus': md.status() is not None,
                    'acknowledgement': md.acknowledgement() is not None,
                    'downloadUrl': md.downloadUrl() is not None,
                    'isOntology': md.repo_type() == 'ontology',
                    'isWeb': md.repo_type() == 'web',
                    'owner': md.owner()
                })

    print('-'*80)

    return cards_data


def html_view(repo_metadata_dir, repo_metadata, embedded, minify=True):

    s = styles.styles()
    md = metadata.metadata(repo_metadata_dir, repo_metadata, embedded)
    sc = scripts.scripts()

    html_card = f"""
    <article class="soca-card" id="{md.repo_url()}">
        <div class="card-row">
            <div class="card-col">
                <div class="flex-horizontal">
                    <a href="{md.repo_url()}" target="_blank" style="text-decoration: none;">
                        <h4 class="title">{md.title()}</h4>
                    </a>
                    {md.copy_btn()}
                </div>
                <div class="description">{md.html_description()}{md.modal(title = md.title(), body = md.html_description())}</div>
            </div>
            <div>
                <div style="min-height: 6rem;display: flex;align-items: center;justify-content: center;">
                    <a href="{md.repo_url()}" target="_blank" style="text-decoration: none;">
                        <img src="{md.logo()}" alt="repo-logo" class="repo-logo">
                    </a>
                </div>
                <div class="flex-horizontal float-right">
                    {md.html_repo_type()}
                    {md.recently_updated()}
                </div>
                <div class="flex-horizontal float-right" style="margin-top: 0.3rem;" {md.add_tooltip('right','Stars')}>
                    <a href="{md.url_stars()}" target="_blank" class="flex-horizontal float-right" style="text-decoration: none;">
                        <b>{md.stars()}</b>
                        <img src="{md.icon_star()}" alt="stars" class="repo-icon">
                    </a>
                </div>
                <div {md.add_tooltip('right','No releases yet' if md.last_release() == '' else 'Last release: '+ md.last_release())} class="flex-horizontal float-right">
                    <a href="{md.url_releases()}" target="_blank" class="flex-horizontal" style="text-decoration: none;">                        
                        <b>{md.n_releases()}</b>
                        <img src="{md.icon_releases()}" alt="releases" class="repo-icon">
                    </a>
                </div>
            </div>
        </div>

        <div class="card-row">
            <div class="card-col">
                <div class="flex-horizontal ref-repo-icons">
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
    {f'<script>{sc.modals}add_modals();</script>' if embedded else ''}
    {f'<style>{s.rules}</style>' if embedded else ''}
    </article>
    """
    
    return htmlmin.minify(html_card, remove_empty_space=True) if minify else html_card