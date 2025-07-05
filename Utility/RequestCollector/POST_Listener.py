# -*- coding: utf-8 -*-

import json
import os
import configparser
import LibGeneral.MariaOperate as Maria
import LibGeneral.funcGeneral as funcGen
import urllib.parse
import logging
from LibGeneral.AddLog import customLog
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn


def confStringToList(string):
    if type(string) is str:
        res = [x.replace(' ', '').strip("'") for x in string.split(',')]
        res.sort()
        return res
    else:
        raise TypeError("Recieved argument is not a string")


def gen_conf_sec_dict(confobj, sec_name):
    basic_args = confobj.items(sec_name)
    service_categories = []
    cat_dict = {}
    for cat in basic_args:
        cat_name = cat[0]
        cat_columns = confStringToList(cat[1])
        service_categories.append(cat_name)
        cat_dict[cat_name] = cat_columns
    return cat_dict


def gen_plain_param_dict(confobj, cat_dict):
    cats = list(cat_dict.keys())
    subtype_dict = {}
    for c in cats:
        base_column = cat_dict[c]
        subtype_column_dict = gen_conf_sec_dict(confobj, c)
        for t in list(subtype_column_dict.keys()):
            full_column = funcGen.uniqMergeList(base_column, subtype_column_dict[t])
            subtype_column_dict[t] = full_column
        subtype_dict[c] = subtype_column_dict
    return subtype_dict

     
def gen_xml_param_dict():
    pass


def gen_json_param_dict():
    pass


