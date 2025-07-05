import time
import json
import LibGeneral.funcGeneral as funcGen
import urllib.request, urllib.parse, urllib.error
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyInvQueryAllowanceInvalid(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'InvQueryAllowanceInvalid'
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

    def verifyQueryAllowInvalidResult(self, req_info, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyQueryAllowInvalidResult' in all_verify_data:
            expect_args_dict = all_verify_data['verifyQueryAllowInvalidResult']
        else:
            raise ValueError(
                "verifyQueryAllowInvalidResult: Secion 'verifyQueryAllowInvalidResult' not found in Verification.ini")

        req_info_dict = self.returnBodyToDic(req_info)

        for dictkey in req_info_dict:
            req_info_dict[dictkey] = ''

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(req_info_dict) != 0:
                    result = {}
                    result['verifyQueryAllowInvalidResult'] = self.verifyRtnData(req_info_dict, expect_args_dict,
                                                                                 datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyQueryAllowInvalidResult: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyQueryAllowInvalidResult: Received expect_args_dict is not an dictionary")

    def verifyQueryAllowInvalidRequestInfo(self, req_info):
        expect_args_dict = self.returnBodyToDic(req_info)
        exclusive_args = ['Reason', 'CheckMacValue']

        query_dict = {}
        for dictkey in expect_args_dict:
            query_dict[dictkey] = expect_args_dict[dictkey]
        for param in exclusive_args:
            query_dict.pop(param)
        query_chksum = self.genChkMacVal(query_dict)

        query_dict['CheckMacValue'] = query_chksum
        query_dict['Reason'] = expect_args_dict['Reason']

        print(expect_args_dict)

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) != 0:
                    if expect_args_dict['RtnCode'] is '1' and query_dict['CheckMacValue'] == expect_args_dict['CheckMacValue']:
                        result = {}
                        result['verifyInvQueryAllowanceRequestInfo'] = self.verifyRtnData(query_dict, expect_args_dict, datatype='dictionary')
                        return result
                    else:
                        Error_result = 'Result: ' + req_info
                        self.log.WARN(Error_result)
                        raise ValueError("verifyQueryAllowInvalidRequestInfo: RtnCode is not one or ReCheckMacValue is not match.")
            else:
                raise ValueError("verifyQueryAllowInvalidRequestInfo: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyQueryAllowInvalidRequestInfo: Received expect_args_dict is not an dictionary.")
