import json
import os
import configparser
import LibGeneral.MariaOperate as Maria
import LibGeneral.funcGeneral as funcGen
import urllib.parse
from  http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


PJOIN = os.path.join

CollectorDB = Maria.MariaOperate('127.0.0.1', 'OTPDB', 'otpdb_usr', '1qaz@WSX3306')
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))



#atm_pinfo_args = funcGen.uniqMergeList(payinfo_root, atm_args)

class PostHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        content_len = int(self.headers.get('content-length'))
        requestBody = self.rfile.read(content_len).decode('UTF-8')
        requestHeader = str(self.headers)
        data = json.loads(requestBody)
        print(data)
        print(type(data))
        print(list(data.keys()))

        stmt = """INSERT INTO OTPDB.tb_recievedOTP (
                PhoneNo,
                OTPType,
                PassCode,
                PhoneRcvUnixTime
                ) VALUES (
                '%s',
                '%s',
                '%s',
                UNIX_TIMESTAMP(NOW())
                )""" % (data['TEL'], data['OTPUsage'], data['Passcode'])


            
            
        CollectorDB.execNonQuery(stmt)        
    
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()        
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        print(self.headers)
        print(self.path)
        if self.path == '/favicon.ico':
            pass
        elif parsed_path is not None and len(parsed_path) > 0:
            query = parsed_path.query.split('&')
            q_dict = {x.split('=')[0] : x.split('=')[1] for x in query}
            if list(q_dict.keys()).__contains__('CellNo'):
                cell_no = q_dict['CellNo']
                if list(q_dict.keys()).__contains__('OTPType'):
                    qtype = q_dict['OTPType']
                    if list(q_dict.keys()).__contains__('TimeRange') is False or q_dict['TimeRange'] == '':
                        t_range = 30
                    else:
                        t_range = int(q_dict['TimeRange'])
                        
                    #if qtype == 'Credit_Payment':
                    stmt = """SELECT
                                PassCode, 
                                PhoneRcvUnixTime
                                FROM tb_recievedOTP
                                WHERE
                                PhoneNo = '%s' AND
                                OTPType = '%s' AND
                                PhoneRcvUnixTime >  (UNIX_TIMESTAMP(NOW()) - %i) 
                                order by id desc limit 1;
                    """ % (cell_no, qtype, t_range)
                    #else:
                        #pass

                    print(stmt)
                    qresult = CollectorDB.queryData(stmt)
                    print(qresult)
                    if len(qresult) == 1:
                        raw_data = qresult[0]
                        data_dic = {}
                        data_dic['OTP'] = raw_data[0]
                        data_dic['RcvTimeStamp'] = raw_data[1]

                        jdata = json.dumps(data_dic, sort_keys=True, indent=4, separators=(',', ': '))
                        self.send_response(200)
                        self.send_header('Content-type', 'text/json')
                        self.end_headers()                        
                        self.wfile.write(jdata)

                    else:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/json')
                        self.end_headers()
                        self.wfile.write('Not_Found')
                        

                        



                else:
                    self.send_error(500, message="Lacking argument : OTPType")
            else:
                self.send_error(500, message="Lacking argument : PhoneNo")


        #self.send_response(404)
        







    

server = HTTPServer(('', 443), PostHandler)
server.serve_forever()
