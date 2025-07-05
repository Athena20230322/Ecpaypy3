import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyRemoveMemberInfo(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'RemoveMemberInfo'
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

    def verifyColumnNames(self, platform_data, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyColumnNames']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) != len(res_dict) + len(platform_data):
                    result['verifyColumnAmount'] = False
                else:
                    result['verifyColumnAmount'] = True
                    for key in res_dict:
                        if key in expect_args_dict:
                            result['verifyColumnName'] = True
                            continue
                        else:
                            self.log.WARN("verifyColumnName different!")
                            result['verifyColumnName'] = False
                            break
                    for key in platform_data:
                        if key in expect_args_dict:
                            result['verifyPlatformDataColName'] = True
                            continue
                        else:
                            self.log.WARN("verifyPlatformDataColName different!")
                            result['verifyPlatformDataColName'] = False
                            break
                return result
            else:
                raise ValueError("verifyColumnNames: Length of expected dict cannot be zero.")
        else:
            raise TypeError("verifyColumnNames: Received expect_args_dict is not a dictionary.")

    def verifyResponseValue(self, res_dict, platform_data, case_id, request_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyValues']
        print(expect_args_dict)
        result = {}
        expect_args_dict['ID'] = request_id
        res_dict.update(platform_data)
        print(res_dict)
        for key in expect_args_dict:
            expect_args_dict[key] = expect_args_dict[key].decode('utf-8')
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyReturnValues'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                return result
            else:
                raise ValueError("verifyResponseValue: Length of expected dict cannot be zero.")
        else:
            raise TypeError("verifyResponseValue: Received expect_args_dict is not a dictionary.")
