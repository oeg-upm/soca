import csv
import json
import os
from os import path
from progressbar import progressbar
from somef.somef_cli import cli_get_data
from soca import HiddenPrints
import subprocess
import shutil
import traceback
import datetime

import requests
import pprint


def extract(repos_csv, output, use_inspect4py, verbose):
    """
    @Param repos_csv: input file from the fetch command, A list of github urls
    @Param output: defined output file
    @Param use_inspect4py: Bool to indicate desire to use inspect4py
    @Param verbose: Bool to choose whether or not to Fetch only repos that are not archived

    Returns:
    @return: folder with a json file per repo url within repos.csv
    """
    # Make output dir
    if not os.path.exists(output):
        os.makedirs(output)

    if os.path.isfile(repos_csv):
        with open(repos_csv) as repos:
            repos_url = [c[0] for c in csv.reader(repos, delimiter=',')]
    else:
        repos_url = str(repos_csv).split(",")

    failed_repos = []
    failed_repos_i4p = []

    print("It may take a while... Depends on repository size and Github API limitations.")
    for repo_url in progressbar(repos_url, redirect_stdout=True):

        try:
            git_clone_dir = f'{output}/' + str(repo_url).split("/")[-1]
        except:
            continue

        ##################################################################
        # somef

        try:
            print(f"Extracting metadata from {repo_url}")
            if not verbose:
                with HiddenPrints():
                    metadata = cli_get_data(0.9, False, repo_url, keep_tmp=git_clone_dir)
                    #metadata = cli_get_data(0.9, False, repo_url, None, False, False, False, keep_tmp=git_clone_dir)
                    
            else:
                metadata = cli_get_data(0.9, False, repo_url, keep_tmp=git_clone_dir)
                #metadata = cli_get_data(0.9, False, repo_url, None, False, False, False, keep_tmp=git_clone_dir)
            if not metadata:
                #print(f'ERROR: {repo_url} is down, skipping it...')
                print(f'ERROR: unable to extract from {repo_url}, skipping it...')
                failed_repos.append(repo_url)
                continue
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            # traceback.print_exc()
            try:
                continue
            except:
                print(f"ERROR: Could not extract metadata from {repo_url}")
                continue
            print(str(e))
            failed_repos.append(repo_url)
            continue

        ##################################################################
        # inspect4py

        if use_inspect4py and 'programming_languages' in metadata.results\
                and any(lang['result']['value'] == "Python" for lang in metadata.results['programming_languages']):
            try:
                metadata.results["inspect4py"] = {}

                if verbose:
                    subprocess.call(
                        f'inspect4py -i {git_clone_dir} -o {output}/inspect4py_tmp -si',
                        shell=True
                    )
                else:
                    subprocess.call(
                        f'inspect4py -i {git_clone_dir} -o {output}/inspect4py_tmp -si',
                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
                    )

                if path.exists(f'{output}/inspect4py_tmp/directory_info.json'):

                    with open(f'{output}/inspect4py_tmp/directory_info.json') as f:
                        ins4py = json.load(f)

                    if 'software_type' in ins4py:
                        metadata.results["inspect4py"]["software_type"] = ins4py["software_type"]

                    if ('software_invocation' in ins4py
                            and isinstance(ins4py["software_invocation"], list)
                            and 'run' in ins4py["software_invocation"][0]):
                        metadata.results["inspect4py"]["run"] = ins4py["software_invocation"][0]["run"]

                else:
                    print(
                        f'ERROR: inspect4py did not create "{output}/inspect4py_tmp/directory_info.json" file. NO python metadata extracted.')

                if path.exists(f'{output}/inspect4py_tmp'):
                    shutil.rmtree(f'{output}/inspect4py_tmp', ignore_errors=False, onerror=None)

                if path.exists(git_clone_dir):
                    shutil.rmtree(git_clone_dir, ignore_errors=False, onerror=None)

            except KeyboardInterrupt:

                if path.exists(git_clone_dir):
                    shutil.rmtree(git_clone_dir, ignore_errors=False, onerror=None)

                exit()

            except:

                if path.exists(git_clone_dir):
                    shutil.rmtree(git_clone_dir, ignore_errors=False, onerror=None)

                print(f"ERROR: Could not run inspect4py for {repo_url}")
                traceback.print_exc()
                failed_repos_i4p.append(repo_url)

        ##################################################################
        # How to add more metadata extraction tools
        # 1. Extract metadata and save it into json file, se below.
        # 2. Use that extracted metadata in metadata.py
        #
        #    Ultimately, the metadata should be present in 'def html_repo_icons(self)'
        #    But is highly encouraged to use the helper function such as self.notebook(), self.docker(), etc,
        #    to extract the metadata from the .json created in this file.

        # if flag_tool selected:
        #   try:
        #       result = run_tool()
        #       metadata['tool_name'] = result
        #   except KeyboardInterrupt:
        #       exit()
        #   except:
        #       traceback.print_exc()
        #       print(f"ERROR: Could not run XX tool for {repo_url}")
        #       failed_repos.append(repo_url)
        #       continue
        #

        # Save metadata
        # repo_full_name = (repo_url[19:]).replace("/", "_").replace(".", "-")
        # with open(f"{output}/{repo_full_name}.json", 'w') as repo_metadata:
        #     json.dump(metadata.results, repo_metadata, indent=4)
        repo_full_name = (repo_url[19:]).replace("/", "_").replace(".", "-")
        today = datetime.date.today().strftime("%Y-%m-%d")
        with open(f"{output}/{repo_full_name}_{today}.json", 'w') as repo_metadata:
            json.dump(metadata.results, repo_metadata, indent=4)

    if len(failed_repos_i4p) > 0:
        print("ERROR: inspect4py could not be ran in the following repo/s:")
        for fr in failed_repos_i4p:
            print(fr)

    if len(failed_repos) > 0:
        print("ERROR: metadata could not be extracted from the following repo/s:")
        for fr in failed_repos:
            print(fr)

    print(
        f"\n✅ Successfully extracted metadata from ({len(repos_url) - len(failed_repos)}/{len(repos_url)}) repositories.")

#This function is to enable the extraction of sufficient information for the creation of a card of a repository without
#readme
#This is due to somef not generating any json if the repository does not have a readme
#This may be fixed in future as there is an issue open. Hence TODO

# def _no_readme():
#     try:
#         next
#     except Exception as e:
#         print(str(e))