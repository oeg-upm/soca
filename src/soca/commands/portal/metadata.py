from ... import base_dir
from pathlib import Path
from os import listdir
from os.path import isfile, join
from datetime import datetime
from html import escape
import re
import sys
from pygments import highlight
from pygments.lexers.scdoc import ScdocLexer
from pygments.formatters import HtmlFormatter
import mistune
import os
import json
from urllib.parse import unquote, urlparse
import ast



# from cffconvert import Citation
# from cffconvert.cli import cli as cff2bibcli

class Metadata(object):

    def __init__(self, repo_metadata_dir, repo_metadata, embedded=False):
        self.repo_metadata_dir = os.path.abspath(repo_metadata_dir)
        self.md = repo_metadata
        self.base = 'https://github.com/oeg-upm/soca/tree/main/src/soca/assets' if embedded else ''
        
    


######################################################
# auxs

#################### QUALITY REPOTS ###############################
# RSFC
    #busqueda del directorio output rsfc
    def rsfc_output_path(self):

        metadata_dir = Path(self.repo_metadata_dir).resolve()

        # /app/outputs/soca/oeg-fair-sergio/metadata
        target_name = metadata_dir.parent.name

        # /app/outputs
        outputs_dir = metadata_dir.parent.parent.parent

        repo_url = self.repo_url()
        if not repo_url:
            return None

        repo_name = repo_url.rstrip("/").split("/")[-1]
        repo_key = self.repository_output_key()

        target_dir = outputs_dir / "rsfc" / target_name
        if not target_dir.exists():
            return None

        candidates = []
        if repo_key:
            candidates.append(target_dir / repo_key)
        candidates.append(target_dir / repo_name)

        for candidate in candidates:
            if candidate.exists():
                return candidate

        candidate_names = {candidate.name.casefold() for candidate in candidates}
        try:
            for path in target_dir.iterdir():
                if path.is_dir() and path.name.casefold() in candidate_names:
                    return path
        except Exception:
            return None

        return None
    
    
    # return del report
    def rsfc_report_path(self):
        rsfc_dir = self.rsfc_output_path()
        if not rsfc_dir:
            return None


        return rsfc_dir / "RSFC_REPORT.md"
    
    # lectura en markdown de rsfc report
    def rsfc_report_markdown(self):
        report_path = self.rsfc_report_path()
        
        if not report_path:
            return None
        try:
            return report_path.read_text(encoding="utf-8")
        except Exception:
            return None
        
    # busuqeda del assessment json generado del software
    def rsfc_assessment_json(self):
        rsfc_dir = self.rsfc_output_path()
        if not rsfc_dir:
            return None
        
        # si existe el output cogemos de el el json
        rsfc_output_dir = rsfc_dir / "rsfc_output"
        if rsfc_output_dir.exists():
            
            file = rsfc_output_dir / "rsfc_assessment.json"
            if file.exists():
                data = json.loads(file.read_text(encoding="utf-8"))
                return data
        
        return None
            
            
    # nº de checks pasados por el assessment
    def rsfc_report_score(self):
        assessment = self.rsfc_assessment_json()
        if not assessment:
            return None

        checks = assessment.get("checks",[])
        
        if not checks:
            return None

        total = len(checks)

        passed = sum(
        1
        for check in checks
        if str(check.get("output", "")).lower() == "true"
    )
        return passed, total


