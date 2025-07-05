import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyInvIssueByPlatform(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvIssueByPlatform'
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
                    result['verifyColumnNumber'] = True
                else:
                    raise ValueError("verifyInvIssueReturn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyInvIssueReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvIssueReturn: Received expect_args_dict is not a dictionary.")

    def verifyResponseValue(self, res_dict, case_id, mode):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if mode == 'success':
                    if res_dict['InvoiceNumber'] != '' and res_dict['InvoiceDate'] != '':
                        result['verifyInvoiceNumber'] = True
                    else:
                        result['verifyInvoiceNumber'] = False
                        self.log.WARN("verifyInvIssueReturn: InvoiceNumber or InvoiceDate is empty\n"
                                      "InvoiceNumber= %s\nInvoiceDate= %s" % (res_dict['InvoiceNumber'],
                                                                               res_dict['InvoiceDate']))
                else:
                    if res_dict['InvoiceNumber'] == '':
                        result['verifyFailCase'] = True
                    else:
                        result['verifyFailCase'] = False
                        self.log.WARN("verifyInvIssueReturn: InvoiceNumber is not empty\n"
                                      "InvoiceNumber= %s\nInvoiceDate= %s" % (res_dict['InvoiceNumber'],
                                                                               res_dict['InvoiceDate']))
                chkMacValue = res_dict['CheckMacValue']
                res_dict.pop('CheckMacValue')
                genCheckMacValue = self.genChkMacVal(res_dict, mode='local')
                print(genCheckMacValue)
                print("test")
                if genCheckMacValue == chkMacValue:
                    result['verifyCheckMacValue'] = True
                else:
                    self.log.WARN("verifyResponseValue: CheckMacValue incorrect!")
                    result['verifyCheckMacValue'] = False
                return result
            else:
                raise ValueError("verifyInvIssueReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvIssueReturn: Received expect_args_dict is not a dictionary.")
    def verifyResponseValueError(self, res_dict, case_id, mode):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                # if mode == 'success':
                #     if res_dict['InvoiceNumber'] != '' and res_dict['InvoiceDate'] != '':
                #         result['verifyInvoiceNumber'] = True
                #     else:
                #         result['verifyInvoiceNumber'] = False
                #         self.log.WARN("verifyInvIssueReturn: InvoiceNumber or InvoiceDate is empty\n"
                #                       "InvoiceNumber= %s\nInvoiceDate= %s" % (res_dict['InvoiceNumber'],
                #                                                                res_dict['InvoiceDate']))
                # else:
                #     if res_dict['InvoiceNumber'] == '':
                #         result['verifyFailCase'] = True
                #     else:
                #         result['verifyFailCase'] = False
                #         self.log.WARN("verifyInvIssueReturn: InvoiceNumber is not empty\n"
                #                       "InvoiceNumber= %s\nInvoiceDate= %s" % (res_dict['InvoiceNumber'],
                #                                                                res_dict['InvoiceDate']))
                chkMacValue = res_dict['CheckMacValue']
                res_dict.pop('CheckMacValue')
                genCheckMacValue = self.genChkMacVal(res_dict, mode='local')
                if genCheckMacValue == chkMacValue:
                    result['verifyCheckMacValue'] = True
                else:
                    self.log.WARN("verifyResponseValue: CheckMacValue incorrect!")
                    result['verifyCheckMacValue'] = False
                return result
            else:
                raise ValueError("verifyInvIssueReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvIssueReturn: Received expect_args_dict is not a dictionary.")