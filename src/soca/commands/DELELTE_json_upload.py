import json
import os
from os import walk
from os import path
import pymongo
from pymongo import MongoClient, InsertOne, DeleteMany, ReplaceOne, UpdateOne

#TODO fix: change to variable path
directory = "home/two_play2nd/git/soca_Miguel_Arroyo_TFG/tmp/metadata"

#client connection to the mongodb
client = MongoClient("localhost",27017)

#use database named "soca_metadata"
db = client["soca_metadata"]
requesting = []
list_of_collections = list() #= db.list_collection_names()


#updates list of collections for debugging purposes
def update_list():
    list_of_collections = db.list_collection_names()



#searches main dir for new directories and if not found in database adds it as collection With all files
def insertCollection(directory):
    for dir in os.listdir(directory):
        if dir not in list_of_collections:
            try:
                col = db[dir]
                upload_files(dir)
            except:
                #TODO
                print("oops")

    print("fin")
    update_list()
    print(list_of_collections)



#function that uploads all jsons in a directory to a collection in bulk
def upload_files(col):
    dir = "/home/two_play2nd/git/soca_Miguel_Arroyo_TFG/tmp/metadata"+"/"+col
    for file_name in os.listdir(dir):
        if file_name.endswith("json"):
            with open(dir+"/"+file_name) as json_file:
                data = json.load(json_file)
                try:
                    db[col].insert_one(data)
                    print("uploaded file: " + file_name)
                except:
                    #TODO
                    print("error")
    



#TODO delete as will not be necessary

#function that takes all jsons within a directory and compiles them into one large file
def merge_files(directory):
        result = list()
        for file_name in os.listdir(directory):
            if file_name.endswith("json"):
                with open(directory+"/"+file_name, 'r') as infile:
                    result.extend(json.loads(infile))
        with open(directory+"/"+'COMPILED.json', 'w+') as output_file:
                json.dump(result, output_file)
       


#merge_files("/home/two_play2nd/git/soca_Miguel_Arroyo_TFG/tmp/metadata/oeg-upm")
insertCollection("/home/two_play2nd/git/soca_Miguel_Arroyo_TFG/tmp/metadata")