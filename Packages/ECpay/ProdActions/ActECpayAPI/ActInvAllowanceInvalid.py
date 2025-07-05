import time
import json
import os
import collections
import urllib.request, urllib.parse, urllib.error
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actInvAllowanceInvalid(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvAllowanceInvalid')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv, all_csv, exclusive_params, revert_params):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if all_csv['IA_Invoice_No'] and all_csv['IA_Allow_No'] is not False:
            req['InvoiceNo'] = all_csv['IA_Invoice_No']
            if len(req['AllowanceNo']) == 0:
                req['AllowanceNo'] = all_csv['IA_Allow_No']
        else:
            raise ValueError("precondition doesn't response InvoiceNumber!")
        for key in req:
            req[key] = req[key].encode('utf-8')
        exclusive_ele = {}
        for param in exclusive_params:
            exclusive_ele[param] = req[param]
            req.pop(param)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        for param in exclusive_ele:
            req[param] = exclusive_ele[param]
        for param in revert_params:
            req[param] = urllib.parse.unquote_plus(req[param])
        print(req)
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvAllowanceInvalid_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genCheckMacValue(self, req_info):
        rtn_chksum = req_info['CheckMacValue']
        req_info.pop('CheckMacValue')
        gen_result = {}
        chksum = self.genChkMacVal(req_info, mode='local')
        print(chksum)
        req_info['CheckMacValue'] = rtn_chksum
        gen_result['CheckMacValue'] = chksum
        return gen_result
