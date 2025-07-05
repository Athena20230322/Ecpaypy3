import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyInvQueryChkMobBarCode(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvQueryChkMobBarCode'
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

    def verifyStatusResult(self, res_info, match_str):
        result = {}
        if res_info.find(match_str) != -1:
            result['verifyStatusResult'] = True
            return result
        else:
            result['verifyStatusResult'] = False
            return result

    def verifyColumn(self, res_dict, case_id):
        querymobbarcode_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                         'Verification.ini')
        if 'verifyReturnColumn' in querymobbarcode_verify_data:
            expect_args_dict = querymobbarcode_verify_data['verifyReturnColumn']
        else:
            raise ValueError("verifyInvDelayResult: Secion 'verifyReturnColumn' not found in Verification.ini")
        print((list(expect_args_dict.keys())))
        print((list(res_dict.keys())))
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) == len(res_dict):
                    result['verifyColumnAmount'] = True
                else:
                    result['verifyColumnAmount'] = False
                    raise ValueError("verifyInvQueryChkMobBarCodeReturn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyInvQueryChkMobBarCodeReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvQueryChkMobBarCodeReturn: Received expect_args_dict is not a dictionary.")

    def verifyInvQueryChkMobBarCodeRequestInfo(self, req_info, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                         'Verification.ini')
        if 'verifyReturnColumn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyReturnColumn']
        else:
            raise ValueError("verifyInvDelayResult: Secion 'verifyReturnColumn' not found in Verification.ini")
        query_dict = {}
        query_dict['RtnCode'] = req_info['RtnCode']
        query_dict['RtnMsg'] = req_info['RtnMsg']
        query_dict['IsExist'] = req_info['IsExist']
        query_chksum = self.genChkMacVal(query_dict)
        expect_args_dict['CheckMacValue'] = query_chksum

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_dict) != 0:
                    if req_info['RtnCode'] == '1':
                        result = {}
                        result['verifyInvQueryChkMobBarCodeRequestInfo'] = self.verifyRtnData(req_info, expect_args_dict, datatype='dictionary')
                        return result
                    else:
                        Error_result = 'Result: ' + req_info
                        self.log.WARN(Error_result)
                        raise ValueError("verifyInvQueryChkMobBarCodeRequestInfo: RtnCode is not one.")
            else:
                raise ValueError("verifyInvQueryChkMobBarCodeRequestInfo: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyInvQueryChkMobBarCodeRequestInfo: Recieved expect_args_dict is not an dictionary.")