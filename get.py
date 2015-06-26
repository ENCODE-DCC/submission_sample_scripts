#!/usr/bin/env python2
# -*- coding: latin-1 -*-
'''GET an object from an ENCODE server'''

import requests, json

# Force return from the server in JSON format
HEADERS = {'accept': 'application/json'}

# This URL locates the ENCODE biosample with accession number ENCBS000AAA
URL = "https://www.encodeproject.org/biosamples/ENCBS000AAA/?frame=object"

# GET the object
response = requests.get(URL, headers=HEADERS)

# Extract the JSON response as a python dict
response_json_dict = response.json()

# Print the object
print json.dumps(response_json_dict, indent=4, separators=(',', ': '))
