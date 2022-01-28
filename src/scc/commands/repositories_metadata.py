import csv
import json
import os

from somef.cli import cli_get_data

def fetch(repos_csv, output):

    # Make output dir
    if not os.path.exists(output):
        os.makedirs(output)

    with open(repos_csv) as repos:

        csv_reader = csv.reader(repos, delimiter=',')

        for repo_url in csv_reader:
            try:

                print(f"Extracting metadata from {repo_url[0]}")
                metadata = cli_get_data(0.9, False, repo_url[0])
                repo_full_name = (repo_url[0][19:]).replace("/", "_").replace(".","-")

                with open(f"{output}/{repo_full_name}.json", 'w') as repo_metadata:
                    json.dump(metadata, repo_metadata, indent = 4)

            except KeyboardInterrupt:
                exit()      
                  
            except:
                print(f"ERROR: Could not extract metadata from {repo_url[0]}")
        

