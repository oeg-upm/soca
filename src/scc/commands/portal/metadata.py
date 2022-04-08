from scc import base_dir
from pathlib import Path
from os import listdir
from os.path import isfile, join
from datetime import datetime
import re
import sys
from pygments import highlight
from pygments.lexers.scdoc import ScdocLexer
from pygments.formatters import HtmlFormatter
import mistune

class metadata(object):

    def __init__(self, repo_metadata, embedded = False):
        self.md = repo_metadata
        self.base = 'https://github.com/dakixr/scc/raw/main/src/scc/assets/' if embedded else ''

    # Assets ####################################################
    def logo(self):
        logo = safe_dic(safe_dic(self.md,'logo'),'excerpt')
        if logo:
            if str(logo).startswith('https://github'):
                logo = logo.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        return logo if logo else f"{self.base}img/github-default.svg"

    def html_repo_type(self):
        repo_type = self.repo_type()
        if not repo_type:
            return ''
        if repo_type == 'web': 
            return f'<img src="{self.base}repo_icons/web.png" {self.add_tooltip("left","Website")} alt="repo-type" class="repo-type">'
        elif repo_type == 'ontology': 
            return f'<img src="{self.base}repo_icons/ontology.png" {self.add_tooltip("left","Ontology")} alt="repo-type" class="repo-type" style="height: 1.3rem;">'
        elif repo_type in ['package','library','service','script']:
            return f'<div class="grey-color-svg" style="display:flex;" {self.add_tooltip("left",f"Python {repo_type}")}><img src="{self.base}language_icons/python.svg" alt="repo-type" class="repo-type"></div>'
        else: return ''

    def icon_star(self):
        return f"{self.base}repo_icons/star.png"

    def icon_releases(self):
        return f"{self.base}repo_icons/releases.png"

    def html_languages(self):

        languages = self.languages()

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
                   style="background:url('{self.base}repo_icons/copy.svg')transparent;background-repeat:no-repeat;background-size:auto;"
                   data-toggle="tooltip" data-placement="right" title="Copy card as embbeded HTML">
                   </button>"""

    def html_license(self, license_input):
        if safe_dic(license_input,"url"):
            html = """
            <h3 class="ref-name"></h3>
            <span class="ref-description-aux">
                <h4>Description:</h4>
                <p class="ref-description" style="text-align: justify;">Loading...</p>

                <h4>Permissions:</h4>
                <div class="ref-permissions"><ul><li>Loading...</li></ul></div>

                <h4>Conditions:</h4>
                <div class="ref-conditions"><ul><li>Loading...</li></ul></div>

                <h4>Limitations:</h4>
                <div class="ref-limitations"><ul><li>Loading...</li></ul></div>
            </span>
            """
        else:
            html = f"""
            <h3 class="ref-name">{safe_dic(license_input,"name")}</h3>

            <h4>Description:</h4>
            <p class="ref-description">There is not an available description.</p>
            """
        return html


    def html_repo_icons(self):

        html = ''

        readme_url = self.readme()
        if readme_url:
            html += self.icon_wrapper(
                    icon_html = f"""<a href="{readme_url}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/readme.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom','Readme')}>
                        </a>""")

        license = self.license()
        if license:
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/license.png" 
                            class="repo-icon"
                            {self.add_tooltip('bottom',f'License: {license["name"]}')}>
                            """,
                modal_html= self.modal(
                    title = 'License',
                    body = self.html_license(license),
                    markdown_translation=False),
                    other_field=f'class="ref-license" data-url="{safe_dic(license,"url")}"'
                    )
        
        notebook = self.notebook()
        if notebook:
            mk_list = "\n".join([f'* <{n}>' for n in notebook])
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/notebook.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom','Notebook')}>""",

                modal_html = self.modal(
                    title = 'Notebook',
                    body = mk_list))


        docker = self.docker()
        if docker:
            mk_list = "\n".join([f'* <{d}>' for d in docker])
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/docker.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom',"Docker")}>""",

                modal_html = self.modal(
                    title = 'Docker',
                    body = mk_list))

        papers = self.paper()
        if papers:
            for paper in papers:
                html += self.icon_wrapper(
                    icon_html = f"""<a href="{paper.link_paper}" target="_blank" class="repo-icon">
                                <img src="{self.base}repo_icons/paper.png" 
                                class="repo-icon" 
                                {self.add_tooltip('bottom',paper.title_paper)}>
                        </a>""")

        citations = self.citations()
        if citations:
            formatter = HtmlFormatter(linenos=False, full=True, style='friendly')
            for citation in citations:
                html += self.icon_wrapper(
                    icon_html = f"""<img src="{self.base}repo_icons/citation.png" 
                                class="repo-icon" 
                                {self.add_tooltip('bottom',f"Citation")}>""",

                    modal_html = self.modal(
                        title = 'Citation',
                        body = f'<div style="font-family: monospace;">{highlight(citation, ScdocLexer(), formatter)}</div>',
                        markdown_translation=False))

        identifier = self.identifier()
        if identifier:
            html += self.icon_wrapper(
                icon_html = f"""<a href="{identifier}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/doi.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom',f"DOI: {identifier}")}>
                    </a>""")

        status = self.status()
        if status:
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/status.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom','Status')}>
                            """,

                modal_html = self.modal(
                    title = 'Status',
                    body = '### Description  \n'+ safe_dic(status,'description') + '#### More information  \n' + f'<{safe_dic(status,"excerpt")}>'))

        installation = self.installation()
        if installation:
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/installation.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom','Installation')}>""",

                modal_html = self.modal(
                    title = 'Installation',
                    body = f'{installation}'))
        
        requirements = self.requirements()
        if requirements:
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/requirements.png"  
                        class="repo-icon" 
                        {self.add_tooltip('bottom','Requirements')}>""",

                modal_html = self.modal(
                    title = 'Requirements',
                    body = requirements))

        usage = self.usage()
        if usage:
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/usage.png"  
                        class="repo-icon" 
                        {self.add_tooltip('bottom','Usage')}>""",

                modal_html = self.modal(
                    title = 'Usage',
                    body = usage))

        help = self.help()
        if help:
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/help.png"  
                        class="repo-icon" 
                        {self.add_tooltip('bottom','Help')}>""",

                modal_html = self.modal(
                    title = 'Help',
                    body = help))

        hasDocumentation = self.hasDocumentation()
        if hasDocumentation:
            html += self.icon_wrapper(
                icon_html = f"""<a href="{hasDocumentation}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/documentation.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom','Documentation')}>
                        </a>""")

        acknowledgement =  self.acknowledgement()
        if acknowledgement:
            html += self.icon_wrapper(

                icon_html = f"""<img src="{self.base}repo_icons/acknowledgement.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom',f"Acknowledgement")}>""",

                modal_html = self.modal(
                    title = 'Acknowledgement',
                    body = f'{acknowledgement}'))

        
        downloadUrl = self.downloadUrl()
        if downloadUrl:
            html += self.icon_wrapper(
                
                icon_html = f"""<a href="{downloadUrl}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/download.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom','Download')}>
                        </a>"""
                )

        return html

    # HTML helper ##################################################

    
    def add_tooltip(self, placement, tooltip_text):
        """Supported placements: ['bottom', 'up', 'right', 'left']"""
        return f'''data-toggle="tooltip" data-placement="{placement}" title="{tooltip_text}" alt="{tooltip_text}"'''
    
    def icon_wrapper(self, icon_html, modal_html = None, other_field = None):
        return f"""<div {other_field if other_field else ''} style="cursor: pointer;">
                        <div class="icon">{icon_html}</div>
                        {modal_html if modal_html else ''}
                    </div>"""
    
    def modal(self, title, body, markdown_translation = True):
    
        if markdown_translation:
            body = mistune.html(body)
           
        return f"""<div class="modal">
                        <div class="modal-content">
                            <span class="close">&times;</span>
                            <h2 style="margin-bottom: 1rem;">{title}</h2>
                            <div style="margin-bottom: 1rem; overflow: auto;">{body}</div>
                        </div>
                    </div>"""


    # Metadata ##################################################
    def last_release(self):
        return self.releases()[0]["tagName"] if self.n_releases() != 0 else ''
        
    def repo_type(self):

        # inspect4py
        ######################

        if 'inspect4py' in self.md:
            return self.md["inspect4py"]["software_type"] # package, library, service, script

        # web and ontology
        ######################

        langs = self.languages()

        if not langs: # Most ontologies doesn't have any language
            return 'ontology'

        web_langs = ['html','css','javascript'] 
        ontology_langs = ['html','css','javascript'] 

        is_ontology = True
        is_web = True

        for lang in langs:
            if lang not in web_langs:
                is_web = False
            if lang not in ontology_langs:
                is_ontology = False

        if (is_ontology and is_web 
                and (   
                    'ontolog' in self.description().lower() 
                    or 
                    'ontolog' in self.title().lower())
                ):
            return 'ontology'
              
        return 'web' if is_web else None
         
    def usage(self):
        usage = safe_dic(safe_list(safe_dic(self.md,'usage'),0),'excerpt')
        run_list = safe_dic(safe_dic(self.md,'inspect4py'),'run')
        if run_list:
            run = '\n'.join([ f'* {x}' for x in run_list])
            run_md = '### How to run it  \n' + run
        else: run_md = ''

        return usage + run_md if usage or run_md else None

    def help(self):
        support = safe_dic(safe_list(safe_dic(self.md,'support'),0),'excerpt')
        faq = safe_dic(safe_list(safe_dic(self.md,'faq'),0),'excerpt')
        supportChannels = safe_dic(safe_list(safe_dic(self.md,'supportChannels'),0),'excerpt')

        support_md = ('### Support  \n' + support) if support else ''
        faq_md = ('### FAQ  \n' + faq) if faq else ''
        supportChannels_md = ('### Support Channels  \n' + supportChannels) if supportChannels else ''

        return support_md + faq_md + supportChannels_md if support or faq or supportChannels else None

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

    def paper(self):
        citations = self.citations()
        p = []
        if citations:
            
            for cita in citations:

                c = citation_parser(cita)
                
                if c.link_paper and 'zenodo' not in c.link_paper:
                    p.append(c)

        return p if len(p) > 0 else None
        
    def identifier(self):
        return safe_dic(safe_list(safe_dic(self.md,'identifier'),0),'excerpt')
    
    def status(self):
        return safe_dic(self.md,'repoStatus')

    def acknowledgement(self):
        return safe_dic(safe_list(safe_dic(self.md,'acknowledgement'),0),'excerpt')

    def hasDocumentation(self):
        return safe_list(safe_dic(safe_dic(self.md,'hasDocumentation'),'excerpt'),0)

    def requirements(self):
        return safe_dic(safe_list(safe_dic(self.md,'requirement'),0),'excerpt')

    def installation(self):
        return safe_dic(safe_list(safe_dic(self.md,'installation'),0),'excerpt')

    def docker(self):
        return safe_dic(safe_dic(self.md,'hasBuildFile'),'excerpt')

    def citations(self):
        all_citations = safe_dic(self.md,'citation')

        if not all_citations:
            return None

        citations = []
        for c in all_citations:
            if c['technique'] == 'Regular expression':
                citations.append(c['excerpt'])
        return citations if len(citations) > 0 else None
        
    def downloadUrl(self):
        return safe_dic(safe_dic(self.md,'downloadUrl'),'excerpt') if self.n_releases() > 0 else None

    def notebook(self):
        return safe_dic(safe_dic(self.md,'hasExecutableNotebook'),'excerpt')

    def readme(self):
        return safe_dic(safe_dic(self.md,'readmeUrl'),'excerpt')

    def languages(self):
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

        return mistune.html(description)

    def license(self):
        return safe_dic(safe_dic(self.md,'license'),'excerpt')

    def last_update(self):
        date_modified_str = safe_dic(safe_dic(self.md,'dateModified'),'excerpt')[:-1]
        date_modified = datetime.strptime(date_modified_str, '%Y-%m-%dT%H:%M:%S')

        return date_modified
    
    def last_update_days(self):
        date_of_extraction_str = safe_dic(safe_dic(safe_dic(self.md,'stargazersCount'),'excerpt'),'date')[:-4]
        date_of_extraction = datetime.strptime(date_of_extraction_str, '%a, %d %b %Y %H:%M:%S') 
        last_update = self.last_update()
        return (date_of_extraction - last_update).days

    def stars(self):
        return safe_dic(safe_dic(safe_dic(self.md,'stargazersCount'),'excerpt'),'count')
    
    def n_releases(self):
        rel = safe_dic(safe_dic(self.md,'releases'),'excerpt')
        return len(rel) if rel is not None else 0

    def releases(self):
        return safe_dic(safe_dic(self.md,'releases'),'excerpt')
    
    def url_releases(self):
        return safe_dic(safe_dic(self.md,'downloadUrl'),'excerpt')
    
    def url_stars(self):
        return self.repo_url()+'/stargazers'
    
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

class citation_parser(object):

    def __init__(self, citation) -> None:
        self.link_paper = re.search('url[ ]*=[ ]*{(.*)}', citation)
        if self.link_paper:
            self.link_paper = self.link_paper.group(1)

        self.doi_paper = re.search('doi[ ]*=[ ]*{(.*)}', citation)
        if self.doi_paper:
            self.doi_paper = self.doi_paper.group(1)
        
        self.title_paper = re.search('title[ ]*=[ ]*{(.*)}', citation)
        if self.title_paper:
            self.title_paper = self.title_paper.group(1)

        if self.doi_paper and not self.link_paper:
            if self.doi_paper and 'http' not in self.doi_paper:
                self.link_paper = 'https://www.doi.org/' + self.doi_paper
            else: self.link_paper = self.doi_paper