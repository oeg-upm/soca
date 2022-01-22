import csv
import json

from somef.cli import cli_get_data

def fetch(repos_csv, output):

    r_metadata = {}

    with open(output, 'w') as repos_metadata:

        with open(repos_csv) as repos:
            csv_reader = csv.reader(repos, delimiter=',')
            for repo_url in csv_reader:
                print(f"Extracting metadata from {repo_url[0]}")
                r_metadata[repo_url[0]] = cli_get_data(0.9, False, repo_url[0])

        json.dump(r_metadata, repos_metadata, indent = 4)
        

