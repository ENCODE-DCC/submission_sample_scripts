#!/usr/bin/env python
# -*- coding: latin-1 -*-
''' POST an object to an ENCODE server'''

import sys, requests, json

'''force return from the server in JSON format'''
HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}
AUTHID = "H7OL67B4" #<- Replace this with your keypair
AUTHPW = "lr5gz2fjowbaqox5" #<- Replace this with your keypair

'''note that the URL is now the collection itself'''
URL = "http://test.encodedcc.org/experiments/"

'''build a Python dict with the experiment metadata'''
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

'''serialize the data structure as JSON'''
json_payload = json.dumps(new_experiment)

'''POST the JSON and print the response'''
response = requests.post(URL, auth=(AUTHID, AUTHPW), headers=HEADERS, data=json_payload)

print json.dumps(response.json(), indent=4, separators=(',', ': '))

''' check the status code and if good, extract the accession number of the new object'''
if not response.status_code == 201:
	#deal with the error
	import sys
	print >> sys.stderr, response.text
else:
	response_dict = response.json()
	posted_experiment = response_dict['@graph'][0]
	new_experiment_accession = posted_experiment['accession']
	print "New ENCODE accession number: %s" %(new_experiment_accession)
