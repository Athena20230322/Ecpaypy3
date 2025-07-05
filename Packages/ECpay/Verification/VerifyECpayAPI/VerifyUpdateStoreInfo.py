import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyUpdateStoreInfo(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'UpdateStoreInfo'
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

    def verifyRATResult(self, response_value):
        result = {}
        if len(response_value) > 0:
            print(response_value)
            result['verifyExistanceOfResult'] = True
        else:
            result['verifyExistanceOfResult'] = False
        return result

    def verifyUpdateStoreResult(self, response_value, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        print(all_verify_data)
        expect_args_dict = all_verify_data['verifyUpdateReturn']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if response_value == expect_args_dict['Result'].decode('utf-8'):
                    result['verifyUpdateStoreInfoResult'] = True
                    return result
                else:
                    print('return value is incorrect!')
                    print(response_value)
                    result['verifyUpdateStoreInfoResult'] = False
                    return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Recieved expect_args_dict is not an dictionary")