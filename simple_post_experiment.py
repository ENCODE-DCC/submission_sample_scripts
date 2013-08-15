#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''Create a new ENCODE experiment object'''

'''use requests to handle the HTTP connection'''
import requests
'''use json to convert between Python dictionaries and JSON objects'''
import json
'''use jsonschema to validate objects against the JSON schemas'''
import jsonschema
import sys

'''store the ENCODE server address and an authorization keypair'''
'''create the keypair from persona or get one from your wrangler'''
SERVER = 'http://test.encodedcc.org'
AUTHID = 'access_key_id'
AUTHPW = 'secret_access_key'
'''force return from the server in JSON format'''
HEADERS = {'content-type': 'application/json'}

def get_ENCODE(obj_id):
    '''GET an ENCODE object as JSON and return as dict'''
    url = SERVER+obj_id+'?limit=all'
    response = requests.get(url, auth=(AUTHID, AUTHPW), headers=HEADERS)
    if not response.status_code == 200:
        print >> sys.stderr, response.text
    return response.json()

def patch_ENCODE(obj_id, patch_json):
    '''PATCH an existing ENCODE object and return the response JSON'''
    url = SERVER+obj_id
    json_payload = json.dumps(patch_json)
    response = requests.patch(url, auth=(AUTHID, AUTHPW), data=json_payload)
    print "Patch:"
    print response.status_code
    if not response.status_code == 200:
        print >> sys.stderr, response.text
    return response.json()

def new_ENCODE(collection_id, object_json):
    '''POST an ENCODE object as JSON and return the resppnse JSON'''
    url = SERVER+collection_id
    json_payload = json.dumps(object_json)
    response = requests.post(url, auth=(AUTHID, AUTHPW), headers=HEADERS, data=json_payload)
    if not response.status_code == 201:
        print >> sys.stderr, response.text
    return response.json()

if __name__ == "__main__":

    experiment_schema = get_ENCODE('/profiles/experiment.json')
    experiment_fields = dict.fromkeys(experiment_schema['properties'].keys())
    # Save the metadata for the new experiment object.  For completeness, all schema fields
    # are shown.  In general, for fields you do not wish to store an explicit value, leave those
    # fields out of the object entirely.  Any value you supply (including None) will over-ride the default.
    new_experiment = {
        u'dataset_type':        'experiment',
        u'lab':                 'bradley-bernstein', #or /labs/b83215c3-3960-4085-b220-614a122eea01/
        u'award':               'U54HG006991',       #or /awards/4621616e-faba-4c60-b7b9-1cd9e5627025/
        #u'possible_controls':   None, 
        u'description':         'TEST1 ChIP-seq for H3K27me3 in human dermal fibroblasts.',
        u'assay_term_name':     'ChIP-seq',
        u'assay_term_id':       'OBI:0000716',
        u'biosample_type':      'primary cell line',
        u'biosample_term_id':   'CL:0002551',
        u'biosample_term_name': 'fibroblast of dermis',
        u'target':              'H3K27me3-human',    #or /targets/9fdbd27b-4118-4851-b566-87d77d467d79/
        #u'aliases':             None, 
        u'submitted_by':        'noamshoresh@gmail.com', #or /users/f1843c60-e027-4b18-8582-64d3f3eae45b/
        #u'date_created':        None,
        u'references':          ['PMID:22955991'], 
        u'geo_dbxrefs':         ['GSM999999'],
        #u'encode2_dbxrefs':     None, 
        u'documents':           ['ENCODE:NHDF-Ad_Bernstein_protocol'], #or /documents/f651422a-d5f1-4cb9-b787-2bc579a329f3/
        #u'files':               None, 
        u'is_current':          True,
        u'schema-version':      '0.01', 
        u'accession':           'ENCSR999BRO', #normally assigned automatically or PATCHED later by a wrangler
        #u'alternate_accessions': None, 
        #u'uuid': None, 
        }
    if not jsonschema.validate(new_experiment, experiment_schema):
        #validate raises an error if validation fails
        pass

    response = new_ENCODE('/experiments/',new_experiment)
    if response['status'] == 'success':
        new_experiment_id = response['@graph'][0]
        print "Experiment %s created" %(new_experiment_id)
    else:
        print "No experiment created"



'''
    create replicates in the same way:
    pull the replicate schema
    create a new replicate dictionary
    add the new_experiment_id to the new replicate dictionary
    validate the new replicate dictionary
    create the new ENCODE object
'''
