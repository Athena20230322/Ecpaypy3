import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections
import urllib.request, urllib.parse, urllib.error


class actInvNotify(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI',
                                                                feature_name='InvNotify')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv, request_dict, revert_args):
        req = self.genArgsDictFromCSV(param_csv)

        for key in req:
            req[key] = req[key].encode('utf-8')

        for res_dict_key in request_dict:
            if res_dict_key == 'IA_Invoice_No' or res_dict_key == 'InvoiceNumber':
                if req['InvoiceNo'] == 'AUTO_GEN_SKIP':
                    req['InvoiceNo'] = ''
                else:
                    req['InvoiceNo'] = request_dict[res_dict_key]
            if res_dict_key == 'IA_Allow_No' or res_dict_key == 'AI_Allow_No':
                if req['AllowanceNo'] == 'AUTO_GEN_SKIP':
                    req['AllowanceNo'] = ''
                else:
                    req['AllowanceNo'] = request_dict[res_dict_key]
        chksum = self.genChkMacVal(req, case='insensitive')
        print(chksum)

        for revert_key in revert_args:
            req[revert_key] = urllib.parse.unquote(req[revert_key])

        req['CheckMacValue'] = chksum
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvNotify_API']
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
