from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper

class verifyInvAllowance(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvAllowance'
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
                    raise ValueError("verifyInvAllowanceReturn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyInvAllowanceReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvAllowanceReturn: Received expect_args_dict is not a dictionary.")

    def verifyResponseValue(self, inv_info, inv_rtn, all_info, all_rtn, case_id, mode):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(all_rtn, expect_args_dict, datatype='dictionary')
                if mode == 'success':
                    # InvoiceNumber
                    if all_rtn['IA_Invoice_No'] is not False:
                        result['verifyInvoiceNoNotEmpty'] = True
                        if all_rtn['IA_Invoice_No'] == inv_rtn['InvoiceNumber']:
                            result['verifyInvoiceNumber'] = True
                        else:
                            result['verifyInvoiceNumber'] = False
                            self.log.WARN("verifyInvAllowanceReturn: InvoiceNumbers are not the same between issue and "
                                          "allowance.\nInvIssue: %s\nInvAllowance: %s" % (inv_rtn['InvoiceNumber'],
                                                                                          all_rtn['IA_Invoice_No']))
                    else:
                        result['verifyInvoiceNoNotEmpty'] = False
                        self.log.WARN("verifyInvAllowanceReturn: InvoiceNumber is empty!\n"
                                      "InvIssue: %s.\nInvAllowance: %s" % (inv_rtn['InvoiceNumber'],
                                                                           all_rtn['IA_Invoice_No']))

                    # AllowanceNo, AllowanceDate not Empty
                    if all_rtn['IA_Allow_No'] is not False and all_rtn['IA_Date'] is not False:
                        result['verifyAllowNoAndDate'] = True
                    else:
                        result['verifyAllowNoAndDate'] = False
                        self.log.WARN("verifyInvAllowanceReturn: IA_Allow_No or IA_Date is empty!\n"
                                      "IA_Allow_No=%s\nIA_Date=%s" % (all_rtn['IA_Allow_No'], all_rtn['IA_Date']))

                    # Remain Amount
                    if all_rtn['IA_Remain_Allowance_Amt'] is not False:
                        result['verifyRemainAmtNotEmpty'] = True
                        if int(inv_info['SalesAmount']) - int(all_info['AllowanceAmount']) == int(all_rtn['IA_Remain_Allowance_Amt']):
                            result['verifyRemainAmt'] = True
                        else:
                            result['verifyRemainAmt'] = False
                            self.log.WARN("verifyInvAllowanceReturn: AI_Remain_Allowance_Amt is incorrect!\n"
                                          "SalesAmt=%s\nAllowanceAmt=%s\nRemain=%s" % (inv_info['SalesAmount'], all_info['AllowanceAmount'],
                                                                                       all_rtn['IA_Remain_Allowance_Amt']))
                    else:
                        result['verifyRemainAmtNotEmpty'] = False
                        self.log.WARN("verifyInvAllowanceReturn: IA_Remain_Allowance_Amt is empty!")
                else:
                    if all_rtn['IA_Allow_No'] and all_rtn['IA_Invoice_No'] and all_rtn['IA_Date'] is False:
                        result['verifyFailCase'] = True
                    else:
                        result['verifyFailCase'] = False
                        self.log.WARN("verifyInvAllowanceReturn: IA_Allow_No or IA_Invoice_No or IA_Date is not empty\n"
                                      "IA_Allow_No=%s.\nIA_Invoice_No=%s\nIA_Date=%s" % (all_rtn['IA_Allow_No'],
                                                                                         all_rtn['IA_Invoice_No'],
                                                                                         all_rtn['IA_Date']))
                chkMacValue = all_rtn['CheckMacValue']
                all_rtn.pop('CheckMacValue')
                genCheckMacValue = self.genChkMacVal(all_rtn, mode='local')
                if genCheckMacValue == chkMacValue:
                    result['verifyCheckMacValue'] = True
                else:
                    self.log.WARN("verifyResponseValue: CheckMacValue incorrect!")
                    result['verifyCheckMacValue'] = False
                return result
            else:
                raise ValueError("verifyInvAllowanceReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvAllowanceReturn: Received expect_args_dict is not a dictionary.")
