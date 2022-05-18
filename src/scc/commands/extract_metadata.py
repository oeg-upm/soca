import csv
import json
import os
from progressbar import progressbar
from somef.cli import cli_get_data
import os
from os import path
from scc import HiddenPrints
import subprocess
import shutil
import traceback

def fetch(repos_csv, output, use_inspect4py, verbose):

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
    failed_repos_i4p = []
    for repo_url in progressbar(repos_url, redirect_stdout=True):
        try:
            print(f"Extracting metadata from {repo_url}")
            if not verbose:
                with HiddenPrints():
                    metadata = cli_get_data(0.9, False, repo_url)
            else: metadata = cli_get_data(0.9, False, repo_url)
            if not metadata:
                print(f'ERROR: {repo_url} is down, skipping it...')
                failed_repos.append(repo_url)
                continue
        except KeyboardInterrupt:
            exit()
        except:
            #traceback.print_exc()
            print(f"ERROR: Could not extract metadata from {repo_url}")
            failed_repos.append(repo_url)
            continue

        if use_inspect4py and 'languages' in metadata and 'Python' in metadata["languages"]["excerpt"]:
            try:
                metadata["inspect4py"] = {}
                if verbose:
                    subprocess.call(
                                    f'cd {output} && git clone {repo_url} && inspect4py -i {str(repo_url).split("/")[-1]} -o inspect4py_tmp -si && cd ..', 
                                    shell = True
                                )
                else:
                    subprocess.call(
                                        f'cd {output} && git clone {repo_url} && inspect4py -i {str(repo_url).split("/")[-1]} -o inspect4py_tmp -si && cd ..', 
                                        shell = True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
                                    )
                if path.exists(f'{output}/inspect4py_tmp/directory_info.json'):        
                    with open(f'{output}/inspect4py_tmp/directory_info.json') as f:
                        ins4py = json.load(f)

                    if 'software_type' in ins4py:
                        metadata["inspect4py"]["software_type"] = ins4py["software_type"]

                    if ('software_invocation' in ins4py 
                        and isinstance(ins4py["software_invocation"],list)
                        and 'run' in ins4py["software_invocation"][0]):
                        metadata["inspect4py"]["run"] = ins4py["software_invocation"][0]["run"]

                shutil.rmtree(f'{output}/inspect4py_tmp', ignore_errors=False, onerror=None)
                shutil.rmtree(f'{output}/{str(repo_url).split("/")[-1]}', ignore_errors=False, onerror=None)
            except:
                shutil.rmtree(f'{output}/{str(repo_url).split("/")[-1]}', ignore_errors=False, onerror=None)
                print(f"ERROR: Could not run inspect4py for {repo_url}: Error in {'sowftware_type' if 'sowftware_type' not in metadata['inspect4py'] else ''} {'software_invocation' if 'run' not in metadata['inspect4py'] else ''}")
                traceback.print_exc()
                failed_repos_i4p.append(repo_url)

            
        repo_full_name = (repo_url[19:]).replace("/", "_").replace(".","-")
        with open(f"{output}/{repo_full_name}.json", 'w') as repo_metadata:
            json.dump(metadata, repo_metadata, indent = 4)

    if len(failed_repos_i4p) > 0:
        print("ERROR: inspect4py could not be ran in the following repo/s:")
        for fr in failed_repos_i4p:
            print(fr)

    if len(failed_repos) > 0:
        print("ERROR: metadata could not be extracted from the following repo/s:")
        for fr in failed_repos:
            print(fr)
    
    print(f"\n✅ Successfully extracted metadata from ({len(repos_url)-len(failed_repos)}/{len(repos_url)}) repositories.")

