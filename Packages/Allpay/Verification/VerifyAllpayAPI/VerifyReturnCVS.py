import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyReturnCVS(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'ReturnCVS'
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
            result['verifyCreateAPCloseResult'] = True
            return result
        else:
            self.log.WARN("verifyCreateAPCloseResult: result in not find close_message!")
            result['verifyCreateAPCloseResult'] = False
            return result

    def verifyReturnCVSCloseResult(self):
        op = self.webop
        tag_body = op.getElem('body', find_by='tag')
        result = {}
        print(tag_body.text)
        tag_str = tag_body.text
        if tag_str.find("TechSupport@allpay.com.tw") != -1:
            result['verifyReturnCVSCloseResult'] = True
            return result
        else:
            self.log.WARN("verifyReturnCVSCloseResult: result in not find close_message!")
            result['verifyReturnCVSCloseResult'] = False
            return result