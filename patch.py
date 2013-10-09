import os
import sys
import csv
import json
import requests
import argparse

def get_settings(key_file,server_name):
    key_list = open(key_file)
    keys = csv.DictReader(key_list,delimiter = '\t')
    settings = {}
    for key in keys:
        if key.get('Server') == server_name:
            settings['USER'] = key.get('User')
            settings['SERVER'] = ('http://' + key.get('Server') + '.encodedcc.org')
            settings['AUTHID'] = key.get('ID')
            settings['AUTHPW'] = key.get('PW')
    key_list.close()
    return settings

def read_objects(object_file):
    json_file = open(object_file)
    json_objects = json.load(json_file)
    json_file.close()
    return json_objects

def filter_object(json_object,key):
    json_duplicate = json_object
    json_duplicate.pop(key)
    return json.dumps(json_duplicate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to patch json objects with only fields you require.')
    parser.add_argument('key_file', help='A tab delimited file that contains keys.')
    parser.add_argument('server', help='The server you want to patch objects to.')
    parser.add_argument('json_file', help='The JSON file that contains a list of objects you want to patch.')
    args = parser.parse_args()

    # set headers.  UNCLEAR IF THIS IS USED PROPERLY
    HEADERS = {'content-type': 'application/json'}
    
    settings = get_settings(args.key_file,str(args.server))

    patch_objects = read_objects(args.json_file)

    for i in range(0,len(patch_objects)):
        object_id = patch_objects[i]['@id']
        patch_object = filter_object(patch_objects[i], '@id')
        url = (settings.get('SERVER') + '/' + str(object_id))
        authid = settings.get('AUTHID')
        authpw = settings.get('AUTHPW')
        response = requests.patch(url, auth=(authid, authpw), headers=HEADERS, data=patch_object)
        print response.text

