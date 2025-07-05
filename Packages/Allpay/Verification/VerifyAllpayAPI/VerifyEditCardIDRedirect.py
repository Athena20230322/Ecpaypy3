# -*- coding: utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyEditCardIDRedirect(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'EditCardIDRedirect'
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

    def verifyServerReplyColumnsCheck(self, response, case_id, mert_no):
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            res_dict = {}
            for ele in res_list:
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
            print(res_dict)
            all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                   'Verification.ini')
            expect_args_dict = all_verify_data['verifyServerReplyColumns']
            insert_value_list = ['Bindingdate', 'AllPayTradeNo', 'gwsr', 'process_date', 'stage']
            expect_args_dict['MerchantTradeNo'] = mert_no
            for key in insert_value_list:
                expect_args_dict[key] = res_dict[key]
                print(key)
            expect_args_dict.pop('CheckMacValue')
            print("##############################")
            print(expect_args_dict)
            query_chksum = self.genChkMacVal(expect_args_dict, mode='local', codec='sha256')
            expect_args_dict['CheckMacValue'] = query_chksum
            if type(expect_args_dict) is dict:
                if len(expect_args_dict) > 0:
                    if len(res_dict) != 0:
                        result = {}
                        result['verifyServerReplyColumnsCheck'] = self.verifyRtnData(res_dict, expect_args_dict,
                                                                                     datatype='dictionary')
                        return result
                else:
                    raise ValueError("verifyServerReplyColumnsCheck: Length of expected result dic cannot be zero.")
            else:
                raise TypeError("verifyServerReplyColumnsCheck: Received expect_args_dict is not an dictionary.")

    def verifyClientRedirectColumnsCheck(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        if 'verifyClientRedirectColumns' in all_verify_data:
            expect_args_dict = all_verify_data['verifyClientRedirectColumns']
        else:
            raise ValueError("verifyClientRedirectColumns: Secion 'verifyClientRedirectColumns' not found in Verification.ini")
        insert_value_list = ['MerchantMemberID', 'CardID']
        print(res_dict)
        for key in insert_value_list:
            expect_args_dict[key] = res_dict[key]
        expect_args_dict.pop('CheckMacValue')
        query_chksum = self.genChkMacVal(expect_args_dict, mode='local', codec='sha256')
        expect_args_dict['CheckMacValue'] = query_chksum
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if res_dict['RtnCode'] == '1':
                    result = {}
                    result['verifyClientRedirectColumnsCheck'] = self.verifyRtnData(res_dict, expect_args_dict,
                                                                                 datatype='dictionary')
                    return result
                else:
                    raise ValueError("verifyClientRedirectColumnsCheck: RtnCode is not '1'.")
            else:
                raise ValueError("verifyClientRedirectColumnsCheck: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyClientRedirectColumnsCheck: Received expect_args_dict is not an dictionary.")

    def verifyEditCardIDRedirectCloseCheck(self, res_text):
        result = {}
        simple_text = '敬愛的使用者您串接的API已停止服務，造成您的不便敬請見諒，若有任何問題請洽客服人員 TechSupport@allpay.com.tw 協助'
        if res_text == simple_text:
            result['verifyEditCardIDRedirectCloseCheck'] = True
            return result
        else:
            result['verifyEditCardIDRedirectCloseCheck'] = False
            raise ValueError("verifyEditCardIDRedirectCloseCheck: Close Message is not match!\n"
                             "Simple Msg: %s\nResponse Msg: %s\n" % (simple_text, res_text))
