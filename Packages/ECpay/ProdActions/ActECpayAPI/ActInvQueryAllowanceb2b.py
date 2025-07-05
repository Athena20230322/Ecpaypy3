import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections
import requests


class actInvQueryAllowanceb2b(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvQueryAllowanceb2b')
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
        data['AllowanceNumber'] = invoice_info['AllowanceNumber']
        data['AllowanceNo'] = invoice_info['AllowanceNo']

        req['MerchantID'] = data['MerchantID']

        data.pop('MerchantID')
        data.pop('Timestamp')
       # data.pop('PlatformID')
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
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('AllowanceNumber')
        rqHeader.pop('AllowanceDate')
        rqHeader.pop('InvoiceCategory')
        rqHeader.pop('Seller_Identifier')
        rqHeader.pop('Buyer_Identifier')

        rqHeader.pop('AllowanceDateBegin')
        rqHeader.pop('AllowanceDateEnd')
        rqHeader.pop('AllowanceType')
        rqHeader.pop('Invalid_Status')
        rqHeader.pop('ExchangeMode')
        rqHeader.pop('ExchangeStatus')
        rqHeader.pop('Upload_Status')
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

    def genOrderRequestInfoB2B(self, param_csv, invoice_info,inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        req = {}
        mid =data['MerchantID']
        all=data['AllowanceNo']
        for key in data:
            if data[key] =='AUTO_INJECT_KEY':
                if data['AllowanceNo'] =='AUTO_INJECT_KEY':
                    data['AllowanceNo'] = inject_value
                    req['MerchantID'] = data['MerchantID']
                    break
                elif data['MerchantID'] =='AUTO_INJECT_KEY':

                    data['AllowanceNo'] = invoice_info['AllowanceNo']
                    req['MerchantID'] = inject_value
                    break
                else:
                    data[key] = inject_value
                    data['AllowanceNo'] = invoice_info['AllowanceNo']
                    req['MerchantID'] = data['MerchantID']
                    break

        if all !='AUTO_INJECT_KEY' and mid !='AUTO_INJECT_KEY':
            data['AllowanceNo'] = invoice_info['AllowanceNo']
            req['MerchantID'] = data['MerchantID']
        # for key in data:
        #     if data[key] == 'AUTO_INJECT_KEY':
        #         data[key] = inject_value
        #         break
        # data['AllowanceNumber'] = invoice_info['AllowanceNumber']
        # data['AllowanceNo'] = invoice_info['AllowanceNo']
        # req['MerchantID'] = data['MerchantID']

        data.pop('MerchantID')
        data.pop('Timestamp')

        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('AllowanceNo')


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
        form_act = self.feature_conf['InvQueryAllowanceb2b_API']
        print('BEFORE DO SORT:', req_info)
        od_arg_dict = collections.OrderedDict(sorted(req_info.items()))
        print('DID SORT:', od_arg_dict)
        query_order = self.postRequestToAPI(self.raw_sess, od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(query_order.decode('utf-8'))
        return query_order


    def genPostRequestToAPIb2b(self, req_info):
        form_act = self.feature_conf['InvQueryAllowanceb2b_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genPostGetStatusCode(self, req_info):
        form_act = self.feature_conf['InvQueryAllowanceb2b_API']
        print('BEFORE DO SORT:', req_info)
        od_arg_dict = collections.OrderedDict(sorted(req_info.items()))
        print('DID SORT:', od_arg_dict)
        response = requests.post(form_act, od_arg_dict)
        print(response.status_code)
        # response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO('response status_code: ' + str(response.status_code))
        return str(response.status_code)