class Logging(customLog):
    
    def __init__(self):
        self.rootdir = ''
        self.log_dir = '/var/log'
        self.log_level = 'INFO'
        self.is_console_out = '0' 
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')             


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        # Check recieved data format: plain text, json, xml
        cols = None
        content_len = int(self.headers.get('content-length'))
        requestBody = self.rfile.read(content_len).decode('UTF-8')
        requestHeader = str(self.headers)
        #print 'Header= ' + requestHeader
        LOG.INFO("POST request, Header:\n %s" % (requestHeader))
        
        #print 'requestBody=' + requestBody
        LOG.INFO("POST request, Body:\n %s" % (requestBody))
        
        if requestBody.startswith('<?xml'):
            pass
        elif requestBody.startswith('{'):
            try:
                payload = json.loads(requestBody)
            except:
                pass
                #print 'Exception occurs when loading return json data'
            else:
                args = list(payload.keys())
                for cat in list(json_base_args.keys()):
                    cols = json_base_args[cat]
                    request_typ = 'Unknown'
                    if cols == args:
                        #print 'JSON return data match pattern [%s]' % (cat)
                        request_cat = cat
                        break
                    else:
                        request_cat = 'Unknown'
        else:
            # If received data is not json or xml, treat it as ordinary text
            LOG.INFO("Request body is not json or xml, treat it as ordinary text")
            recv_data_list = requestBody.split('&')
            recv_data_dict = {x.split('=')[0]: x.split('=')[1] for x in recv_data_list}
            args = list(recv_data_dict.keys())
            args_set = set(args)
            args.sort()
            
            matched_cat = []
            for category in list(plain_base_set.keys()):
                if plain_base_set[category].issubset(args_set):
                    matched_cat.append(category)
                else:
                    pass
            #print "Match Category:", matched_cat
            LOG.INFO("All match Category: %s" % (matched_cat))
            if len(matched_cat) == 0:
                request_cat = 'Unknown'
                request_typ = 'Unknown'
            elif len(matched_cat) > 0:
                for mat in matched_cat:
                    if mat in plain_sub_args:
                        subtypes = plain_sub_args[mat]
                        request_cat = mat
                        request_typ = 'Unknown'
                        for st in list(subtypes.keys()):
                            cols = subtypes[st]
                            if args == cols:
                                #print 'Match subtype %s' % (st)
                                LOG.INFO("Match subtype : %s" % (st))
                                request_typ = st
                                break
                    else:
                        request_cat = mat
                        request_typ = 'N/A'
            else:
                request_cat = 'Exception'
                
        #print "request_cat:", request_cat
        LOG.INFO("Request body maching complete, Category: %s, Subtype : %s" % (request_cat, request_typ))
        
        if request_cat == 'Unknown':
            ident_col = 'Unknown'
            ident_val = 'Unknown'
        elif request_cat in identifier_dict:
            ident_col = identifier_dict[request_cat][0]
            #print ident_col
            LOG.INFO("Find identifier column of %s, Column name : %s" % (request_cat, ident_col))
            ident_val = recv_data_dict[ident_col]
            LOG.INFO("Identifier column value : %s" % (ident_val))
        else:
            ## log unexpected request_cat          
            pass

        stmt = """INSERT INTO RequestCollectorDB.tb_OrderInfo (
                IdentifierCol,
                IdentValue,
                RecvUnixTime,
                RequestCategory,
                RequestType,
                RequestBody,
                RequestArguments
                ) VALUES (
                '%s',
                '%s',
                 %d,
                '%s',
                '%s',
                '%s',
                '%s'
                )""" % (ident_col, ident_val, funcGen.getCurrentDatetimeStamp()[1], request_cat, request_typ, requestBody, ','.join(args))
        
        #print stmt
        LOG.INFO("Ready for insert to database. Statement:\n %s" % (stmt))
        
        try:
            CollectorDB.execNonQuery(stmt)
        except Exception as err:
            errmsg = err.message
            LOG.ERROR("Exception occurs during DB insert. Message: %s" % (errmsg))
        else:
            LOG.INFO("Insert record complete.")  
            
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()        
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        LOG.INFO("Receive GET request. Header:\n %s" % (self.headers))
        #print self.headers
        LOG.INFO("Receive GET request. Query path: %s" % (self.path))
        #print self.path
        if parsed_path is not None and len(parsed_path) > 0:

            query = parsed_path.query.split('&')
            
            #print query
            if query.count('') == 0:
                q_dict = {x.split('=')[0]: x.split('=')[1] for x in query}
                if 'IdentCol' in q_dict:
                    ident_col = q_dict['IdentCol']
                    if 'IdentVal' in q_dict:
                        ident_val = q_dict['IdentVal']
                        stmt = """SELECT
                                    RequestCategory,
                                    RequestType, 
                                    RequestBody,
                                    RequestArguments
                                    FROM tb_OrderInfo
                                    WHERE
                                    IdentifierCol = '%s' AND
                                    IdentValue = '%s';
                        """ % (ident_col, ident_val)
    
                        #print stmt
                        LOG.INFO("Query database. statement:\n %s" % (stmt))
                        try:
                            qresult = CollectorDB.queryData(stmt)
                        except Exception as err:
                            errmsg = err.message
                            LOG.ERROR("Exception occurs during DB query. Message: %s" % (errmsg))
                        else:
                            LOG.INFO("Query database complete.")
                            
                        #print qresult
                        if len(qresult) == 1:
                            raw_data = qresult[0]
                            data_dic = {}
                            data_dic['RequestCategory'] = raw_data[0]
                            data_dic['Subtype'] = raw_data[1]
                            data_dic['RtnBody'] = raw_data[2]
                            data_dic['Arguments'] = raw_data[3].split(',')
                            data_dic['QueryResult'] = 'RECORD_FOUND'
    
                            jdata = json.dumps(data_dic, sort_keys=True, indent=4, separators=(',', ': '))
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(jdata)
                        elif len(qresult) > 1:
                            self.send_error(500, message="Query result is more than 1 record.")
                            self.end_headers()
                        else:
                            data_dic = {}
                            data_dic['RequestCategory'] = 'NOT_FOUND'
                            data_dic['Subtype'] = 'NOT_FOUND'
                            data_dic['RtnBody'] = 'NOT_FOUND'
                            data_dic['Arguments'] = 'NOT_FOUND'
                            data_dic['QueryResult'] = 'RECORD_NOT_FOUND'
                            self.send_response(204, message="Record not found.")
                            self.end_headers()
                            self.wfile.write(jdata)
    
                    else:
                        self.send_error(500, message="Lacking argument : IdentVal")
                else:
                    self.send_error(500, message="Lacking argument : IdentCol")

        # self.send_response(404)


class ThreadHttpServer(ThreadingMixIn, HTTPServer):
    """For handling multiple requests"""


PJOIN = os.path.join
LOG = Logging()

LOG.createLogger('RequestCollector.log')
CollectorDB = Maria.MariaOperate('127.0.0.1', 'RequestCollectorDB', 'testing_usr', '1qaz@WSX3306')
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
argconf_path = os.path.join(SCRIPT_DIR, 'Request_Arguments.ini')
args_config = configparser.ConfigParser()
args_config.optionxform = str
args_config.read(argconf_path)

identifier_dict = gen_conf_sec_dict(args_config, 'RequestIdentifier')
plain_base_args = gen_conf_sec_dict(args_config, 'BasicColumn')
json_base_args = gen_conf_sec_dict(args_config, 'JSONBasic')
LOG.INFO("Initializing RequestCollector, Beae argument of plain text return data:\n %s" % (plain_base_args))

plain_base_set = {}
for key in list(plain_base_args.keys()):
    plain_base_set[key] = set(plain_base_args[key])
    
plain_sub_args = gen_plain_param_dict(args_config, plain_base_args)
LOG.INFO("Initializing RequestCollector, Subtype argument of plain text return data:\n %s" % (plain_sub_args))

server = ThreadHttpServer(('', 5000), RequestHandler)
#server = HTTPServer(('192.168.50.88', 5000), RequestHandler)
server.serve_forever()
