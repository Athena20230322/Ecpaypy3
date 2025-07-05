# -*- coding: utf-8 -*-
import time
import json
import requests

import os
import urllib.request, urllib.parse, urllib.error
import collections
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actEmbeddedG(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='EmbeddedG')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfoKeyExchange(self, param_csv):
        req = {}
        req['ClientPublicKey']='MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBbrA8fqLh0JFLjxcASfW7wjTUiEST+ps2OE68+ZY193rGABIV/MzQ/Y5zSHO8feN/1HMpVOHusTGtTH0FuXptrRUutyJywDS3G/la5+sdb8sBFxIOtl8pW5ZL4S3xAwNqCY1EfOnaaL6zaM1+8Vhg9uxRdGhbU9ZgjgT4k9ATcP6K68R1IuTE4COoI4CehDWUKpupFfQo3GQz/L+HQBRe1WwR/0DSpq8jGp8xZqhGEoxqZHRK8SBXXfyhvSul4x8e8J5+A/ECdA6kcnmXimNNrWP4iO8wFrAcapW5mJjdBuSgX/NlvBFYy/otZb9IQYkb1kQSUxuVLOdvFOXtex1jNAgMBAAE='

        req = json.dumps(req)
        print(req)

        return req

    def genOrderRequestInfoB2Bitem(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        Items1 = self.genArgsDictFromCSV(param_csv)
        Items2 = self.genArgsDictFromCSV(param_csv)
        req = {}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:20]
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ItemSeq')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemAmount')
        data.pop('ItemTax')
        data.pop('ItemRemark')

        rqHeader.pop('MerchantID')
        rqHeader.pop('ItemName')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('InvoiceTime')
        rqHeader.pop('ItemSeq')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('ClearanceMark')
        rqHeader.pop('InvType')
        rqHeader.pop('TaxType')
        rqHeader.pop('TaxRate')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('TaxAmount')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('InvoiceRemark')

        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('MerchantID')
        Items.pop('RelateNumber')
        Items.pop('InvoiceTime')
        Items.pop('CustomerIdentifier')
        Items.pop('CustomerEmail')
        Items.pop('ClearanceMark')
        Items.pop('InvType')
        Items.pop('TaxType')
        Items.pop('TaxRate')
        Items.pop('SalesAmount')
        Items.pop('TaxAmount')
        Items.pop('TotalAmount')
        Items.pop('InvoiceRemark')

        Items1.pop('Timestamp')
        Items1.pop('RqID')
        Items1.pop('Revision')
        Items1.pop('MerchantID')
        Items1.pop('RelateNumber')
        Items1.pop('InvoiceTime')
        Items1.pop('CustomerIdentifier')
        Items1.pop('CustomerEmail')
        Items1.pop('ClearanceMark')
        Items1.pop('InvType')
        Items1.pop('TaxType')
        Items1.pop('TaxRate')
        Items1.pop('SalesAmount')
        Items1.pop('TaxAmount')
        Items1.pop('TotalAmount')
        Items1.pop('InvoiceRemark')

        Items2.pop('Timestamp')
        Items2.pop('RqID')
        Items2.pop('Revision')
        Items2.pop('MerchantID')
        Items2.pop('RelateNumber')
        Items2.pop('InvoiceTime')
        Items2.pop('CustomerIdentifier')
        Items2.pop('CustomerEmail')
        Items2.pop('ClearanceMark')
        Items2.pop('InvType')
        Items2.pop('TaxType')
        Items2.pop('TaxRate')
        Items2.pop('SalesAmount')
        Items2.pop('TaxAmount')
        Items2.pop('TotalAmount')
        Items2.pop('InvoiceRemark')


        data['Items'] = [Items,Items1,Items2]

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
    def decryptDatab2bAppsdk(self, data,aes):
        #data = self.urlDecode(data)
        print(aes)
        aesdata={}
        aesdata=aes
        aes=json.loads(aes)

        print(aes['key'])
        print(aes['iv'])
        print(data)
        print(data)

        return self.aesDecryptforAPP(data,aes['key'],aes['iv'])

    def genOrderRequestInfoB2Bitem1(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        Items1 = self.genArgsDictFromCSV(param_csv)
        Items2 = self.genArgsDictFromCSV(param_csv)
        req = {}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:20]
        req['MerchantID'] = data['MerchantID']
        #req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ItemSeq')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemAmount')
        data.pop('ItemTax')
        data.pop('ItemRemark')

        rqHeader.pop('MerchantID')
        rqHeader.pop('ItemName')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('InvoiceTime')
        rqHeader.pop('ItemSeq')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('ClearanceMark')
        rqHeader.pop('InvType')
        rqHeader.pop('TaxType')
        rqHeader.pop('TaxRate')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('TaxAmount')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('InvoiceRemark')

        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('MerchantID')
        Items.pop('RelateNumber')
        Items.pop('InvoiceTime')
        Items.pop('CustomerIdentifier')
        Items.pop('CustomerEmail')
        Items.pop('ClearanceMark')
        Items.pop('InvType')
        Items.pop('TaxType')
        Items.pop('TaxRate')
        Items.pop('SalesAmount')
        Items.pop('TaxAmount')
        Items.pop('TotalAmount')
        Items.pop('InvoiceRemark')

        Items1.pop('Timestamp')
        Items1.pop('RqID')
        Items1.pop('Revision')
        Items1.pop('MerchantID')
        Items1.pop('RelateNumber')
        Items1.pop('InvoiceTime')
        Items1.pop('CustomerIdentifier')
        Items1.pop('CustomerEmail')
        Items1.pop('ClearanceMark')
        Items1.pop('InvType')
        Items1.pop('TaxType')
        Items1.pop('TaxRate')
        Items1.pop('SalesAmount')
        Items1.pop('TaxAmount')
        Items1.pop('TotalAmount')
        Items1.pop('InvoiceRemark')

        Items1['ItemSeq'] = '2'

        Items2.pop('Timestamp')
        Items2.pop('RqID')
        Items2.pop('Revision')
        Items2.pop('MerchantID')
        Items2.pop('RelateNumber')
        Items2.pop('InvoiceTime')
        Items2.pop('CustomerIdentifier')
        Items2.pop('CustomerEmail')
        Items2.pop('ClearanceMark')
        Items2.pop('InvType')
        Items2.pop('TaxType')
        Items2.pop('TaxRate')
        Items2.pop('SalesAmount')
        Items2.pop('TaxAmount')
        Items2.pop('TotalAmount')
        Items2.pop('InvoiceRemark')

        Items2['ItemSeq'] = '3'

        data['Items'] = [Items,Items1,Items2]

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
    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['Appsdk_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def strToDictAppsdk(self, res_info1):
        res_info = res_info1['content']
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

    def genPostRequestToAPIkeyexchange(self, req_info):
        form_act = self.feature_conf['Appsdk_API']
        print(req_info)
        #od_arg_dict = collections.OrderedDict(req_info.items)
        #print od_arg_dict
        UUID ='ae81566dc1e70479'
        AppName ='com.ecpay.appsdk'
        AppInfo ='{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        req = json.dumps(req_info)

        response = self.postRequestToAPIkeyexchange(self.genSession(), req_info, form_act, UUID,AppName,AppInfo,trencode_dotnet=True)
        self.log.INFO(response['content'].decode('utf-8'))
        return response

    def genPostRequestToAPIkeyexchangeLanguage(self, req_info):
        form_act = self.feature_conf['Appsdk_API']
        print(req_info)
        #od_arg_dict = collections.OrderedDict(req_info.items)
        #print od_arg_dict
        Language = 'zh-TW'
        UUID ='ae81566dc1e70479'
        AppName ='com.ecpay.appsdk'
        AppInfo ='{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        req = json.dumps(req_info)

        response = self.postRequestToAPIkeyexchange(self.genSession(), req_info, form_act, Language,UUID,AppName,AppInfo,trencode_dotnet=True)
        self.log.INFO(response['content'].decode('utf-8'))
        return response


    def strToDict(self, res_info1):
        res_info=res_info1['content']
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
        print('887987897')

        return res_dict

    def quote_item(self, res_dict, revert_list):
        for key in revert_list:
            res_dict[key] = urllib.parse.quote_plus(res_dict[key]).lower()
        return res_dict
    def decryptDatab2b(self, data,aes):
        #data = self.urlDecode(data)
        print(aes)
        aesdata={}
        aesdata=aes
        aes=json.loads(aes)
        print(aes['key'])
        print(aes['iv'])
        print(data)
        return self.aesDecryptforAPP(data,aes['key'],aes['iv'])

    def decryptDatapppsdk(self, data):
        #data = self.urlDecode(data)


        print(data['header'])
        res={}
        res=data['header']
        print(res)
        print(res['KeyInfo'])




        return self.rsaDecrpt(res['KeyInfo'])

    def decryptDatarsa(self, data):
        # data = self.urlDecode(data)

        print(data['header'])
        res = {}
        res = data['header']
        print(res)
        print(res['KeyInfo'])

        return self.rsaDecrpt(res['KeyInfo'])

    def decryptDatab2b2(self, data):
        #data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)



