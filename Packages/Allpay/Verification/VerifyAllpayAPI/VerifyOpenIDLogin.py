import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyOpenIDLogin(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'OpenIDLogin'
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

    def verifyColumnNames(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyColumnNames']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) != len(res_dict):
                    result['verifyColumnAmount'] = False
                else:
                    result['verifyColumnAmount'] = True
                    for key in expect_args_dict:
                        if key in expect_args_dict:
                            result['verifyColumnName'] = True
                            continue
                        else:
                            self.log.WARN("verifyColumnName different!")
                            result['verifyColumnName'] = False
                            break
                return result
            else:
                raise ValueError("verifyColumnNames: Length of expected dict cannot be zero.")
        else:
            raise TypeError("verifyColumnNames: Received expect_args_dict is not a dictionary.")

    def verifyResponseValue(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyValues']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyReturnValues'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if res_dict['Token'] != '':
                    result['verifyToken'] = True
                else:
                    result['verifyToken'] = False
                if res_dict['TimeStamp'] != '':
                    result['verifyTimeStamp'] = True
                else:
                    result['verifyTimeStamp'] = False
                return result
            else:
                raise ValueError("verifyResponseValue: Length of expected dict cannot be zero.")
        else:
            raise TypeError("verifyResponseValues: Received expect_args_dict is not a dictionary.")
