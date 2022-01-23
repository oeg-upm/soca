import os
from distutils.dir_util import copy_tree
import pathlib
from bs4 import BeautifulSoup

def generate(input, output):

    # Project base path
    base = str(pathlib.Path(__file__).parent.parent.resolve())
    
    # Make output dir
    if not os.path.exists(output):
        os.makedirs(output)

    # Copy all img to destination folder
    copy_tree(f"{base}/assets/img", f"{output}/img")

    # load the file
    with open(f"{base}/assets/template.html") as template:
        soup = BeautifulSoup(template.read(), features="html.parser")

    insert_repos_cards(soup)

    # save the file again
    with open(f"{output}/index.html", "w") as index:
        index.write(str(soup))


def insert_repos_cards(soup):

    loc = soup.find(id="myCards")

    titles = ["Meta","Amazon","Netflix","Google","Microsoft"]

    for t in titles:
        html_component = BeautifulSoup(card_view(t), 'html.parser')
        loc.append(html_component)


def card_view(title):
    html_card = f"""
      <article class="item">
	  <h4 class="title">{title}</h4>
	  <img src="img/summico.png" class="ico">
	  <div class="description">
	  	<p><b>EL</b> matches domain-specific entities in the given text and then disambiguates the matches.</p>
	  </div>
   	<div class="bottom">      
      <a href="lynx-swagger-ui.html?openapi-server-url=https://apis.lynx-project.eu/doc/open-api-3/entity-linking"><img src="img/openapi.png" width="24" alt="API description"></a>
      <a href="https://www.poolparty.biz/"><img src="img/home.png" width="24" alt="Webpage"></a>
      <a href="https://zenodo.org/record/3558282#"><img src="img/pdf24.png" width="24" alt="Deliverable"></a>
		  <a href="https://www.youtube.com/watch?v=hDgk65GuORc"><img src="img/youtube.png" width="24" alt="Video"></a>        
    </div>
    <div class="bottom" style="right:10px; float:right;">
      <small>
        <kbd title="English">EN</kbd><kbd title="Spanish">ES</kbd><br>
        <kbd title="German">DE</kbd><kbd title="Dutch">NL</kbd>
      </small>
    </div> 
  </article>"""

    return html_card