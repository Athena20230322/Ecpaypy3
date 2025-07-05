import time
import json
import os
import collections
import urllib.request, urllib.parse, urllib.error
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actInvAllowanceByCollegiateb2c(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvAllowanceByCollegiateb2c')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
    def genOrderRequestInfo(self, param_csv, invoice_info, exclusive_params, revert_params):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        for key in req:
            req[key] = req[key].encode('utf-8')
        if invoice_info['InvoiceNumber'] is not False:
            req['InvoiceNo'] = invoice_info['InvoiceNumber']
        else:
            raise ValueError("precondition doesn't response InvoiceNumber!")
        exclusive_ele = {}
        for param in exclusive_params:
            exclusive_ele[param] = req[param]
            req.pop(param)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        for param in exclusive_params:
            req[param] = exclusive_ele[param]
        for param in revert_params:
            req[param] = urllib.parse.unquote_plus(req[param])
        print(req)
        return req

    def genOrderRequestInfoB2c(self, param_csv,invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        data['InvoiceNo']=invoice_info['InvoiceNo']
        data['InvoiceDate'] = invoice_info['InvoiceDate']
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
        data.pop('ItemSeq')


        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('InvoiceNo')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('AllowanceNotify')
        rqHeader.pop('CustomerName')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('NotifyPhone')
        rqHeader.pop('AllowanceAmount')
        rqHeader.pop('ItemSeq')
        rqHeader.pop('ItemName')
        rqHeader.pop('ItemCount')
        rqHeader.pop('ItemWord')
        rqHeader.pop('ItemPrice')
        rqHeader.pop('ItemTaxType')
        rqHeader.pop('ItemAmount')
        #rqHeader.pop('vat')
        #rqHeader.pop('ItemName')
        #rqHeader.pop('ItemCount')
        #rqHeader.pop('ItemWord')
        #rqHeader.pop('ItemPrice')
        #rqHeader.pop('ItemTaxType')
        #rqHeader.pop('ItemAmount')
        #rqHeader.pop('ItemRemark')


        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('MerchantID')
        Items.pop('InvoiceNo')
        Items.pop('InvoiceDate')
        Items.pop('AllowanceNotify')
        Items.pop('CustomerName')
        Items.pop('NotifyMail')
        Items.pop('NotifyPhone')
        Items.pop('AllowanceAmount')
       # Items.pop('CustomerPhone')
        #Items.pop('CustomerEmail')
        #Items.pop('ClearanceMark')
        #Items.pop('Print')
        #Items.pop('Donation')
        #Items.pop('LoveCode')
        #Items.pop('CarrierType')
        #Items.pop('CarrierNum')
        #Items.pop('TaxType')
        #Items.pop('SalesAmount')
        #Items.pop('InvoiceRemark')
        #Items.pop('InvType')
        #Items.pop('vat')
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

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvAllowanceByCollegiateb2c_API']
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

    def decryptDatab2c(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))