# coding: utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyBindingCardID(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'BindingCardID'
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

    def verifyClientRedirectColumns(self, res_dict, case_id):
        result = {}
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyClientRedirectColumns']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) != len(res_dict):
                    self.log.WARN(
                        'verifyClientRedirectColumns: column amounts not equal!\nexpect: %d\nredirect: %d'
                        % (len(expect_args_dict), len(res_dict)))
                    result['VerifyColumnNumber'] = False
                else:
                    result['VerifyColumnNumber'] = True
                for exp in expect_args_dict:
                    if exp in res_dict:
                        continue
                    else:
                        self.log.WARN('verifyClientRedirectColumns: column name %s not in res_dict!' % exp)
                        result['VerifyColumnName'] = False
                        break
                return result
            else:
                raise ValueError("verifyClientRedirectColumns: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyClientRedirectColumns: Received expect_args_dict is not a dictionary.")

    def verifyClientRedirectColumnsCheck(self, res_dict, case_id):
        result = {}
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        if 'verifyClientRedirectColumns' in all_verify_data:
            expect_args_dict = all_verify_data['verifyClientRedirectColumns']
        else:
            raise ValueError(
                "verifyClientRedirectColumnsCheck: Secion 'verifyClientRedirectColumns' not found in Verification.ini")
        insert_value_list = ['MerchantMemberID', 'CardID']
        print(res_dict)
        for key in insert_value_list:
            expect_args_dict[key] = res_dict[key]
        expect_args_dict.pop('CheckMacValue')
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyValues'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                return result
            else:
                raise ValueError("verifyResponseValues: Length of expected result dict cannot be zero.")
        else:
            raise TypeError("verifyResponseValues: Received expect_args_dict is not a dictionary.")