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




class actInvDelayb2c(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvDelayb2c')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv, revert_args, exclusive_args):
        req = self.genArgsDictFromCSV(param_csv)
        print(repr(req))

        if req['RelateNumber'] == 'AUTO_GEN_RELATENO':
            req['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]

        if req['Tsr'] == 'AUTO_GEN_TSR':
            req['Tsr'] = self.gen_uid(with_dash=False)[0:30]

        for key in req:
            req[key] = req[key].encode('utf-8')

        exclusive_dict = {}
        for param in exclusive_args:
            exclusive_dict[param] = req[param]
            req.pop(param)

        chksum = self.genChkMacVal(req, case='insensitive')
        print(chksum)

        for param in exclusive_args:
            req[param] = exclusive_dict[param]

        for revert_key in revert_args:
            req[revert_key] = urllib.parse.unquote(req[revert_key])

        req['CheckMacValue'] = chksum
        return req
    def genOrderRequestInfoB2c(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req={}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        req['MerchantID'] = data['MerchantID']
        req['PlatformID']='3083192'

        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        #data.pop('ItemSeq')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemTaxType')
        data.pop('ItemAmount')
        # data.pop('InvType')
        # data.pop('DelayFlag')
        # data.pop('DelayDay')
        # data.pop('Tsr')
        # data.pop('PayType')
        # data.pop('PayAct')
        # data.pop('NotifyURL')

        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('CustomerID')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('CustomerName')
        rqHeader.pop('CustomerAddr')
        rqHeader.pop('CustomerPhone')
        rqHeader.pop('CustomerEmail')
        rqHeader.pop('ClearanceMark')
        rqHeader.pop('Print')
        rqHeader.pop('Donation')
        rqHeader.pop('LoveCode')
        rqHeader.pop('CarrierType')
        rqHeader.pop('CarrierNum')
        rqHeader.pop('TaxType')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('InvoiceRemark')



        #rqHeader.pop('ItemSeq')

        rqHeader.pop('ItemName')
        rqHeader.pop('ItemCount')
        rqHeader.pop('ItemWord')
        rqHeader.pop('ItemPrice')
        rqHeader.pop('ItemTaxType')
        rqHeader.pop('ItemAmount')
        rqHeader.pop('InvType')
        rqHeader.pop('DelayFlag')
        rqHeader.pop('DelayDay')
        rqHeader.pop('Tsr')
        rqHeader.pop('PayType')
        rqHeader.pop('PayAct')
        rqHeader.pop('NotifyURL')


        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('PlatformID')
        Items.pop('MerchantID')
        Items.pop('RelateNumber')
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
        Items.pop('DelayFlag')
        Items.pop('DelayDay')
        Items.pop('Tsr')
        Items.pop('PayType')
        Items.pop('PayAct')
        Items.pop('NotifyURL')
        #Items.pop('InvType')
       # Items.pop('vat')
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

    def genOrderRequestInfoB2citem(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        Items1 = self.genArgsDictFromCSV(param_csv)
        Items2 = self.genArgsDictFromCSV(param_csv)
        req = {}
        if data['Tsr'] == 'AUTO_GEN_TSR':
            data['Tsr'] = self.gen_uid(with_dash=False)[0:30]
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
       # data.pop('ItemRemark')
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
        #rqHeader.pop('vat')
        rqHeader.pop('ItemName')
        rqHeader.pop('ItemCount')
        rqHeader.pop('ItemWord')
        rqHeader.pop('ItemPrice')
        rqHeader.pop('ItemTaxType')
        rqHeader.pop('ItemAmount')
        #rqHeader.pop('ItemRemark')
        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('PlatformID')
        Items.pop('MerchantID')
        Items.pop('RelateNumber')
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
        Items.pop('DelayFlag')
        Items.pop('DelayDay')
        Items.pop('Tsr')
        Items.pop('PayType')
        Items.pop('PayAct')
        Items.pop('NotifyURL')


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
        Items1.pop('DelayFlag')
        Items1.pop('DelayDay')
        Items1.pop('Tsr')
        Items1.pop('PayType')
        Items1.pop('PayAct')
        Items1.pop('NotifyURL')
        Items1['ItemTaxType'] = '1'



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
        Items2.pop('DelayFlag')
        Items2.pop('DelayDay')
        Items2.pop('Tsr')
        Items2.pop('PayType')
        Items2.pop('PayAct')
        Items2.pop('NotifyURL')
        data['Items'] = [Items, Items1, Items2]

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
        #rqHeader.pop('vat')
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
        Items1['ItemTaxType'] = '1'

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
        data['Items'] = [Items, Items1, Items2]

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
    def genOrderRequestInfoB2citemS(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        Items1 = self.genArgsDictFromCSV(param_csv)
        Items2 = self.genArgsDictFromCSV(param_csv)
        req = {}
        if data['Tsr'] == 'AUTO_GEN_TSR':
            data['Tsr'] = self.gen_uid(with_dash=False)[0:30]
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
       # data.pop('ItemRemark')
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
        #rqHeader.pop('vat')
        rqHeader.pop('ItemName')
        rqHeader.pop('ItemCount')
        rqHeader.pop('ItemWord')
        rqHeader.pop('ItemPrice')
        rqHeader.pop('ItemTaxType')
        rqHeader.pop('ItemAmount')
        rqHeader.pop('SpecialTaxType')
        #rqHeader.pop('ItemRemark')
        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('PlatformID')
        Items.pop('MerchantID')
        Items.pop('RelateNumber')
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
        Items.pop('DelayFlag')
        Items.pop('DelayDay')
        Items.pop('Tsr')
        Items.pop('PayType')
        Items.pop('PayAct')
        Items.pop('NotifyURL')
        Items.pop('SpecialTaxType')


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
        Items1.pop('DelayFlag')
        Items1.pop('DelayDay')
        Items1.pop('Tsr')
        Items1.pop('PayType')
        Items1.pop('PayAct')
        Items1.pop('NotifyURL')
        Items1['ItemTaxType'] = '1'
        Items1.pop('SpecialTaxType')



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
        Items2.pop('DelayFlag')
        Items2.pop('DelayDay')
        Items2.pop('Tsr')
        Items2.pop('PayType')
        Items2.pop('PayAct')
        Items2.pop('NotifyURL')
        Items2.pop('SpecialTaxType')
        data['Items'] = [Items, Items1, Items2]

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
        form_act = self.feature_conf['InvDelayb2c_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    # def strToDict(self, res):
    #     res_list = res.split('&')
    #     res_dict = {}
    #     for item in res_list:
    #         res_dict[item.split('=')[0]] = item.split('=')[1]
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
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def decryptDatab2c2(self, data):
        #data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)



