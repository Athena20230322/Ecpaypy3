import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyInvAllowanceInvalid(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvAllowanceInvalid'
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
        invalid_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id, 'Verification.ini')
        expect_args_dict = invalid_verify_data['verifyReturnColumn']
        print((list(expect_args_dict.keys())))
        print((list(res_dict.keys())))
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) == len(res_dict):
                    result['verifyColumnAmount'] = True
                else:
                    result['verifyColumnAmount'] = False
                    raise ValueError("verifyAllowanceInvalidReturn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyAllowanceInvalidReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyAllowanceInvalidReturn: Received expect_args_dict is not a dictionary.")

    def verifyInjection(self, invalid_dict, allowance_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id, 'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(invalid_dict, expect_args_dict, datatype='dictionary')
                chkMacValue = invalid_dict['CheckMacValue']
                invalid_dict.pop('CheckMacValue')
                genCheckMacValue = self.genChkMacVal(invalid_dict, mode='local')
                if genCheckMacValue == chkMacValue:
                    result['verifyCheckMacValue'] = True
                else:
                    self.log.WARN("verifyResponseValue: CheckMacValue incorrect!")
                    result['verifyCheckMacValue'] = False
                return result
            else:
                raise ValueError("verifyAllowanceInvalidReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyAllowanceInvalidReturn: Received expect_args_dict is not a dictionary.")

    def verifyResponseValue(self, invalid_dict, allowance_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id, 'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(invalid_dict, expect_args_dict, datatype='dictionary')
                if invalid_dict['IA_Invoice_No'] is not False:
                    result['verifyInvoiceNoNotEmpty'] = True
                    if invalid_dict['IA_Invoice_No'] == allowance_dict['IA_Invoice_No']:
                        result['verifyInvoiceNumber'] = True
                    else:
                        result['verifyInvoiceNumber'] = False
                        self.log.WARN("verifyAllowanceInvalidReturn: InvoiceNumbers are not the same between Allowance "
                                      "and AllowanceInvalid.\nAllowance: %s\nAllowanceInvalid: %s" % (allowance_dict['IA_Invoice_No'], invalid_dict['IA_Invoice_No']))
                else:
                    result['verifyInvoiceNoNotEmpty'] = False
                    self.log.WARN("verifyAllowanceInvalidReturn: InvoiceNumber is empty!\n"
                                  "Allowance: %s\nAllowanceInvalid: %s" % (allowance_dict['IA_Invoice_No'], invalid_dict['IA_Invoice_No']))
                chkMacValue = invalid_dict['CheckMacValue']
                invalid_dict.pop('CheckMacValue')
                genCheckMacValue = self.genChkMacVal(invalid_dict, mode='local')
                if genCheckMacValue == chkMacValue:
                    result['verifyCheckMacValue'] = True
                else:
                    self.log.WARN("verifyResponseValue: CheckMacValue incorrect!")
                    result['verifyCheckMacValue'] = False
                return result
            else:
                raise ValueError("verifyAllowanceInvalidReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyAllowanceInvalidReturn: Received expect_args_dict is not a dictionary.")

    def verifyCheckMacValue(self, res_dict, gen_result):
        result = {}
        result['verifyCheckMacValue'] = self.verifyRtnData(res_dict, gen_result, datatype='dictionary')
        return result
