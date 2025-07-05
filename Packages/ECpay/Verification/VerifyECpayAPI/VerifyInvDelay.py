import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyInvDelay(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvDelay'
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

    def verifyStatusResult(self, res_info, match_str):
        result = {}
        if res_info.find(match_str) != -1:
            result['verifyStatusResult'] = True
            return result
        else:
            result['verifyStatusResult'] = False
            return result

    def verifyColumn(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        if 'verifyReturnColumn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyReturnColumn']
        else:
            raise ValueError("verifyColumn: Secion 'verifyReturnColumn' not found in Verification.ini")
        print((list(expect_args_dict.keys())))
        print((list(res_dict.keys())))
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) == len(res_dict):
                    result['verifyColumnNumber'] = True
                else:
                    raise ValueError("verifyColumn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyColumn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyColumn: Received expect_args_dict is not a dictionary.")

    def verifyInvDelayRequestInfo(self, req_info, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyInvDelayRequestInfo' in all_verify_data:
            expect_args_dict = all_verify_data['verifyInvDelayRequestInfo']
            query_dict = self.returnBodyToDic(req_info)
        else:
            raise ValueError(
                "verifyInvDelayRequestInfo: Secion 'verifyInvDelayRequestInfo' not found in Verification.ini")

        expect_keys_list = ['OrderNumber', 'RtnCode', 'RtnMsg']
        temp_dict = {}
        for key in expect_keys_list:
            temp_dict[key] = query_dict[key]
            if key == 'OrderNumber':
                expect_args_dict[key] = query_dict[key]
        query_chksum = self.genChkMacVal(temp_dict, case='insensitive')
        expect_args_dict['CheckMacValue'] = query_chksum

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_dict) != 0:
                    if expect_args_dict['RtnCode'] == query_dict['RtnCode']:
                        result = {}
                        result['verifyInvDelayRequestInfo'] = self.verifyRtnData(query_dict, expect_args_dict,
                                                                                 datatype='dictionary')
                        return result
                    else:
                        Error_result = 'Result: ' + req_info
                        self.log.WARN(Error_result)
                        raise ValueError("verifyInvDelayRequestInfo: RtnCode is not one.")
            else:
                raise ValueError("verifyInvDelayRequestInfo: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyInvDelayRequestInfo: Received expect_args_dict is not an dictionary.")
