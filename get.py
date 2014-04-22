#!/usr/bin/env python
# -*- coding: latin-1 -*-
''' GET an object from an ENCODE server'''

import requests, json

'''force return from the server in JSON format'''
HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}

'''this URL locates the ENCODE biosample with accession number ENCBS000AAA'''
URL = "https://test.encodedcc.org/biosample/ENCBS000AAA/?frame=object"

'''GET the object'''
response = requests.get(URL, headers=HEADERS)

'''extract the JSON response as a python dict'''
response_json_dict = response.json()

'''print the object'''
print json.dumps(response_json_dict, indent=4, separators=(',', ': '))

biosample = response_json_dict

for doc_URI in biosample['protocol_documents']:
	doc_response = requests.get('https://test.encodedcc.org/'+doc_URI, headers=HEADERS)
	document = doc_response.json()
	print document['description']
