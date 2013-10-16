import sys
import os
import csv
import json
import jsonschema
import requests
from pyelasticsearch import ElasticSearch
import xlrd
import xlwt
from base64 import b64encode

# ENCODE Tools functions
sys.path.append('/Users/Drew/Google Drive/Scripts/ENCODE-DCC/submission_sample_scripts/dte')
from ENCODETools import get_ENCODE
from ENCODETools import patch_ENCODE
from ENCODETools import new_ENCODE
from ENCODETools import GetENCODE
from ENCODETools import KeyENCODE
from ENCODETools import ReadJSON
from ENCODETools import WriteJSON
from ENCODETools import ValidJSON
from ENCODETools import CleanJSON
from ENCODETools import FlatJSON
from ENCODETools import EmbedJSON

# set headers.  UNCLEAR IF THIS IS USED PROPERLY
HEADERS = {'content-type': 'application/json'}


if __name__ == "__main__":
    '''
    This script will read in all objects in the objects folder, determine if they are different from the database object, and post or patch them to the database.
    Authentication is determined from the keys.txt file.
    '''
    # FUTURE: Should also be deal with errors that are only dependency based.

    # set server name.  MODIFY TO HAVE USER CHOOSE SERVER (ENUM LIST FROM THE FILE)
    server_name = 'test'
    
    # set data file.  MODIFY TO HAVE USER CHOOSE SERVER (ENUM LIST FROM THE FILE)
    data_file = 'update.json'

    # get ID, PW.  MODIFY TO USE USERNAME/PASS TO GAIN ACCESS TO CREDENTIALS
    key_file = 'keys.txt'
    keys = KeyENCODE(key_file,server_name)

    # let user know the server/user that is set for running script
    print(keys['user'] + ' will be running this update on ' + keys['server'])
    #print(AUTHID,AUTHPW)

    # load objects in object folder.  MODIFY TO HAVE USER VIEW AND SELECT OBJECTS
    #object_filenames = os.listdir('objects/')
    
    # run for each object in objects folder
    #for object_filename in object_filenames:
        #if '.json' in object_filename:

    # load object  SHOULD HANDLE ERRORS GRACEFULLY
    print('Opening ' + data_file)
    json_object = ReadJSON('objects/' + data_file)
    
    # if the returned json object is not a list, put it in one
    if type(json_object) is dict:
        object_list = []
        object_list.append(json_object)
    elif type(json_object) is list:
        object_list = json_object

    for new_object in object_list:
        
        new_object = FlatJSON(new_object,keys)

        # define object parameters.  NEEDS TO RUN A CHECK TO CONFIRM THESE EXIST FIRST.
        object_type = str(new_object[u'@type'][0])
        object_id = str(new_object[u'@id'])
        object_uuid = str(new_object[u'uuid'])
        object_name = str(new_object[u'accession'])

        # check to see if object already exists  
        # PROBLEM: SHOULD CHECK UUID AND NOT USE ANY SHORTCUT METADATA THAT MIGHT NEED TO CHANGE
        # BUT CAN'T USE UUID IF NEW... HENCE PROBLEM
        old_object = FlatJSON(get_ENCODE(object_id,keys),keys)

#        # test the validity of new object
#        if not ValidJSON(object_type,object_id,new_object):
#            # get relevant schema
#            object_schema = get_ENCODE(('/profiles/' + object_type + '.json'))
#            
#            # test the new object.  SHOULD HANDLE ERRORS GRACEFULLY        
#            try:
#                jsonschema.validate(new_object,object_schema)
#            # did not validate
#            except Exception as e:
#                print('Validation of ' + object_id + ' failed.')
#                print(e)
#
#            # did validate
#            else:
#                # inform the user of the success
#                print('Validation of ' + object_id + ' succeeded.')
#
#                # post the new object(s).  SHOULD HANDLE ERRORS GRACEFULLY
#                response = new_ENCODE(object_collection,new_object)


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
                response = new_ENCODE(object_collection,new_object,keys)


        # if object is found, check for differences and patch it if needed.
        else:

            # compare new object to old one, remove identical fields.  Also, remove fields not present in schema. SHOULD INFORM OF THIS OPERATION, BUT NOT NEEDED WHEN SINGLE PATCH CODE EXISTS.
            for key in new_object.keys():
                if new_object.get(key) == old_object.get(key):
                    new_object.pop(key)
                elif not old_object.get(key):
                    new_object.pop(key)

            # if there are any different fields, patch them.  SHOULD ALLOW FOR USER TO VIEW/APPROVE DIFFERENCES
            if new_object:
                
                # inform user of the updates
                print(object_id + ' has updates.')
                #print(new_object)
                
                # patch each field to object individually
                for key,value in new_object.items():
                    patch_single = {}
                    patch_single[key] = value
                    print(patch_single)
                    response = patch_ENCODE(object_id,patch_single,keys)

            # inform user there are no updates            
            else:
                print(object_id + ' has no updates.')


