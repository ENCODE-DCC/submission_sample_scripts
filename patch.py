#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''PATCH an object on an ENCODE server'''

import sys, requests, json

# Indicate that the content sent to the server is JSON
# Force return from the server in JSON format
HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}

# Authentication is always required to PATCH ENCODE objects
AUTHID = "ABCDEFG" #<- Replace this with your keypair
AUTHPW = "myspecialsecret" #<- Replace this with your keypair

# This URL locates the ENCODE experiment with accession number ENCSR000AJT
URL = "https://test.encodedcc.org/experiments/ENCSR000AJT/"

# Create the JSON to send to the server
payload_dict = {
	"description": "Originally Caltech ChIP-Seq mouse C2C12 EqS_2.0pct_60hr Control_36bp" #Originally Caltech ChIP-Seq mouse C2C12 EqS_2.0pct_60hr Control_36bp
}
json_payload = json.dumps(payload_dict)

# Send the request to the server
response = requests.patch(URL, auth=(AUTHID, AUTHPW), headers=HEADERS, data=json_payload)

# Process the response
if not response.status_code == 200:
	print >> sys.stderr, response.text

# Print the JSON response
print json.dumps(response.json(), indent=4, separators=(',', ': '))
