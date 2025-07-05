# -*- coding: utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyCreditCardPeriodAction(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'CreditCardPeriodAction'
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

    def verifyCurrentUrl(self, case_id, current_url):
        verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id, 'Verification.ini')
        expect_args_dict = verify_data['verifyCurrentUrl']
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = {}
                if current_url == expect_args_dict['url']:
                    result['VerifyCurrentUrl'] = True
                else:
                    result['VerifyCurrentUrl'] = False
                return result
            else:
                raise ValueError("verifyCurrentUrl: Length of expected result dict cannot be zero.")
        else:
            raise TypeError("verifyCurrentUrl: Received expect_args_dict is not an dictionary")
        
    def verifyPaymentInfo(self, merc_tid, case_id, subtyp):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                                self.fea_name,
                                                                case_id,
                                                                'Verification.ini')
        expect_args_dict = all_verify_data['verifyPaymentInfo']
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
                    RtnMsgSubtype = json_dict['Subtype']
                    if RtnMsgSubtype == subtyp:
                        result['VerifyRtnMsgSubtype'] = True
                    else:
                        result['VerifyRtnMsgSubtype'] = False
                        
                    result['VerifyReturnValue'] = self.verifyRtnData(json_dict['RtnBody'], expect_args_dict, re_match_dict=regex_patterns)
                    return result
            else:
                raise ValueError("verifyPaymentInfo: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentInfo: Recieved expect_args_dict is not an dictionary")

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
    
    def verifyPaymentReturn(self, merc_tid, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                                self.fea_name,
                                                                case_id,
                                                                'Verification.ini')
        expect_args_dict = all_verify_data['verifyPaymentReturn']
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
                    result['VerifyReturnValue'] = self.verifyRtnData(json_dict['RtnBody'], expect_args_dict)
                    return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Recieved expect_args_dict is not an dictionary")

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

    def verifyOrderByQuery(self, merc_trade_no, mercid, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                                self.fea_name,
                                                                case_id,
                                                                'Verification.ini')
        if 'verifyOrderByQuery' in all_verify_data:
            expect_args_dict = all_verify_data['verifyOrderByQuery']
        else:
            raise ValueError("verifyOrderByQuery: Secion 'verifyOrderByQuery' not found in Verification.ini")
               
        query_dict = {}
        unix_time = funcGen.getCurrentDatetimeStamp()
        print(unix_time[1])
        query_dict['TimeStamp'] = unix_time[1]
        query_dict['PlatformID'] = ''
        query_dict['MerchantID'] = mercid
        query_dict['MerchantTradeNo'] = merc_trade_no
        
        query_chksum = self.genChkMacVal(query_dict)
        query_dict['CheckMacValue'] = query_chksum
        query_addr = hash_key = self.feature_conf['QueryOrder_API']
        query_order = self.postRequestToAPI(self.raw_sess, query_dict, query_addr)
        if query_order != '':
            result = {}
            print('Query:', query_order)
            result['verifyOrderByQuery'] = self.verifyRtnData(query_order, expect_args_dict)
            return result

    def verifyOrderByQuery3D(self, merc_trade_no, mercid, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyOrderByQuery' in all_verify_data:
            expect_args_dict = all_verify_data['verifyOrderByQuery']
        else:
            raise ValueError("verifyOrderByQuery: Secion 'verifyOrderByQuery' not found in Verification.ini")

        query_dict = {}
        unix_time = funcGen.getCurrentDatetimeStamp()
        print(unix_time[1])
        query_dict['TimeStamp'] = unix_time[1]
        query_dict['PlatformID'] = ''
        query_dict['MerchantID'] = mercid
        query_dict['MerchantTradeNo'] = merc_trade_no

        query_chksum = self.genChkMacVal3D(query_dict)
        query_dict['CheckMacValue'] = query_chksum
        query_addr = hash_key = self.feature_conf['QueryOrder_API']
        query_order = self.postRequestToAPI(self.raw_sess, query_dict, query_addr)
        if query_order != '':
            result = {}
            print('Query:', query_order)
            result['verifyOrderByQuery'] = self.verifyRtnData(query_order, expect_args_dict)
            return result

    def verifyInjection(self):
        op = self.webop
        result = {}
        msg = op.getElem('red', find_by='class').text
        self.log.INFO("response Msg: " + msg)
        if msg != '':
            result['verifyMerchantTradeNoSQLInjection'] = True
        else:
            result['verifyMerchantTradeNoSQLInjection'] = False
        return result
        
    def verifyHtmlPaymentForm(self, merc_trade_no, case_id):
        op = self.webop
        pform = op.getElem('PayForm')
        dict_payform = op.formElemToDict(pform)
        print(dict_payform)
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                                self.fea_name,
                                                                case_id,
                                                                'Verification.ini')
        expect_args_dict = all_verify_data['verifyHtmlPayForm']
        expect_args_dict['merchantTradeNo'] =  merc_trade_no
        
        if 'verifyHtmlPayForm_regex' in all_verify_data:
            regex_patterns = all_verify_data['verifyHtmlPayForm_regex']
            print(regex_patterns)
        else:
            regex_patterns = {}
            
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(dict_payform) != 0:
                    result = {}
                    result['VerifyHtmlPaymentForm'] = self.verifyRtnData(dict_payform, expect_args_dict, re_match_dict=regex_patterns, datatype='dictionary')
                    return result
            else:
                raise ValueError("verifyHtmlPaymentForm: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyHtmlPaymentForm: Received expect_args_dict is not an dictionary")

    def verifyIgnorePayment(self):
        op = self.webop
        result = {}
        msg = op.getElem('mp-nopay-tip', find_by='class').text
        self.log.INFO("response Msg: " + msg)
        if msg != '':
            result['Android Pay does not show on the payment page.'] = True
        else:
            result['Android Pay does not show on the payment page.'] = False
        return result

    def verifyLanguage(self, language):
        op = self.webop
        value = op.getElem('Language').get_attribute('value')
        print(value)
        result = {}
        if value == language:
            result['verifyLanguage'] = True
        else:
            result['verifyLanguage'] = False
        return result

    def verifyQueryMemberBindingReturn(self, query_order_dict, case_id):
        qmb_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini')
        if 'verifyQMBReturn' in qmb_verify_data:
            expect_args_dict = qmb_verify_data['verifyQMBReturn']
        else:
            raise ValueError("verifyQMBReturn: Secion 'verifyQMBReturn' not found in Verification.ini")

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_order_dict) != 0:
                    result = {}
                    result['verifyQMBReturn'] = self.verifyRtnData(query_order_dict, expect_args_dict, datatype='dictionary')
                    return result
                else:
                    raise ValueError("verifyQMBReturn: Length of queried result dic cannot be zero.")
            else:
                raise ValueError("verifyQMBReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyQMBReturn: Received expect_args_dict is not an dictionary")
        
    def verifyPaymentBlock(self):
        pass
    
    def verifyBarcodeSubmitBlock(self):
        pass

    def verifyResponseValues(self, case_id, res_dict, data, status='success'):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_dict = all_verify_data['verifyReturn']
        expect_data = all_verify_data['verifyData']
        result = {}
        res_dict['TransMsg'] = str(res_dict['TransMsg'])
        res_dict['MerchantID'] = str(res_dict['MerchantID'])
        res_dict['TransCode'] = str(res_dict['TransCode'])
        res_dict['TransMsg'] = res_dict['TransMsg'].rstrip(' ')
        if type(expect_dict) is dict:
            if len(expect_dict) > 0:
                result['VerifyResponseValues'] = self.verifyRtnData(res_dict, expect_dict, datatype='dictionary')
            else:
                raise ValueError("verifyResponseValues: Length of expect_dict cannot be zero.")
        else:
            raise TypeError("verifyResponseValues: Received expect_dict is not a dictionary.")
        # for key in data.keys():
        #     if data[key] is not None:
        #         data[key] = data[key].encode('utf-8')
        #     else:
        #         data[key] = ''
        data['RtnCode'] = str(data['RtnCode'])
        data['MerchantID'] = str(data['MerchantID'])
        data['AuthCode'] = str(data['AuthCode'])
        data['amount'] = str(data['amount'])
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
        is_empty_check_dict['MerchantID'] = data['MerchantID']
        is_empty_check_dict['AuthCode'] = data['AuthCode']
        is_empty_check_dict['amount'] = data['amount']
        if status == 'success':
            result['verifyNotEmptyValues'] = self.__valueIsEmpty(is_empty_check_dict)
        else:
            result['verifyMustEmptyValues'] = not self.__valueIsEmpty(is_empty_check_dict)
        return result

    def verifyInfoReturn(self, query_order_dict, case_id):
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
            raise TypeError("verifyCSVReturn: Recieved expect_args_dict is not an dictionary")
        

#ver = verifyAioCheckOut('5294y06JbISpM5x9', 'v77hoKGq4kWxNNIS')
#print ver.verifyPaymentReturn('8eec7edae13f4e9a89f', {'PayAmt':'100'})
