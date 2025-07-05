import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyCreditDetail(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'CreditDetail'
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

    def verifyColumns(self, case_id, res_dict, data):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_dict = all_verify_data['verifyReturn']
        expect_data = all_verify_data['verifyData']
        result = {}
        if type(expect_dict) is dict:
            if len(expect_dict) > 0:
                for key in list(res_dict.keys()):
                    res_dict[key] = ''
                result['VerifyColumnNames'] = self.verifyRtnData(res_dict, expect_dict, datatype='dictionary')
            else:
                raise ValueError("verifyColumns: Length of expect_dict cannot be zero.")
        else:
            raise TypeError("verifyColumns: Received expect_dict is not a dictionary.")
        if type(expect_data) is dict:
            if len(expect_data) > 0:
                for key in list(data.keys()):
                    data[key] = ''
                result['VerifyDataColumnNames'] = self.verifyRtnData(data, expect_data, datatype='dictionary')
            else:
                raise ValueError("verifyColumns: Length of expect_data cannot be zero.")
        else:
            TypeError("verifyColumns: Received expect_data is not a dictionary.")
        return result

    def verifyResponseValues(self, case_id, res_dict, data, status='success'):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_dict = all_verify_data['verifyReturn']
        expect_data = all_verify_data['verifyData']
        result = {}
        res_dict['TransMsg']=str(res_dict['TransMsg'])
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
        data['RtnCode']=str(data['RtnCode'])
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

    def verifyResponseValuesQueryThreeD(self, case_id, res_dict, data, status='success'):
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
       # data['AuthCode'] = str(data['AuthCode'])
       # data['amount'] = str(data['amount'])
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
       # is_empty_check_dict['AuthCode'] = data['AuthCode']
       # is_empty_check_dict['amount'] = data['amount']
        if status == 'success':
            result['verifyNotEmptyValues'] = self.__valueIsEmpty(is_empty_check_dict)
        else:
            result['verifyMustEmptyValues'] = not self.__valueIsEmpty(is_empty_check_dict)
        return result

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
        data['RtnMsg'] = str(data['RtnMsg'])
        if type(expect_data) is dict:
            if len(expect_data) > 0:
                result['VerifyDataValues'] = self.verifyRtnData(data, expect_data, datatype='dictionary')
            else:
                raise ValueError("verifyResponseValues: Length of expect_data cannot be zero.")
        else:
            raise TypeError("verifyResponseValues: Received expect_data is not a dictionary.")
        is_empty_check_dict = {}
        is_empty_check_dict['RtnMsg'] = data['RtnMsg']
        if status == 'Authorized':
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
