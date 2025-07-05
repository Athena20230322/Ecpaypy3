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
        self.category = 'ECpayAPI'
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

    def verifyStatusResult(self, query_str, match_str):
        result = {}
        print(query_str)
        if query_str.find(match_str) != -1:
            result['verifyStatusResult'] = True
            return result
        else:
            self.log.WARN('verifyStatusResult: result is not match')
            result['verifyStatusResult'] = False
            return result

    def verifyprintFAMIC2COrderResult(self):
        op = self.webop
        tag_print = op.getElem('button', find_by='tag')
        result = {}
        print(tag_print.text)
        tag_str = tag_print.text
        if tag_str.find('列印') != -1:
            result['verifyprintFAMIC2COrderResult'] = True
            return result
        else:
            self.log.WARN("verifyprintFAMIC2COrderResult: result is not find '列印' button!")
            result['verifyprintFAMIC2COrderResult'] = False
            return result

    def verifyprintFAMIC2COrderDownload(self):
        op = self.webop
        tag_img = op.getElem('img', find_by='tag')
        result ={}
        print(tag_img.get_attribute('src'))
        tag_url = tag_img.get_attribute('src')
        if tag_url.find('https://logistics-stage.ecpay.com.tw/Upload/Logistics/') != -1:
            result['verifyprintFAMIC2COrderDownload'] = True
            return result
        else:
            self.log.WARN("verifyprintFAMIC2COrderDownload: result is not find img!")
            result['verifyprintFAMIC2COrderDownload'] = False
            return result
