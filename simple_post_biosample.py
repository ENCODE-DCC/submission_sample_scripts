#!/usr/bin/env python2
# -*- coding: latin-1 -*-
'''Create a new ENCODE biosample object'''

'''use requests to handle the HTTP connection'''
import requests
'''use json to convert between Python dictionaries and JSON objects'''
import json
'''use jsonschema to validate objects against the JSON schemas'''
import jsonschema
import sys
import pprint

'''store the ENCODE server address and an authorization keypair'''
'''create the keypair from persona or get one from your wrangler'''
SERVER = 'https://test.encodedcc.org' #replace with your server URL
AUTHID = 'your_access_key_id'               #replace with your access_key_id
AUTHPW = 'your_secret_access_key'           #replace with your secret_access_key

'''pass JSON to the server and force return from the server in JSON format'''
HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}

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
    response = requests.patch(url, auth=(AUTHID, AUTHPW), , headers=HEADERS, data=json_payload)
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

    biosample_schema = get_ENCODE('/profiles/biosample.json')
    #biosample_fields = dict.fromkeys(biosample_schema['properties'].keys())
    #pprint.pprint(biosample_fields)
    # Save the metadata for the new biosample object.  For completeness, all schema fields
    # are shown.  In general, for fields you do not wish to store an explicit value, leave those
    # fields out of the object entirely.  Any value you supply (including an empty string or array) will over-ride the default.
    new_biosample = {
        'age':                  '44',
        'age_units':            'year',
        #'aliases':              ['j-michael-cherry:test_BSXYZ','j-michael-cherry:alternate_BSLMN'], #make unique aliases then uncomment this property
        'award':                'U41HG006992',
        'biosample_term_id':    'CL:0002620',
        'biosample_term_name':  'skin fibroblast',
        'biosample_type':       'primary cell line',
        'constructs':           ['00975aca-0546-4998-b2d6-4dca6f511958'],
        'culture_harvest_date': '2013-01-23',
        'culture_start_date':   '2013-01-13',
        'date_obtained':        '2012-12-20',
        'derived_from':         ['ENCBS016ENC'],
        'description':          'Some free-text description of this arbitrary nonsensical test biosample',
        'donor':                'ENCDO000HUM', #you would not normally use this generic donor object, but rather object for the real donor
        'health_status':        'Some free-text description of the health of the donor at the time of donation.',
        'lab':                  'j-michael-cherry',
        'life_stage':           'adult',
        'lot_id':               '001-234',
        'note':                 'This biosample is a test object created by a script.',
        'organism':             'human',
        'part_of':              ['ENCBS999JSS'],
        'passage_number':       10,
        'phase':                'G1',
        'pooled_from':         ['ENCBS873AAA', 'ENCBS872AAA'],
        'product_id':           '225-X65',
        'protocol_documents':  ['ENCODE:GM04504A_Stam_protocol','ENCODE:HPDE6-E6E7_Crawford_protocol'], #see /documents for a list of aliases
        #'rnais':               None,
        'source':               'atcc',
        'starting_amount':      '10e3',
        'starting_amount_units': 'cells',
        'subcellular_fraction': 'nucleus',
        'transfection_type':    'stable',
        'treatments':           ['062ec8eb-d326-42a0-8ca4-4f01df85c1bc', '0acc7e93-04c9-422d-974b-582cc8814330'],
        'url':                  'hhtp://www.example.com'
    }
    if not jsonschema.validate(new_biosample, biosample_schema):
        #validate raises an error if validation fails
        pass

    response = new_ENCODE('/biosamples/',new_biosample)
    pprint.pprint(response)
    ''' if the object is created successfully, the actual object (complete with server-side calculated properties, like accession)
        is returned in the response @graph
    '''
    if response['status'] == 'success':
        new_biosample_object = response['@graph'][0]
        print "Biosample %s created" %(new_biosample_object['accession'])
    else:
        print "Nothing created"
