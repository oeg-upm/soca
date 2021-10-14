import requests
import csv
import click

__version__ = "0.0.1"


@click.command()
@click.version_option(__version__)
@click.option('-org', '--organization', type=str, required=True, help="organization name in GitHub. Example: oeg-upm")
@click.option('-o', '--out_path', type=str, default="repositories.csv", help="output file path. Default is repositories.csv")
def get_repositories(organization, out_path):

    URL = "https://api.github.com/orgs/" + organization + "/repos"

    page_size = 50

    page = 1

    PARAMS = {'per_page':page_size,'page':page}

    cont = True

    with open(out_path, 'w') as file_out:
        writer = csv.writer(file_out, delimiter=',')
        while cont:
            print("Request " + str(page) + ". " + str(page_size) + " repositories are downloaded per request")
            r = requests.get(url = URL, params = PARAMS)
            data_repos = r.json()
            page += 1
            PARAMS['page'] = page
            for repo in data_repos:
                writer.writerow([repo["html_url"]])

            if len(data_repos) < 50:
                cont = False

if __name__ == '__main__':
    get_repositories()
