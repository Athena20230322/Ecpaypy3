import time
import json
import os
import collections
import urllib.request, urllib.parse, urllib.error
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actInvAllowanceInvalidb2b(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvAllowanceInvalidb2b')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfoB2B(self, param_csv,invoice_info,inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        #Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
       # data['Reason'] = 'Reason'

        data['AllowanceNo'] = invoice_info['AllowanceNo']
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID'] = '3083192'

       # data.pop('MerchantID')
        data.pop('Timestamp')
       # data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')


        rqHeader.pop('MerchantID')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('Reason')
        rqHeader.pop('Remark')
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

    def genOrderRequestInfoB2B(self, param_csv, invoice_info, inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        # Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
        # data['Reason'] = 'Reason'

        data['AllowanceNo'] = invoice_info['AllowanceNo']
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'

        # data.pop('MerchantID')
        data.pop('Timestamp')
        # data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('AllowanceNo')
        rqHeader.pop('Reason')
        rqHeader.pop('Remark')
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
        form_act = self.feature_conf['InvAllowanceInvalidb2b_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genCheckMacValue(self, req_info):
        rtn_chksum = req_info['CheckMacValue']
        req_info.pop('CheckMacValue')
        gen_result = {}
        chksum = self.genChkMacVal(req_info, mode='local')
        print(chksum)
        req_info['CheckMacValue'] = rtn_chksum
        gen_result['CheckMacValue'] = chksum
        return gen_result
