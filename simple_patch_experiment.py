#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''PATCH the description field of an ENCODE experiment'''

'''use requests to handle the HTTP connection'''
import requests
'''use json to convert between Python dictionaries and JSON objects'''
import json

'''store the ENCODE server address and the authorization keypair'''
'''create the keypair from persona or get one from your wrangler'''
SERVER = 'http://test.encodedcc.org'
AUTHID = 'access_key_id'
AUTHPW = 'secret_access_key'
'''force return from the server in JSON format'''
HEADERS = {'content-type': 'application/json'}

'''build a URL that points to an ENCODE object'''
URL = SERVER+'/experiments/ENCSR000AJT/'

'''GET the ENCODE object using it's resource name and store the Response'''
response = requests.get(URL, auth=(AUTHID, AUTHPW), headers=HEADERS)

'''act on the Response object return code'''
print response.status_code
if not response.status_code == requests.codes.ok:
    print response.text
    response.raise_for_status()

'''build a python dictionary from the JSON response content'''
experiment = response.json()

'''extract the description from the ENCODE object'''
description = experiment['description']
#for ENCSR000AJT the original value is 'Caltech ChIP-Seq mouse C2C12 EqS_2.0pct_60hr Control_36bp'

'''save the old description and construct a new one'''
old_description = description
patch_description = old_description+'Hello World'
#patch_description = 'Caltech ChIP-Seq mouse C2C12 EqS_2.0pct_60hr Control_36bp'

'''construct a dictionary with the key and value to be changed'''
patchdict = {'description':patch_description}
'''convert the dictionary to a JSON object'''
json_payload = json.dumps(patchdict)
'''PATCH the ENCODE object with the new value'''
response = requests.patch(URL, auth=(AUTHID, AUTHPW), data=json_payload)
'''act on the Response object return code'''
print response.status_code
if not response.status_code == requests.codes.ok:
    print response.text
    response.raise_for_status()

'''verify that the PATCH worked'''
'''GET the ENCODE object using it's resource name and store the Response'''
response = requests.get(URL, auth=(AUTHID, AUTHPW), headers=HEADERS)

'''act on the Response object return code'''
print response.status_code
if not response.status_code == requests.codes.ok:
    print response.text
    response.raise_for_status()

'''build a python dictionary from the JSON response content'''
experiment = response.json()

'''extract the description from the ENCODE object'''
description = experiment['description']

'''print what we did'''
print "Original:  %s" %(old_description)
print "PATCH:     %s" %(patch_description)
print "New value: %s" %(description)
