import json
import LibGeneral.TestHelper
import TaskDB.ClassTaskDB
import os
import sqlite3
from  http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from LibGeneral.GetConfigValue import getConfig


FRAME_CONF = getConfig()
ROOTDIR = FRAME_CONF.getRootDir()
PJOIN = os.path.join
#ROOTDIR = PJOIN((os.path.dirname(os.path.realpath(__file__))), '..')
TASKDB = PJOIN(ROOTDIR, 'Utility', 'DB', 'TestTaskDB.db')
CLS_TASKDB = TaskDB.ClassTaskDB.classTaskDB(TASKDB)
class JsonResponseHandler(BaseHTTPRequestHandler):

    con = sqlite3.connect(TASKDB)
    cur = con.cursor()
    
    key_add_task = tuple(sorted(
        [
            'GUID',
            'DevFrendName',
            'Test_set',
            'Package'
        ]
    ))
    
    

        

            
    def do_POST(self):
        
        CLS_TASKDB.chkTaskTable() 
        content_len = int(self.headers.get('content-length'))
        requestBody = self.rfile.read(content_len).decode('UTF-8')
        print('requestBody=' + requestBody)
        jsonData = json.loads(requestBody)
        print(jsonData)
        key_in_data = tuple(sorted(jsonData.keys()))
        print(key_in_data)
        cls_helper = LibGeneral.TestHelper.classTestHelper()

        if key_in_data == self.key_add_task:
            print("Recieved POST format correct!")
            dev_name = jsonData['DevFrendName']
            pkg_name = jsonData['Package']
            test_set_name = jsonData['Test_set']
            dev_platform = cls_helper.getDevicePlatform(dev_name)
            
            if CLS_TASKDB.chkTaskAval(dev_name, pkg_name, test_set_name) is True:
                taskuid = jsonData['GUID']
                taskinfo = (taskuid, dev_name, dev_platform, pkg_name, test_set_name)
                CLS_TASKDB.addTestTask(taskinfo)
                query = "select * from tb_testTask"
                self.cur.execute(query)
                res = self.cur.fetchall()
                print(res)
        else:
            print('key verify fail')
        
        print('**JSON**')
        #print(json.dumps(jsonData, sort_keys=False, indent=4, separators={',', ':'}))
        print(json.dumps(jsonData, sort_keys=True, indent=4))
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        #print jsonData[0]

server = HTTPServer(('', 8000), JsonResponseHandler)
server.serve_forever()