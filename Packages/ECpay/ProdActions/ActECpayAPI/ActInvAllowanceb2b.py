import time
import json
import os
import collections
import urllib.request, urllib.parse, urllib.error
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actInvAllowanceb2b(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvAllowanceb2b')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfoB2B(self, param_csv,invoice_info,inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Details = self.genArgsDictFromCSV(param_csv)
        req = {}

        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
        Details['OriginalInvoiceNumber']=invoice_info['InvoiceNumber']
        req['MerchantID'] = data['MerchantID']
        #req['PlatformID'] = '3083192'

        data.pop('Timestamp')

        data.pop('RqID')
        data.pop('Revision')
        data.pop('OriginalInvoiceNumber')
        data.pop('OriginalInvoiceDate')
        data.pop('OriginalSequenceNumber')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemPrice')
        data.pop('ItemAmount')
        data.pop('Tax')



        rqHeader.pop('MerchantID')
        rqHeader.pop('AllowanceDate')
        rqHeader.pop('CustomerEmail')
        rqHeader.pop('TaxAmount')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('OriginalInvoiceNumber')
        rqHeader.pop('OriginalInvoiceDate')
        rqHeader.pop('OriginalSequenceNumber')
        rqHeader.pop('ItemName')
        rqHeader.pop('ItemCount')
        rqHeader.pop('ItemPrice')
        rqHeader.pop('ItemAmount')
        rqHeader.pop('Tax')



        Details.pop('Timestamp')
        Details.pop('RqID')
        Details.pop('Revision')
        Details.pop('MerchantID')
        Details.pop('AllowanceDate')
        Details.pop('CustomerEmail')
        Details.pop('TaxAmount')
        Details.pop('TotalAmount')


        data['Details'] = [Details]
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



    def genPostRequestToAPIb2b(self, req_info):
        form_act = self.feature_conf['InvAllowanceb2b_API']
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
        res_dict = eval(res_info)
        print(res_dict)
        return res_dict



    def decryptDatab2b(self, data):
        #data = self.urlDecode(data)
        #print data
        return json.loads(self.aesDecrypt(data))

    def decryptDatab2b2(self, data):
        #data = self.urlDecode(data)
        #print data
        return self.aesDecrypt(data)
