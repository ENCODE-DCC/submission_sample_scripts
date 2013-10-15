import os
import sys
import csv
import json
import jsonschema
import requests
from pyelasticsearch import ElasticSearch
import xlrd
import xlwt
from base64 import b64encode

# set headers.  UNCLEAR IF THIS IS USED PROPERLY
HEADERS = {'content-type': 'application/json'}

# get object from server
def get_ENCODE(obj_id,keys):
    '''GET an ENCODE object as JSON and return as dict'''
    url = keys['server']+obj_id+'?limit=all'
    response = requests.get(url, auth=(keys['authid'],keys['authpw']), headers=HEADERS)
    if not response.status_code == 200:
        print >> sys.stderr, response.text
    return response.json()

# get object from server
def GetENCODE(object_id,keys):
    '''GET an ENCODE object as JSON and return as dict'''
    if type(object_id) is str:
        url = keys['server']+object_id+'?limit=all'
        print(url)
        try:
            response = requests.get(url, auth=(keys['authid'],keys['authpw']), headers=HEADERS)
        # nope
        except Exception as e:
            print("Get request failed:")
            #print(e)
        else:
            return response.json()


# patch object to server
def patch_ENCODE(obj_id, patch_json):
    '''PATCH an existing ENCODE object and return the response JSON'''
    url = keys['server']+obj_id
    json_payload = json.dumps(patch_json)
    response = requests.patch(url, auth=(keys['authid'],keys['pw']), data=json_payload)
    print "Patch:"
    print response.status_code
    if not response.status_code == 200:
        print >> sys.stderr, response.text
    return response.json()

# post object to server
def new_ENCODE(collection_id, object_json):
    '''POST an ENCODE object as JSON and return the resppnse JSON'''
    url = SERVER+'/'+collection_id+'/'
    json_payload = json.dumps(object_json)
    response = requests.post(url, auth=(AUTHID, AUTHPW), headers=HEADERS, data=json_payload)
    if not response.status_code == 201:
        print >> sys.stderr, response.text
    return response.json()

# get keys from file
def KeyENCODE(key_file,server_name):
    key_open = open(key_file)
    keys = csv.DictReader(key_open,delimiter = '\t')
    for key in keys:
        if key.get('Server') == server_name:
            key_info = {}
            key_info['user'] = key.get('User')
            key_info['server'] = ('http://' + key.get('Server') + '.encodedcc.org')
            key_info['authid'] = key.get('ID')
            key_info['authpw'] = key.get('PW')
    key_open.close()
    return(key_info)

# read json objects from file
def ReadJSON(json_file):
    json_load = open(json_file)
    json_read = json.load(json_load)
    json_load.close()
    return json_read

# write new json obect.  SHOULD BE MODIFIED TO CUSTOM OUTPUT FORMAT (FOR HUMAN VIEWING)
def WriteJSON(new_object,object_file):
    with open(object_file, 'w') as outfile:
        json.dump(new_object, outfile)
        outfile.close()

# check json object for validity.  SHOULD ONLY NEED OBJECT.  NEED DEF TO EXTRACT VALUE (LIKE TYPE) FROM JSON OBJECT GRACEFULLY.
def ValidJSON(object_type,object_id,new_object):
    #get the relevant schema
    object_schema = get_ENCODE(('/profiles/' + object_type + '.json'))
            
    # test the new object.  SHOULD HANDLE ERRORS GRACEFULLY        
    try:
        jsonschema.validate(new_object,object_schema)
    # did not validate
    except Exception as e:
        print('Validation of ' + object_id + ' failed.')
        print(e)
        return False

    # did validate
    else:
        # inform the user of the success
        print('Validation of ' + object_id + ' succeeded.')
        return True

# intended to fix invalid JSON.  DOES NOT DO ANYTHING YET.
def CleanJSON(object_type,object_id,new_object):
    for key,value in new_object.list():
        new_object.pop(key)
        if not ValidJSON(object_type,object_id,new_object):
            new_object[key] = value
        else:
            return True

# flatten embedded json objects to their ID
def FlatJSON(json_object,keys):
    json_object = EmbedJSON(json_object,keys)
    for key,value in json_object.items():
        if type(value) is dict:
            json_object[key] = json_object[key][u'@id']
    return json_object

# expand json object
def EmbedJSON(json_object,keys):
    for key,value in json_object.items():
        if type(value) is unicode:
            if str(value[0]) == '/':
                json_sub_object = GetENCODE(str(value),keys)
                if type(json_sub_object) is dict:
                    #json_sub_object = EmbedJSON(json_sub_object,keys)
                    json_object[key] = json_sub_object
    return json_object
