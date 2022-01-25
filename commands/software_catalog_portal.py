import os
from distutils.dir_util import copy_tree
import pathlib
from bs4 import BeautifulSoup
import json

def generate(input, output):

    global base

    # Project base path
    base = str(pathlib.Path(__file__).parent.parent.resolve())
    
    # Make output dir
    if not os.path.exists(output):
        os.makedirs(output)

    # Copy all img to destination folder
    copy_tree(f"{base}/assets/img", f"{output}/img")

    # Copy all languague_icons
    copy_tree(f"{base}/assets/language_icons", f"{output}/language_icons")

    # Copy all repo_icons
    copy_tree(f"{base}/assets/repo_icons", f"{output}/repo_icons")

    # load the template
    with open(f"{base}/assets/template.html") as template:
        soup = BeautifulSoup(template.read(), features="html.parser")

    insert_repo_cards(input, soup)

    # save index.html
    with open(f"{output}/index.html", "w") as index:
        index.write(str(soup))


def insert_repo_cards(input, soup):

    loc = soup.find(id="myCards")
    meta_dir = os.fsencode(input)
    
    for file in os.listdir(meta_dir):

        filename = os.fsdecode(file)
        if filename.endswith(".json"): 

            with open(f"{input}/{filename}") as json_metadata:
                print(f"Creating card for {filename}")
                repo_metadata = json.load(json_metadata)
                html_component = BeautifulSoup(card_view(repo_metadata), 'html.parser')
                loc.append(html_component)



def card_view(metadata):

    def safe_dic(dic, key):
        try:
            return dic[key]
        except:
            return None

    def safe_list(list, i):
        try:
            return list[i]
        except:
            return None

    title = safe_dic(safe_dic(metadata,'name'),'excerpt')

    description = safe_dic(safe_list(safe_dic(metadata,'description'),0),'excerpt')
    description = description if description is not None else ''
    description = description[:200]+'...' if len(description[:200]) == 200 else description

    html_card = f"""
    <article class="card">

        <div class="card-row">
            <div class="card-col1">
                <h4 class="title">{title}</h4>
                <p class="description">{description}</p>
            </div>
            <div class="card-col2">
                <img src="img/github-default.svg" alt="repo-logo" class="repo-logo">
                <div class="recently-updated"></div>
                <div class="flex-horizontal float-right" style="margin-top: 0.3rem;">
                    <p><b>99</b></p>
                    <img src="repo_icons/star.png" alt="stars" class="repo-icon">
                </div>
                <div class="flex-horizontal float-right">
                    <p><b>10.2k</b></p>
                    <img src="repo_icons/watching.png" alt="watching" class="repo-icon">
                </div>
            </div>
        </div>

        <div class="card-row">
            <div class="card-col1">
                <div class="flex-horizontal">
                    <img src="repo_icons/license.png" alt="license" class="repo-icon">
                    <img src="repo_icons/notebook.png" alt="notebook" class="repo-icon">
                    <img src="repo_icons/readme.png" alt="readme" class="repo-icon">
                    <img src="repo_icons/download.png" alt="stars" class="repo-icon">
                    <img src="repo_icons/citation.png" alt="citation" class="repo-icon">
                    <img src="repo_icons/docker.png" alt="docker" class="repo-icon">
                    <img src="repo_icons/paper.png" alt="paper" class="repo-icon">
                    <img src="repo_icons/installation.png" alt="installation" class="repo-icon">
                    <img src="repo_icons/requirements.png" alt="requirements" class="repo-icon">
                </div>
            </div>
            <div class="card-col2">
                <div class="flex-horizontal float-right grey-color-svg">
                    <img src="language_icons/html.svg" alt="html" class="repo-icon">
                    <img src="language_icons/python.svg" alt="python" class="repo-icon">

                </div>
            </div>
        </div>
    
    </article>
"""

    return html_card