import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyGetUserInfo(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'GetUserInfo'
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

    def verifyGetUserInfoReturn(self, query_order_dict, case_id):
        verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id, 'Verification.ini')
        if 'verifyGetUserInfo' in verify_data:
            expect_args_dict = verify_data['verifyGetUserInfo']
        else:
            raise ValueError("verifyGetUserInfoReturn: Secion 'verifyGetUserInfo' not found in Verification.ini")

        for key in query_order_dict:
            query_order_dict[key] = ''

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_order_dict) != 0:
                    result = {}
                    result['verifyGetUserInfoReturn'] = self.verifyRtnData(query_order_dict, expect_args_dict,
                                                                           datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyGetUserInfoReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyGetUserInfoReturn: Received expect_args_dict is not an dictionary")

    def verifyGetUserInfoFormat(self, query_order_dict, case_id):
        verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id, 'Verification.ini')
        if 'verifyGetUserInfoFormat' in verify_data:
            expect_args_dict = verify_data['verifyGetUserInfoFormat']
        else:
            raise ValueError("verifyGetUserInfoFormat: Secion 'verifyGetUserInfoFormat' not found in Verification.ini")

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_order_dict) != 0:
                    result = {}
                    result['verifyGetUserInfoFormat'] = self.verifyRtnData(query_order_dict, expect_args_dict,
                                                                           datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyGetUserInfoFormat: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyGetUserInfoFormat: Received expect_args_dict is not an dictionary")