# RESQUI

    def repository_output_key(self):
        repo_url = self.repo_url()
        if not repo_url:
            return None

        parsed = urlparse(repo_url.rstrip("/"))
        parts = [part for part in parsed.path.split("/") if part]

        if len(parts) < 2:
            return None

        owner, repo = parts[-2], parts[-1]
        if repo.endswith(".git"):
            repo = repo[:-4]

        return f"{owner}_{repo}".replace(".", "-")

    def resqui_output_path(self):
        metadata_dir = Path(self.repo_metadata_dir).resolve()
        target_name = metadata_dir.parent.name
        outputs_dir = metadata_dir.parent.parent.parent
        target_dir = outputs_dir / "resqui" / target_name
        repo_key = self.repository_output_key()

        if not repo_key or not target_dir.exists():
            return None

        candidate = target_dir / repo_key
        if candidate.exists():
            return candidate

        repo_key_lower = repo_key.casefold()
        try:
            for path in target_dir.iterdir():
                if path.is_dir() and path.name.casefold() == repo_key_lower:
                    return path
        except Exception:
            return None

        return None

    def resqui_report_path(self):
        resqui_dir = self.resqui_output_path()
        if not resqui_dir:
            return None

        return resqui_dir / "resqui_report.md"

    def resqui_report_markdown(self):
        report_path = self.resqui_report_path()

        if not report_path:
            return None

        try:
            return report_path.read_text(encoding="utf-8")
        except Exception:
            return None

    def resqui_summary_json(self):
        resqui_dir = self.resqui_output_path()
        if not resqui_dir:
            return None

        summary_path = resqui_dir / "resqui_summary.json"
        if not summary_path.exists():
            return None

        try:
            return json.loads(summary_path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def resqui_report_score(self):
        summary = self.resqui_summary_json()
        if not summary:
            return None

        checks = summary.get("checks", [])
        if not checks:
            return None

        resqui_checks = []
        for check in checks:
            checking_software = check.get("checkingSoftware") or {}
            tool_name = str(checking_software.get("name", "")).strip().lower()

            if tool_name == "rsfc":
                continue

            resqui_checks.append(check)

        if not resqui_checks:
            return None

        passed_outputs = {"true", "valid", "secure", "passed", "pass"}
        passed = sum(
            1
            for check in resqui_checks
            if str(check.get("output", "")).strip().lower() in passed_outputs
        )

        return passed, len(resqui_checks)

    def resqui_report_html(self):
        report_md = self.resqui_report_markdown()
        score = self.resqui_report_score()

        if not report_md or not score:
            return ""

        passed, total = score
        report_html = mistune.html(report_md)

        return f"""
        <b>
            Quality:
        </b>
            {passed}/{total} checks
            <b><a href="https://github.com/EVERSE-ResearchSoftware/QualityPipelines"
                target="_blank"
                rel="noopener noreferrer"
                style="text-decoration: underline; color: inherit;">
                (by RESQUI)
            </a>
        </b>
        <br>
        <details class="quality-details">
            <summary>Show RESQUI report</summary>

            <div class="rsfc-report resqui-report">
                {report_html}
            </div>
        </details>
        """
    


# sw-metadata-bot

    def sw_metadata_bot_runs_dir(self):
        metadata_dir = Path(self.repo_metadata_dir).resolve()

        # Ejemplo:
        # .../outputs/soca/oeg-fair-sergio/metadata
        target_name = metadata_dir.parent.name

        # .../outputs
        outputs_dir = metadata_dir.parent.parent.parent

        return outputs_dir / "sw-metadata-bot" / target_name / "runs"


    def sw_metadata_bot_latest_record(self):
        """
        Busca el último run_report.json del target actual y devuelve
        el record correspondiente al repo actual.
        """

        runs_dir = self.sw_metadata_bot_runs_dir()

        if not runs_dir.exists():
            return None

        repo_url = self.repo_url()
        if not repo_url:
            return None

        repo_url = repo_url.rstrip("/")

        # Coger runs ordenados por nombre descendente.
        # Con formato yyyyMMdd_HHmmss, el último nombre es el más reciente.
        run_dirs = [
            p for p in runs_dir.iterdir()
            if p.is_dir()
        ]

        run_dirs = sorted(run_dirs, key=lambda p: p.name, reverse=True)

        for run_dir in run_dirs:
            report_file = run_dir / "run_report.json"

            if not report_file.exists():
                continue

            try:
                report_data = json.loads(report_file.read_text(encoding="utf-8"))
            except Exception:
                continue

            records = report_data.get("records", [])
            run_metadata = report_data.get("run_metadata", {})

            for record in records:
                record_repo_url = str(record.get("repo_url", "")).rstrip("/")

                if record_repo_url == repo_url:
                    return {
                        "record": record,
                        "run_metadata": run_metadata,
                        "report_path": report_file
                    }

        return None

    def sw_metadata_bot_failure_message(self, record):
        reason_code = str(record.get("reason_code", ""))
        error = str(record.get("error", ""))

        if reason_code == "missing_pitfall_file":
            return "Metadata quality report unavailable: pitfall file was not generated."

        if "410 Client Error" in error:
            return "Issue publication failed: GitHub Issues are unavailable for this repository."

        if "403 Client Error" in error:
            return "Issue publication failed: insufficient permissions to create GitHub issue."

        if reason_code == "publish_exception":
            return "Issue publication failed."

        return None

    def sw_metadata_bot_report_html(self):
        data = self.sw_metadata_bot_latest_record()

        if not data:
            return ""

        record = data["record"]
        failure_message = self.sw_metadata_bot_failure_message(record)
        pitfalls_count = record.get("pitfalls_count", 0) or 0
        warnings_count = record.get("warnings_count", 0) or 0

        codemeta_status = record.get("codemeta_status")
        issue_url = record.get("issue_url") or record.get("previous_issue_url")

        # Singular o plural según la cantidad
        pitfall_label = "pitfall" if pitfalls_count == 1 else "pitfalls"
        warning_label = "warning" if warnings_count == 1 else "warnings"

        if failure_message:
            quality_result = failure_message
        elif codemeta_status == "missing":
            quality_result = "No CodeMeta file"
        else:
            quality_result = (
                f"{pitfalls_count} {pitfall_label}, "
                f"{warnings_count} {warning_label}"
            )
            
        if issue_url:
            issue_link_html = f"""
            <div style="margin-top:4px; font-size:0.9em;">
                <a href="{issue_url}"
                target="_blank"
                rel="noopener noreferrer"
                style="text-decoration: underline;">
                    Open to see GitHub issue
                </a>
            </div>
            """
        else:
            issue_link_html = """
            <div style="margin-top:4px; font-size:0.9em; color:#555;">
                No related GitHub issue available
            </div>
            """

        return f"""
        <div style="margin-top:8px;">
            <b>Metadata quality:</b>
            {quality_result}
            <a href="https://github.com/SoftwareUnderstanding/RsMetaCheck"
            target="_blank"
            rel="noopener noreferrer"
            style="font-weight:bold; text-decoration:underline; color:inherit;">
                (by RSMetaCheck)
            </a>

            {issue_link_html}
        </div>
        """
######################################################################################
    #agrupacion de tipos de requirements
    def group_requirement_files(self, reqs):
        if not reqs:
            return None

        grouped = {}

        for r in reqs:
            if not isinstance(r, dict):
                continue

            source = r.get("source")
            if not source:
                continue

            filename = source.split("/")[-1].lower()

            if "requirements" in filename:
                key = "Source requirements.txt"
            elif filename == "pyproject.toml":
                key = "Source software configuration file"
            elif filename == "codemeta.json":
                key = "Source codemeta"
            elif filename == "readme.md":
                key = "Source README"
            else:
                continue

            #  dict para deduplicar por source
            grouped.setdefault(key, {})[source] = r

        # convertir a lista final
        grouped = {k: list(v.values()) for k, v in grouped.items()}

        return grouped if grouped else None



    # agrupacion de self.docker por tipos de archivos
    def group_build_files(self, docker):

        if not docker:
            return None

        grouped = {
            "Dockerfiles": [],
            "Docker Compose files": [],
            "Poetry files": []
        }

        for url in docker:
            
            if not url or not isinstance(url, str):
                continue
            name = url.lower().split("/")[-1]

            if name == "dockerfile":
                grouped["Dockerfiles"].append(url)

            elif "docker-compose" in name:
                grouped["Docker Compose files"].append(url)

            elif name == "pyproject.toml":
                grouped["Poetry files"].append(url)

        # quitar categorías vacías
        grouped = {k: v for k, v in grouped.items() if v}

        return grouped if grouped else None


    # convertir raw url a github url
    def raw_to_github_url(self, url: str) -> str:
        if "raw.githubusercontent.com" not in url:
            return url  # ya es normal

        parts = url.split("/")

        # raw.githubusercontent.com/{owner}/{repo}/{branch}/path...
        owner = parts[3]
        repo = parts[4]
        branch = parts[5]
        path = "/".join(parts[6:])

        return f"https://github.com/{owner}/{repo}/blob/{branch}/{path}"


    # funcion para que los archivos de "docker" se vean como containers->dockefile
    def get_repo_relative_path(self, url: str) -> str:
        parts = url.split("/")

        # estructura raw github:
        # https://raw.githubusercontent.com/{owner}/{repo}/{branch}/...
        
        if len(parts) < 7:
            return url  # fallback

        path_parts = parts[6:]  # todo lo que va después de branch

        if not path_parts:
            return ""

        # si está en raíz → solo nombre
        if len(path_parts) == 1:
            return path_parts[0]

        return " → ".join(path_parts)


    # parseo de cff a bibtex
    def cff_to_bibtex(self, cff_text):
        from cffconvert import Citation
        import re
        import yaml
        import unicodedata

        try:
            # Convertir CFF a BibTeX mediante cffconvert
            citation = Citation(cffstr=cff_text)
            bibtex = citation.as_bibtex()

            # Leer los datos del CFF para construir la clave
            parsed = yaml.safe_load(cff_text)

            authors = parsed.get("authors", [])
            first_author = authors[0] if authors else {}

            surname = first_author.get("family-names", "reference").strip()

            date_released = str(parsed.get("date-released", ""))
            year = date_released[:4] if date_released else ""

            title = parsed.get("title", "software")
            title_words = re.findall(r"[A-Za-z0-9]+", title)
            title_word = title_words[0] if title_words else "software"

            # Ejemplo: Toledo + 2024 + RML -> toledo2024rml
            raw_key = f"{surname}{year}{title_word}"

            # Eliminar acentos, espacios y caracteres no válidos
            citation_key = unicodedata.normalize("NFKD", raw_key)
            citation_key = citation_key.encode("ascii", "ignore").decode("ascii")
            citation_key = re.sub(
                r"[^A-Za-z0-9:_-]",
                "",
                citation_key
            ).lower()

            if not citation_key:
                citation_key = "softwareReference"

            # Sustituir únicamente la clave genérica de cffconvert
            bibtex = re.sub(
                r"(@\w+\s*\{)YourReferenceHere(?=,)",
                lambda match: f"{match.group(1)}{citation_key}",
                bibtex,
                count=1
            )

            return bibtex

        except Exception as exc:
            print(f"Could not convert CFF to BibTeX: {exc}")
            return None



    # creacion de boton para copiar bibtex


    def copy_button(self, text, label):
        import html
        import json

        if not text:
            return ""

        safe_html = html.escape(text)
        safe_js = json.dumps(text)

        return f"""
            <div style="margin-bottom:10px;">
                <b style="font-size:0.9em;">{label}</b>
            </div>

            <div style="position:relative;">
                <button
                    onclick='navigator.clipboard.writeText({safe_js})'
                    style="
                        position:absolute;
                        top:5px;
                        right:5px;
                        z-index:1;
                    ">
                    Copy
                </button>

                <pre style="
                    background:#f7f7f7;
                    padding:12px;
                    padding-right:65px;
                    border-radius:6px;
                    font-size:0.85em;
                    line-height:1.45;
                    overflow:auto;
                    max-height:250px;
                    white-space:pre-wrap;
                    overflow-wrap:anywhere;
                    word-break:break-word;
                ">{safe_html}</pre>
            </div>
        """

    
    #parseador de bibtex para estructurar en html
    def parse_bibtex(self, bibtex):
        import bibtexparser

        try:
            bib_database = bibtexparser.loads(bibtex)
            entry = bib_database.entries[0] if bib_database.entries else {}

            return entry 

        except Exception:
            return {}
    def format_bibtex(self, bibtex):
        import bibtexparser
        from bibtexparser.bwriter import BibTexWriter

        if not bibtex:
            return ""

        try:
            bib_database = bibtexparser.loads(bibtex)

            writer = BibTexWriter()

            # Sangría de los campos
            writer.indent = "    "

            # Alinear los signos =
            writer.align_values = True

            # No reordenar las diferentes entradas
            writer.order_entries_by = None

            # Separación entre entradas si hubiera varias
            writer.entry_separator = "\n\n"

            formatted_bibtex = bibtexparser.dumps(
                bib_database,
                writer=writer
            )

            return formatted_bibtex.strip()

        except Exception as exc:
            print(f"Could not format BibTeX: {exc}")

            # Si falla el parseo, mostrar el original
            return str(bibtex).strip()


        
        
    
    def parse_cff(self, cff_text):

        import yaml

        try:
        # si ya es dict no lo parsees
            if isinstance(cff_text, dict):
               parsed = cff_text
            else:
             parsed = yaml.safe_load(cff_text)
        except Exception:
            return None
        
        # TITLE
        title = parsed.get("title")

        # DOI
        doi = parsed.get("doi")
        if not doi:
            identifiers = parsed.get("identifiers", [])
            for i in identifiers:
                if i.get("type") == "doi":
                    doi = i.get("value")
                    break

        if doi and not str(doi).startswith("http"):
            doi = f"https://doi.org/{doi}"

        # AUTHORS
        authors = parsed.get("authors", [])
        authors_str = ", ".join([
            f"{a.get('given-names','')} {a.get('family-names','')}".strip()
            for a in authors
        ]) if authors else None

        # EXTRAS
        abstract = parsed.get("abstract")
        version = parsed.get("version")
        license = parsed.get("license")
        keywords = parsed.get("keywords", [])
        date_released = parsed.get("date-released")
        repo_code = parsed.get("repository-code")
        url = parsed.get("url")

        return {
            "title": title,
            "authors": authors_str,
            "doi": doi,
            "abstract": abstract,
            "version": version,
            "license": license,
            "keywords": keywords,
            "date": date_released,
            "repo_code": repo_code,
            "url": url
        }
    
    
    # Assets ####################################################
    def logo(self):
        
        # import time
        # print(self.md ,"\n", self.repo_metadata_dir,"\n", flush=True )
        # time.sleep(10)
        
        logo = safe_dic(
            safe_dic(safe_dic(safe_list(self.md, 'logo'), 0), 'result'), 'value')
        # if logo:
        # if str(logo).startswith('https://github'):
        # logo = logo.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        return logo if logo else f"{self.base}img/github-default.svg"

    def html_repo_type(self):
        repo_type = self.repo_type()
        if not repo_type:
            return ''
        if repo_type == 'web':
            return f'<img src="{self.base}repo_icons/web.png" {self.add_tooltip("left", "Website")} alt="repo-type" class="repo-type">'
        elif repo_type == 'ontology':
            # ontologies = safe_dic(safe_dic(self.md,'ontologies'),'excerpt')
            ontologies = safe_dic(self.md, 'ontologies')
            onto_list = "No ontology URL available."
            if ontologies:
                ontology_urls = [
                    f'* <{value}>'
                    for x in ontologies
                    if (value := safe_dic(safe_dic(x, "result"), "value"))
                    and 'http' in value
                ]
                if ontology_urls:
                    onto_list = '\n'.join(list(dict.fromkeys(ontology_urls)))
                # onto_list = '\n'.join([ f'* <{safe_dic(x,"file_url")}>' for x in ontologies])
            return self.icon_wrapper(
                icon_html=f'<img src="{self.base}repo_icons/ontology.png" {self.add_tooltip("left", "Ontology")} alt="repo-type" class="repo-type" style="height: 1.3rem;">',
                modal_html=self.modal(
                    title='Ontologies',
                    body=onto_list
                ),
                other_field='class="m_ontology"'
            )
        return f'<div class="grey-color-svg" style="display:flex;" {self.add_tooltip("left", f"Python {repo_type}")}><img src="{self.base}language_icons/python.svg" alt="repo-type" class="repo-type"></div>'

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
        supported_languages = [str(f).removesuffix('.svg').lower() for f in listdir(language_icons_dir) if
                               isfile(join(language_icons_dir, f))]

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
        if safe_dic(license_input, "url"):
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
            <h3 class="ref-name">{safe_dic(license_input, "name")}</h3>

            <h4>Description:</h4>
            <p class="ref-description">There is not an available description.</p>
            """
        return html

    def html_repo_icons(self):
    
        #debugging de nombre del repo para prints
        #raw_url = safe_dic(safe_dic(safe_list(safe_dic(self.md, 'readme_url'), 0), 'result'), 'value')
        #parts = raw_url.split("/")
        #repo = parts[4]
        
        
        

        html = ''

        readme_url = self.readme()
        if readme_url:
            html += self.icon_wrapper(
                icon_html=f"""<a href="{readme_url}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/readme.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom', 'Readme')}>
                        </a>""")

        license = self.license()
        if license:
            
            # nuevo
            license_url = safe_dic(license, "value")
            if not (license_url and str(license_url).startswith("https://api.github.com/licenses/")):
                license_url = safe_dic(license, "url")
            ##
            
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/license.png" 
                            class="repo-icon"
                            {self.add_tooltip('bottom', f'License: {safe_dic(license, "name")}')}>
                            """,
                modal_html=self.modal(
                    title='License',
                    body=self.html_license(license),
                    markdown_translation=False),
                
                
                other_field=f'data-url="{license_url}"',# antes era un safe dict de license, url
                extra_class='ref-license'
            )

        notebook = self.notebook()
        if notebook:
            mk_list = "\n".join([f'* <{n}>' for n in notebook])
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/notebook.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom', 'Notebook')}>""",

                modal_html=self.modal(
                    title='Notebook',
                    body=mk_list))

        
        
        

        
        # docker antiguo
        '''
        docker = self.docker()
        
        if docker:
            

            mk_list = "\n".join([f'* <{d}>' for d in docker])
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/docker.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom', "Docker")}>""",

                modal_html=self.modal(
                    title='Docker',
                    body=mk_list))
        
        
        '''
        #docker propio, saca la parte docker de somef y la agrupa por tipos de archivos importantes
        docker = self.docker()
        grouped = self.group_build_files(docker)


        if grouped:
                
                body = "<div style='max-height:300px; overflow:auto;'>"

                for category, urls in grouped.items():

                    body += f"<b>{category}</b><br>"

                    for url in urls:
                        display = self.get_repo_relative_path(url)
                        github_url = self.raw_to_github_url(url)
                        body += f"""
                        • <a href="{github_url}" target="_blank">{display}</a><br>
                        """

                    body += "<br>"

                body += "</div>"
                
                html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/docker.png" 
                                class="repo-icon" 
                                {self.add_tooltip('bottom', "Docker / Build Files")}>""",
                modal_html=self.modal(
                    title='Docker / Build Files',
                    body=body,
                    markdown_translation=False
    )
)
        
        
        
            
            
            
            
            
        papers = self.paper()
        if papers:
            for paper in papers:
                html += self.icon_wrapper(
                    icon_html=f"""<a href="{paper.link_paper}" target="_blank" class="repo-icon">
                                <img src="{self.base}repo_icons/paper.png" 
                                class="repo-icon" 
                                {self.add_tooltip('bottom', paper.title_paper)}>
                        </a>""")
    
    
    
    

        
        '''
    
        # TODO check ScdocLexer
        citations = self.citations()
        if citations:
            citation = "No Citation Indicated"
            formatter = HtmlFormatter(
                linenos=False, full=True, style='friendly')
            # TODO once fixed turn to if, elif, else  so that it prioritises CFF (converted to bibtex format)
            if 'bibtex' in citations:
                citation = safe_dic(citations, "bibtex")
            elif 'cff' in citations:
                citation = safe_dic(citations, "cff")
                if citation:
                    citation.replace("`", "")
                # try:
                #     cite = Citation(cffstr=safe_dic(citations,"cff"))
                #     citation = cite.as_bibtex()
                # except:
            else:
                try:
                    citation = citations['citation'][0]
                    # citation = safe_list(safe_dic(citations,citation),0)
                except Exception as e:
                    print(str(e))
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/citation.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom', f"Citation")}>""",
                modal_html=self.modal(
                    title='Citation',
                    body=f'<div style="font-family: monospace;">{highlight(citation, ScdocLexer(), formatter)}</div>',
                    markdown_translation=False,
                    extra_html=f"""
                        <button 
                            class="copy-citation-btn" 
                            value="{self.repo_url()}" 
                            style="background:url('repo_icons/copy.svg')transparent;background-repeat:no-repeat;background-size:auto;" 
                            data-toggle="tooltip" 
                            data-placement="right" 
                            data-original-title="Copy citation">
                        </button>
                        """))
        
        
        '''
        
        # citations propio
        citations = self.citations()

        
        if citations:
            
            citation = None
            #formateador  para highlight y cuadrar
            formatter = HtmlFormatter(linenos=False, full=True, style='friendly')
            body = ""
            

            #  1º ver si hay bibtex y añadirlo al body
            if 'bibtex' in citations and citations['bibtex']:

                bib = safe_dic(citations, "bibtex")
                bib_source = safe_dic(citations, "bibtex_source")

                # Obtener el nombre del archivo del que procede el BibTeX
                source_name = self.metadata_item_source_name({
                    "source": bib_source
                })

                # Crear la etiqueta que se mostrará
                if source_name and source_name.lower() == "readme.md":
                    source_label = "Source README.md"
                elif source_name:
                    source_label = f"Source {source_name}"
                else:
                    source_label = "Source BibTeX"

                formatted_bib = self.format_bibtex(bib)
                parsed_bib = self.parse_bibtex(bib)

                bib_clean = ""
                bib_button = self.copy_button(formatted_bib, "BibTeX")
                
                for key, value in parsed_bib.items():
                    
                    if not value:
                        continue

                    # ignorar campos internos
                    if key in ["ID", "ENTRYTYPE"]:
                        continue

                    # label bonito automático
                    label = key.capitalize()

                    # links
                    if key in ["doi", "url"]:
                        if not str(value).startswith("http") and key == "doi":
                            value = f"https://doi.org/{value}"
                        value = f"<a href='{value}' target='_blank'>{value}</a>"

                    # autores más bonitos
                    if key == "author":
                        value = value.replace(" and ", ", ")

                    bib_clean += f"<b>{label}:</b> {value}<br>"
                        

                body = f"""
                <div style="margin-bottom:15px;">
                    {bib_button}
                </div>
                
                <div style="margin-bottom:15px; max-height:350px; overflow:auto;">
                {self.source_anchor(source_label, bib_source, bold=True)}<br><br>
                
                    <div style="font-size:0.9em;">
                        {bib_clean}
                    </div>
                </div>
                """

            # 2º citation
            elif 'cff' in citations and citations['cff']:

                citation = safe_dic(citations, "cff")
                parsed = self.parse_cff(citation)
                import yaml

                if isinstance(citation, dict):
                    citation = yaml.dump(citation)
                    
                bibtex_generated = self.cff_to_bibtex(citation)
                bib_button = self.copy_button(bibtex_generated, "BibTeX")
                
                if parsed:

                    body = f"""
                    <div style="margin-bottom:15px;">
                        {bib_button}
                    </div>
                    
                    <div style="margin-bottom:15px; max-height:350px; overflow:auto;">
                        {self.source_anchor("Source by .cff", safe_dic(citations, "cff_source"), bold=True)}<br><br>

                        {f"<b>Title:</b> {parsed['title']}<br>" if parsed['title'] else ""}
                        {f"<b>Authors:</b> {parsed['authors']}<br>" if parsed['authors'] else ""}
                        {f"<b>DOI:</b> <a href='{parsed['doi']}' target='_blank'>{parsed['doi']}</a><br>" if parsed['doi'] else ""}
                        {f"<b>Version:</b> {parsed['version']}<br>" if parsed['version'] else ""}
                        {f"<b>Released:</b> {parsed['date']}<br>" if parsed['date'] else ""}
                        {f"<b>License:</b> {parsed['license']}<br>" if parsed['license'] else ""}
                        {f"<b>Code:</b> <a href='{parsed['repo_code']}' target='_blank'>{parsed['repo_code']}</a><br>" if parsed['repo_code'] else ""}
                        {f"<b>Project:</b> <a href='{parsed['url']}' target='_blank'>{parsed['url']}</a><br>" if parsed['url'] else ""}
                    """

                    # keywords
                    if parsed["keywords"]:
                        keywords_str = ", ".join(parsed["keywords"][:6])
                        body += f"<b>Keywords:</b> {keywords_str}<br>"

                    # abstract bonito
                    if parsed["abstract"]:
                        body += f"""
                        <br>
                        <b>Abstract:</b>
                        <details>
                            <summary style="cursor:pointer;">Show abstract</summary>
                            <div style="
                                font-size:0.9em;
                                color:#444;
                                text-align: justify;
                                margin-top:5px;
                                padding:8px;
                                background:#f7f7f7;
                                border-radius:6px;
                                max-height:200px;
                                overflow:auto;
                            ">
                                {parsed['abstract']}
                            </div>
                        </details>
                        """

                    body += "</div>"
        
            # 3º si hay texto de cita añadirlo
            elif 'citation' in citations and citations['citation']:
                

                citation = safe_list(safe_dic(citations, 'citation'), 0)
                citation_source = safe_list(safe_dic(citations, 'citation_sources'), 0)
                body += f"""
                {self.source_anchor("Source by documentation", citation_source, bold=True)}<br><br>
                <div style="
                    font-size:0.95em;
                    line-height:1.5;
                    background:#f7f7f7;
                    padding:10px;
                    border-radius:6px;
                ">
                    {citation}
                </div>
                """

            # si no texto
            elif not body or body == "":

            #else:
                
                body = "<i>No citation available</i>"

            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/citation.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom', "Citation")}>""",
                modal_html=self.modal(
                    title='Citation',
                    body=body,
                    markdown_translation=False
                )
            )

        
            
        '''
        identifier = self.identifier()
        if identifier:
            html += self.icon_wrapper(
                icon_html=f"""<a href="{identifier}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/doi.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom', f"DOI: {identifier}")}>
                    </a>""")
        '''
        
        # modificado para que no se construyan rutas relativas de localhost
        identifier = self.identifier()
        
        if identifier:
            identifier = str(identifier)
            
            doi_url = identifier

            # si no viene como URL → construirla
            if not doi_url.startswith("http"):
                doi_url = f"https://doi.org/{doi_url}"

            html += self.icon_wrapper(
                icon_html=f"""<a href="{doi_url}" target="_blank" class="repo-icon">
                                <img src="{self.base}repo_icons/doi.png" 
                                class="repo-icon" 
                                {self.add_tooltip('bottom', f"DOI: {identifier}")}>
                        </a>"""
            )
                


        status = self.status()
        if status:
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/status.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom', 'Status')}>
                            """,

                modal_html=self.modal(
                    title='Status',
                    body='### Description  \n' +
                    safe_dic(safe_dic(safe_list(status, 0),
                             'result'), 'description')
                         + '\n #### More information  \n' + f'<{safe_dic(safe_dic(safe_list(status, 0), "result"), "value")}>'))




        '''
        installation = self.installation()
        if installation:
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/installation.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom', 'Installation')}>""",

                modal_html=self.modal(
                    title='Installation',
                    body=f'{installation}'))
        '''
        installation = self.installation()
        if installation:

            md_text = ""
            source_item = next((i for i in installation if self.metadata_item_source_name(i)), installation[0])
            for item in installation:
                # header de la instalacion
                header = safe_dic(safe_dic(item, "result"), "original_header")
                # contenido del header
                text = safe_dic(safe_dic(item, "result"), "value")

                if header:
                    md_text += f"### {header}\n\n"

                if text:
                    md_text += text.replace("\n", "  \n") + "\n\n"
                    
                md_text += "---\n\n"
                
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/installation.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom', 'Installation')}>""",

                modal_html=self.modal(
                    title='Installation',
                    body=md_text,                
                    markdown_translation=True,
                    footer_html=self.source_footer_html(source_item)
                )
            )


        '''
        requirements = self.requirements()
        if requirements:
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/requirements.png"  
                        class="repo-icon" 
                        {self.add_tooltip('bottom', 'Requirements')}>""",

                modal_html=self.modal(
                    title='Requirements',
                    body=requirements))
        '''
        
        # propio agrupando requirements
        raw_requirements = self.requirements()

        grouped_reqs = self.group_requirement_files(raw_requirements)
        if grouped_reqs:
            body = """
            <div style="
                max-height:300px;
                overflow:auto;
                display:block;
            ">
                <p style="margin-top:0; margin-bottom:12px;">
                    We found the following installation methods:
                </p>
            """

            for filetype, items in grouped_reqs.items():

                for r in items:
                    source = r.get("source")
                    value = safe_dic(safe_dic(r, "result"), "value")

                    if not source:
                        continue

                    filename = source.split("/")[-1].lower()

                    # README: mostrar el contenido detectado y la fuente al final,
                    # alineada a la derecha y en cursiva.
                    if "readme.md" in filename and value:
                        html_md = mistune.html(value).replace("<p>", "").replace("</p>", "")
                        source_link = self.source_anchor("source: README.md", source)

                        body += f"""
                        <div style="
                            background:#f7f7f7;
                            padding:10px;
                            border-radius:6px;
                            font-size:0.9em;
                            margin-bottom:6px;
                        ">
                            {html_md}
                        </div>

                        <div style="
                            text-align:right;
                            font-style:italic;
                            margin-bottom:12px;
                        ">
                            {source_link}
                        </div>
                        """

                    # Resto de ficheros: mostrar solo el path, sin "(source ...)"
                    else:
                        display = self.get_repo_relative_path(source)
                        github_url = self.raw_to_github_url(source)

                        body += f"""
                        <div style="margin-bottom:8px;">
                            • <a href="{escape(github_url, quote=True)}" target="_blank">
                                {escape(display)}
                            </a>
                        </div>
                        """

            body += "</div>"

            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/requirements.png"  
                        class="repo-icon" 
                        {self.add_tooltip('bottom', 'Requirements')}>""",
                modal_html=self.modal(
                    title='Requirements',
                    body=body,
                    markdown_translation=False
                )
            )
        


                
                
                
                
        usage = self.usage()
        if usage:
            has_i4p = safe_dic(safe_dic(self.md, 'inspect4py'), 'run') # TODO:  inspect4py & run are not keys in the new Results class
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/usage.png"  
                        class="repo-icon" 
                        {self.add_tooltip('bottom', 'Usage')}>""",
                modal_html=self.modal(
                    title='How to use it' if has_i4p and '### How to use it' not in usage else 'Usage',
                    body=usage,
                    footer_html=self.source_footer_html_for_items(safe_dic(self.md, 'usage'))))

        help = self.help()
        if help:
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/help.png"  
                        class="repo-icon" 
                        {self.add_tooltip('bottom', 'Help')}>""",

                modal_html=self.modal(
                    title='Help',
                    body=help,
                    footer_html=self.source_footer_html_for_items([
                        safe_list(safe_dic(self.md, 'support'), 0),
                        safe_list(safe_dic(self.md, 'faq'), 0),
                        safe_list(safe_dic(self.md, 'supportChannels'), 0),
                    ])))

        hasDocumentation = self.hasDocumentation()
        if hasDocumentation:
            if len(hasDocumentation) > 1:
                # mk_list = "\n".join([f'* <{d}>' if ('http' in d and not ' ' in d) else f'* {d}' for d in hasDocumentation])

                mk_list = "\n".join([
                    f'* <{safe_dic(safe_dic(d, "result"), "value")}>' if (
                        self._is_valid_url(safe_dic(safe_dic(d, "result"), "value")))
                    else f'* {safe_dic(safe_dic(d, "result"), "value")}' for d in hasDocumentation
                ])

                html += self.icon_wrapper(
                    icon_html=f"""<img src="{self.base}repo_icons/documentation.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom', "Documentation")}>""",

                    modal_html=self.modal(
                        title='Documentation',
                        body=mk_list))
            else:
                doc = safe_dic(
                    safe_dic(safe_list(hasDocumentation, 0), 'result'), 'value')
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

        acknowledgement = self.acknowledgement()
        if acknowledgement:
            html += self.icon_wrapper(

                icon_html=f"""<img src="{self.base}repo_icons/acknowledgement.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom', f"Acknowledgement")}>""",

                modal_html=self.modal(
                    title='Acknowledgement',
                    body=f'{acknowledgement}'))

        downloadUrl = self.downloadUrl()
        if downloadUrl:
            html += self.icon_wrapper(

                icon_html=f"""<a href="{downloadUrl}" target="_blank" class="repo-icon">
                            <img src="{self.base}repo_icons/download.png" 
                            class="repo-icon" 
                            {self.add_tooltip('bottom', 'Download')}>
                        </a>"""
            )
            
            
        # quality report
        rsfc_report_md = self.rsfc_report_markdown()
        rsfc_score = self.rsfc_report_score()
        resqui_html = self.resqui_report_html()
        resqui_score = self.resqui_report_score()
        sw_bot_html = self.sw_metadata_bot_report_html()

        if (rsfc_report_md and rsfc_score) or resqui_html or sw_bot_html:

            body_parts = []
            tooltip_summary_parts = []

            if rsfc_report_md and rsfc_score:
                passed, total = rsfc_score
                score_text = f"{passed}/{total} checks"

                # Resumen RSFC para el tooltip
                tooltip_summary_parts.append(f"{passed}/{total}")

                report_html = mistune.html(rsfc_report_md)

                body_parts.append(f"""
                <b>
                    FAIR & health: 
                </b>
                    {score_text}
                    <b><a href="https://github.com/oeg-upm/rsfc"
                        target="_blank"
                        rel="noopener noreferrer"
                        style="text-decoration: underline; color: inherit;">
                        (by RSFC)
                    </a>
                </b>
                <br>
                <details class="quality-details">
                    <summary>Show RSFC report</summary>

                    <div class="rsfc-report">
                        {report_html}
                    </div>
                </details>
                """)

            if resqui_html:
                if resqui_score:
                    passed, total = resqui_score
                    tooltip_summary_parts.append(f"RESQUI {passed}/{total}")

                body_parts.append(resqui_html)

            if sw_bot_html:
                sw_bot_data = self.sw_metadata_bot_latest_record()
                issue_count = 0

                if sw_bot_data:
                    record = sw_bot_data["record"]
                    issue_url = record.get("issue_url") or record.get("previous_issue_url")

                    if issue_url:
                        issue_count = 1

                issue_label = "issue" if issue_count == 1 else "issues"
                tooltip_summary_parts.append(f"{issue_count} {issue_label}")

                body_parts.append(sw_bot_html)

            body = "<hr>".join(body_parts)

            tooltip_summary = ", ".join(tooltip_summary_parts)
            tooltip = f"Software Quality and Project Health ({tooltip_summary})" if tooltip_summary else "Software Quality and Project Health"
            
            html += self.icon_wrapper(
                icon_html=f"""<img src="{self.base}repo_icons/quality.png" 
                        class="repo-icon" 
                        {self.add_tooltip('bottom', tooltip)}>""",

                modal_html=self.modal(
                    title="Software Quality and Project Health",
                    body=body,
                    markdown_translation=False
                )
            )
            

        return html




    def _is_valid_url(self, url):
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



    def icon_wrapper(self, icon_html, modal_html=None, other_field=None, extra_class=None):
         return f"""<div {other_field if other_field else ''} class="icon-wrapper{' ' + extra_class if extra_class else ''}">
                        <div class="icon">{icon_html}</div>
                        {modal_html if modal_html else ''}
                     </div>"""



    def modal(self, title, body, markdown_translation=True, extra_html='', footer_html=''):

        if markdown_translation:
            body = mistune.html(body)

        return f"""<div class="modal">
                        <div class="modal-content">
                            <span class="close">&times;</span>
                            <span style="display:flex;">
                                <h2 style="margin-bottom: 1rem;">{title}</h2>
                                {extra_html}
                            </span>
                            <div class="modal-body">{body}</div>
                            {footer_html}
                        </div>
                    </div>"""

    # Metadata ##################################################
    def last_release(self):
        if self.n_releases() != 0:
            if not safe_dic(safe_dic(safe_list(self.releases(), 0), 'result'), 'name'):
                if (tag := safe_dic(safe_dic(safe_list(self.releases(), 0), 'result'), 'tag')):
                    return tag
                else:
                    return "Missing Descriptors"
            return safe_dic(safe_dic(safe_list(self.releases(), 0), 'result'), 'name')
        else:
            return ''
        # return safe_dic(safe_dic(safe_list(self.releases(),0),'result'),'name') if self.n_releases() != 0 else ''

    # TODO
    def repo_type(self):
        if "type" in self.md.keys():
            return self.md["type"]

        langs = self.languages()
        lang_set = set(langs or [])
        title = str(self.title() or "").lower()
        description = str(self.description() or "").lower()
        repo_url = str(self.repo_url() or "").lower()
        searchable_text = f"{title} {description}"

        software_languages = {
            "python", "java", "c", "c++", "c#", "go", "rust", "ruby", "php",
            "r", "scala", "kotlin", "swift", "typescript",
        }
        ontology_formats = {
            "turtle", "rdf", "owl", "sparql", "json-ld", "jsonld",
            "n-triples", "ntriples",
        }
        web_languages = {"html", "css", "javascript", "scss", "sass", "less"}
        ontology_name_terms = (
            "ontolog", "ontologi", "vocab", "vocabulary", "semantic-model",
            "semanticmodel",
        )
        ontology_description_terms = (
            "ontolog", "vocabular", "semantic model", "knowledge model", "domain model"
        )
        ontology_publication_terms = (
            "w3id.org", "vocab.linkeddata.es", "lov.linkeddata.es", "purl.org"
        )
        web_name_terms = ("github.io", "website", "homepage", "portal", "site")
        web_description_terms = (
            "website", "web site", "homepage", "portal", "landing page",
            "static site", "documentation site", "aplicación web",
            "aplicacion web", "sitio web", "página web", "pagina web",
            "web oficial",
        )
        software_terms = (
            "tool", "library", "api", "service", "framework", "generator",
            "extractor", "converter", "parser", "pipeline", "platform",
        )
        software_metadata_keys = (
            "installation", "usage", "requirements", "has_build_file", "inspect4py",
        )

        software_score = 0
        if lang_set.intersection(software_languages):
            software_score += 3
        if "shell" in lang_set:
            software_score += 1
        if any(safe_dic(self.md, key) for key in software_metadata_keys):
            software_score += 2
        if any(term in searchable_text for term in software_terms):
            software_score += 2

        ontology_score = 0
        if safe_dic(self.md, "ontologies"):
            ontology_score += 3
        if any(term in title or term in repo_url for term in ontology_name_terms):
            ontology_score += 3
        if any(term in description for term in ontology_description_terms):
            ontology_score += 2
        if any(term in repo_url for term in ontology_publication_terms):
            ontology_score += 2
        if lang_set.intersection(ontology_formats):
            ontology_score += 1 if software_score else 2

        if ontology_score >= 4 and software_score <= 1:
            return 'ontology'

        web_score = 0
        if lang_set and lang_set.issubset(web_languages) and lang_set.intersection({"html", "css", "javascript"}):
            web_score += 3
        if any(term in title or term in repo_url for term in web_name_terms):
            web_score += 3
        if any(term in description for term in web_description_terms):
            web_score += 2

        if web_score >= 4 and software_score <= 1 and ontology_score < 4:
            return 'web'

        return 'software'

    def metadata_item_value(self, item):
        result = safe_dic(item, 'result')
        return safe_dic(result, 'value') or safe_dic(item, 'excerpt')

    def metadata_item_header(self, item):
        result = safe_dic(item, 'result')
        return (
            safe_dic(result, 'original_header')
            or safe_dic(result, 'originalHeader')
            or safe_dic(item, 'original_header')
            or safe_dic(item, 'originalHeader')
        )

    def metadata_item_source_name(self, item):
        source = safe_dic(item, 'source') or safe_dic(safe_dic(item, 'result'), 'source')
        if not source:
            return None
        source_path = urlparse(source).path if '://' in source else source
        return unquote(os.path.basename(source_path.rstrip('/'))) or source

    def metadata_item_source_url(self, item):
        source = safe_dic(item, 'source') or safe_dic(safe_dic(item, 'result'), 'source')
        return self.raw_to_github_url(source) if source else None

    def source_anchor(self, label, source, bold=False):
        if not source:
            return escape(label)
        github_url = self.raw_to_github_url(source)
        text = f"<strong>{escape(label)}</strong>" if bold else escape(label)
        return f'<a href="{escape(github_url, quote=True)}" target="_blank">{text}</a>'

    def source_footer_html(self, item=None, source=None):
        source_name = self.metadata_item_source_name(item) if item else None
        source_url = self.metadata_item_source_url(item) if item else None
        if source and not source_name:
            source_path = urlparse(source).path if '://' in source else source
            source_name = unquote(os.path.basename(source_path.rstrip('/'))) or source
            source_url = self.raw_to_github_url(source)
        if not source_name:
            return ''
        label = f"source: {source_name}"
        if source_url:
            source = f'<a href="{escape(source_url, quote=True)}" target="_blank">{escape(label)}</a>'
        else:
            source = escape(label)
        return f'<div style="text-align:right; font-style:italic;">{source}</div>'

    def source_footer_html_for_items(self, items):
        footers = ''
        seen_sources = set()
        for item in items or []:
            source_name = self.metadata_item_source_name(item)
            source_url = self.metadata_item_source_url(item)
            source_key = source_url or source_name
            if source_key and source_key not in seen_sources:
                footers += self.source_footer_html(item)
                seen_sources.add(source_key)
        return footers

    def usage(self):
        usage_list = safe_dic(self.md, 'usage')
        usage = None
        if usage_list:
            usage = ''
            '''
            for u in usage_list:
                usage += u['result']['value'] + '\n'
            '''
        # ipmlementacion propia, añade los títulos del markdown
            for u in usage_list:
                value = self.metadata_item_value(u)
                header = self.metadata_item_header(u)

                if header and header.lower() != 'usage':
                    usage += f'\n### {header}\n\n'

                if value:
                    usage += value.rstrip() + '\n\n'
            ###
            
            
        run_list = safe_dic(safe_dic(self.md, 'inspect4py'), 'run') # TODO:  inspect4py & run are not keys in the new Results class
        if run_list:
            if isinstance(run_list, list):
                run = '\n'.join(
                    [f'* {str(x).replace(self.repo_metadata_dir, "")}' for x in run_list])
            else:
                run = run_list.replace(self.repo_metadata_dir, "")
            run_md = '---\n  ### How to use it  \n' + run if usage else run

        else:
            run_md = ''

        usage = usage if usage else ''

        return usage + run_md if usage or run_md else None

    # TODO cannot find correct implementation
    def help(self):
        support_item = safe_list(safe_dic(self.md, 'support'), 0)
        faq_item = safe_list(safe_dic(self.md, 'faq'), 0)
        supportChannels_item = safe_list(safe_dic(self.md, 'supportChannels'), 0)

        support = self.metadata_item_value(support_item)
        faq = self.metadata_item_value(faq_item)
        supportChannels = self.metadata_item_value(supportChannels_item)

        support_md = ('### Support  \n' + support + '\n\n') if support else ''
        faq_md = ('### FAQ  \n' + faq + '\n\n') if faq else ''
        supportChannels_md = ('### Support Channels  \n' + supportChannels + '\n\n') if supportChannels else ''

        return support_md + faq_md + supportChannels_md if support or faq or supportChannels else None

    def recently_updated(self):
        # TODO: Retreive days_threshold from properties file
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
        value = safe_dic(
            safe_dic(
                safe_list(safe_dic(self.md, "identifier"), 0),
                "result"
            ),
            "value"
        )

        if not value:
            return None

        # Lista real
        if isinstance(value, list):
            value = value[0] if value else None

        # Cadena que representa una lista:
        # "['https://doi.org/10.5281/zenodo.xxxxxxx']"
        elif isinstance(value, str):
            cleaned = value.strip()

            if cleaned.startswith("[") and cleaned.endswith("]"):
                try:
                    parsed = ast.literal_eval(cleaned)

                    if isinstance(parsed, list) and parsed:
                        value = parsed[0]
                except (ValueError, SyntaxError):
                    pass

        if not value:
            return None

        return str(value).strip()

    def status(self):
        return safe_dic(self.md, 'repository_status')

    def acknowledgement(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md, 'acknowledgement'), 0), 'result'), 'value')

    def hasDocumentation(self):
        docList = safe_dic(self.md, 'documentation')
        return docList if docList else None


    def requirements(self):
        reqs = safe_dic(self.md, 'requirements')
        if not reqs:
            return None
        '''
        for d in reqs:
            source = d.get("source")
            if source == "https://raw.githubusercontent.com/oeg-upm/rsfc/main/README.md":
                print("ENCONTRADO EN README:")
                import json
                print(json.dumps(reqs, indent=4, ensure_ascii=False))
        '''        
 
        return reqs

       
    def installation(self):
        inst = safe_dic(self.md, 'installation')
        if not inst:
            return None
        return inst

    
    '''
    def installation(self):
        inst = safe_dic(self.md, 'installation')
        import json

        if not inst:
            return None

        values = []

        for d in inst:
            source = d.get("source")

            if source == "https://raw.githubusercontent.com/oeg-upm/rsfc/main/README.md":
                print("ENCONTRADO EN README:")
                print(json.dumps(inst, indent=4, ensure_ascii=False))


            values.append(safe_dic(safe_dic(d, 'result'), 'value'))

        return "\n".join(values)
    '''
    
    '''
    def docker(self):

        hasBuildFileList = safe_dic(self.md, 'has_build_file')
        if not hasBuildFileList:
            return None
    
        return [safe_dic(safe_dic(d, 'result'), 'value') for d in hasBuildFileList]
    '''
    
    # implementación para sacar los requirements del build file y que no haya requirements.txt
    # esto para que se filtre bien todo en el portal
    def docker(self):

        hasBuildFileList = safe_dic(self.md, 'has_build_file')

        if not hasBuildFileList:
            return None

        urls = [safe_dic(safe_dic(d, 'result'), 'value') for d in hasBuildFileList]

        grouped = self.group_build_files(urls)

        if not grouped:
            return None

        # devolver SOLO los archivos válidos
        filtered_urls = []
        for v in grouped.values():
            filtered_urls.extend(v)

        return filtered_urls
    
    
    

    def downloadUrl(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md, 'download_url'), 0), 'result'), 'value') \
            if self.n_releases() > 0 else None

    # TODO change name to something more self explanatory
    def notebook(self):
        exe_l = safe_dic(self.md, 'executable_example')
        exe_l = exe_l if exe_l else []
        exe = [x['result']['value'] for x in exe_l]
        return exe if len(exe) > 0 else None

    '''
    def readme(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md, 'readme_url'), 0), 'result'), 'value')
    '''
    
    
    # nuevo readme para leer del readme desde gitub y no raw
    def readme(self):
        raw_url = safe_dic(safe_dic(safe_list(safe_dic(self.md, 'readme_url'), 0), 'result'), 'value')
        
        if not raw_url:
            return None

        if "raw.githubusercontent.com" in raw_url:
            parts = raw_url.split("/")
            user = parts[3]
            repo = parts[4]
            branch = parts[5]
            filename = parts[-1]
            return f"https://github.com/{user}/{repo}/tree/{branch}/{filename}"

        return raw_url

    def languages(self):
        langs = safe_dic(self.md, 'programming_languages')
        if not langs:
            return None

        values = [
            str(safe_dic(safe_dic(lang, 'result'), 'value')).lower()
            for lang in langs
            if safe_dic(safe_dic(lang, 'result'), 'value')
        ]

        return list(dict.fromkeys(values))

    def repo_url(self):
        return safe_dic(safe_list(safe_dic(safe_dic(self.md, 'code_repository'), 0), 'result'), 'value')

    def title(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md, 'name'), 0), 'result'), 'value')

    def _metadata_confidence(self, item):
        result = safe_dic(item, 'result') or {}
        raw_confidence = safe_dic(result, 'confidence')
        if raw_confidence is None:
            raw_confidence = safe_dic(item, 'confidence')

        try:
            return float(raw_confidence)
        except (TypeError, ValueError):
            return None

    def _technique_matches(self, item, expected_technique):
        technique = str(safe_dic(item, 'technique') or '').lower().replace('_', ' ')
        return technique == expected_technique.lower().replace('_', ' ')

    def _normalize_description_value(self, value):
        if value is None:
            return None

        if isinstance(value, list):
            for item in value:
                normalized = self._normalize_description_value(item)
                if normalized:
                    return normalized
            return None

        if isinstance(value, dict):
            for nested_key in ('value', 'text', 'name'):
                normalized = self._normalize_description_value(safe_dic(value, nested_key))
                if normalized:
                    return normalized
            return None

        text = str(value).strip()
        return text or None

    def _metadata_values(self, field_name):
        values = safe_dic(self.md, field_name) or []
        return values if isinstance(values, list) else []

    def first_metadata_value(self, field_name, preferred_technique=None):
        values = self._metadata_values(field_name)

        if preferred_technique:
            for value in values:
                if not self._technique_matches(value, preferred_technique):
                    continue

                result = safe_dic(value, 'result') or {}
                normalized = self._normalize_description_value(
                    safe_dic(result, 'value')
                )
                if normalized:
                    return normalized

        for value in values:
            result = safe_dic(value, 'result') or {}
            normalized = self._normalize_description_value(
                safe_dic(result, 'value')
            )
            if normalized:
                return normalized

        return None

    def homepage(self):
        candidates = []

        for index, item in enumerate(self._metadata_values('homepage')):
            result = safe_dic(item, 'result') or {}
            homepage = self._normalize_description_value(
                safe_dic(result, 'value')
            )
            if not homepage or not self._is_valid_url(homepage):
                continue

            candidates.append((
                index,
                homepage,
                self._metadata_confidence(item),
                0 if self._technique_matches(item, 'GitHub API') else 1,
            ))

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda candidate: (
                candidate[3],
                -(candidate[2] if candidate[2] is not None else -1.0),
                candidate[0],
            ),
        )[1]

    def application_domain(self):
        return self.first_metadata_value('application_domain')

    # TODO find new
    def description(self):

        all_descriptions = safe_dic(self.md, 'description')
        candidates = []

        if all_descriptions:
            for index, item in enumerate(all_descriptions):
                result = safe_dic(item, 'result') or {}
                description = self._normalize_description_value(
                    safe_dic(result, 'value')
                )
                if not description:
                    continue

                candidates.append((
                    index,
                    description,
                    self._metadata_confidence(item),
                    0 if self._technique_matches(item, 'GitHub API') else 1,
                ))

        if not candidates:
            return 'No description available yet.'

        return min(
            candidates,
            key=lambda candidate: (
                candidate[3],
                -(candidate[2] if candidate[2] is not None else -1.0),
                len(candidate[1]),
                candidate[0],
            ),
        )[1]

    def license(self):
        license = safe_dic(
            safe_list(safe_dic(self.md, 'license'), 0), 'result')
        if (typ := safe_dic(license, "type")) and ((typ == "File_dump") or (typ == "Text_excerpt")):
            self._find_license_name(license)
            return license
        else:
            return license

    def _find_license_name(self, license):
        find_name = safe_dic(license, "value")
        if 'Apache' in find_name:
            license['name'] = 'Apache License 2.0'
            license['url'] = 'https://api.github.com/licenses/apache-2.0'
        elif 'MIT' in find_name:
            license['name'] = 'MIT License'
            license['url'] = 'https://api.github.com/licenses/MIT'
        elif 'GPL' in find_name:
            license['name'] = 'GNU General Public License v3.0'
            license['url'] = 'https://api.github.com/licenses/gpl-3.0'
        else:
            license['name'] = 'Other'

    def last_update(self):
        result = safe_dic(
            safe_list(safe_dic(self.md, 'date_updated'), 0), 'result')
        date_modified_str = of_correctType(result, 'Date')[:-1]
        date_modified = datetime.strptime(
            date_modified_str, '%Y-%m-%dT%H:%M:%S')
        return date_modified

    def last_update_days(self):
        date_of_extraction_str = safe_dic(
            safe_dic(self.md, 'somef_provenance'), 'date')[:]
        date_of_extraction = datetime.strptime(
            date_of_extraction_str, '%Y-%m-%d %H:%M:%S')
        last_update = self.last_update()
        return (date_of_extraction - last_update).days

    def stars(self):
        value = safe_dic(safe_dic(safe_list(safe_dic(self.md, 'stargazers_count'), 0), 'result'), 'value')
        if value is None or value == "" or str(value).lower() == "none":
            return 0
        return value
    
    def n_releases(self):
        rel = safe_dic(self.md, 'releases')
        return len(rel) if rel is not None else 0

    def releases(self):
        return safe_dic(self.md, 'releases')

    def url_releases(self):
        return safe_dic(safe_dic(safe_list(safe_dic(self.md, 'download_url'), 0), 'result'), 'value')

    def url_stars(self):
        return self.repo_url() + '/stargazers'

    def owner(self):
        owner = safe_dic(safe_dic(safe_list(safe_dic(self.md, 'owner'), 0), 'result'), 'value')
        owner = self._clean_owner(owner)
        if owner:
            return owner

        repo_url = self.repo_url()
        if not repo_url:
            return None

        parsed_url = urlparse(repo_url.rstrip("/"))
        path_parts = [part for part in parsed_url.path.split("/") if part]
        if parsed_url.netloc.lower() != "github.com" or len(path_parts) < 2:
            return None

        return self._clean_owner(path_parts[-2])

    def _clean_owner(self, owner):
        if owner is None:
            return None

        owner = str(owner).strip()
        if not owner or owner.lower() in {"none", "null", "undefined"}:
            return None

        return owner

    # IMPORTANT !!!!! ASSUMES only 1 CFF per repo
    # USE SOMEF as example it lists SOMEF CFF then WIDOCO then SOMEF then CAPTUM
    def citations(self):
        all_citations = safe_dic(self.md, 'citation')

        if not all_citations:
            return None

        citations = {'citation': []}

        for c in all_citations:
            source = safe_dic(c, 'source') or safe_dic(safe_dic(c, 'result'), 'source')
            try:
                type = ""
                type = c['result']['format']
            except:
                try:
                    if c['result']['type'] == 'Text_excerpt':
                        citations['citation'].append(c['result']['value'])
                        if source:
                            citations.setdefault('citation_sources', []).append(source)
                except:
                    continue
            match type:
                case 'cff':
                    citations['cff'] = c['result']['value']
                    if source:
                        citations['cff_source'] = source
                case 'bibtex':
                    citations['bibtex'] = c['result']['value']
                    if source:
                        citations['bibtex_source'] = source
                case _:
                    continue
        # return citations if len(citations) > 0 else None
        test = len(citations)
        
        '''COMENTADO POR PROPIO'''
        '''return citations if bool(citations) else None '''

        has_content = (
            citations.get("bibtex") is not None or
            citations.get("cff") is not None or
            (citations.get("citation") and len(citations.get("citation")) > 0)
        )

        return citations if has_content else None
    # Originally citations Took the ver8 somef "regular expression" output and would create a list of excerpts

    def paper(self):
        citations = safe_dic(self.citations(), 'citation')
        p = []
        if citations:
            for cita in citations:

                c = CitationParser(cita)

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


class CitationParser(object):

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
