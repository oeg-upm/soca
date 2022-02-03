from scc import base_dir
from pathlib import Path
from os import listdir
from os.path import isfile, join

class metadata(object):

    def __init__(self, repo_metadata):
        self.md = repo_metadata
    
    def title(self):
        return safe_dic(safe_dic(self.md,'name'),'excerpt')
        
    def description(self):
        description = safe_dic(safe_list(safe_dic(self.md,'description'),0),'excerpt')
        description = description if description is not None else 'No description available yet.'
        return description

    def last_update(self):
        date_modified = safe_dic(safe_dic(self.md,'dateModified'),'excerpt')
        return date_modified

    def stars(self):
        return safe_dic(safe_dic(safe_dic(self.md,'stargazers_count'),'excerpt'),'count')
    
    def n_releases(self):
        rel = safe_dic(safe_dic(self.md,'releases'),'excerpt')
        return len(rel) if rel is not None else 0
    
    def url_releases(self):
        return safe_dic(safe_dic(self.md,'downloadUrl'),'excerpt')

    def html_languages(self):

        languages = safe_dic(safe_dic(self.md,'languages'),'excerpt')

        if not languages:
            return ''

        language_icons_dir = Path(base_dir, 'assets', 'language_icons')
        supported_languages = [str(f).removesuffix('.svg').lower() for f in listdir(language_icons_dir) if isfile(join(language_icons_dir, f))]

        html = ''

        for lang in languages:
            lang = str(lang).lower()
            if lang in supported_languages:
                html += f"""<img src="language_icons/{lang}.svg" alt="{lang}" class="repo-icon" title={lang.capitalize()}>\n"""
        
        return html
        
    def html_repo_icons(self):

        html = ''
    
        license = safe_dic(safe_dic(self.md,'license'),'excerpt')
        if license:
            html += f"""<a href="{safe_dic(license,'url')}" target="_blank" class="repo-icon"><img src="repo_icons/license.png" alt="license" class="repo-icon" title="License: {license['name']}"></a>"""
        
        readme_url = safe_dic(safe_dic(self.md,'readme_url'),'excerpt')
        if readme_url:
            html += f"""<a href="{readme_url}" target="_blank" class="repo-icon"><img src="repo_icons/readme.png" alt="readme" class="repo-icon" title="Readme"></a>"""
        
        notebook = safe_dic(safe_dic(self.md,'hasExecutableNotebook'),'excerpt')
        if notebook:
            html += f"""<img src="repo_icons/notebook.png" alt="notebook" class="repo-icon" title="Notebook">"""

        download_url = safe_dic(safe_dic(self.md,'downloadUrl'),'excerpt')
        if download_url:
            html += f"""<a href="{download_url}" target="_blank" class="repo-icon"><img src="repo_icons/download.png" alt="download" class="repo-icon" title="Download"></a>"""

        # TODO: Could be more than one citation
        citations = safe_dic(self.md,'citation')
        citation = None
        if citations:
            for c in citations:
                if c['technique'] == 'Regular expression':
                    citation = c['excerpt']
        if citation:
            html += f"""<img src="repo_icons/citation.png" alt="citation" class="repo-icon" title="{citation}">"""
        
        docker = safe_dic(safe_dic(self.md,'hasBuildFile'),'excerpt')
        if docker:
            html += f"""<img src="repo_icons/docker.png" alt="docker" class="repo-icon" title="{[str(d) for d in docker]}">"""
        
        installation = safe_dic(self.md,'installation')
        if installation:
            installation = safe_dic(installation[0],'excerpt')
            html += f"""<img src="repo_icons/installation.png" alt="installation" class="repo-icon" title="Installation:\n{installation}">"""
        
        requirements = safe_dic(self.md,'requirement')
        if requirements:
            requirements = safe_dic(requirements[0],'excerpt')
            html += f"""<img src="repo_icons/requirements.png" alt="requirements" class="repo-icon" title="Requirements:\n{requirements}">"""

        paper = None
        # resolve DOI add https://www.doi.org/
        # TODO: extract from citation from regular expresion -> url
        if paper:
            html += f"""<img src="repo_icons/paper.png" alt="paper" class="repo-icon" title="Paper">"""

        return html

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