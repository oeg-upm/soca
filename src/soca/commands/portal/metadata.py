from soca import base_dir
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
import os
#from cffconvert import Citation
#from cffconvert.cli import cli as cff2bibcli

class metadata(object):

    def __init__(self, repo_metadata_dir, repo_metadata, embedded = False):
        self.repo_metadata_dir = os.path.abspath(repo_metadata_dir)
        self.md = repo_metadata
        self.base = 'https://github.com/dakixr/soca/raw/main/src/soca/assets/' if embedded else ''

    # Assets ####################################################
    def logo(self):
        logo = safe_dic(safe_dic(safe_dic(safe_list(self.md,'logo'),0),'result'),'value')
        #if logo:
            #if str(logo).startswith('https://github'):
                #logo = logo.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        return logo if logo else f"{self.base}img/github-default.svg"

    def html_repo_type(self):
        repo_type = self.repo_type()
        if not repo_type:
            return ''
        if repo_type == 'web': 
            return f'<img src="{self.base}repo_icons/web.png" {self.add_tooltip("left","Website")} alt="repo-type" class="repo-type">'
        elif repo_type == 'ontology': 
            #ontologies = safe_dic(safe_dic(self.md,'ontologies'),'excerpt')
            ontologies = safe_dic(self.md,'ontologies')
            if ontologies:
                onto_list = '\n'.join(list(dict.fromkeys([ f'* <{safe_dic(safe_dic(x,"result"),"value")}>' for x in ontologies if 'http' in safe_dic(safe_dic(x,"result"),"value")])))
                #onto_list = '\n'.join([ f'* <{safe_dic(x,"file_url")}>' for x in ontologies])
            return self.icon_wrapper(
                icon_html = f'<img src="{self.base}repo_icons/ontology.png" {self.add_tooltip("left","Ontology")} alt="repo-type" class="repo-type" style="height: 1.3rem;">',
                modal_html= self.modal(
                    title= 'Ontologies',
                    body= onto_list
                ),
                other_field='class="m_ontology"'
            )
        return f'<div class="grey-color-svg" style="display:flex;" {self.add_tooltip("left",f"Python {repo_type}")}><img src="{self.base}language_icons/python.svg" alt="repo-type" class="repo-type"></div>'

    def icon_star(self):
        return f"{self.base}repo_icons/star.png"

    def icon_releases(self):
        return f"{self.base}repo_icons/releases.png"

    def html_description(self):
        return f'<span>{mistune.html(self.description())}</span>'

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
                            {self.add_tooltip('bottom',f'License: {safe_dic(license,"name")}')}>
                            """,
                modal_html= self.modal(
                    title = 'License',
                    body = self.html_license(license),
                    markdown_translation=False),
                other_field = f'data-url="{safe_dic(license,"url")}"',
                extra_class = 'ref-license' 
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
        #TODO check ScdocLexer
        citations = self.citations()
        if citations:
            citation = "No Citation Indicated"
            formatter = HtmlFormatter(linenos=False, full=True, style='friendly')
            #TODO once fixed turn to if, elif, else  so that it prioritises CFF (converted to bibtex format)
            if 'cff' in citations:
                # try:
                #     cite = Citation(cffstr=safe_dic(citations,"cff"))
                #     citation = cite.as_bibtex()
                # except:
                pass
            if 'bibtex' in citations:
                citation = safe_dic(citations,"bibtex")
            else:
                try:
                    citation = citations['citation'][0]
                    #citation = safe_list(safe_dic(citations,citation),0)
                except Exception as e:
                    print(str(e))
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/citation.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom',f"Citation")}>""",
                modal_html = self.modal(
                    title = 'Citation',
                    body = f'<div style="font-family: monospace;">{highlight(citation, ScdocLexer(), formatter)}</div>',
                    markdown_translation=False,
                    extra_html=
                        f"""
                        <button 
                            class="copy-citation-btn" 
                            value="{self.repo_url()}" 
                            style="background:url('repo_icons/copy.svg')transparent;background-repeat:no-repeat;background-size:auto;" 
                            data-toggle="tooltip" 
                            data-placement="right" 
                            data-original-title="Copy citation">
                        </button>
                        """))

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
                    body = '### Description  \n'+ safe_dic(safe_dic(safe_list(status,0),'result'),'description')
                           + '\n #### More information  \n' + f'<{safe_dic(safe_dic(safe_list(status,0),"result"),"value")}>'))

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
            has_i4p = safe_dic(safe_dic(self.md,'inspect4py'),'run')
            html += self.icon_wrapper(
                icon_html = f"""<img src="{self.base}repo_icons/usage.png"  
                        class="repo-icon" 
                        {self.add_tooltip('bottom','Usage')}>""",
                modal_html = self.modal(
                    title = 'How to use it' if has_i4p and '### How to use it' not in usage else 'Usage' ,
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
            if len(hasDocumentation) > 1:
                #mk_list = "\n".join([f'* <{d}>' if ('http' in d and not ' ' in d) else f'* {d}' for d in hasDocumentation])

                mk_list = "\n".join([
                    f'* <{safe_dic(safe_dic(d, "result"), "value")}>' if (
                                 self._is_valid_url(safe_dic(safe_dic(d, "result"), "value")))
                    else f'* {safe_dic(safe_dic(d, "result"), "value")}' for d in hasDocumentation
                ])

                html += self.icon_wrapper(
                    icon_html = f"""<img src="{self.base}repo_icons/documentation.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom',"Documentation")}>""",

                    modal_html = self.modal(
                        title = 'Documentation',
                        body = mk_list))
            else:
                doc = safe_dic(safe_dic(safe_list(hasDocumentation,0),'result'),'value')
                if self._is_valid_url(doc):
                    html += self.icon_wrapper(
                        icon_html=f"""<a href="{doc}" target="_blank" class="repo-icon">
                                                    <img src="{self.base}repo_icons/documentation.png" 
                                                    class="repo-icon" 
                                                    {self.add_tooltip('bottom', 'Documentation')}>
                                                </a>""")
                else:
                    html += self.icon_wrapper(
                        icon_html=f"""<img src="{self.base}repo_icons/documentation.png" 
                                class="repo-icon" 
                                {self.add_tooltip('bottom', 'Documentation')}>""",

                        modal_html=self.modal(
                            title='Documentation',
                            body=f'{doc}'))


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

    def _is_valid_url(self,url):
        """Private function to check if a string is a valid URL."""
        import re

        # Regular expression to match a valid URL
        url_regex = re.compile(r"^https?://[^\s/$.?#].[^\s]*$")

        # Check if the input string matches the URL regex
        return bool(url_regex.match(url))

    # HTML helper ##################################################

    
    def add_tooltip(self, placement, tooltip_text):
        """Supported placements: ['bottom', 'up', 'right', 'left']"""
        return f'''data-toggle="tooltip" data-placement="{placement}" title="{tooltip_text}" alt="{tooltip_text}"'''
    
    def icon_wrapper(self, icon_html, modal_html = None, other_field = None, extra_class = None):
        return f"""<div {other_field if other_field else ''} class="icon-wrapper{' '+extra_class if extra_class else ''}">
                        <div class="icon">{icon_html}</div>
                        {modal_html if modal_html else ''}
                    </div>"""
    
    def modal(self, title, body, markdown_translation = True, extra_html = ''):
    
        if markdown_translation:
            body = mistune.html(body)
           
        return f"""<div class="modal">
                        <div class="modal-content">
                            <span class="close">&times;</span>
                            <span style="display:flex;">
                                <h2 style="margin-bottom: 1rem;">{title}</h2>
                                {extra_html}
                            </span>
                            <div style="margin-bottom: 1rem; overflow: auto;">{body}</div>
                        </div>
                    </div>"""


    # Metadata ##################################################
    def last_release(self):
        if self.n_releases() != 0:
            if not safe_dic(safe_dic(safe_list(self.releases(),0),'result'),'name'):
                if (tag:=safe_dic(safe_dic(safe_list(self.releases(),0),'result'),'tag')):
                    return tag
                else:
                    return "Missing Descriptors"
            return safe_dic(safe_dic(safe_list(self.releases(),0),'result'),'name')
        else:
            return ''
        #return safe_dic(safe_dic(safe_list(self.releases(),0),'result'),'name') if self.n_releases() != 0 else ''

    #TODO
    def repo_type(self):

        # inspect4py
        ######################

        if 'inspect4py' in self.md and "software_type" in self.md["inspect4py"]:
            return self.md["inspect4py"]["software_type"]

        # web and ontology
        ######################

        if (safe_dic(self.md,'ontologies') is not None):
            return 'ontology'

        langs = self.languages()
        is_web = (langs and 'html' in langs)
        
        if langs:
            for lang in langs:
                if lang not in ['html','css','javascript']:
                    is_web = False
                #if lang not in ['html','css','javascript']:
                    #is_ontology = False
        if is_web:
            return 'web'
        
        return None

    def usage(self):
        usage_list = safe_dic(self.md,'usage')
        usage = None
        if usage_list:
            usage = ''
            for u in usage_list:
                usage += u['result']['value'] + '\n'
        #TODO
        run_list = safe_dic(safe_dic(self.md,'inspect4py'),'run')
        if run_list:
            if isinstance(run_list, list):
                run = '\n'.join([ f'* {str(x).replace(self.repo_metadata_dir,"")}' for x in run_list])
            else: run =  run_list.replace(self.repo_metadata_dir,"")
            run_md = '---\n  ### How to use it  \n' + run if usage else run

        else: run_md = ''

        usage = usage if usage else ''

        return usage + run_md if usage or run_md else None

#TODO cannot find correct implementation
    def help(self):
        support = safe_dic(safe_dic(safe_list(safe_dic(self.md,'support'),0),'result'),'value')
        faq = safe_dic(safe_dic(safe_list(safe_dic(self.md,'faq'),0),'result'),'value')
        supportChannels = safe_dic(safe_dic(safe_list(safe_dic(self.md,'supportChannels'),0),'result'),'value')

        support_md = ('### Support  \n' + support) if support else ''
        faq_md = ('### FAQ  \n' + faq) if faq else ''
        supportChannels_md = ('### Support Channels  \n' + supportChannels) if supportChannels else ''

        return support_md + faq_md + supportChannels_md if support or faq or supportChannels else None

    def recently_updated(self):
        #TODO: Retreive days_threshold from properties file
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

        
    def identifier(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md,'identifier'),0),'result'),'value')
    def status(self):
        return safe_dic(self.md,'repository_status')


    def acknowledgement(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md,'acknowledgement'),0),'result'),'value')

    def hasDocumentation(self):
        docList = safe_dic(self.md, 'documentation')
        return docList if docList else None

    def requirements(self):

        reqs = safe_dic(self.md,'requirements')
        if not reqs:
            return None
        return "\n".join([safe_dic(safe_dic(d,'result'),'value') for d in reqs])

    def installation(self):
        inst = safe_dic(self.md,'installation')
        if not inst:
            return None
        return "\n".join([safe_dic(safe_dic(d,'result'),'value') for d in inst])
    def docker(self):

        hasBuildFileList = safe_dic(self.md,'has_build_file')
        
        if not hasBuildFileList:
            return None

        return [safe_dic(safe_dic(d,'result'),'value') for d in hasBuildFileList]

        
    def downloadUrl(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md,'download_url'),0),'result'),'value') \
            if self.n_releases() > 0 else None

    #TODO change name to something more self explanatory
    def notebook(self):
        exe_l = safe_dic(self.md,'executable_example')
        exe_l = exe_l if exe_l else []
        exe = [ x['result']['value'] for x in exe_l ]
        return exe if len(exe)>0 else None

    def readme(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md,'readme_url'),0),'result'),'value')

    def languages(self):
        langs = safe_dic(self.md,'programming_languages')
        if not langs:
            return None
        return [str(safe_dic(safe_dic(lang,'result'),'value')).lower() for lang in langs]

    def repo_url(self):
        return safe_dic(safe_list(safe_dic(safe_dic(self.md,'code_repository'),0),'result'),'value')
            
    def title(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md,'name'),0),'result'),'value')
    #TODO find new
    def description(self):

        all_descriptions = safe_dic(self.md,'description')

        description = None
        if all_descriptions:
            for d in all_descriptions:
                if safe_dic(d,'technique') == 'GitHub API':
                    description = safe_dic(safe_dic(d,'result'),'value')
                    break

        if not description:
            description = safe_dic(safe_dic(safe_list(all_descriptions,0),'result'),'value')
            if not description:
                description = 'No description available yet.'

        return description

    def license(self):
        license = safe_dic(safe_list(safe_dic(self.md, 'license'), 0), 'result')
        if (typ := safe_dic(license, "type")) and (typ == "File_dump"):
            self._find_license_name(license)

            return license
        else:
            return license


    def _find_license_name(self, license):
        find_name = safe_dic(license, "value")
        if 'Apache' in find_name:
            license['name'] = 'Apache License 2.0'
        elif 'MIT' in find_name:
            license['name'] = 'MIT License'
        elif 'GPL' in find_name:
            license['name'] = 'GNU General Public License v3.0'
        else:
            license['name'] = 'Other'

    def last_update(self):
        result = safe_dic(safe_list(safe_dic(self.md,'date_updated'),0),'result')
        date_modified_str = of_correctType(result,'Date')[:-1]
        date_modified = datetime.strptime(date_modified_str, '%Y-%m-%dT%H:%M:%S')
        return date_modified

    def last_update_days(self):
        date_of_extraction_str = safe_dic(safe_dic(self.md,'somef_provenance'),'date')[:]
        date_of_extraction = datetime.strptime(date_of_extraction_str, '%Y-%m-%d %H:%M:%S')
        last_update = self.last_update()
        return (date_of_extraction - last_update).days


    def stars(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md,'stargazers_count'),0),'result'),'value')
    
    def n_releases(self):
        rel = safe_dic(self.md,'releases')
        return len(rel) if rel is not None else 0

    def releases(self):
        return safe_dic(self.md,'releases')
    
    def url_releases(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md,'download_url'),0),'result'),'value')
    
    def url_stars(self):
        return self.repo_url()+'/stargazers'

    def owner(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md,'owner'),0),'result'),'value')


    #IMPORTANT !!!!! ASSUMES only 1 CFF per repo
    #USE SOMEF as example it lists SOMEF CFF then WIDOCO then SOMEF then CAPTUM
    def citations(self):
        all_citations = safe_dic(self.md,'citation')

        if not all_citations:
            return None

        citations = { 'citation': []}

        for c in all_citations:
            try:
                type = ""
                type = c['result']['format']
            except:
                try:
                    if c['result']['type'] == 'Text_excerpt':
                        citations['citation'].append(c['result']['value'])
                except:
                    continue
            match type:
                case 'cff':
                    citations['cff'] = c['result']['value']
                case 'bibtex':
                    citations['bibtex'] = c['result']['value']
                case _:
                    continue
        return citations if len(citations) > 0 else None

    # Originally citations Took the ver8 somef "regular expression" output and would create a list of excerpts

    def paper(self):
        citations = safe_dic(self.citations(),'citation')
        p = []
        if citations:
            for cita in citations:

                c = citation_parser(cita)

                if c.link_paper and 'zenodo' not in c.link_paper:
                    p.append(c)

        return p if len(p) > 0 else None

    
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
def of_correctType(result, ofType):
    if safe_dic(result, 'type') == ofType:
        return safe_dic(result, 'value')
    else:
        raise Exception("not of correct %s type" % ofType)

class citation_parser(object):

    def __init__(self, citation) -> None:
        self.link_paper = re.search('url[ ]*=[ ]*{(.*)}', citation)
        if self.link_paper:
            self.link_paper = self.link_paper.group(1)

        self.doi_paper = re.search('doi[ ]*=[ ]*{(.*)}', citation)
        if self.doi_paper:
            self.doi_paper = self.doi_paper.group(1)
        
        self.title_paper = re.search('title[ ]*=[ "]*{(.*)}', citation)
        if self.title_paper:
            self.title_paper = self.title_paper.group(1)

        if self.doi_paper and 'http' not in self.doi_paper:
            self.doi_paper = 'https://www.doi.org/' + self.doi_paper
            self.link_paper = self.doi_paper