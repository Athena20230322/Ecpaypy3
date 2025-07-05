# -*- coding:utf-8 -*-
import urllib.request, urllib.parse, urllib.error
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyExpressMap(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'ExpressMap'
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat=self.category,
                                                                feature_name=self.fea_name)

        self.htm_helper = HtmlHelper()
        self.raw_sess = self.genSession()

    def verifyExpressFAMIMap(self, driver):
        op = WebOperate.webOperate(driver)
        verify_obj = op.getElem('TOP_', find_by='id')
        result = {}
        if verify_obj == False:
            #api is closed
            result['verifyExpressFAMIMap'] = True
            return result
        result['verifyExpressFAMIMap'] = False
        return result
