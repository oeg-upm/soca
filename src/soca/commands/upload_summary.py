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
    org = config_obj["DATABASE"]["org"]
except Exception as e:
    print(str(e))
    exit(1)




#Setup database
client = InfluxDBClient(url=url, token=mytoken, org=org)
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
    database['measurement'] = "SOCA_Summary"
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
    database['fields']['readme_score_0'] = 0
    database['fields']['readme_score_1'] = 0
    database['fields']['readme_score_2'] = 0
    database['fields']['readme_score_3'] = 0
    database['fields']['num_repos'] = 0
    database['fields']['num_CFF'] = 0


def summaryToDatabase(summary_output):
    """Function that takes the "output" dictionary from create_summary.py and equates it to influxdb
        database dictionary
    Returns
    -------
    Nothing
    """
    #tags
    database['tags'].update({
        'somef_ver': summary_output['_somef_version'],
        'soca_ver': summary_output['_soca_version'],
        'org_name': summary_output['_org_name']
    })
    #for key in ['org_name', 'soca_version', 'somef_version']:
    #    database['tags'][key] = summary_output[f"_{key}"]

    #fields
    database['fields'].update({
        'has_documentation': summary_output['has_documentation'],
        'num_doi': summary_output['identifiers']['num_pid'],
        'num_pid': summary_output['identifiers']['num_pid'],
        'num_withoutId': summary_output['identifiers']['num_without_identifier'],
        'num_withId': summary_output['identifiers']['num_pid'] +summary_output['identifiers']['num_pid'],
        'num_Apache': summary_output['licenses']['APACHE'],
        'num_GPL': summary_output['licenses']['GPL'],
        'num_MIT': summary_output['licenses']['MIT'],
        'num_Other': summary_output['licenses']['OTHER'],
        'num_Missing': summary_output['licenses']['MISSING'],
        'sum_licenses': summary_output['licenses']['APACHE'] + summary_output['licenses']['GPL'] + summary_output['licenses']['MIT'] + summary_output['licenses']['OTHER'],
        'num_with_citation': summary_output['has_citation'],
        'num_no_citation': summary_output['no_citation'],
        'release_more_twoMon': summary_output['released']['LONGER'],
        'release_less_twoMon': summary_output['released']['<2 MONTHS'],
        'readme_score_0': summary_output['readme']['Level 0'],
        'readme_score_1': summary_output['readme']['Level 1'],
        'readme_score_2': summary_output['readme']['Level 2'],
        'readme_score_3': summary_output['readme']['Level 3'],
        'sum_readme': summary_output['num_repos'] - summary_output['readme']['Level 0'],
        'num_repos': summary_output['num_repos'],
        'num_no_readme': summary_output['num_no_readme'],
        'num_with_readme': summary_output['num_with_readme'],
        'num_with_description': summary_output['num_with_description'],
        'num_with_acknowledgement': summary_output['num_with_acknowledgement'],
        'num_with_installation': summary_output['num_with_installation'],
        'num_with_requirement': summary_output['num_with_requirement']
    })
    for language in summary_output['language_count']:
            if language is not None and language != "ERROR":
                field_name = f"num_lang_{language.lower()}"
                database['fields'][field_name] = summary_output['language_count'][language]
            else:
                continue


    x = database['fields']['has_documentation'] \
        + (database['fields']['num_repos'] - database['fields']['num_withoutId']) \
        + (database['fields']['num_repos'] - database['fields']['num_Missing']) \
        + (database['fields']['num_repos'] - database['fields']['readme_score_0']) \
        + database['fields']['release_less_twoMon']
    database['fields']['percentageGoodPrac'] = round(
        (x / (database['fields']['num_repos'] * 5)) * database['fields']['num_repos'])

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
