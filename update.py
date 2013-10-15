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
def get_ENCODE(obj_id):
    '''GET an ENCODE object as JSON and return as dict'''
    url = SERVER+obj_id+'?limit=all'
    response = requests.get(url, auth=(AUTHID, AUTHPW), headers=HEADERS)
    if not response.status_code == 200:
        print >> sys.stderr, response.text
    return response.json()

# patch object to server
def patch_ENCODE(obj_id, patch_json):
    '''PATCH an existing ENCODE object and return the response JSON'''
    url = SERVER+obj_id
    json_payload = json.dumps(patch_json)
    response = requests.patch(url, auth=(AUTHID, AUTHPW), data=json_payload)
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

# write new json obect.  SHOULD BE MODIFIED TO CUSTOM OUTPUT FORMAT (FOR HUMAN VIEWING)
def WriteJSON(new_object,object_file):
    with open(object_file, 'w') as outfile:
        json.dump(new_object, outfile)
        outfile.close()


if __name__ == "__main__":
    '''
    This script will read in all objects in the objects folder, determine if they are different from the database object, and post or patch them to the database.
    Authentication is determined from the keys.txt file.
    '''
    # FUTURE: Should also be deal with errors that are only dependency based.

    # set server name.  MODIFY TO HAVE USER CHOOSE SERVER (ENUM LIST FROM THE FILE)
    server_name = 'staging'

    # get ID, PW.  MODIFY TO USE USERNAME/PASS TO GAIN ACCESS TO CREDENTIALS
    key_file = open('keys.txt')
    keys = csv.DictReader(key_file,delimiter = '\t')

    for key in keys:
        if key.get('Server') == server_name:
            USER = key.get('User')
            SERVER = ('http://' + key.get('Server') + '.encodedcc.org')
            AUTHID = key.get('ID')
            AUTHPW = key.get('PW')
    key_file.close()

    # let user know the server/user that is set for running script
    print(USER + ' will be running this update on ' + SERVER)
    #print(AUTHID,AUTHPW)

    # load objects in object folder.  MODIFY TO HAVE USER VIEW AND SELECT OBJECTS
    object_filenames = os.listdir('objects/')
    
    # run for each object in objects folder
    for object_filename in object_filenames:
        if '.json' in object_filename:

            # define object parameters.  SHOULD NOT RELY ON FILENAME.  NEED WAY TO IDENTIFY OBJECT TYPE/NAME BY REVIEWING DATA
            object_type,object_name = object_filename.strip('.json').split(';')
            object_file = ('objects/' + object_type + ';' + object_name + '.json')
            object_collection = (object_type.replace('_','-') + 's')
            object_id = ('/' + object_collection + '/' + object_name + '/')

            # load object  SHOULD HANDLE ERRORS GRACEFULLY
            json_object = open(object_file)
            new_object = json.load(json_object)
            json_object.close()

            # check to see if object already exists  
            # PROBLEM: SHOULD CHECK UUID AND NOT USE ANY SHORTCUT METADATA THAT MIGHT NEED TO CHANGE
            # BUT CAN'T USE UUID IF NEW... HENCE PROBLEM
            old_object = get_ENCODE(object_id)

            # if object is not found, verify and post it
            if old_object.get(u'title') == u'Not Found':

                # get relevant schema
                object_schema = get_ENCODE(('/profiles/' + object_type + '.json'))
            
                # test the new object.  SHOULD HANDLE ERRORS GRACEFULLY        
                try:
                    jsonschema.validate(new_object,object_schema)
                # did not validate
                except Exception as e:
                    print('Validation of ' + object_id + ' failed.')
                    print(e)

                # did validate
                else:
                    # inform the user of the success
                    print('Validation of ' + object_id + ' succeeded.')

                    # post the new object(s).  SHOULD HANDLE ERRORS GRACEFULLY
                    response = new_ENCODE(object_collection,new_object)


            # if object is found, check for differences and patch it if needed.
            else:

                # compare new object to old one, remove identical fields.
                for key in new_object.keys():
                    if new_object.get(key) == old_object.get(key):
                        new_object.pop(key)

                # if there are any different fields, patch them.  SHOULD ALLOW FOR USER TO VIEW/APPROVE DIFFERENCES
                if new_object:
                
                    # inform user of the updates
                    print(object_id + ' has updates.')
                    print(new_object)
                
                    # patch object
                    response = patch_ENCODE(object_id, new_object)

                # inform user there are no updates            
                else:
                    print(object_id + ' has no updates.')


