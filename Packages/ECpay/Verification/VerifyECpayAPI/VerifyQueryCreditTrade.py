# -*- coding: utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyQueryCreditTrade(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'QueryCreditTrade'
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

    def verifyResponseColumnName(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyPaymentReturn']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = {}
                expect_list = sorted(expect_args_dict.keys())
                print(('expect_list: ' + str(len(expect_list))))
                print(('res_dict: ' + str(len(res_dict))))
                if len(expect_list) != len(res_dict):
                    result['VerifyReturnKey'] = False
                    return result
                for exp in expect_list:
                    if exp in res_dict:
                        continue
                    else:
                        result['VerifyReturnKey'] = False
                        return result
                result['VerifyReturnKey'] = True
                return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Received expect_args_dict is not a dictionary.")

    def verifyQueryInfo(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                                self.fea_name,
                                                                case_id,
                                                                'Verification.ini')
        for key in res_dict:
            if type(res_dict[key]) is int:
                res_dict[key] = str(res_dict[key])
        expect_args_dict = all_verify_data['verifyPaymentReturn']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = {}
                result['VerifyQueryInfo'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if res_dict['process_date'] != '' and res_dict['process_date'] != None:
                    if res_dict['TotalSuccessTimes'] != str(len(res_dict['ExecLog'])):
                        result['VerifyTotalSuccessTimes'] = False
                    else:
                        result['VerifyTotalSuccessTimes'] = True
                    rtnCode = 1
                    if res_dict['ExecLog'] is not None:
                        for i in range(len(res_dict['ExecLog'])):
                            if res_dict['ExecLog'][i]['RtnCode'] != 1:
                                result['VerifyExecLogRtnCode'] = False
                                rtnCode = res_dict['ExecLog'][i]['RtnCode']
                                break
                    else:
                        return result
                    if rtnCode == 1:
                        result['VerifyExecLogRtnCode'] = True
                    return result
                else:

                    return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Received expect_args_dict is not an dictionary")

    def verifyQueryInfo1(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        for key in res_dict:
            if type(res_dict[key]) is int:
                res_dict[key] = str(res_dict[key])
        expect_args_dict = all_verify_data['verifyPaymentReturn']
        print(expect_args_dict)
        process_date = res_dict['ExecLog']
        process_date2 = process_date[1]
        print('123')
        print(process_date2['process_date'])
        print('123')
        if type(expect_args_dict) is dict and process_date2['process_date']=='2021/01/13 16:16:37':
            if len(expect_args_dict) > 0:
                result = {}
                result['VerifyQueryInfo'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if res_dict['process_date'] != '' and res_dict['process_date'] != None:
                    if res_dict['TotalSuccessTimes'] != str(len(res_dict['ExecLog'])):
                        result['VerifyTotalSuccessTimes'] = False
                    else:
                        result['VerifyTotalSuccessTimes'] = True
                    rtnCode = 1
                    if res_dict['ExecLog'] is not None:
                        for i in range(len(res_dict['ExecLog'])):
                            if res_dict['ExecLog'][i]['RtnCode'] != 1:
                                result['VerifyExecLogRtnCode'] = False
                                rtnCode = res_dict['ExecLog'][i]['RtnCode']
                                break
                    else:
                        return result
                    if rtnCode == 1:
                        result['VerifyExecLogRtnCode'] = True
                    return result
                else:

                    return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Received expect_args_dict is not an dictionary")
    def verifyInjection(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        for key in res_dict:
            if type(res_dict[key]) is int:
                res_dict[key] = str(res_dict[key])
        expect_args_dict = all_verify_data['verifyPaymentReturn']
        print(res_dict)
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = dict()
                result['VerifyQueryInfo'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if res_dict['process_date'] == '' or res_dict['process_date'] is None:
                    result['verifyProcessDate'] = True
                    if res_dict['TotalSuccessTimes'] != '0':
                        self.log.WARN('TotalSuccessTimes is incorrect!')
                        result['VerifySuccessTimes'] = False
                        return result
                    else:
                        result['VerifySuccessTimes'] = True
                        return result
                else:
                    self.log.WARN('process_date is not empty!')
                    result['verifyProcessDate'] = False
                    return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Received expect_args_dict is not an dictionary")

    def verifyFailQueryInfo(self, res_dict, case_id):
        all_verify_dict = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        for key in res_dict:
            if type(res_dict[key]) is int:
                res_dict[key] = str(res_dict[key])
        expect_args_dict = all_verify_dict['verifyPaymentReturn']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = {}
                result['verifyRtnInfo'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Received expect_args_dict is not an dictionary.")
