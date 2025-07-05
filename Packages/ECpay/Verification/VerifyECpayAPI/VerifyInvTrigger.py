import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyInvTrigger(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvTrigger'
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
                    raise ValueError("verifyInvTriggerReturn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyInvTriggerReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvTriggerReturn: Received expect_args_dict is not a dictionary.")

    def verifyResponseValue(self, res_dict, delay_rtn_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if res_dict['Tsr'] == delay_rtn_dict['OrderNumber']:
                    result['verifyTSR'] = True
                else:
                    self.log.WARN("verifyInvTriggerReturn: TSR not match!\nTrigger: %s\nDelay: %s" % (res_dict['Tsr'], delay_rtn_dict['OrderNumber']))
                    result['verifyTSR'] = False
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
                raise ValueError("verifyInvTriggerReturn: Length of expected result cannot be zero!")
        else:
            raise TypeError("verifyInvTriggerReturn: Received expect_args_dict is not a dictionary!")

    def verifyInjection(self, res_dict, delay_rtn_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
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
                raise ValueError("verifyInvTriggerReturn: Length of expected result cannot be zero!")
        else:
            raise TypeError("verifyInvTriggerReturn: Received expect_args_dict is not a dictionary!")

    def verifyChkValue(self, res_dict, chksum):
        result = {}
        if res_dict['CheckMacValue'] == chksum:
            result['verifyCheckMacValue'] = True
        else:
            self.log.WARN("verifyInvTriggerReturn: CheckMacValue not match!\nAPI: %s\nself generate: %s" % (res_dict['CheckMacValue'], chksum))
            result['verifyCheckMacValue'] = False
        return result
