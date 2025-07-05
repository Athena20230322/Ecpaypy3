#-*- coding: utf-8 -*-
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper

class verifyUpdateShipInfo(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'UpdateShipInfo'
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

    def verifyApiServing(self, response_value):
        result = {}
        expect_result = '0|敬愛的使用者您串接的API已停止服務，造成您的不便敬請見諒，若有任何問題請洽客服人員 TechSupport@allpay.com.tw 協助'
        if response_value == expect_result:
            result['verifyApiServing'] = True
        else:
            self.log.WARN("Api response error!\nexpect: %s\nresponse: %s" % (expect_result, response_value))
            result['verifyApiServing'] = False
        return result

    def verifyPrecondition(self, text):
        result = {}
        expect_result = '敬愛的使用者您串接的API已停止服務，造成您的不便敬請見諒，若有任何問題請洽客服人員 TechSupport@allpay.com.tw 協助'
        if text == expect_result:
            result['verifyPrecondition'] = True
        else:
            self.log.WARN("Api response error!\nexpect: %s\nresponse: %s" % (expect_result, text))
            result['verifyPrecondition'] = False
        return result
