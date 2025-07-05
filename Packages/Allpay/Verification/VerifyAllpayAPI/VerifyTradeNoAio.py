import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyTradeNoAio(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayAPI'
        self.fea_name = 'TradeNoAio'
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

    def verifyCSVReturnDownload(self, query_order_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyCSVReturn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyCSVReturn']
        else:
            raise ValueError("verifyCSVReturn: Secion 'verifyCSVReturn' not found in Verification.ini")

        for key in query_order_dict:
            query_order_dict[key] = ''
        # print query_order_dict

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_order_dict) != 0:
                    result = {}
                    result['verifyCSVReturnDownload'] = self.verifyRtnData(query_order_dict, expect_args_dict, datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyCSVReturnDownload: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyCSVReturnDownload: Recieved expect_args_dict is not an dictionary")

    def verifyCSVReturn(self, query_order_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyCSVReturn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyCSVReturn']
        else:
            raise ValueError("verifyCSVReturn: Secion 'verifyCSVReturn' not found in Verification.ini")

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_order_dict) != 0:
                    result = {}
                    result['verifyCSVReturn'] = self.verifyRtnData(query_order_dict, expect_args_dict,
                                                                   datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyCSVReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyCSVReturn: Received expect_args_dict is not an dictionary")

    def verifyStrCSVReturn(self, query_order, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyCSVReturn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyCSVReturn']
        else:
            raise ValueError("verifyStrCSVReturn: Secion 'verifyCSVReturn' not found in Verification.ini")

        print('Query_order: ', query_order)
        query_order_split_list = ['=', '-', '"', ',']

        for split_list_range in range(1, 5):
            query_order = query_order.split(query_order_split_list[split_list_range - 1])
            if split_list_range < 4:
                query_order = ''.join(query_order)
            else:
                query_order = [x for x in query_order if x != '']

        query_order_dict = dict((query_order_dict, '') for query_order_dict in query_order)

        try:
            coworker_remark_enter = '\xb6K\xaf\xc8\xa6W\xba\xd9\r\n'
            coworker_remark = "\xb6K\xaf\xc8\xa6W\xba\xd9"
            query_order_dict[coworker_remark] = query_order_dict.pop(coworker_remark_enter)
        except KeyError as e:
            raise KeyError("keyerror: key %s is not exist" % (e.message))

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_order_dict) != 0:
                    result = {}
                    result['verifyStrCSVReturn'] = self.verifyRtnData(query_order_dict, expect_args_dict, datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyStrCSVReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyStrCSVReturn: Received expect_args_dict is not an dictionary")
