import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections
import urllib.request, urllib.parse, urllib.error


class actInvNotifyb2b(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI',
                                                                feature_name='InvNotifyb2b')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv, request_dict, revert_args, inject_value=''):
        req = self.genArgsDictFromCSV(param_csv)

        for key in req:
            req[key] = req[key].encode('utf-8')

        if req['MerchantID'] == 'AUTO_INJECT_KEY':
            req['MerchantID'] = inject_value

        for res_dict_key in request_dict:
            if res_dict_key == 'IA_Invoice_No' or res_dict_key == 'InvoiceNumber':
                if req['InvoiceNo'] == 'AUTO_GEN_SKIP':
                    req['InvoiceNo'] = ''
                elif req['InvoiceNo'] == 'AUTO_INJECT_KEY':
                    req['InvoiceNo'] = inject_value
                else:
                    req['InvoiceNo'] = request_dict[res_dict_key]
            if res_dict_key == 'IA_Allow_No' or res_dict_key == 'AI_Allow_No':
                if req['AllowanceNo'] == 'AUTO_GEN_SKIP':
                    req['AllowanceNo'] = ''
                elif req['AllowanceNo'] == 'AUTO_INJECT_KEY':
                    req['AllowanceNo'] = inject_value
                else:
                    req['AllowanceNo'] = request_dict[res_dict_key]
        chksum = self.genChkMacVal(req, case='insensitive')
        print(chksum)

        for revert_key in revert_args:
            req[revert_key] = urllib.parse.unquote(req[revert_key])

        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestInfoB2B(self, param_csv,invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        #Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        data['InvoiceNumber'] = invoice_info['InvoiceNumber']
       # data['InvoiceDate'] = invoice_info['InvoiceDate']
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID'] = '3083192'

        data.pop('Timestamp')
        #data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        #data.pop('ItemName


        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')





       # data['Items'] = [Items]
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
    def genOrderRequestInfoB2B01(self, param_csv,invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
       # Items = self.genArgsDictFromCSV(param_csv)
        req = {}

        data['AllowanceNo'] = invoice_info['AllowanceNumber']
        req['MerchantID'] = data['MerchantID']
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')
      #  data['Items'] = [Items]
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

    def genOrderRequestInfoB2B0(self, param_csv, inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
        data['InvoiceNumber'] = inject_value['InvoiceNumber']
        req['MerchantID'] = data['MerchantID']
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')
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

    def genOrderRequestInfoB2B1(self, param_csv, invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        # Items = self.genArgsDictFromCSV(param_csv)
        req = {}

       # data['InvoiceNumber'] = invoice_info['InvoiceNumber']
        #data['InvoiceDate'] = invoice_info['InvoiceDate']

        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'

        data.pop('Timestamp')
        # data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')

        # data['Items'] = [Items]
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
    def genOrderRequestInfoB2B2(self, param_csv,invoice_info,inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
        data['AllowanceNo'] = invoice_info['AllowanceNo']
        data['InvoiceNumber'] = inject_value['InvoiceNumber']
       # data['InvoiceDate'] = invoice_info['InvoiceDate']
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID'] = '3083192'

        data.pop('Timestamp')
        #data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        #data.pop('ItemName')

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')




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

    def genOrderRequestInfoB2B21(self, param_csv, inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
        data['AllowanceNo'] = inject_value['AllowanceNo']
        #data['InvoiceNumber'] = inject_value['InvoiceNumber']
        # data['InvoiceDate'] = invoice_info['InvoiceDate']
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'

        data.pop('Timestamp')
        # data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName')

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')

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

    def genOrderRequestInfoB2B22(self, param_csv, invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        # Items = self.genArgsDictFromCSV(param_csv)
        req = {}
       # data['AllowanceNo'] = invoice_info['AllowanceNo']
        # data['InvoiceDate'] = invoice_info['InvoiceDate']
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'

        data.pop('Timestamp')
        # data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')

        # data['Items'] = [Items]
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

    def genOrderRequestInfoB2B3(self, param_csv, invoice_info,invoice_info1):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        # Items = self.genArgsDictFromCSV(param_csv)
        req = {}

        data['InvoiceNumber'] = invoice_info['InvoiceNumber']
        data['AllowanceNo'] = invoice_info1['AllowanceNo']
       # data['AllowanceNo'] = invoice_info['AllowanceNo']
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'

        data.pop('Timestamp')
        # data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName')

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')

        # data['Items'] = [Items]
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

    def genOrderRequestInfoB2B5(self, param_csv, invoice_info, inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        # Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
        data['InvoiceNumber'] = invoice_info['InvoiceNumber']
        # data['AllowanceNo'] = invoice_info['AllowanceNo']
        # data['InvoiceNo'] = invoice_info['InvoiceNo']
        # data['AllowanceNo'] = inject_value['AllowanceNo']
        # data['InvoiceDate'] = invoice_info['InvoiceDate']
        req['MerchantID'] = data['MerchantID']

        #req['PlatformID'] = '3083192'

        data.pop('Timestamp')
       # data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName')

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')
        # data['Items'] = [Items]
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
    def genOrderRequestInfoB2B6(self, param_csv, invoice_info, inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        # Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
       # data['InvoiceNo'] = invoice_info['InvoiceNo']
        data['AllowanceNo'] = invoice_info['AllowanceNo']
       # data['AllowanceNo'] = invoice_info['AllowanceNo']
        # data['AllowanceNo'] = invoice_info['AllowanceNo']
        # data['InvoiceNo'] = invoice_info['InvoiceNo']
        # data['AllowanceNo'] = inject_value['AllowanceNo']
        # data['InvoiceDate'] = invoice_info['InvoiceDate']
        req['MerchantID'] = data['MerchantID']
        #req['PlatformID'] = '3083192'

        data.pop('Timestamp')
       # data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName')

        rqHeader.pop('MerchantID')
        rqHeader.pop('InvoiceDate')
        rqHeader.pop('InvoiceNumber')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('NotifyMail')
        rqHeader.pop('InvoiceTag')
        rqHeader.pop('Notified')
        # data['Items'] = [Items]
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



    def genPostRequestToAPI(self, req_info, api_url='InvNotifyb2b_API'):
        form_act = self.feature_conf[api_url]
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    # def strToDict(self, res_info):
    #     res_dict = {}
    #     str_to_list = res_info.split('&')
    #     for item in str_to_list:
    #         tmp = item.split('=')
    #         res_dict[tmp[0]] = tmp[1]
    #     print res_dict
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

    def decryptDatab2b(self, data):
        # data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def decryptDatab2b2(self, data):
        # data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)

