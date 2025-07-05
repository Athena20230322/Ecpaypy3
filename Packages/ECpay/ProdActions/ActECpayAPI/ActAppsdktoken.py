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


class actAppsdktoken(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='APPSDKTOKEN')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)


    def genOrderRequestInfoTokenGet(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        OrderInfo = self.genArgsDictFromCSV(param_csv)
        ConsumerInfo = self.genArgsDictFromCSV(param_csv)
        req={}
        # if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
        #     data['RelateNumber'] = self.gen_uid(with_dash=False)[0:20]
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID']='3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('MerchantTradeNo')
        data.pop('MerchantTradeDate')
        data.pop('TotalAmount')
        # data.pop('TradeDesc')
        data.pop('Email')
        data.pop('Phone')
        data.pop('Name')
        data.pop('CountryCode')





        rqHeader.pop('MerchantID')
        rqHeader.pop('UseType')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('TotalAmount')
        # rqHeader.pop('TradeDesc')
        rqHeader.pop('Email')
        rqHeader.pop('Phone')
        rqHeader.pop('Name')
        rqHeader.pop('CountryCode')
        rqHeader.pop('AppStoreName')

        OrderInfo.pop('MerchantID')
        OrderInfo.pop('UseType')
        OrderInfo.pop('Timestamp')
        OrderInfo.pop('Revision')
        OrderInfo.pop('Email')
        OrderInfo.pop('Phone')
        OrderInfo.pop('Name')
        OrderInfo.pop('CountryCode')
        OrderInfo.pop('AppStoreName')

        ConsumerInfo.pop('MerchantID')
        ConsumerInfo.pop('Timestamp')
        ConsumerInfo.pop('Revision')
        ConsumerInfo.pop('MerchantTradeNo')
        ConsumerInfo.pop('MerchantTradeDate')
        ConsumerInfo.pop('TotalAmount')
        ConsumerInfo.pop('AppStoreName')





        data['OrderInfo'] = OrderInfo
        data['ConsumerInfo'] = ConsumerInfo
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

    def genOrderRequestInfoTokenQuery(self, param_csv,token):
        data = self.genArgsDictFromCSV(param_csv)
        print(token)
        data['Token']=token['Token']
        print(data['Token'])
        data = json.dumps(data)
        data = data.encode('utf-8')

        print(data)
        data = self.urlEncode(data)
        #print data
        data = self.aesEncrypt(data)
        #print data
        print(data)
        return data
    def genOrderRequestInfoB2B(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req={}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:20]
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID']='3083192'
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
        form_act = self.feature_conf['Appsdktoken_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genPostRequestToAPIkeyexchange(self, req_info):
        form_act = self.feature_conf['Appsdktoken_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        UUID ='ae81566dc1e70479'
        AppName ='com.ecpay.appsdk'
        AppInfo ='{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        response = self.postRequestToAPIkeyexchange(self.genSession(), od_arg_dict, form_act, UUID,AppName,AppInfo,trencode_dotnet=True)
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
    def decryptDatab2b(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def decryptDatab2b2(self, data):
        #data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)



