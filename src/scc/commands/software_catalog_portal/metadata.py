from matplotlib.pyplot import title
from scc import base_dir
from pathlib import Path
from os import listdir
from os.path import isfile, join
from datetime import datetime
import re
import sys

class metadata(object):

    def __init__(self, repo_metadata, embedded = False):
        self.md = repo_metadata
        self.base = 'https://github.com/dakixr/scc/raw/main/src/scc/assets/' if embedded else ''

    # Assets ####################################################
    def logo(self):
        return f"{self.base}img/github-default.svg"

    def icon_star(self):
        return f"{self.base}repo_icons/star.png"

    def icon_releases(self):
        return f"{self.base}repo_icons/releases.png"
    
    def html_languages(self):

        languages = self.languagues()

        if not languages:
            return ''

        language_icons_dir = Path(base_dir, 'assets', 'language_icons')
        supported_languages = [str(f).removesuffix('.svg').lower() for f in listdir(language_icons_dir) if isfile(join(language_icons_dir, f))]

        html = ''

        for lang in languages:
            if lang in supported_languages:
                html += f"""<img src="{self.base}language_icons/{lang}.svg" 
                                alt="{lang}" class="repo-icon grey-color-svg"
                                data-toggle="tooltip" data-placement="bottom" title="{lang.capitalize()}">"""
        return html

    def copy_btn(self):
        return f"""<button class="copy-btn" 
                   value="{self.repo_url()}" 
                   style="background:url('{self.base}repo_icons/copy.svg')transparent;background-repeat:no-repeat;background-size:auto;">
                   </button>"""

    def html_repo_icons(self):

        html = ''
    
        license = self.license()
        if license:
            html += f"""<a href="{safe_dic(license,'url')}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/license.png" 
                            alt="license" class="repo-icon" 
                            data-toggle="tooltip" data-placement="bottom" title="License: {license['name']}">
                        </a>"""
        
        readme_url = self.readme()
        if readme_url:
            html += f"""<a href="{readme_url}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/readme.png" 
                            alt="readme" class="repo-icon" 
                            data-toggle="tooltip" data-placement="bottom" title="Readme">
                        </a>"""
        
        notebook = self.notebook()
        if notebook:
            html += f"""<img src="{self.base}repo_icons/notebook.png" 
                        alt="notebook" class="repo-icon" 
                        data-toggle="tooltip" data-placement="bottom" title="Notebook">"""

        download_url = self.download_url()
        if download_url:
            html += f"""<a href="{download_url}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/download.png" 
                            alt="download" class="repo-icon" 
                            data-toggle="tooltip" data-placement="bottom" title="Download">
                        </a>"""


        citations = self.citations()
        if citations:
            for citation in citations:
                html += f"""<img src="{self.base}repo_icons/citation.png" 
                            alt="citation" class="repo-icon" 
                            data-toggle="tooltip" data-placement="bottom" title="{citation}">"""
                            
        papers = self.citations()
        if papers:
            for paper in papers:

                link_paper = re.search('url={.*}', paper)
                if link_paper:
                    link_paper = link_paper.group(0)[5:-1]

                doi_paper = re.search('doi={.*}', paper)
                if doi_paper:
                    doi_paper = doi_paper.group(0)[5:-1]
                
                title_paper = re.search('title={.*}', paper)
                if title_paper:
                    title_paper = title_paper.group(0)[7:-2]

                if doi_paper and not link_paper:
                    link_paper = 'https://www.doi.org/' + doi_paper

                if link_paper and 'zenodo' not in link_paper:
                    html += f"""<a href="{link_paper}" target="_blank" class="repo-icon">
                                    <img src="{self.base}repo_icons/paper.png" 
                                    alt="{title_paper}" class="repo-icon" 
                                    data-toggle="tooltip" data-placement="bottom" title="Paper: {title_paper}">
                            </a>"""
            
        docker = self.docker()
        if docker:
            html += f"""<img src="{self.base}repo_icons/docker.png" 
                        alt="docker" class="repo-icon" 
                        data-toggle="tooltip" data-placement="bottom" title="{[str(d) for d in docker]}">"""
        
        installation = self.installation()
        if installation:
            html += f"""<img src="{self.base}repo_icons/installation.png" 
                        alt="installation" class="repo-icon" 
                        data-toggle="tooltip" data-placement="bottom" title="Installation:\n{installation}">"""
        
        requirements = self.requirements()
        if requirements:
            requirements = safe_dic(requirements[0],'excerpt')
            html += f"""<img src="{self.base}repo_icons/requirements.png" 
                        alt="requirements" 
                        class="repo-icon" 
                        data-toggle="tooltip" data-placement="bottom" title="Requirements:\n{requirements}">"""

        return html
    
    def recently_updated(self):

        #TODO: Retreive days_theshold from properties file
        hex_states = [
            {'hex': '#6da862', 'days_threshold': 30},
            {'hex': '#a88d62', 'days_threshold': 90},
            {'hex': '#a86262', 'days_threshold': sys.maxsize}
        ]

        delta = self.last_update_days()

        state_updated = ''
        for state in hex_states:
            if delta < state['days_threshold']:
                state_updated = state['hex']
                break

        return f"""<div class="recently-updated" style="background-color: {state_updated};"
                   data-toggle="tooltip" data-placement="right" 
                   title="Last updated on: {self.last_update().strftime('%d-%m-%Y')}">
                   </div>"""

    # Metadata ##################################################
    def requirements(self):
        return safe_dic(self.md,'requirement')

    def installation(self):
        return safe_dic(safe_list(safe_dic(self.md,'installation'),0),'excerpt')

    def docker(self):
        return safe_dic(safe_dic(self.md,'hasBuildFile'),'excerpt')

    def paper(self):
        return None

    def citations(self):
        all_citations = safe_dic(self.md,'citation')

        if not all_citations:
            return None

        citations = []
        for c in all_citations:
            if c['technique'] == 'Regular expression':
                citations.append(c['excerpt'])
        return citations if len(citations) > 0 else None
        
    def download_url(self):
        return safe_dic(safe_dic(self.md,'downloadUrl'),'excerpt')

    def notebook(self):
        return safe_dic(safe_dic(self.md,'hasExecutableNotebook'),'excerpt')

    def readme(self):
        return safe_dic(safe_dic(self.md,'readme_url'),'excerpt')

    def languagues(self):
        langs = safe_dic(safe_dic(self.md,'languages'),'excerpt')
        if not langs:
            return None
        return [str(lang).lower() for lang in langs]

    def repo_url(self):
        return safe_dic(safe_dic(self.md,'codeRepository'),'excerpt')
            
    def title(self):
        return safe_dic(safe_dic(self.md,'name'),'excerpt')
        
    def description(self):

        all_descriptions = safe_dic(self.md,'description')

        description = None
        if all_descriptions:
            for d in all_descriptions:
                if safe_dic(d,'technique') == 'GitHub API':
                    description = safe_dic(d,'excerpt')
                    break

        if not description:
            description = safe_dic(safe_list(all_descriptions,0),'excerpt')
            if not description:
                description = 'No description available yet.'
            
        return description

    def license(self):
        return safe_dic(safe_dic(self.md,'license'),'excerpt')

    def last_update(self):
        date_modified_str = safe_dic(safe_dic(self.md,'dateModified'),'excerpt')[:-1]
        date_modified = datetime.strptime(date_modified_str, '%Y-%m-%dT%H:%M:%S')

        return date_modified
    
    def last_update_days(self):
        date_of_extraction_str = safe_dic(safe_dic(safe_dic(self.md,'stargazers_count'),'excerpt'),'date')[:-4]
        date_of_extraction = datetime.strptime(date_of_extraction_str, '%a, %d %b %Y %H:%M:%S') 
        last_update = self.last_update()
        return (date_of_extraction - last_update).days

    def stars(self):
        return safe_dic(safe_dic(safe_dic(self.md,'stargazers_count'),'excerpt'),'count')
    
    def n_releases(self):
        rel = safe_dic(safe_dic(self.md,'releases'),'excerpt')
        return len(rel) if rel is not None else 0
    
    def url_releases(self):
        return safe_dic(safe_dic(self.md,'downloadUrl'),'excerpt')
        
    
# Aux ##########################################################
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