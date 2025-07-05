#-*- coding:utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyReturnHiLifeCVS(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'ReturnHiLifeCVS'
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo',
                                                                feature_cat=self.category,
                                                                feature_name=self.fea_name)
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']        
        APIHelper.__init__(self, hash_key, hash_iv)
        self.hkey = hash_key
        self.hiv = hash_iv
        self.htm_helper = HtmlHelper()
        self.raw_sess = self.genSession()

    def enableWebOperate(self, webdrv):
        self.webop = WebOperate.webOperate(webdrv)

    def verifyReturnCVSResult(self):
        op =self.webop
        tag_body = op.getElem('body', find_by='tag')
        result = {}
        print(tag_body.text)
        tag_str = tag_body.text
        tag_str = tag_str.split('|')
        print(tag_str)
        if tag_str[0] and tag_str[1] != '':
            result['verifyReturnCVSResult'] = True
            return result
        else:
            self.log.WARN('verifyReturnCVSResult: result is not RtnMerchantTradeNo|RtnOrderNo!')
            result['verifyReturnCVSResult'] = False
            return result

    def verifyReturnCVSStrResult(self, query_str):
        result = {}
        query_str = query_str.split('|')
        print(query_str)
        if query_str[0] == '' \
                and query_str[1] == '敬愛的使用者您串接的API已停止服務，造成您的不便敬請見諒，若有任何問題請洽客服人員 TechSupport@allpay.com.tw 協助':
            result['verifyReturnCVSStrResult'] = True
            return result
        else:
            self.log.WARN('verifyReturnCVSResult: result is not RtnMerchantTradeNo|RtnOrderNo!')
            result['verifyReturnCVSStrResult'] = False
            return result
