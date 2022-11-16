from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

from influxdb_client import Point

#token for Auth
mytoken = 'G9tlsRl1J-dYeOYp5OkWGNOSipEmbeN3gyp0wBbxDp6KRSZ-1foOkdTbhj8rkhN7Onj7CV105OYAQqAvr4C8-w=='
#
bucket = "my-bucket"
#Setup database
client = InfluxDBClient(url="http://localhost:8086", token=mytoken, org="test1")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

#timestamp
unix_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

#=================
#dict to upload the files
database = {}
def reset_database_dict():
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
    database['fields']['release_more_twoMon'] = 0
    database['fields']['release_less_twoMon'] = 0
    database['fields']['timestamp'] = 0
    #database['fields']['time_upload'] =

def summaryToDatabase(summary_output):
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
    database['fields']['release_more_twoMon'] = summary_output['released']['LONGER']
    database['fields']['release_less_twoMon'] = summary_output['released']['<2 MONTHS']
    #TODO check if this is correct way to do it
    auxdate = datetime.strptime(summary_output['_timestamp'],'%Y-%m-%dT%H:%M:%S.%f')
    influxdate = auxdate.strftime('%Y-%m-%dT%H:%M:%SZ')
    database['fields']['timestamp'] = influxdate



def upload_summary(dictionary):
    reset_database_dict()
    summaryToDatabase(dictionary)
    try:
     p = Point("test2").from_dict(database)
     write_api.write(bucket="my-bucket", record=p)
    except Exception as e:
        print('there was an error while uploading the file to the database')
        print(str(e))
        return

