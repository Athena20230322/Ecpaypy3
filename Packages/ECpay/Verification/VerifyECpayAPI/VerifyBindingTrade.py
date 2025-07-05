import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyBindingTrade(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'BindingTrade'
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

    def verifyColumns(self, res_dict, case_id):
        result = {}
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyColumns']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) != len(res_dict):
                    self.log.WARN('verifyColumns: column amounts not equal!\nexpect: %d\nresponse: %d' % (len(expect_args_dict), len(res_dict)))
                    result['VerifyColumnNumber'] = False
                    return result
                else:
                    result['VerifyColumnNumber'] = True
                for exp in expect_args_dict:
                    if exp in res_dict:
                        continue
                    else:
                        self.log.WARN('verifyColumns: column name %s not in res_dict!' % exp)
                        result['VerifyColumnName'] = False
                        return result
                return result
            else:
                raise ValueError("verifyColumns: Length of expected result dict cannot be zero.")
        else:
            raise TypeError("verifyColumns: Received expect_args_dict is not a dictionary.")

    def verifyResponseValues(self, res_dict, case_id, binding_info):
        result = {}
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyValues']
        expect_args_dict['MerchantTradeNo'] = binding_info['MerchantTradeNo']
        expect_args_dict['AllpayTradeNo'] = binding_info['AllpayTradeNo']
        expect_args_dict['MerchantMemberID'] = binding_info['MerchantMemberID']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyValues'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                return result
            else:
                raise ValueError("verifyResponseValues: Length of expected result dict cannot be zero.")
        else:
            raise TypeError("verifyResponseValues: Received expect_args_dict is not a dictionary.")
