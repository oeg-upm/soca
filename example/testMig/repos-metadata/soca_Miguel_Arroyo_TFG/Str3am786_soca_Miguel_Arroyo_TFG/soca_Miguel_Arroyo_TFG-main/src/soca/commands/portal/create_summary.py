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
output['timestamp'] = datetime.now()
output['num_doc'] = 0
output['identifiers'] = {'num_doi':0,'num_pid':0}
output['readme'] = {'EMPTY':0,'OK':0,'GOOD':0,'GREAT':0}
output['licenses']= {'APACHE':0,'MIT':0,'GPL':0,'OTHER':0}
#TODO
output['citation'] = 0
output['releases'] = {'IN PROGRESS': 0, 'UPDATED':0}

def reset_dict():
    output['timestamp'] = datetime.now()
    output['num_doc'] = 0
    output['identifiers'] = {'num_doi': 0, 'num_pid': 0}
    output['readme'] = {'EMPTY': 0, 'OK': 0, 'GOOD': 0, 'GREAT': 0}
    output['licenses'] = {'APACHE': 0, 'MIT': 0, 'GPL': 0, 'OTHER': 0}
    output['releases'] = {'IN PROGRESS': 0, 'UPDATED': 0}


#This file is to create a function that will then be sent to the grafana interface for now


#function to return list of available organisations

def find_organisations():
    for dir in os.listdir(directory):
        if dir not in __listOrg:
            __listOrg.append(dir)


#function to create directory named summary to save summaries if doesnt exist already
def create_summary_dir(self):
    if not os.path.exists(directory+"/summary"):
        os.makedirs(directory+"/summary")
        print("summary directory created")
    else:
        print("summary directory already exists")

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
            score += 1
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

#function
def __has_doi(json_obj):
    if "doi.org" in json_obj['html_card_embedded']:
        return True
def __has_pid(json_obj):
    #TODO
    return False

def __is_MIT(json_obj):
    if "License: Apache" in json_obj['html_card_embedded']:
        return True
def __is_APACHE(json_obj):
    if "License: MIT" in json_obj['html_card_embedded']:
        return True
def __is_GPL(json_obj):
    if "License: GPL" in json_obj['html_card_embedded']:
        return True

#function that opens array of jsons given the organisation
def __open_Json(dir):
    file_dir = directory + "/" + dir + "/" + "cards_data.json"
    with open(file_dir) as json_file:
        data = json.load(json_file)
        print("opened the file ")
        return data

#function to create summary for each organisation
def create_summary():
    #counters to store data
    numWithDocumentation = 0

    #updates the list of organisations 
    find_organisations()

    for dir in __listOrg:
        json_array = __open_Json(dir)
        counter = 0
        for item in json_array:
            #TODO add comprobacion?
            if item['hasDocumentation']:
                output['num_doc'] = output['num_doc']+1
                counter +=1
            if __has_doi(item):
                output['identifiers']['num_doi'] = output['identifiers']['num_doi'] +1
            if __has_pid(item):
                output['identifiers']['num_pid'] = output['identifiers']['num_pid'] + 1

            if item['license']:
                if __is_MIT(item):
                    output['licenses']['MIT'] = output['licenses']['MIT'] + 1
                if __is_APACHE(item):
                    output['licenses']['APACHE'] = output['licenses']['APACHE'] + 1
                if __is_GPL(item):
                    output['licenses']['GPL'] = output['licenses']['GPL'] + 1
                else:
                    output['licenses']['OTHER'] = output['licenses']['OTHER'] + 1

            output['readme'][readme_score(item)]=output['readme'][readme_score(item)] +1

        print(output['num_doc'])
        print(output['readme'])
        print(output['identifiers'])
        print(output['licenses'])
        reset_dict()




create_summary()
