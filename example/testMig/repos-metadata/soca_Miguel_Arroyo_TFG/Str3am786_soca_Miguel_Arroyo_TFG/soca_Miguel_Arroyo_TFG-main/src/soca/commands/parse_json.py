import json
import os
from os import path
from xmlrpc.server import DocCGIXMLRPCRequestHandler



#function that creates a dictionary from a json file
def parse_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        print("opened the file ")
        return data


#function that seeks for a key in a dictionary
def seek_key(dictionary, key):
    for k, v in dictionary.items():
        if k == key:
            print("found")


#function that counts number of file type within a given directory  and returns a number
def count_file_type(directory):
    count = 0
    for file in os.listdir(directory):
        if file.endswith("json"):
            count += 1
    return count

def test (directory):
    for file in os.listdir(directory):
        print(file)
        print("====")
    
    

print(count_file_type("/home/two_play2nd/git/soca_Miguel_Arroyo_TFG/tmp/metadata"))
data = parse_json('/home/two_play2nd/git/soca_Miguel_Arroyo_TFG/tmp/metadata/KnowledgeCaptureAndDiscoveryANDmintproject/KnowledgeCaptureAndDiscovery_-github.json')
test("/home/two_play2nd/git/soca_Miguel_Arroyo_TFG/tmp/metadata")
seek_key(data,"codeRepository")

