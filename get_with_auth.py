#!/usr/bin/env python2
# -*- coding: latin-1 -*-
'''GET an object from an ENCODE server with authentication'''

import requests, json

# Force return from the server in JSON format
HEADERS = {'accept': 'application/json'}

# This URL locates the ENCODE biosample with accession number ENCBS000AAA
URL = "https://www.encodedcc.org/biosample/ENCBS000AAA/?frame=object"

# Authentication is only required to GET unreleased ENCODE objects
AUTHID = "H7OL67B4" #<- Replace with your keypair, available from your ENCODE wrangler
AUTHPW = "lr5gz2fjowbaqox5" #<- Replace with your keypair, available from your ENCODE wrangler
 
# GET the object
response = requests.get(URL, auth=(AUTHID, AUTHPW), headers=HEADERS)

# Extract the JSON response as a python dict
response_json_dict = response.json()

# Print the object
print json.dumps(response_json_dict, indent=4, separators=(',', ': '))
