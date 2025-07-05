# -*- coding: utf-8 -*-

import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections
import urllib.request, urllib.parse, urllib.error


class actInvIssueInvalid(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvIssueInvalid')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
    def genOrderRequestInfo(self, param_csv, invoice_no, revert_params, inject_value=''):
        req = self.genArgsDictFromCSV(param_csv)

        for key in req:
            req[key] = req[key].encode('utf-8')

        temp_dict = {}
        if req['InvoiceNumber'] == 'AUTO_INJECT_KEY':
            req['InvoiceNumber'] = inject_value
        else:
            req['InvoiceNumber'] = invoice_no
        temp_dict['Reason'] = req['Reason']
        req.pop('Reason')

        chksum = self.genChkMacVal(req, case='insensitive')
        print(chksum)
        req['Reason'] = temp_dict['Reason']

        for param in revert_params:
            req[param] = urllib.parse.unquote_plus(req[param])

        req['CheckMacValue'] = chksum
        return req

    def createOrderByRequest(self, req_info):
        pass

    def genpostRequestToAPI(self, order_info_crt_res, api_url):
        query_order = self.postRequestToAPI(self.raw_sess, order_info_crt_res, api_url)
        return query_order

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvIssueInvalid_API']
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
