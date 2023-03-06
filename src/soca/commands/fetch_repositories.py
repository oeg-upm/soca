import json
import os
import requests
import csv
from pathlib import Path




def fetch(input, output, type, not_archived, not_forked, not_disabled):


   open(output, 'w')


   if os.path.isfile(input):
       with open(input) as org_list:
           for org in org_list.readlines():
               _fetch(org.rstrip("\n"), output, type, not_archived, not_forked, not_disabled)
   else:
       _fetch(input, output, type, not_archived, not_forked, not_disabled)




def _fetch(name, out_path, type, not_archived, not_forked, not_disabled):


   if type not in ['orgs','users']:
       raise ValueError(f'Type {type} is not supported.')


   print(f"Fetching repositories from {type} {name}:")


   URL = f"https://api.github.com/{type}/{name}/repos"
   page_size = 50
   page = 1
   PARAMS = {'per_page':page_size,'page':page}
   #TOKEN
   hasToken = False
   try:
       if os.path.isfile(Path("~/.somef/config.json").expanduser()):
           with open(Path("~/.somef/config.json").expanduser()) as json_file:
               data = json.load(json_file)
       try:
           TOKEN = data['Authorization']
           HEADERS = {
               "accept": "application/vnd.github.v3+json",
               "Authorization": TOKEN
           }
           hasToken = True
       except:
           print("please provide Valid Authorisation Token\n")
           print("Will commence fetch WITHOUT token \n")
   except Exception as e:
       print(str(e))


   cont = True


   with open(out_path, 'a') as file_out:
       writer = csv.writer(file_out, delimiter=',')
       while cont:
           try:
               if not hasToken:
                   r = requests.get(url = URL, params = PARAMS)
               else:
                   r = requests.get(url = URL, params = PARAMS, headers = HEADERS)


               data_repos = r.json()
               print("Request " + str(page) + ". " + str(len(data_repos)) + " repositories are downloaded per request")
               page += 1
               PARAMS['page'] = page
               for repo in data_repos:
                   if (
                       (not not_archived or not repo["archived"])
                       and
                       (not not_forked or not repo["fork"])
                       and
                       (not not_disabled or not repo["disabled"])
                   ):
                       writer.writerow([repo["html_url"]])
                   else: print(f"    - The repository '{repo['url']}' has been filtered out...")


               if len(data_repos) < 50:
                   cont = False
           except Exception as e:
               print(str(e))
               print(f"ERROR: '{type} {name}'")
               return
