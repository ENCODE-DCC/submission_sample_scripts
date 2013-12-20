import sys
import csv
import json
import jsonschema
import requests
import gdata.spreadsheet.service


# set headers
HEADERS = {'content-type': 'application/json'}

def get_ENCODE(obj_id,keys):
    '''GET an ENCODE object as JSON and return as dict'''
    url = keys['server']+obj_id+'?limit=all'
    response = requests.get(url, auth=(keys['authid'],keys['authpw']), headers=HEADERS)
    if not response.status_code == 200:
        print >> sys.stderr, response.text
    return response.json()

def GetENCODE(object_id,keys):
    '''GET an ENCODE object as JSON and return as dict'''
    if type(object_id) is str:
        url = keys['server']+object_id+'?limit=all'
        #print(url)
        try:
            response = requests.get(url,auth=(keys['authid'],keys['authpw']), headers=HEADERS)
            if not response.status_code == 200:
                print >> sys.stderr, response.text
        # no
        except Exception as e:
            print("Get request failed:")
            #print(e)
        # yes
        else:
            return response.json()

def patch_ENCODE(obj_id,patch_json,keys):
    '''PATCH an existing ENCODE object and return the response JSON'''
    url = keys['server']+obj_id
    json_payload = json.dumps(patch_json)
    response = requests.patch(url, auth=(keys['authid'],keys['authpw']), data=json_payload)
    print "Patch:"
    print response.status_code
    if not response.status_code == 200:
        print >> sys.stderr, response.text
    return response.json()

def new_ENCODE(collection_id, object_json,keys):
    '''POST an ENCODE object as JSON and return the resppnse JSON'''
    url = keys['server'] +'/'+collection_id+'/'
    json_payload = json.dumps(object_json)
    response = requests.post(url, auth=(keys['authid'],keys['authpw']), headers=HEADERS, data=json_payload)
    print(response.status_code)
    if not response.status_code == 201:
        print >> sys.stderr, response.text
    return response.json()

def KeyENCODE(key_file,user_name,server_name):
    '''
    get keys from file
    '''
    key_open = open(key_file)
    keys = csv.DictReader(key_open,delimiter = '\t')
    for key in keys:
        if (key.get('Server') == server_name) & (key.get('User') == user_name):
            key_info = {}
            key_info['user'] = key.get('User')
            key_info['server'] = ('http://' + key.get('Server') + '.encodedcc.org')
            key_info['authid'] = key.get('ID')
            key_info['authpw'] = key.get('PW')
            print('Identity confirmed')
    key_open.close()
    return(key_info)

def ReadJSON(json_file):
    '''
    read json objects from file
    '''
    json_load = open(json_file)
    json_read = json.load(json_load)
    json_load.close()
    # if the returned json object is not a list, put it in one
    if type(json_read) is dict:
        json_list = []
        json_list.append(json_read)
    elif type(json_read) is list:
        json_list = json_read
    return json_list

def WriteJSON(new_object,object_file):
    '''
    write new json obect.
    '''
    # SHOULD BE MODIFIED TO CUSTOM OUTPUT FORMAT (FOR HUMAN VIEWING)
    with open(object_file, 'w') as outfile:
        json.dump(new_object, outfile)
        outfile.close()

def ValidJSON(object_type,object_id,new_object,keys):
    '''
    check json object for validity
    '''
    # SHOULD ONLY NEED OBJECT.  NEED DEF TO EXTRACT VALUE (LIKE TYPE) FROM JSON OBJECT GRACEFULLY.
    # get the relevant schema
    object_schema = GetENCODE(('/profiles/' + object_type + '.json'),keys)

    # test the new object.  SHOULD HANDLE ERRORS GRACEFULLY        
    try:
        jsonschema.validate(new_object,object_schema)
    # did not validate
    except Exception as e:
        print('Validation of ' + object_id + ' failed.')
        print(e)
        return False

    # did validate
    else:
        # inform the user of the success
        print('Validation of ' + object_id + ' succeeded.')
        return True

def CleanJSON(new_object,object_schema,action):
    '''
    intended to fix invalid JSON.  removes unexpected or unpatchable properties
    '''
    # DOES NOT REMOVE ITEMS THAT CAN ONLY BE POSTED
    for key in new_object.keys():
        if not object_schema[u'properties'].get(key):
            new_object.pop(key)
        elif object_schema[u'properties'][key].has_key(u'requestMethod'):
            if object_schema[u'properties'][key][u'requestMethod'] is []:
                new_object.pop(key)
            elif action not in object_schema[u'properties'][key][u'requestMethod']:
                new_object.pop(key)
    return new_object

def FlatJSON(json_object,keys):
    '''
    flatten embedded json objects to their ID
    '''
    # RATE LIMITING STEP:  this should be changed to check whether it is needed or not
    #json_object = EmbedJSON(json_object,keys)
    #print json_object
    for key,value in json_object.items():
        if type(value) is dict:
            #print key,value
            if json_object[key].has_key(u'@id'):
                json_object[key] = json_object[key][u'@id']
            elif json_object[key].has_key(u'href'):
                json_object[key] = json_object[key][u'href']
        if type(value) is list:
            #print("Found List: " + key)
            value_new = []
            for value_check in value:
                #print("Checking...")
                if type(value_check) is dict:
                    #print("Found Object")
                    if value_check.has_key(u'@id'):
                        value_check = value_check[u'@id']
                    elif value_check.has_key(u'href'):
                        value_check = value_check[u'href']
                    #print(value_check)
                value_new.append(value_check)
            json_object[key] = value_new
    return json_object

