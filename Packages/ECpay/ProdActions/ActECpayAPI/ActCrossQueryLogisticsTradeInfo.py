import time
import json
import collections
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actCrossQueryLogisticsTradeInfo(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='CrossQueryLogisticsTradeInfo')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestInfoWithALID(self, param_csv, alid):
        req = self.genArgsDictFromCSV(param_csv)
        req['AllpayLogisticsID'] = alid
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info, api_url):
        op = self.webop
        form_act = self.feature_conf[api_url]
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def createOrderByRequest(self, req_info):
        pass

    def genOrderRequestCreateCVS(self, param_csv, merc_tno, merc_tdate, mode='B2C'):
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = merc_tno
        req['MerchantTradeDate'] = merc_tdate
        if mode == 'C2C':
            hash_key = 'XBERn1YOvpM9nfZc'
            hash_iv = 'h1ONHk4P4yqbl5LK'
            APIHelper.__init__(self, hash_key, hash_iv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genPostRequestToApi(self, order_info_res, api_url):
        form_actQueryLogisticsTradeInfo = self.feature_conf[api_url]
        query_order = self.postRequestToAPI(self.raw_sess, order_info_res, form_actQueryLogisticsTradeInfo)
        return query_order

    def modifyAllpaylogisticsSplit(self, modify_str, Split=False):
        print('####test_modify_str####')
        print(modify_str.decode('utf-8'))
        modify_str_chek = modify_str
        modify_str_chek = modify_str_chek.split('|')
        if modify_str_chek[0] != '1':
            raise IndexError("modifyAllpaylogisticsSplit: Input str index[0] is not one")
        if type(modify_str) is str:
            modify_str = modify_str.split('&')
            print('####test_allpaylogistics####')
            # print modify_str
            if Split:
                data = self.strToDict(modify_str_chek[1])
                print(data)
                return data
            else:
                print(modify_str[0][20:])
                return modify_str[0][20:]
        else:
            print('####Type_Info####')
            print(type(modify_str))
            print(TypeError("modifyAllpaylogisticsSplit: Paramter type is not a str"))
            return ''

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

    def strToDict11(self, res):
        res_list = res.split('&')
        res_dict = {}
        for item in res_list:
            res_dict[item.split('=')[0]] = item.split('=')[1]

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
    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['QueryLogisticsTradeInfo_API']

        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))

        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        print('789')
       # self.log.INFO(response.decode('utf-8'))
        print('1111')
        return response
    def decryptDatab2c(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))
