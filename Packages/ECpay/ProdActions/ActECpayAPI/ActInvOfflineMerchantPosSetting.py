import time
import json
import os
import collections
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate



class actInvOfflineMerchantPosSetting(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvOfflineMerchantPosSetting')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv, inv_info):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if len(req['RelateNumber']) == 0:
            req['RelateNumber'] = inv_info['RelateNumber']
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req
    def genOrderRequestInfoB2c(self, param_csv,invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)

        req = {}
        data['RelateNumber'] = invoice_info['RelateNumber']
       # data['AllowanceNo'] = invoice_info['IA_Allow_No']

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
        rqHeader.pop('RelateNumber')
        # rqHeader.pop('AllowanceNo')
        # rqHeader.pop('Reason')
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
        # data['AllowanceNo'] = invoice_info['IA_Allow_No']

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
        rqHeader.pop('RelateNumber')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNo')
        # rqHeader.pop('AllowanceNo')
        # rqHeader.pop('Reason')
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

    def genOrderRequestInfoB2cSAddWordSetting(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)

        req = {}

        req['MerchantID'] = data['MerchantID']

        data.pop('MerchantID')
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceYear')
        rqHeader.pop('InvoiceTerm')
        rqHeader.pop('UseStatus')
        rqHeader.pop('InvoiceCategory')
        rqHeader.pop('InvType')
        rqHeader.pop('InvoiceHeader')

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


    def genOrderRequestInfoB2cSWordSetting(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)

        req = {}

        req['MerchantID'] = data['MerchantID']

        data.pop('MerchantID')
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceYear')
        rqHeader.pop('InvoiceTerm')
        rqHeader.pop('UseStatus')
        rqHeader.pop('InvoiceCategory')
        rqHeader.pop('InvType')
        rqHeader.pop('InvoiceHeader')

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

    def genOrderRequestInfoInvOfflineMerchantPosSetting(self, param_csv ):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)

        req = {}

        req['MerchantID'] = data['MerchantID']

        #data.pop('MerchantID')
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('ActionType')
        rqHeader.pop('MachineID')
        rqHeader.pop('Remark')

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

    def genOrderRequestInfoB2cSOfflineWordSetting(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)

        req = {}

        req['MerchantID'] = data['MerchantID']

        data.pop('MerchantID')
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceYear')


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

    def genOrderRequestInfoB2c2(self, param_csv,invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
       #data['RelateNumber'] = invoice_info['RelateNumber']

        req = {}
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'

        data.pop('MerchantID')
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('RelateNumber')
        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')

        print(data)
        data = self.urlEncode(data)
        data = self.aesEncrypt(data)
        print(rqHeader)
        req['Data'] = data
        req['RqHeader'] = rqHeader
        print(req)
        return req
    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvQueryb2c_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response
    def genPostRequestToAPIWordSetting(self, req_info):
        form_act = self.feature_conf['InvQueryb2cWordSetting_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def createOrderByRequest(self, req_info):
        pass
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
        #print data
        return self.aesDecrypt(data)

