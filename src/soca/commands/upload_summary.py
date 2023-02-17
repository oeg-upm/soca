from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from configparser import ConfigParser
from pathlib import Path
import os

from influxdb_client import Point

config_obj = ConfigParser()


home = str(Path("~").expanduser())
try:
    config_obj.read(home+"/.soca/config.ini")
    url = config_obj["DATABASE"]["host"]
    mytoken = config_obj["DATABASE"]["token"]
    bucket = config_obj["DATABASE"]["bucket"]
except Exception as e:
    print(str(e))
    exit(1)




#Setup database
client = InfluxDBClient(url=url, token=mytoken, org="test1")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

#timestamp
unix_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

#=================
#dict to upload the files
database = {}
def reset_database_dict():
    """Function that ensures the dictionary that will be uploaded to influx is created and empty
    Returns
    -------
    Nothing
    """
    database['measurement'] = "test3"
    database['tags'] = {}
    database['tags']['org_name'] = ""
    database['tags']['soca_ver'] = 0
    database['tags']['somef_ver'] = 0
    database['fields'] = {}
    database['fields']['has_documentation'] = 0
    database['fields']['num_doi'] = 0
    database['fields']['num_pid'] = 0
    database['fields']['num_withoutId'] = 0
    database['fields']['num_Apache'] = 0
    database['fields']['num_GPL'] = 0
    database['fields']['num_MIT'] = 0
    database['fields']['num_Other'] = 0
    database['fields']['num_Missing'] = 0
    database['fields']['num_with_citation'] = 0
    database['fields']['num_no_citation'] = 0
    database['fields']['release_more_twoMon'] = 0
    database['fields']['release_less_twoMon'] = 0
    #TODO readme
    database['fields']['readme_score_0'] = 0
    database['fields']['readme_score_1'] = 0
    database['fields']['readme_score_2'] = 0
    database['fields']['readme_score_3'] = 0


    #database['fields']['timestamp'] = 0
    #TODO placeholder
    database['fields']['num_repos'] = 0
    database['fields']['num_CFF'] = 0
    #database['fields']['time_upload'] =

def summaryToDatabase(summary_output):
    """Function that takes the "output" dictionary from create_summary.py and equates it to influxdb
        database dictionary
    Returns
    -------
    Nothing
    """
    #tags
    database['tags']['org_name'] = summary_output['_org_name']
    database['tags']['soca_ver'] = summary_output['_soca_version']
    database['tags']['somef_ver'] = summary_output['_somef_version']
    #fields
    database['fields']['has_documentation'] = summary_output['has_documentation']
    database['fields']['num_doi'] = summary_output['identifiers']['num_doi']
    database['fields']['num_pid'] = summary_output['identifiers']['num_pid']
    database['fields']['num_withoutId'] = summary_output['identifiers']['num_without_identifier']
    database['fields']['num_Apache'] = summary_output['licenses']['APACHE']
    database['fields']['num_GPL'] = summary_output['licenses']['GPL']
    database['fields']['num_MIT'] = summary_output['licenses']['MIT']
    database['fields']['num_Other'] = summary_output['licenses']['OTHER']
    database['fields']['num_Missing'] = summary_output['licenses']['MISSING']
    database['fields']['num_with_citation'] = summary_output['has_citation']
    database['fields']['num_no_citation'] = summary_output['no_citation']
    database['fields']['release_more_twoMon'] = summary_output['released']['LONGER']
    database['fields']['release_less_twoMon'] = summary_output['released']['<2 MONTHS']
    #TODO licenses sum this is a "dirty" way but keeps the database lightweight and portable
    database['fields']['sum_licenses'] = summary_output['num_repos'] - summary_output['licenses']['MISSING']
    database['fields']['test'] =    summary_output['licenses']['MIT'] + \
                                    summary_output['licenses']['GPL'] + \
                                    summary_output['licenses']['APACHE'] + \
                                    summary_output['licenses']['OTHER']
    #TODO readme scores
    database['fields']['readme_score_0'] = summary_output['readme']['Level 0']
    database['fields']['readme_score_1'] = summary_output['readme']['Level 1']
    database['fields']['readme_score_2'] = summary_output['readme']['Level 2']
    database['fields']['readme_score_3'] = summary_output['readme']['Level 3']
    #TODO sum of readmes
    database['fields']['sum_readme'] = summary_output['num_repos'] - summary_output['readme']['Level 0']

    #TODO placeholder
    database['fields']['num_repos'] = summary_output['num_repos']
    
    x = database['fields']['has_documentation'] +\
        (database['fields']['num_repos'] - database['fields']['num_withoutId'])+ \
        (database['fields']['num_repos'] - database['fields']['num_Missing']) + \
        (database['fields']['num_repos'] - database['fields']['readme_score_0']) + \
        database['fields']['release_less_twoMon']

    database['fields']['percentageGoodPrac'] = round((x/(database['fields']['num_repos']*5)) *database['fields']['num_repos'])
    #TODO verificar
    #TODO check if this is correct way to do it
    auxdate = datetime.strptime(summary_output['_timestamp'],'%Y-%m-%dT%H:%M:%S.%f')
    influxdate = auxdate.strftime('%Y-%m-%dT%H:%M:%SZ')
    database['timestamp'] = influxdate



def upload_summary(dictionary):
    """Function that uploads a given dictionary to predefined influxdb database.
    Returns
    -------
    Nothing
    """
    #TODO ask about reset dict might be superfluous
    reset_database_dict()
    summaryToDatabase(dictionary)
    print("Attempting to upload file to the influxdb")
    try:
     p = Point("test2").from_dict(database)
     write_api.write(bucket="my-bucket", record=p)

    except Exception as e:
        print('there was an error while uploading the file to the database')
        print(str(e))
        return
    #TODO check if need to return to normal colour
    print('\033[92m',"Success",'\033[0m')
    print("Successfully uploaded the file to the influxdb")
