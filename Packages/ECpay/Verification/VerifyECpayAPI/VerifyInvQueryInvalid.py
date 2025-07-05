import time
import json
import LibGeneral.funcGeneral as funcGen
import urllib.request, urllib.parse, urllib.error
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyInvQueryInvalid(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvQueryInvalid'
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

    def verifyColumn(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnColumn']
        print((list(expect_args_dict.keys())))
        print((list(res_dict.keys())))
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) == len(res_dict):
                    result['verifyColumnAmount'] = True
                else:
                    result['verifyColumnAmount'] = False
                    raise ValueError("verifyInvQueryInvalidReturn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyInvQueryInvalidReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvQueryInvalidReturn: Received expect_args_dict is not a dictionary.")

    def verifyResponseValue(self, res_dict, issue_dict, issue_rtn, invalid_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if res_dict['II_Mer_ID'] == issue_dict['MerchantID']:
                    result['verifyII_Mer_ID'] = True
                else:
                    self.log.WARN("II_Mer_ID not match!\nInvQueryInvalid: %s\nInvIssue: %s" % (res_dict['IIS_Mer_ID'], issue_dict['MerchantID']))
                    result['verifyII_Mer_ID'] = False
                if res_dict['II_Invoice_No'] == issue_rtn['InvoiceNumber']:
                    result['verifyII_Invoice_No'] = True
                else:
                    self.log.WARN("II_Invoice_No not match!\nInvQueryInvalid: %s\nInvIssueRtn: %s" % (res_dict['II_Invoice_No'], issue_rtn['InvoiceNumber']))
                    result['verifyII_Invoice_No'] = False
                if res_dict['II_Date'] != '':
                    result['verifyII_Date'] = True
                else:
                    self.log.WARN("II_Date is empty!")
                    result['verifyII_Date'] = False
                if res_dict['II_Upload_Date'] == '':
                    result['verifyII_Upload_Date'] = True
                else:
                    result['verifyII_Upload_Date'] = False
                print(invalid_dict)
                print(res_dict)
                if res_dict['Reason'] == urllib.parse.quote_plus(invalid_dict['Reason']).lower():
                    result['verifyReason'] = True
                else:
                    self.log.WARN("Reason not match!\nInvQueryInvali: %s\nInvIssueInvalid: %s" % (res_dict['Reason'], urllib.parse.quote_plus(invalid_dict['Reason']).lower()))
                    result['verifyReason'] = False
                if res_dict['II_Seller_Identifier'] == '53538851':
                    result['verifyII_Seller_Identifier'] = True
                else:
                    self.log.WARN("II_Seller_Identifier not match!\nInvQueryInvalid: %s" % res_dict['II_Seller_Identifier'])
                    result['verifyII_Seller_Identifier'] = False
                if res_dict['II_Buyer_Identifier'] == issue_dict['CustomerIdentifier']:
                    result['verifyII_Buyer_Identifier'] = True
                elif res_dict['II_Buyer_Identifier'] == '0000000000':
                    result['verifyII_Buyer_Identifier'] = True
                else:
                    self.log.WARN("II_Buyer_Identifier not match!\nInvQueryInvalid: %s" % res_dict['II_Buyer_Identifier'])
                    result['verifyII_Buyer_Identifier'] = False
                chkMacValue = res_dict['CheckMacValue']
                res_dict.pop('CheckMacValue')
                res_dict.pop('Reason')
                genCheckMacValue = self.genChkMacVal(res_dict, mode='local')
                if genCheckMacValue == chkMacValue:
                    result['verifyCheckMacValue'] = True
                else:
                    self.log.WARN("verifyResponseValue: CheckMacValue incorrect!")
                    result['verifyCheckMacValue'] = False
                return result
            else:
                raise ValueError("verifyInvQueryInvalidReturn: Length of expected result cannot be zero!")
        else:
            raise TypeError("verifyInvQueryInvalidReturn: Received expect_args_dict is not a dictionary!")
