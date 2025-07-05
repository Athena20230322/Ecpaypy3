import time
import json
import os
import collections
import urllib.request, urllib.parse, urllib.error
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actInvAllowance(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='InvAllowance')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
    def genOrderRequestInfo(self, param_csv, invoice_info, exclusive_params, revert_params):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        for key in req:
            req[key] = req[key].encode('utf-8')
        if invoice_info['InvoiceNumber'] is not False:
            req['InvoiceNo'] = invoice_info['InvoiceNumber']
        else:
            raise ValueError("precondition doesn't response InvoiceNumber!")
        exclusive_ele = {}
        for param in exclusive_params:
            exclusive_ele[param] = req[param]
            req.pop(param)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        for param in exclusive_params:
            req[param] = exclusive_ele[param]
        for param in revert_params:
            req[param] = urllib.parse.unquote_plus(req[param])
        print(req)
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvAllowance_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def strToDict(self, res_info):
        res_dict = {}
        str_to_list = res_info.split('&')
        for item in str_to_list:
            tmp = item.split('=')
            res_dict[tmp[0]] = tmp[1]
        print(res_dict)
        return res_dict

