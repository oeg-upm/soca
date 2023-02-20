from datetime import date, datetime
import json
import os
from soca import __version__ as soca_ver
from somef import __version__ as somef_ver
from .upload_summary import upload_summary

output = {}
def __json_serial(obj):
    """JSON serializer for objects not serializable by default json code
    Returns
    -------
    serialized obj

    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

def reset_dict():
    output['has_documentation'] = 0
    output['identifiers'] = {'num_doi': 0, 'num_pid': 0, 'num_without_identifier': 0}
    output['readme'] = {'Level 0': 0, 'Level 1': 0, 'Level 2': 0, 'Level 3': 0}
    output['licenses'] = {'APACHE': 0, 'MIT': 0, 'GPL': 0, 'OTHER': 0, 'MISSING': 0}
    output['has_citation'] = 0
    output['no_citation'] = 0
    output['CFF_file'] = 0
    output['released'] = {'<2 MONTHS': 0, 'LONGER': 0}
    output['_soca_version'] = soca_ver
    output['_somef_version'] = somef_ver
    output['_org_name'] = ""
    #TODO look into portal date/time
    output['_timestamp'] = __json_serial(datetime.now())
    output['num_repos'] = 0



#functions below to identify good practices
#TODO look into correct identifiers
def __findId(json_obj):
    """JSON finds ID within the dictionary and adds 1 to number in output"""
    if json_obj['hasIdentifier']:
        #follows assumption that doi.org -> hasPid
        if "doi.org" in json_obj['identifierLink']:
            output['identifiers']['num_pid'] = output['identifiers']['num_pid'] + 1
        elif "zenodo" or "Zenodo" in json_obj['identifierLink']:
            output['identifiers']['num_doi'] = output['identifiers']['num_doi'] + 1

    else:
        output['identifiers']['num_without_identifier'] = output['identifiers']['num_without_identifier'] + 1


#TODO change to switch case when updated to python 3.10
#TODO try except with dictionary
def __findLicense(json_obj):
    """Function that looks for the name of the license within the cards_data.json (json_obj)
    Returns
    -------
    Usable string within the "output dictionary"
    """
    if not json_obj['license']:
        return "MISSING"
    else:
        if(json_obj['licenseName'] == 'Apache License 2.0'):
            return "APACHE"
        elif(json_obj['licenseName'] == 'MIT License'):
            return "MIT"
        elif(json_obj['licenseName'] == 'GNU General Public License v3.0' ):
            return "GPL"
        elif(json_obj['licenseName'] == 'Other'):
            return "OTHER"
        else:
            return "MISSING"

#TODO change soca output: recently updated to a more fitting name: Days last update?
def __last_update(json_obj):
    """Function that looks how many days since last update: "recently_updated" within the cards_data.json (json_obj)
    Returns
    -------
    Usable string within the "output dictionary"
    """
    if json_obj['recently_updated'] > 60:
        return "LONGER"
    else:
        return "<2 MONTHS"

#function given a json object will give readme score OK, GOOD, GREAT, EMPTY
#TODO clean UP
def readme_score(json_obj):
    """Function that returns the readme score counting how many good practices are met
        within the cards_data.json (json_obj)
    Returns
    -------
    Usable string within the "output dictionary"
    """
    score = 0
    #if no readme return EMPTY/level 0
    if not json_obj['readmeUrl']:
        return "Level 0"
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
        return "Level 3"
    if score > 2:
        return "Level 2"
    if score <= 2:
        return "Level 1"

#function that opens array of jsons given the organisation
def __open_Json(directory):
        if os.path.isfile(directory):
            with open(directory) as json_file:
                data = json.load(json_file)
            return data
        else:
            raise Exception("please provide a correct path to cards_json file")
            return


#function to create summary for each organisation
def create_summary(directory_org_data,outFile, want2Upload):

    #prepares dictionary to create json
    reset_dict()
    #updates the list of organisations
    try:

        json_array = __open_Json(directory_org_data)
        if not os.path.exists(outFile):
            os.makedirs(outFile)
        for item in json_array:
            if item['hasDocumentation']:
                output['has_documentation'] = output['has_documentation'] + 1
            if item['citation']:
                output['has_citation'] = output['has_citation'] + 1
            #TODO citation recognition
            else:
                output['no_citation'] = output['no_citation'] + 1
            # finds licenses
            output['licenses'][__findLicense(item)] = output['licenses'][__findLicense(item)] + 1
            # finds identifiers
            __findId(item)
            # gives readme evaluation
            output['readme'][readme_score(item)] = output['readme'][readme_score(item)] + 1
            # release time
            output['released'][__last_update(item)] = output['released'][__last_update(item)] + 1
            # adds org_name
            output['_org_name'] = item['owner']
            output['num_repos'] += 1


        # saves dictionary to json file
        with open(outFile + "/" + item['owner'] + "_summary.json", 'w+') as out_file:
            json.dump(output, out_file, sort_keys=True, indent=4,
                      ensure_ascii=False)
            #console outputs
            print("Creating: "+ outFile + "/" + item['owner'] + "_summary.json in current directory")
            #print(out_file)
            print('\033[92m', "Success", '\033[0m')
            print("========")

        if(want2Upload):
            upload_summary(output)


    except Exception as e:
        print("error create_summary")
        print(str(e))
        return


