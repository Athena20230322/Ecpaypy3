# -*- coding:utf-8 -*-

import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections


class actInvQueryChkLoveCodeb2c(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvQueryChkLoveCodeb2c')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
    def genOrderRequestInfo(self, param_csv, inject_value=''):
        req = self.genArgsDictFromCSV(param_csv)
        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value
                break
        chksum = self.genChkMacVal(req, case='insensitive')
        req['CheckMacValue'] = chksum
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvQueryChkLoveCodeb2c_API']
        print('BEFORE DO SORT:', req_info)
        od_arg_dict = collections.OrderedDict(sorted(req_info.items()))
        print('DID SORT:', od_arg_dict)
        query_order = self.postRequestToAPIb2c(self.raw_sess, od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(query_order.decode('utf-8'))
        return query_order

    def genOrderRequestInfoB2c(self, param_csv,inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        # Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
       # data['InvoiceNo'] = invoice_info['InvoiceNumber']
        # data['InvoiceDate'] = invoice_info['InvoiceDate']
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'

        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName')

        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('LoveCode')
        # rqHeader.pop('InvoiceDate')
        # rqHeader.pop('NotifyMail')
        # rqHeader.pop('Phone')
        # rqHeader.pop('Notify')
        # rqHeader.pop('InvoiceTag')
        # rqHeader.pop('Notified')

        # data['Items'] = [Items]
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

    # def strToDict(self, res_info):
    #     res_dict = {}
    #     str_to_list = res_info.split('&')
    #     for item in str_to_list:
    #         tmp = item.split('=')
    #         res_dict[tmp[0]] = tmp[1]
    #     print res_dict
    #     return res_dict

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
        res_dict = eval(res_info)
        print(res_dict)
        return res_dict

    def decryptDatab2c(self, data):
        # data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def decryptDatab2c2(self, data):
        # data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)
    
