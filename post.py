#!/usr/bin/env python2
# -*- coding: latin-1 -*-
'''POST an object to an ENCODE server'''

import sys, requests, json

# Send and accept JSON format
HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}

# Authentication is always required to PATCH ENCODE objects
AUTHID = "H7OL67B4" #<- Replace this with your keypair
AUTHPW = "lr5gz2fjowbaqox5" #<- Replace this with your keypair

# The URL is now the collection itself
URL = "http://test.encodedcc.org/experiments/"

# Build a Python dict with the experiment metadata
new_experiment = {
	"description": "POST example experiment",
	"assay_term_name": "ChIP-seq",
	"biosample_term_name": "Stromal cell of bone marrow",
	"target": "/targets/SMAD6-human/",
	"award": "/awards/U41HG006992/",
	"lab": "/labs/j-michael-cherry/",
	"references": [
		"PMID:12345",
		"PMID:67890"
	]
}

# Serialize the data structure as JSON
json_payload = json.dumps(new_experiment)

# POST the JSON and print the response
response = requests.post(URL, auth=(AUTHID, AUTHPW), headers=HEADERS, data=json_payload)

# If the POST succeeds, the response is the new object in JSON format
print json.dumps(response.json(), indent=4, separators=(',', ': '))

# Check the status code and if good, extract the accession number of the new object'''
if not response.status_code == 201:
	print >> sys.stderr, response.text
else:
	response_dict = response.json()
	posted_experiment = response_dict['@graph'][0]
	new_experiment_accession = posted_experiment['accession']
	print "New ENCODE accession number: %s" %(new_experiment_accession)
