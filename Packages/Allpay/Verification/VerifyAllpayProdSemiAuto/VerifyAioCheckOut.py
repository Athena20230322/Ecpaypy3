import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyAioCheckOut(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'AllpayProdSemiAuto'
        self.fea_name = 'AioCheckOut'
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
            raise TypeError("verifyHtmlPaymentForm: Recieved expect_args_dict is not an dictionary")
        
    def verifyPaymentBlock(self):
        pass
    
    def verifyBarcodeSubmitBlock(self):
        pass
        

#ver = verifyAioCheckOut('5294y06JbISpM5x9', 'v77hoKGq4kWxNNIS')
#print ver.verifyPaymentReturn('8eec7edae13f4e9a89f', {'PayAmt':'100'})