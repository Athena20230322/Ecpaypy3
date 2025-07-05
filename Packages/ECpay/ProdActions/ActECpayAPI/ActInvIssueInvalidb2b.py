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


class actInvIssueInvalidb2b(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvIssueInvalidb2b')
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

            # chksum = self.genChkMacVal(req, case='insensitive')
            # print chksum
            # req['Reason'] = temp_dict['Reason']
            #
            # for param in revert_params:
            #     req[param] = urllib.unquote_plus(req[param])
            #
            # req['CheckMacValue'] = chksum
            # return req

    def genOrderRequestInfoB2B(self, param_csv,invoice_info,invoice_info1,inject_value=''):

        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
       # Items = self.genArgsDictFromCSV(param_csv)

        req = {}
        data['InvoiceNumber'] = invoice_info['InvoiceNumber']
        data['RelateNumber'] = invoice_info1['RelateNumber']


        # if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
        #     data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        req['MerchantID'] = data['MerchantID']
        #req['PlatformID'] = '3083192'


        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('Reason')
        rqHeader.pop('Remark')
       # rqHeader.pop('InvType')




        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')

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

    def createOrderByRequest(self, req_info):
        pass

    def genpostRequestToAPI(self, order_info_crt_res, api_url):
        query_order = self.postRequestToAPI(self.raw_sess, order_info_crt_res, api_url)
        return query_order

    def genpostRequestToAPI(self, order_info_crt_res, api_url):
        query_order = self.postRequestToAPIb2c(self.raw_sess, order_info_crt_res, api_url)
        return query_order

    def genPostRequestToAPIb2b(self, req_info):
        form_act = self.feature_conf['InvIssueInvalidb2b_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response



    def strToDict(self, res_info):
        res_info = self.urlEncode(res_info)
        print('str1: ' + res_info)
        res_dict = {}
        res_info = self.urlDecode(res_info)
        print('str2: ' + res_info)
        # str_to_list = res_info.split('&')
        # for item in str_to_list:
        #     tmp = item.split('=')
        #     res_dict[tmp[0]] = tmp[1]
        res_dict = json.loads(res_info)
        print(res_dict)
        return res_dict

    def quote_item(self, res_dict, revert_list):
        for key in revert_list:
            res_dict[key] = urllib.parse.quote_plus(res_dict[key]).lower()
        return res_dict
    def decryptDatab2b(self, data):
        #data = self.urlDecode(data)
        print(data)

        return json.loads(self.aesDecrypt(data))
    def decryptDatab2b2(self, data):
        #data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)
