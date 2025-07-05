# -*- coding: utf-8 -*-
import time
import json
import os
import urllib.request, urllib.parse, urllib.error
import collections
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate



class actInvOfflineIssue(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvOfflineIssue')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfoB2c(self, param_csv ,create ,inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req={}
        print('1235555')
        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]

        req['MerchantID'] = data['MerchantID']
        #req['PlatformID']='3083192'
        data.pop('Timestamp')
        #data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemTaxType')
        data.pop('ItemAmount')
        data.pop('ItemRemark')
        #data.pop('CustomerIdentifier')
       # data.pop('CustomerID')
       # data.pop('CustomerAddr')
       # data.pop('CustomerPhone')
        #data.pop('CustomerEmail')
       # data.pop('ClearanceMark')
        #data.pop('SpecialTaxType')
       # data.pop('vat')
       #data.pop('InvoiceRemark')
       # data.pop('CustomerName')
        #data.pop('Print')
        #data.pop('Donation')
        #data.pop('LoveCode')
        #data.pop('CarrierType')
        #data.pop('CarrierNum')





        rqHeader.pop('MerchantID')
        rqHeader.pop('MachineID')
        rqHeader.pop('InvoiceNo')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('TaxType')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('InvType')
        rqHeader.pop('RandomNumber')
        rqHeader.pop('ItemName')
        rqHeader.pop('ItemCount')
        rqHeader.pop('ItemWord')
        rqHeader.pop('ItemPrice')
        rqHeader.pop('ItemTaxType')
        rqHeader.pop('ItemAmount')
        rqHeader.pop('ItemRemark')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('CustomerID')
        rqHeader.pop('CustomerAddr')
        rqHeader.pop('CustomerPhone')
        rqHeader.pop('CustomerEmail')
        rqHeader.pop('ClearanceMark')
        #rqHeader.pop('SpecialTaxType')
        rqHeader.pop('vat')
        rqHeader.pop('InvoiceRemark')
        rqHeader.pop('CustomerName')
        rqHeader.pop('Print')
        rqHeader.pop('Donation')
        rqHeader.pop('LoveCode')
        rqHeader.pop('CarrierType')
        rqHeader.pop('CarrierNum')

        print('7766')
        print(create)
        dcreate=eval(create)
        print(dcreate)
        InvoiceInfo=dcreate['InvoiceInfo']
        InvoiceHeaderdict=InvoiceInfo[0]
        InvoiceNo=InvoiceHeaderdict['InvoiceNo']
        InvoiceHeader=InvoiceHeaderdict['InvoiceHeader']
        InvoiceNo=int(InvoiceNo)+1
        InvoiceNo=str(InvoiceNo)
        data['InvoiceNo']=InvoiceHeader+InvoiceNo
        #data['InvoiceNo'] = create["InvoiceNo"]
       # print data['InvoiceNo']

        print(data['InvoiceNo'])
        #= 'InvoiceNo'
       # print '7788'
        #data['InvoiceInfo'] = 'InvoiceNo'

        #print data['InvoiceInfo']

       # Items.pop('PlatformID')
        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('MerchantID')
        Items.pop('MachineID')
        Items.pop('InvoiceNo')
        Items.pop('InvoiceDate')
        Items.pop('RelateNumber')
        Items.pop('TaxType')
        Items.pop('SalesAmount')
        Items.pop('InvType')
        Items.pop('RandomNumber')
        Items.pop('CustomerIdentifier')
        Items.pop('CustomerID')
        Items.pop('CustomerAddr')
        Items.pop('CustomerPhone')
        Items.pop('CustomerEmail')
        Items.pop('ClearanceMark')
        #Items.pop('SpecialTaxType')
        Items.pop('vat')
        Items.pop('InvoiceRemark')
        Items.pop('CustomerName')
        Items.pop('Print')
        Items.pop('Donation')
        Items.pop('LoveCode')
        Items.pop('CarrierType')
        Items.pop('CarrierNum')





        data['Items'] = [Items]

        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')

        print(data)
        data = self.urlEncode(data)
        #print data
        data = self.aesEncrypt(data)
        #print data
        print(rqHeader)
        req['Data'] = data
        req['RqHeader'] = rqHeader
        print(req)
        return req

    def genOrderRequestInfoB2cS(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemTaxType')
        data.pop('ItemAmount')
        data.pop('ItemRemark')
        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('CustomerID')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('CustomerName')
        rqHeader.pop('CustomerAddr')
        rqHeader.pop('CustomerPhone')
        rqHeader.pop('CustomerEmail')
        rqHeader.pop('Print')
        rqHeader.pop('Donation')
        rqHeader.pop('LoveCode')
        rqHeader.pop('CarrierType')
        rqHeader.pop('CarrierNum')
        rqHeader.pop('TaxType')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('ClearanceMark')
        rqHeader.pop('InvoiceRemark')
        rqHeader.pop('InvType')
        rqHeader.pop('vat')
        rqHeader.pop('ItemName')
        rqHeader.pop('ItemCount')
        rqHeader.pop('ItemWord')
        rqHeader.pop('ItemPrice')
        rqHeader.pop('ItemTaxType')
        rqHeader.pop('ItemAmount')
        rqHeader.pop('ItemRemark')
        rqHeader.pop('SpecialTaxType')
        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('RelateNumber')
        Items.pop('PlatformID')
        Items.pop('MerchantID')
        Items.pop('CustomerID')
        Items.pop('CustomerIdentifier')
        Items.pop('CustomerName')
        Items.pop('CustomerAddr')
        Items.pop('CustomerPhone')
        Items.pop('CustomerEmail')
        Items.pop('ClearanceMark')
        Items.pop('Print')
        Items.pop('Donation')
        Items.pop('LoveCode')
        Items.pop('CarrierType')
        Items.pop('CarrierNum')
        Items.pop('TaxType')
        Items.pop('SalesAmount')
        Items.pop('InvoiceRemark')
        Items.pop('InvType')
        Items.pop('SpecialTaxType')
        Items.pop('vat')
        data['Items'] = [Items]

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

    def genOrderRequestInfoB2citem(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        Items1 = self.genArgsDictFromCSV(param_csv)
        Items2 = self.genArgsDictFromCSV(param_csv)
        req = {}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemTaxType')
        data.pop('ItemAmount')
        data.pop('ItemRemark')
        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('CustomerID')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('CustomerName')
        rqHeader.pop('CustomerAddr')
        rqHeader.pop('CustomerPhone')
        rqHeader.pop('CustomerEmail')
        rqHeader.pop('Print')
        rqHeader.pop('Donation')
        rqHeader.pop('LoveCode')
        rqHeader.pop('CarrierType')
        rqHeader.pop('CarrierNum')
        rqHeader.pop('TaxType')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('ClearanceMark')
        rqHeader.pop('InvoiceRemark')
        rqHeader.pop('InvType')
        rqHeader.pop('vat')
        rqHeader.pop('ItemName')
        rqHeader.pop('ItemCount')
        rqHeader.pop('ItemWord')
        rqHeader.pop('ItemPrice')
        rqHeader.pop('ItemTaxType')
        rqHeader.pop('ItemAmount')
        rqHeader.pop('ItemRemark')
        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('RelateNumber')
        Items.pop('PlatformID')
        Items.pop('MerchantID')
        Items.pop('CustomerID')
        Items.pop('CustomerIdentifier')
        Items.pop('CustomerName')
        Items.pop('CustomerAddr')
        Items.pop('CustomerPhone')
        Items.pop('CustomerEmail')
        Items.pop('ClearanceMark')
        Items.pop('Print')
        Items.pop('Donation')
        Items.pop('LoveCode')
        Items.pop('CarrierType')
        Items.pop('CarrierNum')
        Items.pop('TaxType')
        Items.pop('SalesAmount')
        Items.pop('InvoiceRemark')
        Items.pop('InvType')
        Items.pop('vat')

        Items1.pop('Timestamp')
        Items1.pop('RqID')
        Items1.pop('Revision')
        Items1.pop('RelateNumber')
        Items1.pop('PlatformID')
        Items1.pop('MerchantID')
        Items1.pop('CustomerID')
        Items1.pop('CustomerIdentifier')
        Items1.pop('CustomerName')
        Items1.pop('CustomerAddr')
        Items1.pop('CustomerPhone')
        Items1.pop('CustomerEmail')
        Items1.pop('ClearanceMark')
        Items1.pop('Print')
        Items1.pop('Donation')
        Items1.pop('LoveCode')
        Items1.pop('CarrierType')
        Items1.pop('CarrierNum')
        Items1.pop('TaxType')
        Items1.pop('SalesAmount')
        Items1.pop('InvoiceRemark')
        Items1.pop('InvType')
        Items1.pop('vat')

        Items2.pop('Timestamp')
        Items2.pop('RqID')
        Items2.pop('Revision')
        Items2.pop('RelateNumber')
        Items2.pop('PlatformID')
        Items2.pop('MerchantID')
        Items2.pop('CustomerID')
        Items2.pop('CustomerIdentifier')
        Items2.pop('CustomerName')
        Items2.pop('CustomerAddr')
        Items2.pop('CustomerPhone')
        Items2.pop('CustomerEmail')
        Items2.pop('ClearanceMark')
        Items2.pop('Print')
        Items2.pop('Donation')
        Items2.pop('LoveCode')
        Items2.pop('CarrierType')
        Items2.pop('CarrierNum')
        Items2.pop('TaxType')
        Items2.pop('SalesAmount')
        Items2.pop('InvoiceRemark')
        Items2.pop('InvType')
        Items2.pop('vat')
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

    def genOrderRequestInfoB2citem1(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        Items1 = self.genArgsDictFromCSV(param_csv)
        Items2 = self.genArgsDictFromCSV(param_csv)
        req = {}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemTaxType')
        data.pop('ItemAmount')
        data.pop('ItemRemark')
        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('CustomerID')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('CustomerName')
        rqHeader.pop('CustomerAddr')
        rqHeader.pop('CustomerPhone')
        rqHeader.pop('CustomerEmail')
        rqHeader.pop('Print')
        rqHeader.pop('Donation')
        rqHeader.pop('LoveCode')
        rqHeader.pop('CarrierType')
        rqHeader.pop('CarrierNum')
        rqHeader.pop('TaxType')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('ClearanceMark')
        rqHeader.pop('InvoiceRemark')
        rqHeader.pop('InvType')
        rqHeader.pop('vat')
        rqHeader.pop('ItemName')
        rqHeader.pop('ItemCount')
        rqHeader.pop('ItemWord')
        rqHeader.pop('ItemPrice')
        rqHeader.pop('ItemTaxType')
        rqHeader.pop('ItemAmount')
        rqHeader.pop('ItemRemark')
        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('RelateNumber')
        Items.pop('PlatformID')
        Items.pop('MerchantID')
        Items.pop('CustomerID')
        Items.pop('CustomerIdentifier')
        Items.pop('CustomerName')
        Items.pop('CustomerAddr')
        Items.pop('CustomerPhone')
        Items.pop('CustomerEmail')
        Items.pop('ClearanceMark')
        Items.pop('Print')
        Items.pop('Donation')
        Items.pop('LoveCode')
        Items.pop('CarrierType')
        Items.pop('CarrierNum')
        Items.pop('TaxType')
        Items.pop('SalesAmount')
        Items.pop('InvoiceRemark')
        Items.pop('InvType')
        Items.pop('vat')

        Items1.pop('Timestamp')
        Items1.pop('RqID')
        Items1.pop('Revision')
        Items1.pop('RelateNumber')
        Items1.pop('PlatformID')
        Items1.pop('MerchantID')
        Items1.pop('CustomerID')
        Items1.pop('CustomerIdentifier')
        Items1.pop('CustomerName')
        Items1.pop('CustomerAddr')
        Items1.pop('CustomerPhone')
        Items1.pop('CustomerEmail')
        Items1.pop('ClearanceMark')
        Items1.pop('Print')
        Items1.pop('Donation')
        Items1.pop('LoveCode')
        Items1.pop('CarrierType')
        Items1.pop('CarrierNum')
        Items1.pop('TaxType')
        Items1.pop('SalesAmount')
        Items1.pop('InvoiceRemark')
        Items1.pop('InvType')
        Items1.pop('vat')
        Items1['ItemTaxType']='3'

        Items2.pop('Timestamp')
        Items2.pop('RqID')
        Items2.pop('Revision')
        Items2.pop('RelateNumber')
        Items2.pop('PlatformID')
        Items2.pop('MerchantID')
        Items2.pop('CustomerID')
        Items2.pop('CustomerIdentifier')
        Items2.pop('CustomerName')
        Items2.pop('CustomerAddr')
        Items2.pop('CustomerPhone')
        Items2.pop('CustomerEmail')
        Items2.pop('ClearanceMark')
        Items2.pop('Print')
        Items2.pop('Donation')
        Items2.pop('LoveCode')
        Items2.pop('CarrierType')
        Items2.pop('CarrierNum')
        Items2.pop('TaxType')
        Items2.pop('SalesAmount')
        Items2.pop('InvoiceRemark')
        Items2.pop('InvType')
        Items2.pop('vat')
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
        form_act = self.feature_conf['InvIssueb2c_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genPostRequestToAPIOfflineIssue(self, req_info):
        form_act = self.feature_conf['InvOfflineIssueb2_API']
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

    def quote_item(self, res_dict, revert_list):
        for key in revert_list:
            res_dict[key] = urllib.parse.quote_plus(res_dict[key]).lower()
        return res_dict
    def decryptDatab2c(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def decryptDatab2c2(self, data):
        #data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)



