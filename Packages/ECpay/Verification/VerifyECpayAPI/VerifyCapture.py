# -*- coding: utf-8 -*-
import time
import json
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActCapture import actCapture

class verifyCapture(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'Capture'
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat=self.category,
                                                                feature_name=self.fea_name)
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']        
        APIHelper.__init__(self, hash_key, hash_iv)
        self.hkey = hash_key
        self.hiv = hash_iv
        self.htm_helper = HtmlHelper()
        self.raw_sess = self.genSession()

    def verifyResponseColumnName(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyPaymentReturn']
        print(expect_args_dict)
        print(res_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = {}
                expect_list = sorted(expect_args_dict.keys())
                print(('expect_list: ' + str(len(expect_list))))
                print(('res_dict: ' + str(len(res_dict))))
                if len(expect_list) != len(res_dict):
                    result['VerifyReturnKey'] = False
                    return result
                for exp in expect_list:
                    if exp in res_dict:
                        break
                    else:
                        result['VerifyReturnKey'] = False
                        return result
                result['VerifyReturnKey'] = True
                return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Recieved expect_args_dict is not an dictionary")

    def verifyCaptureInfo(self, order_dict, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyPaymentReturn']
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = {}
                if expect_args_dict['RtnCode'] == '1':
                    if (expect_args_dict['RtnCode'] == str(res_dict['RtnCode'])
                            and expect_args_dict['RtnMsg'].decode('utf-8') == res_dict['RtnMsg']
                            and order_dict['MerchantID'] == res_dict['MerchantID']
                            and order_dict['MerchantTradeNo'] == res_dict['MerchantTradeNo']
                            and res_dict['AllocationDate'] != '' and res_dict['AllocationDate'] is not None):
                        query = actCapture()
                        query_dict = query.queryTradeInfo(order_dict)
                        if res_dict['TradeNo'] == query_dict['TradeNo']:
                            print('TradeNo correct!')
                            result['VerifyReturnKey'] = True
                        else:
                            print((res_dict['TradeNo']))
                            print((query_dict['TradeNo']))
                            result['VerifyReturnKey'] = False
                            print('TradeNo wrong!')
                    else:
                        result['VerifyReturnKey'] = False
                        print('RtnCode/RtnMsg/MerchantID/MerchantTradeNo/AllocationDate wrong!')
                else:
                    if(expect_args_dict['RtnCode'] == str(res_dict['RtnCode'])
                       and expect_args_dict['RtnMsg'].decode('utf-8') == res_dict['RtnMsg']
                       and order_dict['MerchantID'] == res_dict['MerchantID']
                       and order_dict['MerchantTradeNo'] == res_dict['MerchantTradeNo']
                       and res_dict['AllocationDate'] == ''):
                        result['VerifyReturnKey'] = True
                    else:
                        print('RtnCode != 1, RtnCode/RtnMsg/MerchantID/MerchantTradeNo/AllocationDate wrong')
                        result['VerifyReturnKey'] = False
                return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Received expect_args_dict is not an dictionary")

    def verifyInjectResult(self, order_dict, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        for key in res_dict:
            if type(res_dict[key]) is int:
                res_dict[key] = str(res_dict[key])
        expect_args_dict = all_verify_data['verifyPaymentReturn']
        for key in expect_args_dict:
            expect_args_dict[key] = expect_args_dict[key].decode('utf-8')
        print(expect_args_dict)
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result = {}
                result['VerifyReturnKey'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if (order_dict['MerchantID'] == res_dict['MerchantID']
                        and order_dict['MerchantTradeNo'] == res_dict['MerchantTradeNo']
                        and (res_dict['AllocationDate'] == '' or res_dict['AllocationDate'] is None)):
                    result['VerifyMerchantData'] = True
                    query = actCapture()
                    query_dict = query.queryTradeInfo(order_dict)
                    if res_dict['TradeNo'] == query_dict['TradeNo']:
                        result['VerifyTradeNo'] = True
                        return result
                    else:
                        self.log.WARN(
                            "Return string comparing not match or AllocationDate is null, "
                            "return body : %s \n Sample TradeNo : %s \n Expected TradeNo: %s." % (
                            res_dict, res_dict['TradeNo'], query_dict['TradeNo']))
                        result['VerifyTradeNo'] = False
                        return result
                else:
                    result['VerifyMerchantData'] = False
                    self.log.WARN("Return string comparing not match: \n MerchantID : Sample %s, Expected %s, \n "
                                  "MerchantTradeNo : Sample %s, Expected %s, \n AllocationDate=%s"
                                  %(res_dict['MerchantID'], order_dict['MerchantID'], res_dict['MerchantTradeNo'],
                                    order_dict['MerchantTradeNo'], res_dict['AllocationDate']))
                    return result
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Received expect_args_dict is not an dictionary")

    def verifyPlatformCharge(self, order_dict, query_fee):
        result = {}
        if order_dict['PlatformChargeFee'] == query_fee:
            result['VerifyChargeFee'] = True
        else:
            self.log.WARN('ChargeFee not match: Sample %s, Expected %s' % (query_fee, order_dict['PlatformChargeFee']))
            result['VerifyChargeFee'] = False
        return result

    def verifyRefundInfo(self, order_dict, information):
        result = {}
        query = actCapture()
        query_dict = query.queryTradeInfo(order_dict)
        if information['TradeNo'] == query_dict['TradeNo']:
            if information['refundAMT'] == query_dict['UserRefundAMT']:
                result['verifyRefundAMT'] = True
            else:
                result['verifyRefundAMT'] = False
        else:
            result['TradeNoMatch'] = False
        return result

    def verifyQueryOTP(self, phone_no):
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI',
                                                                feature_name='Capture')
        result = {}
        for _ in range(3):
            time.sleep(10)
            dic_otp_queryinfo = {
                            'CellNo': phone_no,
                            'OTPType': 'ECpay_Refund',
                            'TimeRange': 50
                            }
            otp_query = self.getRequestFromAPI(dic_otp_queryinfo, self.feature_conf['OtpCollectorAddr'])
            if otp_query != 'Not_Found':
                result['verifyOTP'] = False
                return result
        result['verifyOTP'] = True
        return result