import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper


class actInvTrigger(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvTrigger')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def strToDict(self, res):
        res_list = res.split('&')
        res_dict = {}
        for item in res_list:
            res_dict[item.split('=')[0]] = item.split('=')[1]
        return res_dict

    def genCheckMacValue(self, res_dict):
        chk = res_dict['CheckMacValue']
        res_dict.pop('CheckMacValue')
        chksum = self.genChkMacVal(res_dict, mode='local')
        print(chksum)
        res_dict['CheckMacValue'] = chk
        return chksum

    def genOrderRequestInfo(self, param_csv, delay_dict):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if type(delay_dict) is dict:
            if len(req['Tsr']) == 0:
                req['Tsr'] = delay_dict['OrderNumber']
        else:
            raise TypeError("ActGenOrderRequestInfo: Received delay_dict is not a dictionary.")
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvTrigger_API']
        response = self.postRequestToAPI(self.genSession(), req_info, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response
