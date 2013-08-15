#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''GET an ENCODE antibody lot object'''

'''use requests to handle the HTTP connection'''
import requests
'''use json to convert between Python dictionaries and JSON objects'''
import json

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
    if not response.status_code == requests.codes.ok:
        print >> sys.stderr, response.text
        response.raise_for_status()
    return response.json()

if __name__ == "__main__":

    '''GET the ENCODE object using it's resource name'''
    antibody_lot = get_ENCODE('/antibody-lots/ENCAB000AUX/')

    '''extract some fields from the ENCODE object'''
    print "accession:  %s" %(antibody_lot['accession'])
    print "source:     %s" %(antibody_lot['source']['description'])
    print "product_id: %s" %(antibody_lot['product_id'])
    print "lot_id:     %s" %(antibody_lot['lot_id'])
    print "lab ID:     %s" %(antibody_lot['lab'])

    '''link through the lab object'''
    lab = get_ENCODE(antibody_lot['lab'])
    print "lab name:   %s" %(lab['name'])
    print "lab city:   %s" %(lab['city'])

    '''get accession and ENCODE ID for all the antibody lots from that lab'''
    my_labid = antibody_lot['lab']
    antibody_lots_collection = get_ENCODE('/antibody-lots/')
    antibody_lots = antibody_lots_collection['@graph']
    my_lots = [lot for lot in antibody_lots if lot['lab'] == my_labid]
    print "Of %d lots %d are submitted by the same lab" %(len(antibody_lots), len(my_lots))
    my_lot_index = {lot['accession']:lot['@id'] for lot in my_lots}
    print my_lot_index

    '''at this point we have an index of all the antibody lots submitted by that lab'''
    '''use that index to make a report of approvals and status'''
