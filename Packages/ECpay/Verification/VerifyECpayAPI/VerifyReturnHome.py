import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyReturnHome(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'ReturnHome'
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

    def verifyStatusResult(self, query_str, match_str):
        result = {}
        print(query_str)
        if query_str.find(match_str) != -1:
            result['verifyStatusResult'] = True
            return result
        else:
            self.log.WARN('verifyStatusResult: result is not match')
            result['verifyStatusResult'] = False
            return result

    def verifyReturnHomeResult(self):
        op = self.webop
        tag_body = op.getElem('body', find_by='tag')
        result = {}
        print(tag_body.text)
        tag_str = tag_body.text
        if tag_str.find('1|OK') != -1:
            result['verifyReturnHomeResult'] = True
            return result
        else:
            self.log.WARN('verifyReturnHomeResult: result is not "1|OK"')
            result['verifyReturnHomeResult'] = False
            return result

    def verifyReturnHomeCVSResult(self, cvs_result):
        result = {}
        print(cvs_result)
        if cvs_result.find('1|OK') != -1:
            result['verifyReturnHomeCVSResult'] = True
            return result
        else:
            self.log.WARN('verifyReturnHomeResult: result is not "1|OK"')
            result['verifyReturnHomeCVSResult'] = False
            return result

    def verifyServerReplyValues(self, response, case_id):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            res_dict = {}
            for ele in res_list:
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
            print(res_dict)
            res_dict['RtnMsg'] = res_dict['RtnMsg'].encode('utf-8')
            all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                   'Verification.ini')
            expect_args_dict = all_verify_data['verifyServerReplyRtnData']
            print(expect_args_dict)
            if type(expect_args_dict) is dict:
                if len(expect_args_dict) > 0:
                    result['verifyRtnData'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                    # if res_dict['MerchantTradeNo'] == m_trade_no:
                    #     result['verifyMerchantTradeNo'] = True
                    # else:
                    #     self.log.WARN('MerchantTradeNo not match!\nexpect: %s\nreply: %s' % (m_trade_no, res_dict['MerchantTradeNo']))
                    #     result['verifyMerchantTradeNo'] = False
                    # if res_dict['MerchantMemberID'] == m_mid:
                    #     result['verifyMerchantMemberID'] = True
                    # else:
                    #     self.log.WARN('MerchantMemberID not match!\nexpect: %s\nreply: %s' % (m_mid, res_dict['MerchantMemberID']))
                    #     result['verifyMerchantMemberID'] = False
                    # if res_dict['process_date'] is not False:
                    #     result['verifyProcessDate'] = True
                    # else:
                    #     self.log.WARN("process_date is empty!")
                    #     result['verifyProcessDate'] = False
                    return result
                else:
                    raise ValueError("verifyServerReplyValues: Length of expected result dic cannot be zero.")
            else:
                raise TypeError("verifyServerReplyValues: Received expect_args_dict is not a dictionary.")
