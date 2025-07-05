# -*- coding: utf-8 -*-

import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections


class actInvQueryAllowanceInvalidb2b(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvQueryAllowanceInvalidb2b')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv, request_dict, inject_value=''):
        req = self.genArgsDictFromCSV(param_csv)

        if req['MerchantID'] == 'AUTO_INJECT_KEY':
            req['MerchantID'] = inject_value

        for res_dict_key in request_dict:
            if res_dict_key == 'IA_Invoice_No' or res_dict_key == 'InvoiceNumber':
                if req['InvoiceNo'] == 'AUTO_GEN_SKIP':
                    req['InvoiceNo'] = ''
                elif req['InvoiceNo'] == 'AUTO_INJECT_KEY':
                    req['InvoiceNo'] = inject_value
                else:
                    req['InvoiceNo'] = request_dict[res_dict_key]
            if res_dict_key == 'IA_Allow_No' or res_dict_key == 'AI_Allow_No':
                if req['AllowanceNo'] == 'AUTO_GEN_SKIP':
                    req['AllowanceNo'] = ''
                elif req['AllowanceNo'] == 'AUTO_INJECT_KEY':
                    req['AllowanceNo'] = inject_value
                else:
                    req['AllowanceNo'] = request_dict[res_dict_key]

        for key in req:
            req[key] = req[key].encode('utf-8')

        chksum = self.genChkMacVal(req, case='insensitive')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestInfoB2B(self, param_csv, invoice_info,invoice_info1,inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        req = {}

        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
       # data['InvoiceNo'] = invoice_info['IA_Invoice_No']
        data['AllowanceNo'] = invoice_info1['AllowanceNo']

        req['MerchantID'] = data['MerchantID']
       # req['PlatformID'] = '3083192'

        data.pop('MerchantID')
        data.pop('Timestamp')
       # data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        #rqHeader.pop('InvoiceNo')
        rqHeader.pop('AllowanceNo')
       # rqHeader.pop('PlatformID')

        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')
        print("113")
        print(data)
        data = self.urlEncode(data)
        # print data
        data = self.aesEncrypt(data)
        # print data
        print(rqHeader)
        req['Data'] = data
        req['RqHeader'] = rqHeader
        print(req)
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvQueryAllowanceInvalidb2b_API']
        print('BEFORE DO SORT:', req_info)
        od_arg_dict = collections.OrderedDict(sorted(req_info.items()))
        print('DID SORT:', od_arg_dict)
        query_order = self.postRequestToAPIb2c(self.raw_sess, od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(query_order.decode('utf-8'))
        return query_order
