import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyCrossCreate(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'CrossCreate'
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

    def verifyServerReplyValues(self, response, case_id):
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

    def verifyReturnCVSResult(self):
        op = self.webop
        tag_body = op.getElem('body', find_by='tag')
        result = {}
        print(tag_body.text)
        tag_str = tag_body.text
        tag_str = tag_str.split('|')
        print(tag_str)
        if tag_str[0] and tag_str[1] != '':
            print(True)
            result['verifyReturnCVSResult'] = True
            return result
        else:
            self.log.WARN('verifyReturnCVSResult: result is not RtnMerchantTradeNo|RtnOrderNo!')
            result['verifyReturnCVSResult'] = False
            return result

    def verifyColumns(self, case_id, res_dict):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_dict = all_verify_data['verifyReturn']
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

    def verifyResponseValues(self, case_id, res_dict, mode='CVS', cat='B2C'):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_dict = all_verify_data['verifyReturn']
        result = {}
        print('---------------------------')
        print("res_dict[\'RtnMsg\'] : " + res_dict['RtnMsg'].decode('utf-8'))
        print("expect_dict[\'RtnMsg\'] : " + expect_dict['RtnMsg'].decode('big5'))
        print('---------------------------')
        res_dict['RtnMsg'] = res_dict['RtnMsg'].rstrip(' ')
        expect_dict['RtnMsg'] = expect_dict['RtnMsg'].decode('big5').encode('utf-8')
        expect_dict['MerchantTradeNo'] = res_dict['MerchantTradeNo']
        expect_dict['AllPayLogisticsID'] = res_dict['AllPayLogisticsID']
        expect_dict['UpdateStatusDate'] = res_dict['UpdateStatusDate']
        expect_dict['CheckMacValue'] = res_dict['CheckMacValue']
        if mode == 'HOME':
            expect_dict['BookingNote'] = res_dict['BookingNote']
        if cat == 'C2C':
            expect_dict['CVSPaymentNo'] = res_dict['CVSPaymentNo']
            expect_dict['CVSValidationNo'] = res_dict['CVSValidationNo']
            hash_key = 'XBERn1YOvpM9nfZc'
            hash_iv = 'h1ONHk4P4yqbl5LK'
            APIHelper.__init__(self, hash_key, hash_iv)
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
        origin_chkMacValue = res_dict['CheckMacValue']
        print('origin : ' + origin_chkMacValue)
        res_dict.pop('CheckMacValue')
        generate_chkMacValue = self.genChkMacVal(res_dict, mode='local', codec='md5', case='insensitive')
        print(generate_chkMacValue)
        res_dict['CheckMacValue'] = origin_chkMacValue
        if res_dict['CheckMacValue'] == generate_chkMacValue:
            result['VerifyReturnCheckMacValue'] = True
        else:
            result['VerifyReturnCheckMacValue'] = False
        return result

    def verifyResponseValuesb2c(self, case_id, data, status='success'):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_data = all_verify_data['verifyData']

        result = {}
        # for key in data.keys():
        #     if data[key] is not None:
        #         data[key] = data[key].encode('utf-8')
        #     else:
        #         data[key] = ''
        data['RtnCode'] = str(data['RtnCode'])

        data['RtnCode'] = data['RtnCode'].rstrip(' ')
        if type(expect_data) is dict:
            if len(expect_data) > 0:
                result['VerifyDataValues'] = self.verifyRtnData(data, expect_data, datatype='dictionary')
            else:
                raise ValueError("verifyResponseValues: Length of expect_data cannot be zero.")
        else:
            raise TypeError("verifyResponseValues: Received expect_data is not a dictionary.")
        is_empty_check_dict = {}
        is_empty_check_dict['RtnCode'] = data['RtnCode']

        if status == 'success':
            result['verifyNotEmptyValues'] = self.__valueIsEmpty(is_empty_check_dict)
        else:
            result['verifyMustEmptyValues'] = not self.__valueIsEmpty(is_empty_check_dict)
        return result

    def verifyResult(self, res):
        result = {}
        if res.find('10500040') != -1:
            result['verifyResult'] = True
        else:
            self.log.WARN(
                "verifyResult: result should be '10500040', but it is " + res)
            result['verifyResult'] = False
        return result

    def __valueIsEmpty(self, is_empty_check_dict):
        pass