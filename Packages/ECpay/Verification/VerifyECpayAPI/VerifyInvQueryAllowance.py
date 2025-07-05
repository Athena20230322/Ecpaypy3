import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import urllib.request, urllib.parse, urllib.error

class verifyInvQueryAllowance(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvQueryAllowance'
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

    def verifyInvQueryAllowanceResult(self, req_info, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyInvQueryAllowanceResult' in all_verify_data:
            expect_args_dict = all_verify_data['verifyInvQueryAllowanceResult']
        else:
            raise ValueError("verifyInvQueryAllowanceResult: Secion 'verifyInvQueryAllowanceResult' not found in Verification.ini")

        req_info_dict = self.returnBodyToDic(req_info)

        for dictkey in req_info_dict:
            req_info_dict[dictkey] = ''

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) == len(req_info_dict):
                result = {}
                result['verifyInvQueryAllowanceResult'] = self.verifyRtnData(req_info_dict, expect_args_dict, datatype='dictionary')
                return result
            else:
                raise ValueError("verifyInvQueryAllowanceResult: the amount of columns is not equal to the expected result.")
        else:
            raise TypeError("verifyInvQueryAllowanceResult: Recieved expect_args_dict is not an dictionary")

    def verifyInvQueryAllowanceRequestInfo(self, req_info):
        expect_args_dict = self.returnBodyToDic(req_info)
        exclusive_args = ['ItemName', 'ItemWord', 'CheckMacValue']

        query_dict = {}
        for dictkey in expect_args_dict:
            query_dict[dictkey] = expect_args_dict[dictkey]
        for param in exclusive_args:
            query_dict.pop(param)
        query_chksum = self.genChkMacVal(query_dict, case='insensitive')

        query_dict['CheckMacValue'] = query_chksum
        query_dict['ItemName'] = expect_args_dict['ItemName']
        query_dict['ItemWord'] = expect_args_dict['ItemWord']

        print('Query_dict: ', query_dict)

        print(expect_args_dict)

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if expect_args_dict['RtnCode'] is '1' and query_dict['CheckMacValue'] == expect_args_dict['CheckMacValue']:
                    result = {}
                    result['verifyInvQueryAllowanceRequestInfo'] = True
                    return result
                else:
                    Error_result = 'Result: ' + req_info
                    self.log.WARN(Error_result)
                    raise ValueError("verifyInvQueryAllowanceRequestInfo: RtnCode is not one or ReCheckMacValue is not match.")
            else:
                raise ValueError("verifyInvQueryAllowanceRequestInfo: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyInvQueryAllowanceRequestInfo: Recieved expect_args_dict is not an dictionary.")