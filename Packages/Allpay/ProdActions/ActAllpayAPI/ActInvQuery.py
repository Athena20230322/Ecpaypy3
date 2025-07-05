import time
import json
import os
import collections
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actInvQuery(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='InvQuery')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv, inv_info):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req['RelateNumber'] = inv_info['RelateNumber']
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvQuery_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def createOrderByRequest(self, req_info):
        pass

