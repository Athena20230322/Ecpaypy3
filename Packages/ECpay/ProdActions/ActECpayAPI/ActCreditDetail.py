import time
import json
import os
import dicttoxml
import xmltodict
import re
import collections
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actCreditDetail(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='CreditDetail')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['MerchantID'] = data['MerchantID']
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        rqHeader.pop('MerchantID')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('PlatformID')
        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')
        print(data)
        data = self.urlEncode(data)
        print(data)
        data = self.aesEncrypt(data)
        print(data)
        req['Data'] = data
        req['RqHeader'] = rqHeader
        return req
    def getBarcode(self, payment_type):
        get_dict = {}
        if payment_type == 1:
            get_dict['paymenttype'] = '1'
        elif payment_type == 3:
            get_dict['paymenttype'] = '3'
        elif payment_type == 4:
            get_dict['paymenttype'] = '4'
        response = self.getRequestFromAPI(get_dict, 'https://cvs-stage.opay.tw/PaymentRule/Mobile/MockGetBarCode')
        m = re.search('AP\d{3}[A-Z]{1}\d{1}\w{11}', response)
        if m:
            found = m.group()
            return found
        else:
            raise Exception('Barcode not found from https://cvs-stage.opay.tw/PaymentRule/Mobile/MockGetBarCode')

    def createOrderByRequest(self, req_info):
        form_act = self.feature_conf['QueryTrade_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def createOrderByRequestThreeD(self, req_info):
        form_act = self.feature_conf['QueryTrade_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        #od_arg_dict = json.dumps(od_arg_dict)
        response = self.postRequestToAPIThreeD(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
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
    def strToDict3D(self, res_info):
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

    def decryptData(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))
    def decryptData3D(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def ThreeURL(self, data):
        # data = self.urlDecode(data)
        data['ThreeDURL'] = str(data['ThreeDURL'])
        threeD=data['ThreeDURL']
        print(threeD)
        return threeD

    def ActthreeDVerify(self, threed):
        op=self.webop
        op.goToURL(threed)
        time.sleep(5)
        op.clickElem('Send')
        time.sleep(7)
    def GetInfoFromClientRedirectUrl(self):
        op = self.webop
        divText = op.drv.find_element_by_tag_name('body').text
        #divText=json.dumps(divText)
        divText = divText.encode('utf-8')
        divText=divText.replace("ResultData:","")
        self.log.INFO(divText)
        return divText
    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['QueryTrade_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        #od_arg_dict = json.dumps(od_arg_dict)
        response = self.postRequestToAPIThreeD(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response
