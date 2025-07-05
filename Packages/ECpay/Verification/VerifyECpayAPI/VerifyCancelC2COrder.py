# -*- coding: utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyCancelC2COrder(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'CancelC2COrder'
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

    def verifyStatusResult(self, match_str):
        op = self.webop
        tag_body = op.getElem('body', find_by='tag')
        result = {}
        print(tag_body.text)
        tag_str = tag_body.text
        if tag_str.find(match_str) != -1:
            result['verifyStatusResult'] = True
            return result
        else:
            result['verifyStatusResult'] = False
            return result

    def verifyCancelC2COrderResult(self):
        op = self.webop
        tag_body = op.getElem('body', find_by='tag')
        result = {}
        print(tag_body.text)
        tag_str = tag_body.text
        if tag_str.find('1|OK') != -1:
            result['verifyCancelC2COrderResult'] = True
            return result
        else:
            self.log.WARN("verifyCancelC2COrderResult: result is not 1|OK!")
            result['verifyCancelC2COrderResult'] = False
            return result