def EmbedJSON(json_object,keys):
    '''
    expand json object
    '''
    for key,value in json_object.items():
        if (type(value) is unicode):
            if (len(value) > 1):
                if str(value[0]) == '/':
                    json_sub_object = GetENCODE(str(value),keys)
                    if type(json_sub_object) is dict:
                        #json_sub_object = EmbedJSON(json_sub_object,keys)
                        json_object[key] = json_sub_object
        elif type(value) is list:
            values_embed = []
            for entry in value:
                if (type(entry) is unicode):
                    if (len(entry) > 1):
                        if str(entry[0]) == '/':
                            json_sub_object = GetENCODE(str(entry),keys)
                            if type(json_sub_object) is dict:
                                #json_sub_object = EmbedJSON(json_sub_object,keys)
                                values_embed.append(json_sub_object)
            if len(values_embed) is len(json_object[key]):
                json_object[key] = values_embed
    return json_object

def FindSets(jsonobjects,query,returnset):
    '''
    Find a set of objects that contain a particular key value pair in any part of the set.
    
    Input
    jsonobjects: a list of JSON objects that will be searched.
    This can either be a uniform collection or not, but each object
    will be treated as a set.
    query: a dict with key:value pair(s) to search for.
    Currently, only works as an 'OR' search.
    returnset: a string to indicate how to return values
        'original': returns only root object
        'only': returns only objects containing the match
        'all': returns all objects from the set with the match
    
    Output
    foundobjects: a list of JSON objects that match the search parameters.
    otherobjects: a list of JSON objects that don't match.
    '''
    foundobjects = []
    otherobjects = []
    for jsonobject in jsonobjects:
        if jsonobject.has_key(u'@id'):
            subfoundobjects = []
            subotherobjects = []
            foundobject = False
            querycheck = {}
            #print('Checking...')
            for key,value in jsonobject.items():
                if type(value) is dict:
                    #print('Dictionary')
                    #print value
                    [sfobjs,soobjs] = FindSets([value],query,returnset)
                    if sfobjs:
                        for sfobj in sfobjs:
                            subfoundobjects.append(sfobj)
                    if soobjs:
                        for soobj in soobjs:
                            subotherobjects.append(soobj)
                elif value and (type(value) is list) and (type(value[0]) is dict):
                    #print('Dictionary List')
                    for item in value:
                        [sfobjs,soobjs] = FindSets([item],query,returnset)
                        if sfobjs:
                            for sfobj in sfobjs:
                                subfoundobjects.append(sfobj)
                        if soobjs:
                            for soobj in soobjs:
                                subotherobjects.append(soobj)
                elif value and ((type(value) is list) and (type(value[0]) is not dict)) or (type(value) is not dict) or (type(value) is not list):
                    #print('Checking...')
                    for searchkey,searchvalue in query.items():
                        if searchkey in str(key):
                            #print 'inkey',key,value
                            if searchvalue in str(value):
                                #print 'invalue',value
                                querycheck.update({searchkey:searchvalue})

            # CURRENTLY ONLY CHECKS FOR ANY HIT.  WORKS LIKE 'OR' INSTEAD OF 'AND'.
            if querycheck:
                #print 'Found.'
                foundobject = True

            if foundobject:
                foundobjects.append(jsonobject)
            elif subfoundobjects and ((returnset == 'all') or (returnset == 'original')):
                foundobjects.append(jsonobject)
            else:
                otherobjects.append(jsonobject)
    
            if subfoundobjects and ((returnset == 'all') or (returnset == 'only')):
                for subfoundobject in subfoundobjects:
                    foundobjects.append(subfoundobject)
    
            if subfoundobjects and subotherobjects and (returnset == 'all'):
                for subotherobject in subotherobjects:
                    foundobjects.append(subotherobject)
            else:
                for subotherobject in subotherobjects:
                    otherobjects.append(subotherobject)

    if foundobjects:
        foundobjects = {foundobj['@id']:foundobj for foundobj in foundobjects}.values()
    if otherobjects:
        otherobjects = {otherobj['@id']:otherobj for otherobj in otherobjects}.values()
    return foundobjects,otherobjects

def LoginGSheet(email,password):
    '''
    start a connection
    '''
    sheetclient = gdata.spreadsheet.service.SpreadsheetsService()
    sheetclient.email = email
    sheetclient.password = password
    sheetclient.ProgrammaticLogin()
    return sheetclient

def FindGSpreadSheet(sheetclient,spreadname):
    '''
    find a specific spreadsheet and get the id
    '''
    query = gdata.spreadsheet.service.DocumentQuery()
    query.title = spreadname
    query.title_exact = 'true'
    spreadfeed = sheetclient.GetSpreadsheetsFeed(query=query)
    if len(spreadfeed.entry) >= 1:
        spreadsheet = spreadfeed.entry[0]
        spreadid = spreadsheet.id.text.rsplit('/',1)[1]
    else:
        spreadsheet = ''
        spreadid = ''
    return(spreadid,spreadsheet)

def FindGWorkSheet(sheetclient,spreadid,workname):
    '''
    find a specific worksheet and get the id
    '''
    query = gdata.spreadsheet.service.DocumentQuery()
    query.title = workname
    query.title_exact = 'true'
    workfeed = sheetclient.GetWorksheetsFeed(spreadid,query=query)
    if len(workfeed.entry) >= 1:
        worksheet = workfeed.entry[0]
        workid = worksheet.id.text.rsplit('/',1)[1]
    else:
        worksheet = ''
        workid = ''
    return(workid,worksheet)

def FindGSheetCells(sheetclient,spreadid,workid):
    '''
    find specified cells (currently returns all, including empty)
    '''
    query = gdata.spreadsheet.service.CellQuery()
    query.return_empty = "true" 
    cells = sheetclient.GetCellsFeed(spreadid,workid,query=query).entry
    return(cells)


