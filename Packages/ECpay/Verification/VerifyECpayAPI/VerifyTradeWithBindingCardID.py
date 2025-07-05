# -*- coding: utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyTradeWithBindingCardID(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'TradeWithBindingCardID'
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

    def verifyServerReplyColumns(self, response, case_id):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            res_dict = {}
            for ele in res_list:
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
            print(res_dict)
            all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                   'Verification.ini')
            expect_args_dict = all_verify_data['verifyServerReplyColumns']
            print(expect_args_dict)
            if type(expect_args_dict) is dict:
                if len(expect_args_dict) > 0:
                    if len(expect_args_dict) != len(res_dict):
                        self.log.WARN(
                            'verifyServerReplyColumns: column amounts not equal!\nexpect: %d\nreply: %d' % (
                            len(expect_args_dict), len(res_dict)))
                        result['VerifyColumnNumber'] = False
                        return result
                    else:
                        result['VerifyColumnNumber'] = True
                    for exp in expect_args_dict:
                        if exp in res_dict:
                            continue
                        else:
                            self.log.WARN('verifyServerReplyColumns: column name %s not in res_dict!' % exp)
                            result['VerifyColumnName'] = False
                            return result
                    return result
                else:
                    raise ValueError("verifyServerReplyColumns: Length of expected result dic cannot be zero.")
            else:
                raise TypeError("verifyServerReplyColumns: Received expect_args_dict is not a dictionary.")

    def verifyResultWithoutFillingClientURL(self, res):
        result = {}
        if res == '歡迎使用綠界科技ECPay'.decode('utf-8'):
            result['verifyTag'] = True
        else:
            self.log.WARN("verifyResultWithoutFillingClientURL: expect: 歡迎使用綠界科技ECPay, redirect: %s" %res)
            result['verifyTag'] = False
        return result

    def verifyClientRedirectColumns(self, res_dict, case_id):
        result = {}
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyClientRedirectColumns']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) != len(res_dict):
                    self.log.WARN('verifyClientRedirectColumns: column amounts not equal!\nexpect: %d\nredirect: %d' % (len(expect_args_dict), len(res_dict)))
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

    def verifyServerReplyValues(self, response, case_id, m_trade_no, m_mid):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            res_dict = {}
            for ele in res_list:
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
            print(res_dict)
            all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                   'Verification.ini')
            expect_args_dict = all_verify_data['verifyServerReplyRtnData']
            print(expect_args_dict)
            if type(expect_args_dict) is dict:
                if len(expect_args_dict) > 0:
                    result['verifyRtnData'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                    if res_dict['MerchantTradeNo'] == m_trade_no:
                        result['verifyMerchantTradeNo'] = True
                    else:
                        self.log.WARN('MerchantTradeNo not match!\nexpect: %s\nreply: %s' % (m_trade_no, res_dict['MerchantTradeNo']))
                        result['verifyMerchantTradeNo'] = False
                    if res_dict['MerchantMemberID'] == m_mid:
                        result['verifyMerchantMemberID'] = True
                    else:
                        self.log.WARN('MerchantMemberID not match!\nexpect: %s\nreply: %s' % (m_mid, res_dict['MerchantMemberID']))
                        result['verifyMerchantMemberID'] = False
                    if res_dict['process_date'] is not False:
                        result['verifyProcessDate'] = True
                    else:
                        self.log.WARN("process_date is empty!")
                        result['verifyProcessDate'] = False
                    return result
                else:
                    raise ValueError("verifyServerReplyValues: Length of expected result dic cannot be zero.")
            else:
                raise TypeError("verifyServerReplyValues: Received expect_args_dict is not a dictionary.")

    def verifyClientRedirectValues(self, res_dict, case_id, m_trade_no, m_mid):
        result = {}
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyClientRedirectRtnData']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnData'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if res_dict['MerchantTradeNo'] == m_trade_no:
                    result['verifyMerchantTradeNo'] = True
                else:
                    self.log.WARN(
                        'MerchantTradeNo not match!\nexpect: %s\nredirect: %s' % (m_trade_no, res_dict['MerchantTradeNo']))
                    result['verifyMerchantTradeNo'] = False
                if res_dict['MerchantMemberID'] == m_mid:
                    result['verifyMerchantMemberID'] = True
                else:
                    self.log.WARN(
                        'MerchantMemberID not match!\nexpect: %s\nredirect: %s' % (m_mid, res_dict['MerchantMemberID']))
                    result['verifyMerchantMemberID'] = False
                if res_dict['process_date'] is not False:
                    result['verifyProcessDate'] = True
                else:
                    self.log.WARN("process_date is empty!")
                    result['verifyProcessDate'] = False
                return result
            else:
                raise ValueError("verifyClientRedirectValues: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyClientRedirectValues: Received expect_args_dict is not a dictionary.")

    def verifyRtnCode(self, res_dict, case_id):
        result = {}
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyRtnCode']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCode'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                return result
            else:
                raise ValueError("verifyRtnCode: Length of expected result dict cannot be zero.")
        else:
            raise TypeError("verifyRtnCode: Received expect_args_dict is not a dictionary.")
