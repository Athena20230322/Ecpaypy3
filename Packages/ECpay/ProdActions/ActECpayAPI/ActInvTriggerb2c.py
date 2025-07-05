import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper


class actInvTriggerb2c(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvTriggerb2c')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
    #
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
        # data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def decryptDatab2c2(self, data):
        # data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)

    def genCheckMacValue(self, res_dict):
        chk = res_dict['CheckMacValue']
        res_dict.pop('CheckMacValue')
        chksum = self.genChkMacVal(res_dict, mode='local')
        print(chksum)
        res_dict['CheckMacValue'] = chk
        return chksum

    def genOrderRequestInfo(self, param_csv, delay_dict):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if type(delay_dict) is dict:
            if len(req['Tsr']) == 0:
                req['Tsr'] = delay_dict['OrderNumber']
        else:
            raise TypeError("ActGenOrderRequestInfo: Received delay_dict is not a dictionary.")
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestInfoB2c(self, param_csv,delay_dict):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        # if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
        #     data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        if type(delay_dict) is dict:
            if len(data['Tsr']) == 0:
                data['Tsr'] = delay_dict['Tsr']
        else:
            raise TypeError("ActGenOrderRequestInfo: Received delay_dict is not a dictionary.")
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'

        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemSeq')
        # data.pop('ItemName')
        # data.pop('ItemCount')
        # data.pop('ItemWord')
        # data.pop('ItemPrice')
        # data.pop('ItemTaxType')
        # data.pop('ItemAmount')
        # data.pop('InvType')
        # data.pop('DelayFlag')
        # data.pop('DelayDay')
        # data.pop('Tsr')
        # data.pop('PayType')
        # data.pop('PayAct')
        # data.pop('NotifyURL')

        rqHeader.pop('MerchantID')
        rqHeader.pop('Tsr')
        rqHeader.pop('PayType')
        # rqHeader.pop('CustomerID')
        # rqHeader.pop('CustomerIdentifier')
        # rqHeader.pop('CustomerName')
        # rqHeader.pop('CustomerAddr')
        # rqHeader.pop('CustomerPhone')
        # rqHeader.pop('CustomerEmail')
        # rqHeader.pop('ClearanceMark')
        # rqHeader.pop('Print')
        # rqHeader.pop('Donation')
        # rqHeader.pop('LoveCode')
        # rqHeader.pop('CarrierType')
        # rqHeader.pop('CarrierNum')
        # rqHeader.pop('TaxType')
        # rqHeader.pop('SalesAmount')
        # rqHeader.pop('InvoiceRemark')

        # rqHeader.pop('ItemSeq')

        # rqHeader.pop('ItemName')
        # rqHeader.pop('ItemCount')
        # rqHeader.pop('ItemWord')
        # rqHeader.pop('ItemPrice')
        # rqHeader.pop('ItemTaxType')
        # rqHeader.pop('ItemAmount')
        # rqHeader.pop('InvType')
        # rqHeader.pop('DelayFlag')
        # rqHeader.pop('DelayDay')
        # rqHeader.pop('Tsr')
        # rqHeader.pop('PayType')
        # rqHeader.pop('PayAct')
        # rqHeader.pop('NotifyURL')
        #
        # Items.pop('Timestamp')
        # Items.pop('RqID')
        # Items.pop('Revision')
        # Items.pop('PlatformID')
        # Items.pop('MerchantID')
        # Items.pop('RelateNumber')
        # Items.pop('CustomerID')
        # Items.pop('CustomerIdentifier')
        # Items.pop('CustomerName')
        # Items.pop('CustomerAddr')
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
        # Items.pop('DelayFlag')
        # Items.pop('DelayDay')
        # Items.pop('Tsr')
        # Items.pop('PayType')
        # Items.pop('PayAct')
        # Items.pop('NotifyURL')
        # Items.pop('InvType')
        # Items.pop('vat')
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

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvTriggerb2c_API']
        response = self.postRequestToAPIb2c(self.genSession(), req_info, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response
