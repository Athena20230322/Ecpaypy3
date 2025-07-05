# -*- coding: utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyprintFAMIC2COrder(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'printFAMIC2COrder'
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

    def verifyApCreateCloseResult(self, create_res):
        print(type(create_res))
        result = {}
        if create_res.find("TechSupport@allpay.com.tw") != -1:
            result['verifyApCreateCloseResult'] = True
            return result
        else:
            self.log.WARN("verifyApCreateCloseResult: result is not find close_message!")
            result['verifyApCreateCloseResult'] = False
            return result

    def verifypriFAMIC2COrderCloseResult(self):
        op = self.webop
        tag_body = op.getElem('body', find_by='tag')
        result = {}
        print(tag_body.text)
        tag_str = tag_body.text
        if tag_str.find("TechSupport@allpay.com.tw") != -1:
            result['verifypriFAMIC2COrderCloseResult'] = True
            return result
        else:
            self.log.WARN("verifypriFAMIC2COrderCloseResult: result is not find close_message!")
            result['verifypriFAMIC2COrderCloseResult'] = False
            return result