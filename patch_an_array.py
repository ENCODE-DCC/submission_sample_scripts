#!/usr/bin/env python2
# -*- coding: latin-1 -*-
'''PATCH an object array on an ENCODE server'''
 
import sys, requests, json
 
# Send and accept JSON format
HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}

# Authentication is always required to PATCH ENCODE objects
AUTHID = "ABCDEFG" #<- Replace this with your keypair
AUTHPW = "myspecialsecret" #<- Replace this with your keypair
 
# This URL locates the ENCODE experiment with accession number ENCSR000AJT
URL = "https://test.encodedcc.org/experiments/ENCSR000AJT/"
 
# GET the object we'll be PATCH'ing
response = requests.get(URL, auth=(AUTHID, AUTHPW), headers=HEADERS)
experiment = response.json()
 
# Extract the aliases array from the JSON object
alias_array = experiment['aliases']
 
# Append our new alias to the array
alias_array.remove('test:some_unique_string') #<- This must be a unique string.
 
# Construct the JSON payload
payload_dict = {
	"aliases": alias_array
}
json_payload = json.dumps(payload_dict)
 
# Do the PATCH and parse the response
response = requests.patch(URL, auth=(AUTHID, AUTHPW), headers=HEADERS, data=json_payload)

# Process the response
if not response.status_code == 200:
	print >> sys.stderr, response.text

# Print the JSON response
print json.dumps(response.json(), indent=4, separators=(',', ': '))
