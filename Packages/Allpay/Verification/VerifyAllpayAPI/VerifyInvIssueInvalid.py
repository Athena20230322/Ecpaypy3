import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyInvIssueInvalid(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'InvIssueInvalid'
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

    def verifyColumn(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        if 'verifyReturnColumn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyReturnColumn']
        else:
            raise ValueError("verifyInvDelayResult: Secion 'verifyReturnColumn' not found in Verification.ini")
        print((list(expect_args_dict.keys())))
        print((list(res_dict.keys())))
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) == len(res_dict):
                    result['verifyColumnNumber'] = True
                else:
                    raise ValueError(
                        "verifyInvIssueInvalidReturn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyInvIssueInvalidReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvIssueInvalidReturn: Received expect_args_dict is not a dictionary.")

    def verifyInvIssueInvalidResult(self, req_info, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyInvIssueInvalidResult' in all_verify_data:
            expect_args_dict = all_verify_data['verifyInvIssueInvalidResult']
            query_dict = self.returnBodyToDic(req_info)
        else:
            raise ValueError(
                "verifyInvIssueInvalidResult: Secion 'verifyInvIssueInvalidResult' not found in Verification.ini")

        expect_keys_list = ['InvoiceNumber', 'RtnCode', 'RtnMsg']
        temp_dict = {}
        for key in expect_keys_list:
            temp_dict[key] = query_dict[key]
            if key == 'InvoiceNumber':
                temp_dict[key] = query_dict[key]
                expect_args_dict[key] = query_dict[key]
        query_chksum = self.genChkMacVal(temp_dict, case='insensitive')
        query_dict['CheckMacValue'] = query_chksum
        expect_args_dict['CheckMacValue'] = query_chksum

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_dict) != 0:
                    if expect_args_dict['RtnCode'] == query_dict['RtnCode']:
                        result = {}
                        result['verifyInvIssueInvalidResult'] = self.verifyRtnData(query_dict, expect_args_dict, datatype='dictionary')
                        return result
                    else:
                        Error_result = 'Result: ' + req_info
                        self.log.WARN(Error_result)
                        raise ValueError("verifyInvIssueInvalidResult: RtnCode is not one.")
            else:
                raise ValueError("verifyInvIssueInvalidResult: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyInvIssueInvalidResult: Received expect_args_dict is not an dictionary.")
