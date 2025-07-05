# -*- coding: utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyAuthCardIDRedirect(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'AuthCardIDRedirect'
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo',
                                                                feature_cat=self.category,
                                                                feature_name=self.fea_name)
        hash_key = self.feature_conf['JumpKey']
        hash_iv = self.feature_conf['JumpIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.hkey = hash_key
        self.hiv = hash_iv
        self.htm_helper = HtmlHelper()
        self.raw_sess = self.genSession()

    def verifyResponseColumns(self, res_dict, case_id):
        result = {}
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyColumns']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) != len(res_dict):
                    self.log.WARN('verifyResponseColumns: column amounts not equal!\nexpect: %d\nresponse: %d' % (len(expect_args_dict), len(res_dict)))
                    result['VerifyColumnAmount'] = False
                    return result
                else:
                    result['VerifyColumnAmount'] = True
                for exp in expect_args_dict:
                    if exp in res_dict:
                        continue
                    else:
                        self.log.WARN('verifyResponseColumns: column name %s not in res_dict!' % exp)
                        result['VerifyColumnName'] = False
                        return result
                return result
            else:
                raise ValueError("verifyResponseColumns: Length of expected result dict cannot be zero.")
        else:
            raise TypeError("verifyResponseColumns: Received expect_args_dict is not a dictionary.")

    def verifyReturnMsg(self, msg):
        result = {}
        if msg == '敬愛的使用者您串接的API已停止服務，造成您的不便敬請見諒，若有任何問題請洽客服人員 TechSupport@allpay.com.tw 協助':
            result['verifyRtnMsg'] = True
        else:
            self.log.WARN("rtnMsg is incorrect!")
            result['verifyRtnMsg'] = False
        return result
