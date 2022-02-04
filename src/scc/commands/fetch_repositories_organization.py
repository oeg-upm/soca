import os
import requests
import csv

def fetch(input, output):

    open(output, 'w')

    if os.path.isfile(input):
        with open(input) as org_list:
            for org in org_list.readlines():
                fetch_org(org.rstrip("\n"), output)
    else:
        fetch_org(input, output)


def fetch_org(organization, out_path):

    print(f"Fetching repositories from {organization}:")

    URL = "https://api.github.com/orgs/" + organization + "/repos"
    page_size = 50
    page = 1
    PARAMS = {'per_page':page_size,'page':page}

    cont = True

    with open(out_path, 'a') as file_out:
        writer = csv.writer(file_out, delimiter=',')
        while cont:
            try:
                r = requests.get(url = URL, params = PARAMS)
                data_repos = r.json()
                print("    Request " + str(page) + ". " + str(len(data_repos)) + " repositories are downloaded per request")
                page += 1
                PARAMS['page'] = page
                for repo in data_repos:
                    writer.writerow([repo["html_url"]])

                if len(data_repos) < 50:
                    cont = False
            except Exception as e: 
                print(f"ERROR: '{organization}' does not exist.")
                return

