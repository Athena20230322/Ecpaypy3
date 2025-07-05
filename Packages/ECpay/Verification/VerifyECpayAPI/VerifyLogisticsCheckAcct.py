import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyLogisticsCheckAcct(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'LogisticsCheckAcct'
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

    def verifyResponseExist(self, response):
        result = {}
        if response != '' or response != None:
            result['verifyRtnExist'] = True
        else:
            result['verifyRtnExist'] = False
        return result

    def verifyResponse(self, response, case_id):
        result = {}
        verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name,
                                                           case_id, 'Verification.ini')
        expect_args_dict = verify_data['verifyReturn']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if response == expect_args_dict['Return'].decode('UTF-8'):
                    result['verifyRtnVal'] = True
                else:
                    self.log.WARN('response: %s\nexpect: %s' % (response, expect_args_dict['Return'].decode('UTF-8')))
                    result['verifyRtnVal'] = False
                return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Recieved expect_args_dict is not an dictionary")
