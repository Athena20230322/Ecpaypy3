import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper


class actInvQueryInvalidb2c(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvQueryInvalidb2c')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()

    def genOrderRequestInfob2c(self, query_dict, issue_dict):
        req = self.genArgsDictFromCSV(query_dict, de_strip=True)
        req['RelateNumber'] = issue_dict['RelateNumber']
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestInfoB2c(self, param_csv, invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        req = {}
        data['RelateNumber'] = invoice_info['RelateNumber']
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('PlatformID')



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

    def genOrderRequestInfoB2cS(self, param_csv, invoice_info,invoice_info1):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        req = {}
        data['RelateNumber'] = invoice_info['RelateNumber']
        data['InvoiceDate'] = invoice_info1['InvoiceDate']
        data['InvoiceNo'] = invoice_info1['InvoiceNo']
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('PlatformID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')

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
    def genOrderRequestInfoB2c2(self, param_csv, invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('PlatformID')



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

    def clearChkMacValue(self, query_dict):
        query_dict['CheckMacValue'] = ''
        return query_dict

    def genPostRequestToAPIb2c(self, req_info):
        form_act = self.feature_conf['InvQueryInvalidb2c_API']
        response = self.postRequestToAPIb2c(self.genSession(), req_info, form_act, trencode_dotnet=True)
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
        res_dict = eval(res_info)
        print(res_dict)
        return res_dict
    def decryptDatab2c2(self, data):
        #data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)