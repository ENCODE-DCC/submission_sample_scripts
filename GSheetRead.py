
from ENCODETools import GetENCODE
from ENCODETools import LoginGSheet
from ENCODETools import FindGSpreadSheet
from ENCODETools import FindGWorkSheet
from ENCODETools import FindGSheetCells
from ENCODETools import WriteJSON

from identity import keys

if __name__ == "__main__":
    '''
    This script will read in a google spreadsheet of objects and save them to json
    '''

    json_file = 'update.json'

    email = "yourname@gmail.com"
    password = "abcdefg1234567"

    spreadname = 'My Latest Data'
    typelist = ['human_donor','target','biosample']

    # start a spreadsheet login
    sheetclient = LoginGSheet(email,password)

    # get the spreadsheet id
    [spreadid,spreadsheet] = FindGSpreadSheet(sheetclient,spreadname)

    # check for data of each potential object type
    object_list = []
    for workname in typelist:
        print workname
        # find the worksheet
        [workid,worksheet] = FindGWorkSheet(sheetclient,spreadid,workname)
        
        if workid:
            # get rows
            rows = sheetclient.GetListFeed(spreadid, workid).entry
            # get list of compressed header names
            headers = rows[0].custom.keys()
            # get cells from sheet
            cells = FindGSheetCells(sheetclient,spreadid,workid)
            # get schema for current object type
            object_schema = GetENCODE(('/profiles/' + workname + '.json'),keys)

            # for each header name, replace the compressed name with the full name
            for colindex,header in enumerate(headers):
                headers[colindex] = cells[colindex].content.text

            # for each row, load in each key/value pair that has a value assigned
            # convert value to schema defined type

            for row in rows:
                new_object = {u'@type':[workname,u'item']}
                for header in headers:
                    if object_schema[u'properties'].has_key(header):
                        value = row.custom[header.replace('_','').lower()].text
                        if value is not None:
                            # need to fix dates before adding them.  Google API does not allow disabling of autoformat.
                            # use regexp to check for dates (MM/DD/YYYY)
                            # then format them as we enter them (YYYY-MM-DD)
#                            if "\u03bc" in value:
#                                value = unicode(value)
#                                print value
#                                print type(value)
                            if object_schema[u'properties'][header].has_key(u'format') and object_schema[u'properties'][header][u'format'] == 'date':
                                #print value
                                date = value.split('/')
                                if len(date[0]) is 1:
                                    date[0] = '0' + date[0]
                                if len(date[1]) is 1:
                                    date[1] = '0' + date[1]
                                value = date[2] + '-' + date[0] + '-' + date[1]
                                #print value
                            if object_schema[u'properties'][header][u'type'] == 'string':
                                new_object.update({header:unicode(value)})
                            elif object_schema[u'properties'][header][u'type'] == 'integer':
                                new_object.update({header:int(value)})
                            elif object_schema[u'properties'][header][u'type'] == 'float':
                                new_object.update({header:float(value)})
                            elif object_schema[u'properties'][header][u'type'] == 'array':
                                value = value.split(', ')
                                if object_schema[u'properties'][header][u'items'][u'type'] == 'string':
                                    new_object.update({header:value})
    #                            elif object_schema[u'properties'][header][u'items'][u'type'] is 'integer':
    #                                new_object.update({header:int(value)})
                    
                object_list.append(new_object)

    # write object to file
    WriteJSON(object_list,json_file)
    print('Done.')

