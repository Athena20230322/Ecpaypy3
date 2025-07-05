import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyMobileCreateServerOrder(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'MobileCreateServerOrder'
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

    def verifyColumns(self, case_id, res_dict):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id, 'Verification.ini')
        expect_dict = all_verify_data['verifyReturn']
        # expect_data = all_verify_data['verifyData']
        result = {}
        if type(expect_dict) is dict:
            if len(expect_dict) > 0:
                for key in list(res_dict.keys()):
                    res_dict[key] = ''
                result['VerifyColumnNames'] = self.verifyRtnData(res_dict, expect_dict, datatype='dictionary')
            else:
                raise ValueError("verifyColumns: Length of expect_dict cannot be zero.")
        else:
            raise TypeError("verifyColumns: Received expect_dict is not a dictionary.")
        # if type(expect_data) is dict:
        #     if len(expect_data) > 0:
        #         for key in data.keys():
        #             data[key] = ''
        #         result['VerifyDataColumnNames'] = self.verifyRtnData(data, expect_data, datatype='dictionary')
        #     else:
        #         raise ValueError("verifyColumns: Length of expect_data cannot be zero.")
        # else:
        #     raise TypeError("verifyColumns: Received expect_data is not a dictionary.")
        return result

    def verifyOrderResult(self, result_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id, 'Verification.ini')
        expect_args_dict = all_verify_data['verifyPaymentReturn']
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = {'VerifyOrderResult': self.verifyRtnData(result_dict, expect_args_dict, datatype='dictionary')}
                return result
            else:
                raise ValueError("verifyQueryResult: Length of expected result dict cannot be zero.")
        else:
            raise TypeError("verifyQueryResult: Received expect_args_dict is not a dictionary.")

    # def verifyPaymentReturn(self, merc_tid, case_id):
    #     all_verify_data = self.t_helper.getTestDataIniSections(self.category,
    #                                                             self.fea_name,
    #                                                             case_id,
    #                                                             'Verification.ini')
    #     expect_args_dict = all_verify_data['verifyPaymentReturn']
    #     if type(expect_args_dict) is dict:
    #         if len(expect_args_dict) > 0:
    #             result = {}
    #             query_dict = {}
    #             query_dict['IdentCol'] = 'MerchantTradeNo'
    #             query_dict['IdentVal'] = merc_tid
    #             q = self.getRequestFromAPI(query_dict, self.conf.getRtnCollectorAddr())
    #             if q != '':
    #                 print q
    #                 json_dict = json.loads(q)
    #                 result['VerifyReturnValue'] = self.verifyRtnData(json_dict['RtnBody'], expect_args_dict)
    #                 return result
    #         else:
    #             raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
    #     else:
    #         raise TypeError("verifyPaymentReturn: Recieved expect_args_dict is not an dictionary")

    def verifyATMPaymentInfo(self, merc_tid):
        result = {}
        query_dict = {}
        query_dict['IdentCol'] = 'MerchantTradeNo'
        query_dict['IdentVal'] = merc_tid
        q = self.getRequestFromAPI(query_dict, self.conf.getRtnCollectorAddr())
        if q != '':
            print(q)
            result_dict = json.loads(q)
            if 'BankCode' in result_dict['RtnBody']:
                result['containBankCode'] = True
            else:
                result['containBankCode'] = False
            if 'vAccount' in result_dict['RtnBody']:
                result['containvAccount'] = True
            else:
                result['containvAccount'] = False
            if 'ExpireDate' in result_dict['RtnBody']:
                result['containExpireDate'] = True
            else:
                result['containExpireDate'] = False
            return result

    def verifyInjection(self):
        op = self.webop
        result = {}
        msg = op.getElem('h4', find_by='tag').text
        self.log.INFO("response Msg: " + msg)
        if msg == 'MerchantTradeNo Must be Number or English Letter.':
            result['verifyMerchantTradeNoSQLInjection'] = True
        else:
            result['verifyMerchantTradeNoSQLInjection'] = False
        return result

    def verifyPaymentBlock(self):
        pass

        

#ver = verifyAioCheckOut('5294y06JbISpM5x9', 'v77hoKGq4kWxNNIS')
#print ver.verifyPaymentReturn('8eec7edae13f4e9a89f', {'PayAmt':'100'})
