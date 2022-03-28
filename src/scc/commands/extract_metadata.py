import csv
import json
import os
from progressbar import progressbar
from somef.cli import cli_get_data
import os
from scc import HiddenPrints


def fetch(repos_csv, output):

    # Make output dir
    if not os.path.exists(output):
        os.makedirs(output)
    
    if os.path.isfile(repos_csv):
        with open(repos_csv) as repos:
            repos_url = [c[0] for c in csv.reader(repos, delimiter=',')]
    else:
        repos_url = str(repos_csv).split(",")

    print("It may take a while... Depends on repository size and Github API limitations.")
    failed_repos = []
    for repo_url in progressbar(repos_url, redirect_stdout=True):
        try:
            print(f"Extracting metadata from {repo_url}")
            with HiddenPrints():
                metadata = cli_get_data(0.9, False, repo_url)
            repo_full_name = (repo_url[19:]).replace("/", "_").replace(".","-")
            with open(f"{output}/{repo_full_name}.json", 'w') as repo_metadata:
                json.dump(metadata, repo_metadata, indent = 4)

        except KeyboardInterrupt:
            exit()      
              
        except:
            print(f"ERROR: Could not extract metadata from {repo_url}")
            failed_repos.append(repo_url)
    
    if len(failed_repos) > 0:
        print("ERROR: metadata could not be extracted from the following repo/s:")
        for fr in failed_repos:
            print(fr)
    
    print(f"\n✅ Successfully extracted metadata from ({len(repos_url)-len(failed_repos)}/{len(repos_url)}) repositories.")

