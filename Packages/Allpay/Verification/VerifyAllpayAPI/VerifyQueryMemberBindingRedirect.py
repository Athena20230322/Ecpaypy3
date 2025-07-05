#-*-coding:utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyQueryMemberBindingRedirect(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'QueryMemberBindingRedirect'
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
                    raise ValueError(
                        "verifyColumn: the amount of columns is not equal to the expected result.")
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
            raise TypeError("verifyQueryMemberBindingResult: Received expect_args_dict is not a dictionary.")

    def verifyQueryMemberBindingReturn(self, query_order_dict, case_id):
        qmb_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyQMBReturn' in qmb_verify_data:
            expect_args_dict = qmb_verify_data['verifyQMBReturn']

        else:
            raise ValueError("verifyQueryMemberBindingReturn: Secion 'verifyQMBReturn' not found in Verification.ini")

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_order_dict) != 0:
                    result = {}
                    result['verifyQueryMemberBindingReturn'] = self.verifyRtnData(query_order_dict, expect_args_dict,
                                                                                  datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyQueryMemberBindingReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyQueryMemberBindingReturn: Received expect_args_dict is not an dictionary")

    def verifyReturnMsg(self, msg):
        result = {}
        if msg == '敬愛的使用者您串接的API已停止服務，造成您的不便敬請見諒，若有任何問題請洽客服人員 TechSupport@allpay.com.tw 協助':
            result['verifyRtnMsg'] = True
        else:
            self.log.WARN("RtnMsg is incorrect!")
            result['verifyRtnMsg'] = False
        return result
