import time
import json
import os

import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actCreate(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='Create')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv, mode='B2C'):
        req = self.genArgsDictFromCSV(param_csv)
        if mode == 'B2C':
            chksum = self.genChkMacVal(req, mode='local')
            print (chksum)
            req['CheckMacValue'] = chksum
        elif mode == 'C2C':
            hash_key = 'XBERn1YOvpM9nfZc'
            hash_iv = 'h1ONHk4P4yqbl5LK'
            APIHelper.__init__(self, hash_key, hash_iv)
            chksum = self.genChkMacVal(req, mode='local')
            print (chksum)
            req['CheckMacValue'] = chksum

        print((req['MerchantTradeNo']))
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info, api_url):
        op = self.webop
        form_act = self.feature_conf[api_url]
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print (form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def modifyAllpaylogisticsSplit(self, modify_str):
        print ('####test_modify_str####')
        print((modify_str.decode('utf-8')))
        print('123')
        modify_str_chek = modify_str
        modify_str_chek = modify_str_chek.split('|')
        if modify_str_chek[0] != '1':
            raise IndexError("modifyAllpaylogisticsSplit: Input str index[0] is not one")
        elif modify_str_chek[0] == '0':
            print ('TOFT3 Mode')
        if type(modify_str) is str:
            modify_str = modify_str.split('&')
            print ('####test_allpaylogistics####')
            # print modify_str
            print((modify_str[0][20:]))

            # return modify_str[0][20:]
            return self.returnBodyToDic(modify_str_chek[1])
        else:
            print ('####Type_Info####')

            print((type(modify_str)))
            print((TypeError("modifyAllpaylogisticsSplit: Paramter type is not a str")))
            return ''

    def GetInfoFromServerReplyUrl(self, allpaylogisticsid):
        serverReplyUrl = 'http://192.168.150.131:5000/?IdentCol=AllPayLogisticsID&IdentVal=' + allpaylogisticsid
        print(serverReplyUrl)
        response = requests.get(serverReplyUrl, headers={'Connection': 'close'})
        self.log.INFO("response msg: " + response.text)
        self.log.INFO("status code: " + str(response.status_code))
        return response

    def genOrderRequestCreateCVS(self, param_csv, merc_tno, merc_tdate, mode='B2C', TOFT3_Key='', TOFT3_Value=''):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req['MerchantTradeNo'] = merc_tno
        req['MerchantTradeDate'] = merc_tdate
        if mode == 'C2C':
            hash_key = 'XBERn1YOvpM9nfZc'
            hash_iv = 'h1ONHk4P4yqbl5LK'
            APIHelper.__init__(self, hash_key, hash_iv)
        if TOFT3_Key != '' and TOFT3_Value != '':
            req[TOFT3_Key] = TOFT3_Value
        chksum = self.genChkMacVal(req, mode='local')
        print (chksum)
        print (chksum)
        req['CheckMacValue'] = chksum
        #print req['ReceiverAddress']
        return req

    def genpostRequestToAPI(self, order_info_crt_res, api_url):
        query_order = self.postRequestToAPI(self.raw_sess, order_info_crt_res, api_url)
        return query_order
