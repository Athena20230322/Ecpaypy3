import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyQueryMemberInfo(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'QueryMemberInfo'
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

    def verifyQueryMemberInfoReturn(self, query_order_dict, case_id):
        verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyQueryMemberInfo' in verify_data:
            expect_args_dict = verify_data['verifyQueryMemberInfo']
        else:
            raise ValueError("verifyQueryMemberInfoReturn: Secion 'verifyQueryMemberInfo' not found in Verification.ini")

        for key in query_order_dict:
            query_order_dict[key] = ''
        # print query_order_dict

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_order_dict) != 0:
                    result = {}
                    result['verifyQueryMemberInfoReturn'] = self.verifyRtnData(query_order_dict, expect_args_dict,
                                                                               datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyQueryMemberInfoReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyQueryMemberInfoReturn: Received expect_args_dict is not an dictionary")

    def verifyQueryMemberInfoFormat(self, query_order_dict, case_id):
        verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyQueryMemberInfoFormat' in verify_data:
            expect_args_dict = verify_data['verifyQueryMemberInfoFormat']
        else:
            raise ValueError("verifyQueryMemberInfo: Secion 'verifyQueryMemberInfoFormat' not found in Verification.ini")

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_order_dict) != 0:
                    result = {}
                    result['verifyQueryMemberInfo'] = self.verifyRtnData(query_order_dict, expect_args_dict,
                                                                         datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyQueryMemberInfo: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyQueryMemberInfo: Received expect_args_dict is not an dictionary")