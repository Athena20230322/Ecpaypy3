import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections
import requests


class actInvQueryAllowanceb2c(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvQueryAllowanceb2c')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
    def genOrderRequestInfo(self, param_csv, invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)

        req = {}
        data['InvoiceNo'] = invoice_info['IA_Invoice_No']
        data['AllowanceNo'] = invoice_info['IA_Allow_No']

        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'

        data.pop('MerchantID')
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName')
        # data.pop('ItemCount')
        # data.pop('ItemWord')
        # data.pop('ItemPrice')
        # data.pop('ItemTaxType')
        # data.pop('ItemAmount')
        # data.pop('ItemSeq')
        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceNo')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('PlatformID')
        # rqHeader.pop('CustomerName')
        # rqHeader.pop('NotifyMail')
        # rqHeader.pop('NotifyPhone')
        # rqHeader.pop('AllowanceAmount')
        # rqHeader.pop('ItemSeq')
        # rqHeader.pop('ItemName')
        # rqHeader.pop('ItemCount')
        # rqHeader.pop('ItemWord')
        # rqHeader.pop('ItemPrice')
        # rqHeader.pop('ItemTaxType')
        # rqHeader.pop('ItemAmount')
        # rqHeader.pop('vat')
        # rqHeader.pop('ItemName')
        # rqHeader.pop('ItemCount')
        # rqHeader.pop('ItemWord')
        # rqHeader.pop('ItemPrice')
        # rqHeader.pop('ItemTaxType')
        # rqHeader.pop('ItemAmount')
        # rqHeader.pop('ItemRemark')

        # Items.pop('CustomerPhone')
        # Items.pop('CustomerEmail')
        # Items.pop('ClearanceMark')
        # Items.pop('Print')
        # Items.pop('Donation')
        # Items.pop('LoveCode')
        # Items.pop('CarrierType')
        # Items.pop('CarrierNum')
        # Items.pop('TaxType')
        # Items.pop('SalesAmount')
        # Items.pop('InvoiceRemark')
        # Items.pop('InvType')
        # Items.pop('vat')
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

    def genOrderRequestInfoB2c(self, param_csv, invoice_info,inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        req = {}
        inv =data['InvoiceNo']
        all=data['AllowanceNo']
        for key in data:
            if data[key] =='AUTO_INJECT_KEY':
                if data['InvoiceNo'] =='AUTO_INJECT_KEY':

                    data['InvoiceNo'] = inject_value
                    data['AllowanceNo'] = invoice_info['IA_Allow_No']
                    req['MerchantID'] = data['MerchantID']
                    break
                elif data['AllowanceNo'] =='AUTO_INJECT_KEY':

                    data['InvoiceNo'] = invoice_info['IA_Invoice_No']
                    data['AllowanceNo'] = inject_value
                    req['MerchantID'] = data['MerchantID']
                    break
                elif data['MerchantID'] =='AUTO_INJECT_KEY':

                    data['InvoiceNo'] = invoice_info['IA_Invoice_No']
                    data['AllowanceNo'] = invoice_info['IA_Allow_No']
                    req['MerchantID'] = inject_value
                    break
                else:
                    data[key] = inject_value
                    data['InvoiceNo'] = invoice_info['IA_Invoice_No']
                    data['AllowanceNo'] = invoice_info['IA_Allow_No']
                    req['MerchantID'] = data['MerchantID']
                    break
        if inv !='AUTO_INJECT_KEY' and all !='AUTO_INJECT_KEY' and data['MerchantID'] !='AUTO_INJECT_KEY':
            data['InvoiceNo'] = invoice_info['IA_Invoice_No']
            data['AllowanceNo'] = invoice_info['IA_Allow_No']
            req['MerchantID'] = data['MerchantID']

        req['PlatformID'] = '3083192'

        data.pop('MerchantID')
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName')
        # data.pop('ItemCount')
        # data.pop('ItemWord')
        # data.pop('ItemPrice')
        # data.pop('ItemTaxType')
        # data.pop('ItemAmount')
        # data.pop('ItemSeq')
        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceNo')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('PlatformID')
        # rqHeader.pop('CustomerName')
        # rqHeader.pop('NotifyMail')
        # rqHeader.pop('NotifyPhone')
        # rqHeader.pop('AllowanceAmount')
        # rqHeader.pop('ItemSeq')
        # rqHeader.pop('ItemName')
        # rqHeader.pop('ItemCount')
        # rqHeader.pop('ItemWord')
        # rqHeader.pop('ItemPrice')
        # rqHeader.pop('ItemTaxType')
        # rqHeader.pop('ItemAmount')
        # rqHeader.pop('vat')
        # rqHeader.pop('ItemName')
        # rqHeader.pop('ItemCount')
        # rqHeader.pop('ItemWord')
        # rqHeader.pop('ItemPrice')
        # rqHeader.pop('ItemTaxType')
        # rqHeader.pop('ItemAmount')
        # rqHeader.pop('ItemRemark')

        # Items.pop('CustomerPhone')
        # Items.pop('CustomerEmail')
        # Items.pop('ClearanceMark')
        # Items.pop('Print')
        # Items.pop('Donation')
        # Items.pop('LoveCode')
        # Items.pop('CarrierType')
        # Items.pop('CarrierNum')
        # Items.pop('TaxType')
        # Items.pop('SalesAmount')
        # Items.pop('InvoiceRemark')
        # Items.pop('InvType')
        # Items.pop('vat')
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
        form_act = self.feature_conf['InvQueryAllowanceb2c_API']
        print('BEFORE DO SORT:', req_info)
        od_arg_dict = collections.OrderedDict(sorted(req_info.items()))
        print('DID SORT:', od_arg_dict)
        query_order = self.postRequestToAPI(self.raw_sess, od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(query_order.decode('utf-8'))
        return query_order


    def genPostRequestToAPIb2c(self, req_info):
        form_act = self.feature_conf['InvQueryAllowanceb2c_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genPostGetStatusCode(self, req_info):
        form_act = self.feature_conf['InvQueryAllowanceb2c_API']
        print('BEFORE DO SORT:', req_info)
        od_arg_dict = collections.OrderedDict(sorted(req_info.items()))
        print('DID SORT:', od_arg_dict)
        response = requests.post(form_act, od_arg_dict)
        print(response.status_code)
        # response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO('response status_code: ' + str(response.status_code))
        return str(response.status_code)
