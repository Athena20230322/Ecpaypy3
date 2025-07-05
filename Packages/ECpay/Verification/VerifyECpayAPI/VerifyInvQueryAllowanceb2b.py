import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import urllib.request, urllib.parse, urllib.error

class verifyInvQueryAllowanceb2b(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvQueryAllowanceb2b'
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

    def verifyStatusResult(self, res_info, match_str):
        result = {}
        if res_info.find(match_str) != -1:
            result['verifyStatusResult'] = True
            return result
        else:
            result['verifyStatusResult'] = False
            return result

    def verifyInvQueryAllowanceResult(self, req_info, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,self.fea_name,case_id,
                                                               'Verification.ini')
        if 'verifyInvQueryAllowanceResult' in all_verify_data:
            expect_args_dict = all_verify_data['verifyInvQueryAllowanceResult']
        else:
            raise ValueError("verifyInvQueryAllowanceResult: Secion 'verifyInvQueryAllowanceResult' not found in Verification.ini")

        req_info_dict = self.returnBodyToDic(req_info)

        for dictkey in req_info_dict:
            req_info_dict[dictkey] = ''

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) == len(req_info_dict):
                result = {}
                result['verifyInvQueryAllowanceResult'] = self.verifyRtnData(req_info_dict, expect_args_dict, datatype='dictionary')
                return result
            else:
                raise ValueError("verifyInvQueryAllowanceResult: the amount of columns is not equal to the expected result.")
        else:
            raise TypeError("verifyInvQueryAllowanceResult: Recieved expect_args_dict is not an dictionary")

    def verifyInvQueryAllowanceRequestInfo(self, req_info):
        expect_args_dict = self.returnBodyToDicb2c(req_info)
        print(req_info)
        exclusive_args = ['AllowanceNo', 'AllowanceNumber', 'AllowanceDate','Seller_Identifier','Buyer_Identifier','AllowanceType','ExchangeStatus', 'Upload_Status', 'Buyer_Name','Buyer_Address','Buyer_TelephoneNumber','Buyer_EmailAddress','Seller_Name','Invalid_Status', 'OriginalInvoiceNumber','TaxType', 'TotalAmount',

                          'IP','ConfirmDate','OriginalSequenceNumber','OriginalDescription','InvoiceType','AllowanceSequenceNumber','BalanceAmount','TaxAmount', 'Upload_Date']

        query_dict = {}
        for dictkey in expect_args_dict:
            query_dict[dictkey] = expect_args_dict[dictkey]
        for param in exclusive_args:
            query_dict.pop(param)


        query_dict['AllowanceNo'] = expect_args_dict['AllowanceNo']
        query_dict['AllowanceNumber'] = expect_args_dict['AllowanceNumber']
        query_dict['AllowanceDate'] = expect_args_dict['AllowanceDate']
        query_dict['Seller_Identifier'] = expect_args_dict['Seller_Identifier']
        query_dict['Buyer_Identifier'] = expect_args_dict['Buyer_Identifier']
        query_dict['AllowanceType'] = expect_args_dict['AllowanceType']
        query_dict['Invalid_Status'] = expect_args_dict['Invalid_Status']
        query_dict['ExchangeStatus'] = expect_args_dict['ExchangeStatus']
        query_dict['Upload_Status'] = expect_args_dict['Upload_Status']
        query_dict['Buyer_Name'] = expect_args_dict['Buyer_Name']
        query_dict['Buyer_Address'] = expect_args_dict['Buyer_Address']
        query_dict['Buyer_TelephoneNumber'] = expect_args_dict['Buyer_TelephoneNumber']
        query_dict['Buyer_EmailAddress'] = expect_args_dict['Buyer_EmailAddress']
        query_dict['Seller_Name'] = expect_args_dict['Seller_Name']
        query_dict['TotalAmount'] = expect_args_dict['TotalAmount']
        query_dict['TaxAmount'] = expect_args_dict['TaxAmount']
        query_dict['IP'] = expect_args_dict['IP']
        query_dict['Upload_Date'] = expect_args_dict['Upload_Date']
        query_dict['ConfirmDate'] = expect_args_dict['ConfirmDate']
        query_dict['OriginalInvoiceNumber'] = expect_args_dict['OriginalInvoiceNumber']
        query_dict['OriginalSequenceNumber'] = expect_args_dict['OriginalSequenceNumber']
        query_dict['OriginalDescription'] = expect_args_dict['OriginalDescription']
        query_dict['InvoiceType'] = expect_args_dict['InvoiceType']
        query_dict['TaxType'] = expect_args_dict['TaxType']
        query_dict['AllowanceSequenceNumber'] = expect_args_dict['AllowanceSequenceNumber']
        query_dict['BalanceAmount'] = expect_args_dict['BalanceAmount']










        print('Query_dict: ', query_dict)

        print(expect_args_dict)

        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if expect_args_dict['RtnCode'] is '1':
                    result = {}
                    result['verifyInvQueryAllowanceRequestInfo'] = True
                    return result
                else:
                    Error_result = 'Result: ' + req_info
                    self.log.WARN(Error_result)
                    raise ValueError("verifyInvQueryAllowanceRequestInfo: RtnCode is not one ")
            else:
                raise ValueError("verifyInvQueryAllowanceRequestInfo: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyInvQueryAllowanceRequestInfo: Recieved expect_args_dict is not an dictionary.")

    def verifyInvQueryAllowanceResultb2b(self, req_info, case_id):
            all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                   'Verification.ini')
            if 'verifyInvQueryAllowanceResult' in all_verify_data:
                expect_args_dict = all_verify_data['verifyInvQueryAllowanceResult']
            else:
                raise ValueError(
                    "verifyInvQueryAllowanceResult: Secion 'verifyInvQueryAllowanceResult' not found in Verification.ini")
            req_info_dict = self.returnBodyToDicb2c2(req_info)
            print((list(req_info_dict.keys())))
            for dictkey in req_info_dict:
                req_info_dict[dictkey] = ''

            if type(expect_args_dict) is dict:
                if len(expect_args_dict) == len(req_info_dict):
                    result = {}
                    result['verifyInvQueryAllowanceResult'] = self.verifyRtnData(req_info_dict, expect_args_dict,
                                                                                 datatype='dictionary')
                    return result
                else:
                    raise ValueError(
                        "verifyInvQueryAllowanceResult: the amount of columns is not equal to the expected result.")
            else:
                raise TypeError("verifyInvQueryAllowanceResult: Recieved expect_args_dict is not an dictionary")
    def verifyInvQueryAllowanceResultb2bforerr(self, req_info, case_id):
            all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                   'Verification.ini')
            if 'verifyInvQueryAllowanceResult' in all_verify_data:
                expect_args_dict = all_verify_data['verifyInvQueryAllowanceResult']
            else:
                raise ValueError(
                    "verifyInvQueryAllowanceResult: Secion 'verifyInvQueryAllowanceResult' not found in Verification.ini")
            req_info_dict = self.returnBodyToDicb2c2(req_info)
            # print(req_info_dict.keys())
            # for dictkey in req_info_dict:
            #     req_info_dict[dictkey] = ''

            if type(expect_args_dict) is dict:
                if len(expect_args_dict) == len(req_info_dict):
                    result = {}
                    result['verifyInvQueryAllowanceResult'] = self.verifyRtnData(req_info_dict, expect_args_dict,
                                                                                 datatype='dictionary')
                    return result
                else:
                    raise ValueError(
                        "verifyInvQueryAllowanceResult: the amount of columns is not equal to the expected result.")
            else:
                raise TypeError("verifyInvQueryAllowanceResult: Recieved expect_args_dict is not an dictionary")



