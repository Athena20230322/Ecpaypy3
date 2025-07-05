import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections
import requests


class actReturnHiLifeCVSV2(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='ReturnHiLifeCVSV2')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
    def genOrderRequestInfo(self, param_csv, inject_value=''):
        req = self.genArgsDictFromCSV(param_csv)
        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value
                break
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestInfoB2cCSV2(self, param_csv, inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        # Items = self.genArgsDictFromCSV(param_csv)
        req = {}

        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value
           #if data['LogisticsID'] == 'AUTO_GEN_RELATENO':
               # data['LogisticsID'] = self.gen_uid(with_dash=False)[0:30]
        # if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
        #     data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = ''
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('LogisticsID')
        rqHeader.pop('ServerReplyURL')
        rqHeader.pop('GoodsName')
        rqHeader.pop('GoodsAmount')
        rqHeader.pop('CollectionAmount')
        rqHeader.pop('ServiceType')
        rqHeader.pop('SenderName')
        rqHeader.pop('SenderPhone')
        rqHeader.pop('Remark')

        # data['Items'] = [Items]
       # data['LogisticsID'] = "1691"
        # data['LogisticsID'] = [create["LogisticsID"]]

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


    def genOrderRequestInfoB2c(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
       # Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        # if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
        #     data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID'] = ''
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('LogisticsID')
        rqHeader.pop('ServerReplyURL')
        rqHeader.pop('GoodsName')
        rqHeader.pop('GoodsAmount')
        rqHeader.pop('CollectionAmount')
        rqHeader.pop('ServiceType')
        rqHeader.pop('SenderName')
        rqHeader.pop('SenderPhone')
        rqHeader.pop('Remark')



        #data['Items'] = [Items]

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

    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_actCreateHiLifeTestData = self.feature_conf['CretHiLife_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_actCreateHiLifeTestData, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def genPostGetStatusCode(self, req_info):
        form_act = self.feature_conf['CretHiLife_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = requests.post(form_act, od_arg_dict)
        print(response.status_code)
        # response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO('response status_code: ' + str(response.status_code))
        return str(response.status_code)

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['CrossCre_API']

        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))

        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        print('789')
       # self.log.INFO(response.decode('utf-8'))
        print('1111')
        return response

    # def strToDict(self, res):
    #     res_list = res.split('&')
    #     res_dict = {}
        # for item in res_list:
        #     res_dict[item.split('=')[0]] = item.split('=')[1]
        # return res_dict

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
        res_dict = json.loads(res_info)
        print(res_dict)
        return res_dict
    def decryptDatab2c(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))
