import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyShopifyN(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'ShopifyN'
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

    def verifyColumn(self,  case_id,res_dict):
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

    def verifyResponseValuesb2b(self, case_id, data, status='success'):
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
    def verifyResponseValuesforApp(self, case_id, data, status='success'):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_data = all_verify_data['verifyData']
        result = {}
        # for key in data.keys():
        #     if data[key] is not None:
        #         data[key] = data[key].encode('utf-8')
        #     else:
        #         data[key] = ''

        data=eval(data)
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

    def __valueIsEmpty(self, data):
        for key in list(data.keys()):
            if len(data[key]) > 0:
                pass
            else:
                return False
        return True
    def verifyColumn(self, case_id,res_dict):
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
    def verifyPaymentReturn(self, data, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                                self.fea_name,
                                                                case_id,
                                                                'Verification.ini')
        expect_data = all_verify_data['verifyData']
        orderinfo=data['OrderInfo']
        TradeStatus=orderinfo['TradeStatus']
        print(data)
        print(orderinfo)
        print(TradeStatus)
        result = {}
        if type(expect_data) is dict:
            if len(expect_data) > 0:
                result['VerifyDataValues'] = self.verifyRtnData(orderinfo, expect_data, datatype='dictionary')
            else:
                raise ValueError("verifyResponseValues: Length of expect_data cannot be zero.")
        else:
            raise TypeError("verifyResponseValues: Received expect_data is not a dictionary.")
        is_empty_check_dict = {}
        is_empty_check_dict['TradeStatus'] = orderinfo['TradeStatus']
        status = 'success'
        if status == 'success':
            result['verifyNotEmptyValues'] = self.__valueIsEmpty(is_empty_check_dict)
        else:
            result['verifyMustEmptyValues'] = not self.__valueIsEmpty(is_empty_check_dict)
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
       # query_dict['TimeStamp'] = unix_time[1]
       # query_dict['PlatformID'] = ''
        query_dict['TradeStatus'] = mercid
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

    def verifyResponseValuesThreeD(self, case_id, res_dict, data, status='success'):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_data = all_verify_data['verifyData']
        result = {}
        res_dict['TransMsg'] = str(res_dict['TransMsg'])
        res_dict['MerchantID'] = str(res_dict['MerchantID'])
        res_dict['TransCode'] = str(res_dict['TransCode'])
        res_dict['TransMsg'] = res_dict['TransMsg'].rstrip(' ')
        data['RtnCode'] = str(data['RtnCode'])
        data['MerchantID'] = str(data['MerchantID'])
        data['RtnMsg'] = str(data['RtnMsg'])
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
        is_empty_check_dict['RtnMsg'] = data['RtnMsg']
        if status == 'success':
            result['verifyNotEmptyValues'] = self.__valueIsEmpty(is_empty_check_dict)
        else:
            result['verifyMustEmptyValues'] = not self.__valueIsEmpty(is_empty_check_dict)
        return result
    def __valueIsEmpty(self, data):
        for key in list(data.keys()):
            if len(data[key]) > 0:
                pass
            else:
                return False
        return True