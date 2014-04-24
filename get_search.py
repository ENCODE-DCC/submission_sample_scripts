#!/usr/bin/env python2
# -*- coding: latin-1 -*-
'''GET the results of a search from an ENCODE server'''

import requests, json

# Force return from the server in JSON format
HEADERS = {'accept': 'application/json'}

# This searches the ENCODE database for the phrase "bone chip"
URL = "https://www.encodedcc.org/search/?searchTerm=bone+chip&frame=object"

# GET the search result
response = requests.get(URL, headers=HEADERS)

# Extract the JSON response as a python dict
response_json_dict = response.json()

# Print the object
print json.dumps(response_json_dict, indent=4, separators=(',', ': '))
