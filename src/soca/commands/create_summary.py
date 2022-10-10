import json
import os
from datetime import datetime
from os import path

#TODO fix: change to variable path
directory = "/home/two_play2nd/git/soca_Miguel_Arroyo_TFG/example"
__listOrg = list()

#IMPORTANT used to create json
output = {}
#TODO CLEANUP
#model of output json

#output['timestamp'] = datetime.now()+""


def reset_dict():
 #   output['timestamp'] = datetime.now()+""
    output['has_documentation'] = 0
    output['identifiers'] = {'num_doi': 0, 'num_pid': 0}
    output['readme'] = {'EMPTY': 0, 'OK': 0, 'GOOD': 0, 'GREAT': 0}
    output['licenses'] = {'APACHE': 0, 'MIT': 0, 'GPL': 0, 'OTHER': 0}
    output['releases'] = {'IN PROGRESS': 0, 'UPDATED': 0}
    output['has_citation'] = 0
    output['releases'] = {'IN PROGRESS': 0, 'UPDATED':0}

reset_dict()

#function to return list of available organisations

def find_organisations():
    for dir in os.listdir(directory):
        if dir not in __listOrg and os.path.isdir(directory+"/"+dir):
            __listOrg.append(dir)


#function to create directory named summary to save summaries if doesnt exist already
def create_summary_dir(self):
    if not os.path.exists(directory+"/summary"):
        os.makedirs(directory+"/summary")
        print("summary directory created")
    else:
        print("summary directory already exists")



#function that return true if given good practice is found
def __has_doi(json_obj):
    if "doi.org" in json_obj['html_card_embedded']:
        return True
def __has_pid(json_obj):
    if "zenodo" or "Zenodo" in json_obj['html_card_embedded']:
        return True

def __has_MIT(json_obj):
    if "License: Apache" in json_obj['html_card_embedded']:
        return True
def __has_APACHE(json_obj):
    if "License: MIT" in json_obj['html_card_embedded']:
        return True
def __has_GPL(json_obj):
    if "License: GPL" in json_obj['html_card_embedded']:
        return True

#function given a json object will give readme score OK, GOOD, GREAT, EMPTY
#TODO clean UP
def readme_score(json_obj):
    score = 0
    #if no readme return EMPTY
    if not json_obj['readmeUrl']:
        return "EMPTY"
    else:
        if json_obj['installation']:
            score +=1
        if json_obj['acknowledgement']:
            score +=1
        #TODO
        if json_obj['requirement']:
            score +=1
        #TODO
        if json_obj['description'] is not None:
            score +=1

    if score > 3:
        return "GREAT"
    if score > 2:
        return "GOOD"
    if score <= 2:
        return "OK"

#function that opens array of jsons given the organisation
def __open_Json(dir):
    file_dir = directory + "/" + dir + "/" + "cards_data.json"
    with open(file_dir) as json_file:
        data = json.load(json_file)
        return data

#function to create summary for each organisation
def create_summary():
    #updates the list of organisations 
    find_organisations()
    for org in __listOrg:
        json_array = __open_Json(org)
        for item in json_array:
            if item['hasDocumentation']:
                output['has_documentation'] = output['has_documentation']+1
            if item['identifier']:
                if __has_doi(item):
                    output['identifiers']['num_doi'] = output['identifiers']['num_doi'] + 1
                if __has_pid(item):
                    output['identifiers']['num_pid'] = output['identifiers']['num_pid'] + 1
            if item['license']:
                if __has_MIT(item):
                    output['licenses']['MIT'] = output['licenses']['MIT'] + 1
                elif __has_APACHE(item):
                    output['licenses']['APACHE'] = output['licenses']['APACHE'] + 1
                elif __has_GPL(item):
                    output['licenses']['GPL'] = output['licenses']['GPL'] + 1
                else:
                    output['licenses']['OTHER'] = output['licenses']['OTHER'] + 1
            if item['readmeUrl']:
                output['readme'][readme_score(item)]=output['readme'][readme_score(item)] + 1
            if item['citation']:
                output['has_citation'] = output['has_citation']+1
        
        with open(directory+"/"+org+"sample.json", "w+") as outfile:
            json.dump(output, outfile)
        
        reset_dict()




create_summary()
