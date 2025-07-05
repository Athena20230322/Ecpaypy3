import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyInvIssueInvalidb2b(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvIssueInvalidb2b'
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

    def verifyColumn(self, case_id, res_dict):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnColumn']
        print((list(expect_args_dict.keys())))
        print((list(res_dict.keys())))
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) == len(res_dict):
                    result['verifyColumnNumber'] = True
                else:
                    raise ValueError("verifyInvIssueReturn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyInvIssueReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvIssueReturn: Received expect_args_dict is not a dictionary.")

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
        expect_args_list = ['RtnCode', 'RtnMsg', 'InvoiceNumber']
        temp_dict = {}
        for key in expect_args_list:
            temp_dict[key] = query_dict[key]
        query_chksum = self.genChkMacVal(temp_dict, case='insensitive')
        expect_args_dict['InvoiceNumber'] = query_dict['InvoiceNumber']
        expect_args_dict['CheckMacValue'] = query_chksum

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_dict) != 0:
                    if expect_args_dict['RtnCode'] == query_dict['RtnCode']:
                        result = {}
                        result['verifyInvIssueInvalidResult'] = self.verifyRtnData(query_dict, expect_args_dict,
                                                                                   datatype='dictionary')
                        return result
                    else:
                        Error_result = 'Result: ' + req_info
                        self.log.WARN(Error_result)
                        raise ValueError("verifyInvIssueInvalidResult: RtnCode is not one.")
            else:
                raise ValueError("verifyInvIssueInvalidResult: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyInvIssueInvalidResult: Received expect_args_dict is not an dictionary.")

    def verifyResponseValuesb2b(self, case_id, data, status='success'):
            all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                   'Verification.ini')
            expect_data = all_verify_data['verifyData']
            result = {}
            # for key in data.keys():
            #     if data[key] is not None:
            #         data[key] = data[key].encode('utf-8')
            #     else:
            #         data[key] = ''
            data['RtnCode'] = str(data['RtnCode'])

            data['RtnCode'] = data['RtnCode'].rstrip(' ')
            if type(expect_data) is dict:
                if len(expect_data) > 0:
                    result['VerifyDataValues'] = self.verifyRtnData(data, expect_data, datatype='dictionary')
                else:
                    raise ValueError("verifyResponseValues: Length of expect_data cannot be zero.")
            else:
                raise TypeError("verifyResponseValues: Received expect_data is not a dictionary.")
            is_empty_check_dict = {}
            is_empty_check_dict['RtnCode'] = data['RtnCode']

            if status == 'success':
                result['verifyNotEmptyValues'] = self.__valueIsEmpty(is_empty_check_dict)
            else:
                result['verifyMustEmptyValues'] = not self.__valueIsEmpty(is_empty_check_dict)
            return result

    def __valueIsEmpty(self, data):
        for key in list(data.keys()):
            if len(data[key]) > 0:
                pass
            else:
                return False
        return True


