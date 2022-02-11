import os
import json
from bs4 import BeautifulSoup
import htmlmin

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
    md = metadata.metadata(repo_metadata, embedded)

    if not embedded:
        # Instert embedded html data to be able to copy it
        html_copy_embedded = f"""<div class="copy_card_html" style="display: none;" id="{md.repo_url()}"> {html_view(repo_metadata, embedded=True)} </div>"""
        copy_btn = f"""<button class="copy-btn" value="{md.repo_url()}"></button>"""
        tooltip_script = ''
    else:
        html_copy_embedded = ''
        copy_btn = ''
        tooltip_script = """<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
                            <script>$(document).ready(function(){$('[data-toggle="tooltip"]').tooltip();});</script>"""

    html_card = f"""
<style>
*{{margin:0;box-sizing:border-box;color:#3e3e3e;font-family:"Helvetica Neue",Helvetica}}
{s.get_rules()}
.copy-btn:active{{position:relative;top:1px;background-color:#3e3e3e;color:#e0e0e0}}
.copy-btn:hover{{background-color:#e9e9e9}}
.copy-btn{{margin-left: 0.3rem;border:none;height:1.1rem;width:1rem;cursor:pointer;background:url("repo_icons/copy.svg")transparent;background-repeat:no-repeat;background-size: auto;}}
.tooltip{{position:absolute;z-index:1070;display:block;font-style:normal;font-weight:400;line-height:1.42857143;line-break:auto;text-align:left;text-align:start;text-decoration:none;text-shadow:none;text-transform:none;letter-spacing:normal;word-break:normal;word-spacing:normal;word-wrap:normal;white-space:normal;font-size:12px;opacity:0}}
.tooltip.in{{opacity:.9}}
.tooltip.top{{padding:5px 0;margin-top:-3px}}
.tooltip.right{{padding:0 5px;margin-left:3px}}
.tooltip.bottom{{padding:5px 0;margin-top:3px}}
.tooltip.left{{padding:0 5px;margin-left:-3px}}
.tooltip.top .tooltip-arrow{{bottom:0;left:50%;margin-left:-5px;border-width:5px 5px 0;border-top-color:#3e3e3e}}
.tooltip.top-left .tooltip-arrow{{right:5px;bottom:0;margin-bottom:-5px;border-width:5px 5px 0;border-top-color:#3e3e3e}}
.tooltip.top-right .tooltip-arrow{{bottom:0;left:5px;margin-bottom:-5px;border-width:5px 5px 0;border-top-color:#3e3e3e}}
.tooltip.right .tooltip-arrow{{top:50%;left:0;margin-top:-5px;border-width:5px 5px 5px 0;border-right-color:#3e3e3e}}
.tooltip.left .tooltip-arrow{{top:50%;right:0;margin-top:-5px;border-width:5px 0 5px 5px;border-left-color:#3e3e3e}}
.tooltip.bottom .tooltip-arrow{{top:0;left:50%;margin-left:-5px;border-width:0 5px 5px;border-bottom-color:#3e3e3e}}
.tooltip.bottom-left .tooltip-arrow{{top:0;right:5px;margin-top:-5px;border-width:0 5px 5px;border-bottom-color:#3e3e3e}}
.tooltip.bottom-right .tooltip-arrow{{top:0;left:5px;margin-top:-5px;border-width:0 5px 5px;border-bottom-color:#3e3e3e}}
.tooltip-inner{{max-width:200px;padding:3px 8px;color:#e0e0e0;text-align:center;background-color:#3e3e3e;border-radius:4px}}
.tooltip-arrow{{position:absolute;width:0;height:0;border-color:transparent;border-style:solid}}
</style>
    <article {s.get('card')}>
        <div {s.get('card-row')}>
            <div {s.get('card-col1')}>
                <div {s.get('flex-horizontal')}>
                    <a href="{md.repo_url()}" target="_blank" style="text-decoration: none;">
                        <h4 class="title" style="{s.get_global_css()}">{md.title()}</h4>
                    </a>
                    {copy_btn}
                </div>
                <p {s.get('description')}>{md.description()}</p>
            </div>
            <div>
                <img src="{md.logo()}" alt="repo-logo" {s.get('repo-logo')}>
                <div {s.get(['flex-horizontal','float-right'])}>
                    {md.recently_updated()}
                </div>
                <div {s.get(['flex-horizontal','float-right'], custom_css='margin-top: 0.3rem;')} data-toggle="tooltip" data-placement="right" title="Stars">
                    <b>{md.stars()}</b>
                    <img src="{md.icon_star()}" alt="stars" {s.get('repo-icon')}>
                </div>
                <div data-toggle="tooltip" data-placement="right" title="Releases">
                    <a href="{md.url_releases()}" target="_blank" {s.get(['flex-horizontal','float-right'], custom_css='text-decoration: none;')}>
                        <b>{md.n_releases()}</b>
                        <img src="{md.icon_releases()}" alt="releases" {s.get('repo-icon')}>
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
                <div {s.get(['flex-horizontal','float-right'])}>
                    {md.html_languages()}
                </div>
            </div>
        </div>
        {html_copy_embedded}
    </article>
    {tooltip_script}
    """

    return html_card
    return html_card if not embedded else htmlmin.minify(html_card, remove_empty_space=True)