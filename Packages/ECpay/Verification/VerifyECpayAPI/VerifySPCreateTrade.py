import time
import json
import LibGeneral.funcGeneral as funcGen
import re
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifySPCreateTrade(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'SPCreateTrade'
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

    def verifyRtnColumn(self, case_id, res_dict):
        verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                        self.fea_name,
                                                        case_id,
                                                        'Verification.ini')

        expect_dict = verify_data['verifyReturn']
        result = {}
        if type(res_dict) is dict:
            if type(expect_dict) is dict:
                if len(expect_dict) > 0:
                    if len(res_dict) == len(expect_dict):
                        for key in list(res_dict.keys()):
                            res_dict[key] = ''
                        result['VerifyColumnNames'] = self.verifyRtnData(res_dict, expect_dict, datatype='dictionary')
                    else:
                        raise ValueError("verifyColumns: Length of expect_dict & res_dict not same.")
                else:
                    raise ValueError("verifyColumns: Length of expect_dict cannot be zero.")
            else:
                raise TypeError("verifyColumns: Received expect_dict is not a dictionary.")
        else:
            raise TypeError("NOT THE CORRECT TYPE")
        return result

    def verifyRtnValue(self, case_id, res_dict):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_dict = all_verify_data['verifyReturn']
        for key in list(expect_dict.keys()):
            expect_dict[key] = expect_dict[key].decode('big5')
        result = {}
        res_dict['RtnMsg'] = res_dict['RtnMsg'].rstrip(' ')
        res_dict['RtnMsg'] = res_dict['RtnMsg']
        expect_dict['MerchantTradeNo'] = res_dict['MerchantTradeNo']
        expect_dict['TradeNo'] = res_dict['TradeNo']
        expect_dict['TradeDate'] = res_dict['TradeDate']
        if res_dict['PaymentType'] == 'ATM_CHINATRUST':
            expect_dict['vAccount'] = res_dict['vAccount']
            expect_dict['BankCode'] = res_dict['BankCode']
            expect_dict['ExpireDate'] = res_dict['ExpireDate']
        elif res_dict['PaymentType'] == 'CVS_CVS':
            expect_dict['PaymentNo'] = res_dict['PaymentNo']
            # expect_dict['PaymentNo'] = re.match("^[A-Z][A-Z][A-Z]\\d", res_dict['PaymentNo'])
            # print expect_dict['PaymentNo']
            # if expect_dict['PaymentNo'] == res_dict['PaymentNo']:
            #     expect_dict['PaymentNo'] = res_dict['PaymentNo']
            # else:
            #     raise KeyError('PaymentNo not match .')
            expect_dict['ExpireDate'] = res_dict['ExpireDate']
        elif res_dict['PaymentType'] == 'Credit_CreditCard':
            expect_dict['SimulatePaid'] = res_dict['SimulatePaid']
            expect_dict['PaymentDate'] = res_dict['PaymentDate']
        else:
            raise ValueError('Unknown key included .')
        if type(expect_dict) is dict:
            if len(expect_dict) > 0:
                result['VerifyResponseValues'] = self.verifyRtnData(res_dict, expect_dict, datatype='dictionary')
            else:
                raise ValueError("verifyResponseValues: Length of expect_dict cannot be zero.")
        else:
            raise TypeError("verifyResponseValues: Received expect_dict is not a dictionary.")
        # for key in res_dict.keys():
        #     if res_dict[key] is not None:
        #         res_dict[key] = res_dict[key].encode('utf-8')
        #     else:
        #         res_dict[key] = ''
        return result
    def verifyRtnValuePanhsin(self, case_id, res_dict):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_dict = all_verify_data['verifyReturn']
        for key in list(expect_dict.keys()):
            expect_dict[key] = expect_dict[key].decode('big5')
        result = {}
        res_dict['RtnMsg'] = res_dict['RtnMsg'].rstrip(' ')
        res_dict['RtnMsg'] = res_dict['RtnMsg']
        expect_dict['MerchantTradeNo'] = res_dict['MerchantTradeNo']
        expect_dict['TradeNo'] = res_dict['TradeNo']
        expect_dict['TradeDate'] = res_dict['TradeDate']
        if res_dict['PaymentType'] == 'ATM_PANHSIN':
            expect_dict['vAccount'] = res_dict['vAccount']
            expect_dict['BankCode'] = res_dict['BankCode']
            expect_dict['ExpireDate'] = res_dict['ExpireDate']
        elif res_dict['PaymentType'] == 'CVS_CVS':
            expect_dict['PaymentNo'] = res_dict['PaymentNo']
            # expect_dict['PaymentNo'] = re.match("^[A-Z][A-Z][A-Z]\\d", res_dict['PaymentNo'])
            # print expect_dict['PaymentNo']
            # if expect_dict['PaymentNo'] == res_dict['PaymentNo']:
            #     expect_dict['PaymentNo'] = res_dict['PaymentNo']
            # else:
            #     raise KeyError('PaymentNo not match .')
            expect_dict['ExpireDate'] = res_dict['ExpireDate']
        elif res_dict['PaymentType'] == 'Credit_CreditCard':
            expect_dict['SimulatePaid'] = res_dict['SimulatePaid']
            expect_dict['PaymentDate'] = res_dict['PaymentDate']
        else:
            raise ValueError('Unknown key included .')
        if type(expect_dict) is dict:
            if len(expect_dict) > 0:
                result['VerifyResponseValues'] = self.verifyRtnData(res_dict, expect_dict, datatype='dictionary')
            else:
                raise ValueError("verifyResponseValues: Length of expect_dict cannot be zero.")
        else:
            raise TypeError("verifyResponseValues: Received expect_dict is not a dictionary.")
        # for key in res_dict.keys():
        #     if res_dict[key] is not None:
        #         res_dict[key] = res_dict[key].encode('utf-8')
        #     else:
        #         res_dict[key] = ''
        return result

    def verifyPaymentReturn(self, merc_tid, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                                self.fea_name,
                                                                case_id,
                                                                'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturn']
        if 'verifyPaymentInfo_regex' in all_verify_data:
            regex_patterns = all_verify_data['verifyPaymentInfo_regex']
            print(regex_patterns)
        else:
            regex_patterns = {}

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = {}
                query_dict = {}
                query_dict['IdentCol'] = 'MerchantTradeNo'
                query_dict['IdentVal'] = merc_tid
                q = self.getRequestFromAPI(query_dict, self.conf.getRtnCollectorAddr())
                if q != '':
                    print(q)
                    json_dict = json.loads(q)

                    result['VerifyReturnValue'] = self.verifyRtnData(json_dict['RtnBody'].encode('utf-8'), expect_args_dict, re_match_dict=regex_patterns)
                    return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Recieved expect_args_dict is not an dictionary")
