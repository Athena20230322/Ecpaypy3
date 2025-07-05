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


    def verifyCSVReturnDownload(self, query_order, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyCSVReturn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyCSVReturn']
            #print expect_args_dict, "test"
        else:
            raise ValueError("verifyCSVReturn: Secion 'verifyCSVReturn' not found in Verification.ini")

        print(query_order)
        query_order_split_list = ['=', '-', '"', ',']
        for split_list_range in range(1, 5):
            query_order = query_order.split(query_order_split_list[split_list_range - 1])
            #print type(query_order),
            #print query_order
            if split_list_range < 4:
                query_order = ''.join(query_order)
                #print type(query_order),
                #print query_order
            else:
                query_order = [x for x in query_order if x != '']
                print(query_order)
        result = {}
        query_order_dict = {}
        query_order_dict = dict((query_order_dict, '') for query_order_dict in query_order)
        print(query_order_dict)

        print('##########')
        if type(query_order_dict) is dict:
            print('True')
            result['verifyCSVReturn'] = True
            return result
        else:
            print('False')
            result['verifyCSVReturn'] = False
            return result

    def verifyCSVReturn(self, query_order, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyCSVReturn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyCSVReturn']

        else:
            raise ValueError("verifyCSVReturn: Secion 'verifyCSVReturn' not found in Verification.ini")

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
            download_1min_limit_enter = '\xa4@\xa4\xc0\xc4\xc1\xa4\xa7\xa4\xba\xb6\xc8\xad\xad\xa4U\xb8\xfc\xa4@\xad\xd3\xb4C\xc5\xe9\xc0\xc9\r\n'
            download_1min_limit = "\xa4@\xa4\xc0\xc4\xc1\xa4\xa7\xa4\xba\xb6\xc8\xad\xad\xa4U\xb8\xfc\xa4@\xad\xd3\xb4C\xc5\xe9\xc0\xc9"
            sticker_name_enter = '\xb6K\xaf\xc8\xa6W\xba\xd9\r\n'
            sticker_name = "\xb6K\xaf\xc8\xa6W\xba\xd9"
            query_order_dict[download_1min_limit] = query_order_dict.pop(download_1min_limit_enter)
            query_order_dict[sticker_name] = query_order_dict.pop(sticker_name_enter)
        except KeyError as e:
            raise KeyError("keyerror: key %s is not exist" % (e.message))
        print('Query_order_dict: ', query_order_dict)
        print('Expect_args_dict: ', expect_args_dict)
        result = {}
        if cmp(expect_args_dict, query_order_dict) == 0:
            print('True')
            result['verifyCSVReturn'] = True
            return result
        else:
            print('False')
            result['verifyCSVReturn'] = False
            return result

    def verifyCSVReturnOldFormat(self, query_order, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyCSVReturn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyCSVReturn']
        else:
            raise ValueError("verifyCSVReturn: Secion 'verifyCSVReturn' not found in Verification.ini")

        print('Query_order: ',query_order)
        query_order_split_list = ['=', '-', '"', ',']

        for split_list_range in range(1, 5):
            query_order = query_order.split(query_order_split_list[split_list_range - 1])
            if split_list_range < 4:
                query_order = ''.join(query_order)
            else:
                query_order = [x for x in query_order if x != '']

        query_order_dict = dict((query_order_dict, '') for query_order_dict in query_order)

        try:
            remark_1min_limit_enter = '\xb3\xc6\xb5\xf9\r\n'
            remark_1min_limit = "\xb3\xc6\xb5\xf9"
            key_enter = '\r\n'
            query_order_dict[remark_1min_limit] = query_order_dict.pop(remark_1min_limit_enter)
            query_order_dict.pop(key_enter)
        except KeyError as e:
            raise KeyError("keyerror: key %s is not exist" % (e.message))

        print('Query_order_dict: ', query_order_dict)
        print('Expect_args_dict: ', expect_args_dict)
        result = {}
        if cmp(expect_args_dict, query_order_dict) == 0:
            print('True')
            result['verifyCSVReturn'] = True
            return result
        else:
            print('False')
            result['verifyCSVReturn'] = False
            return result