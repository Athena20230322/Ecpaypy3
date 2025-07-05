# -*- coding: utf-8 -*-
import time
import json
import LibGeneral.funcGeneral as funcGen
import urllib.request, urllib.parse, urllib.error
import collections
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class verifyInvOfflineQueryOfflineMerchantPosSetting(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'InvOfflineQueryOfflineMerchantPosSetting'
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
        res_dict=self.returnBodyToDicb2c(res_dict)
        print((list(res_dict.keys())))
        result = {}
        # print "AAA"
        # print expect_args_dict
        # print res_dict
        # print "AAA"
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) == len(res_dict):
                    result['verifyColumnAmount'] = True
                else:
                    result['verifyColumnAmount'] = False
                    raise ValueError("verifyInvQueryReturn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyInvQueryReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvQueryReturn: Received expect_args_dict is not a dictionary.")
    def verifyInjection(self, res_dict, query_info, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id, 'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        print(res_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyInjection'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                if query_info['RelateNumber'] == res_dict['IIS_Relate_Number']:
                    result['verifyRelateNum'] = True
                else:
                    result['verifyRelateNum'] = False
                return result
            else:
                raise ValueError("verifyInjection: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInjection: Received expect_args_dict is not a dictionary.")

    def verifyResponseValue(self, res_dict, inv_dict, inv_rtn, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyData']
        print(expect_args_dict)
        inv_dict=self.returnBodyToDicb2c(inv_dict)
        res_dict = self.returnBodyToDicb2c(res_dict)
        inv_rtn=self.returnBodyToDicb2c(inv_rtn)
        print(inv_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                revert_list = ['PosBarCode', 'QRCode_Left', 'QRCode_Right','SpecialTaxType']
                revert_dict = {}
                for key in revert_list:
                    revert_dict[key] = res_dict[key]
                    res_dict.pop(key)
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                res_dict.pop('ItemSeq')
                res_dict.pop('RtnCode')
                res_dict.pop('RtnMsg')
                res_dict.update(revert_dict)
                res_dict.pop('QRCode_Right')
                res_dict.pop('PosBarCode')
                res_dict.pop('QRCode_Left')
                res_dict.pop('SpecialTaxType')
                for key in res_dict:
                    result['verify'+key] = self.compare(key, res_dict, inv_dict, inv_rtn)
                return result
            else:
                raise ValueError("verifyInvIssueReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvIssueReturn: Received expect_args_dict is not a dictionary.")

    def verifyResponseValueTax(self, res_dict, inv_dict, inv_rtn, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyData']
        print(expect_args_dict)
        inv_dict=self.returnBodyToDicb2c(inv_dict)
        res_dict = self.returnBodyToDicb2c(res_dict)
        inv_rtn=self.returnBodyToDicb2c(inv_rtn)
        print(inv_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                revert_list = ['PosBarCode', 'QRCode_Left', 'QRCode_Right','SpecialTaxType']
                revert_dict = {}
                for key in revert_list:
                    revert_dict[key] = res_dict[key]
                    res_dict.pop(key)
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                res_dict.pop('ItemSeq')
                res_dict.pop('RtnCode')
                res_dict.pop('RtnMsg')
                res_dict.pop('IIS_Tax_Rate')
                res_dict.update(revert_dict)
                res_dict.pop('QRCode_Right')
                res_dict.pop('PosBarCode')
                res_dict.pop('QRCode_Left')
                res_dict.pop('SpecialTaxType')
                for key in res_dict:
                    result['verify'+key] = self.compare(key, res_dict, inv_dict, inv_rtn)
                return result
            else:
                raise ValueError("verifyInvIssueReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvIssueReturn: Received expect_args_dict is not a dictionary.")

    def verifyCertainResponseValue(self, res_dict, inv_dict, inv_rtn, case_id, certain_keys):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        expect_args_dict = all_verify_data['verifyReturnValue']
        print(expect_args_dict)
        print(inv_dict)
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                result['verifyRtnCodeAndMsg'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
                for key in certain_keys:
                    result['verify'+key] = self.compare(key, res_dict, inv_dict, inv_rtn)
                return result
            else:
                raise ValueError("verifyInvIssueReturn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyInvIssueReturn: Received expect_args_dict is not a dictionary.")

    def verifyResponseValueb2c(self, case_id, data, status='success'):
            all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                   'Verification.ini')
            expect_data = all_verify_data['verifyData']
            result = {}
            data=json.loads(data)
            print(data['RtnCode'])
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

    def __valueIsEmpty(self, data):
            for key in list(data.keys()):
                if len(data[key]) > 0:
                    pass
                else:
                    return False
            return True

    def verifyFlag(self, res_dict, key, value):
        result = {}
        if res_dict[key] == value:
            result['verify'+key] = True
        else:
            result['verify'+key] = False
        return result

    def compare(self, key, res_dict, inv_dict, inv_rtn):
        correspond_dict = {
            'IIS_Mer_ID': ['inv_dict', 'MerchantID'],
            'IIS_Number': ['inv_rtn', 'InvoiceNo'],
            'IIS_Relate_Number': ['inv_dict', 'RelateNumber'],
            'IIS_Customer_ID': ['inv_dict', 'CustomerID'],
            'IIS_Identifier': ['inv_dict', 'CustomerIdentifier'],
            'IIS_Customer_Name': ['inv_dict', 'CustomerName'],
            'IIS_Customer_Addr': ['inv_dict', 'CustomerAddr'],
            'IIS_Customer_Phone': ['inv_dict', 'CustomerPhone'],
            'IIS_Customer_Email': ['inv_dict', 'CustomerEmail'],
            'IIS_Clearance_Mark': ['inv_dict', 'ClearanceMark'],
            'IIS_Type': ['inv_dict', 'InvType'],
            'IIS_Category': 'B2C',
            'IIS_Tax_Type': ['inv_dict', 'TaxType'],
            'IIS_Tax_Rate': '0.050',
            'IIS_Tax_Amount': ['inv_dict', 'ItemCount', 'ItemPrice', 'SalesAmount'],
            'IIS_Sales_Amount': ['inv_dict', 'SalesAmount'],
            'IIS_Check_Number': 'P',
            'IIS_Carrier_Type': ['inv_dict', 'CarrierType'],
            'IIS_Carrier_Num': ['inv_dict', 'CarrierNum'],
            'IIS_Love_Code': ['inv_dict', 'LoveCode'],
            'IIS_IP': '211.23.76.78',
            'IIS_Create_Date': ['inv_rtn', 'InvoiceDate'],
            'IIS_Issue_Status': '1',
            'IIS_Invalid_Status': '0',
            'IIS_Upload_Status': '0',
            'IIS_Upload_Date': '',
            'IIS_Turnkey_Status': '',
            'IIS_Remain_Allowance_Amt': '0',
            'IIS_Print_Flag': ['inv_dict', 'Print'],
            'IIS_Award_Flag': '',
            'IIS_Award_Type': '0',
            'ItemName': ['inv_dict', 'ItemName'],
            'ItemCount': ['inv_dict', 'ItemCount'],
            'ItemSeq': ['inv_dict', 'ItemSeq'],
            'ItemWord': ['inv_dict', 'ItemWord'],
            'ItemPrice': ['inv_dict', 'ItemPrice'],
            'ItemTaxType': ['inv_dict', 'ItemTaxType'],
            'ItemAmount': ['inv_dict', 'ItemAmount'],
            'ItemRemark': ['inv_dict', 'ItemRemark'],
            'IIS_Random_Number': ['inv_rtn', 'RandomNumber'],
            'InvoiceRemark': ['inv_dict', 'InvoiceRemark']
        }
        if key == 'IIS_Identifier':
            if correspond_dict[key][0] == 'inv_dict':
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                self.log.INFO('inv_dict[%s]=%s' % (correspond_dict[key][1], inv_dict[correspond_dict[key][1]]))
                if res_dict[key] == '0000000000' and inv_dict[correspond_dict[key][1]] == '':
                    return True
                else:
                    return True if res_dict[key] == inv_dict[correspond_dict[key][1]] else False
            else:
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                self.log.INFO('inv_rtn[%s]=%s' % (correspond_dict[key][1], inv_rtn[correspond_dict[key][1]]))
                if res_dict[key] == '0000000000' and inv_rtn[correspond_dict[key][1]] == '':
                    return True if res_dict[key] == inv_rtn[correspond_dict[key][1]] else False
        elif key == 'IIS_Tax_Amount':
            if correspond_dict[key][0] == 'inv_dict':
                item_count = inv_dict[correspond_dict[key][1]].split('|')
                item_price = inv_dict[correspond_dict[key][2]].split('|')
                total = 0
                for i in range(len(item_count)):
                    total += (float(item_count[i]) * float(item_price[i]))
                total=round(total)
                tax_amount = int(total) - int(inv_dict[correspond_dict[key][3]])

                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                self.log.INFO('tax_amount=%s' % (tax_amount))
                return True if res_dict[key] == str(tax_amount) else False
            else:
                item_count = inv_rtn[correspond_dict[key][1]].split('|')
                item_price = inv_rtn[correspond_dict[key][2]].split('|')
                total = 0
                for i in range(len(item_count)):
                    total += (float(item_count[i]) * float(item_price[i]))
                tax_amount = total - int(inv_rtn[correspond_dict[key][3]])
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                self.log.INFO('tax_amount=%s' % (tax_amount))
                return True if res_dict[key] == str(tax_amount) else False
        elif key == 'IIS_Award_Flag':
            if res_dict['IIS_Identifier'] != '0000000000':
                self.log.INFO('res_dict[IIS_Identifier]=%s' % (res_dict['IIS_Identifier']))
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                return True if res_dict[key] == 'X' else False
            elif res_dict['IIS_Love_Code'] != '0':
                self.log.INFO('res_dict[IIS_Love_Code]=%s' % (res_dict['IIS_Love_Code']))
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                return True if res_dict[key] == '' else False
            else:
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                return True if res_dict[key] == '' else False
        elif key == 'IIS_Love_Code':
            if correspond_dict[key][0] == 'inv_dict':
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                self.log.INFO('inv_dict[%s]=%s' % (correspond_dict[key][1], inv_dict[correspond_dict[key][1]]))
                if res_dict[key] == '0' and inv_dict[correspond_dict[key][1]] == '':
                    return True
                else:
                    return True if res_dict[key] == inv_dict[correspond_dict[key][1]] else False
            else:
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                self.log.INFO('inv_rtn[%s]=%s' % (correspond_dict[key][1], inv_rtn[correspond_dict[key][1]]))
                if res_dict[key] == '0' and inv_rtn[correspond_dict[key][1]] == '':
                    return True
                else:
                    return True if res_dict[key] == inv_rtn[correspond_dict[key][1]] else False
        elif key == 'IIS_Customer_Email':
            self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
            self.log.INFO('inv_dict[%s]=%s' % (correspond_dict[key][1], urllib.parse.unquote(inv_dict[correspond_dict[key][1]])))
            if res_dict[key] == urllib.parse.unquote(inv_dict[correspond_dict[key][1]]):
                return True
            else:
                return False
        elif key == 'IIS_Carruer_Num':
            if res_dict['IIS_Carruer_Type'] == '1':
                self.log.INFO('res_dict[IIS_Carruer_Type] = %s' % (res_dict['IIS_Carruer_Type']))
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                return True if res_dict[key] == '53538851' + res_dict['IIS_Relate_Number'] else False
        else:
            if type(correspond_dict[key]) is str:
                self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                return True if res_dict[key] == correspond_dict[key] else False
            else:
                if correspond_dict[key][0] == 'inv_dict':
                    self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                    self.log.INFO('inv_dict[%s]=%s' % (correspond_dict[key][1], inv_dict[correspond_dict[key][1]]))
                    return True if res_dict[key] == inv_dict[correspond_dict[key][1]] else False
                else:
                    self.log.INFO('res_dict[%s]=%s' % (key, res_dict[key]))
                    self.log.INFO('inv_rtn[%s]=%s' % (correspond_dict[key][1], inv_rtn[correspond_dict[key][1]]))
                    return True if res_dict[key] == inv_rtn[correspond_dict[key][1]] else False

    def verifyUrlEncode(self, res_dict, columns):
        result = {}
        for item in columns:
            if '%' in res_dict[item]:
                result['verify'+item] = True
            else:
                result['verify'+item] = False
        return result

    def verifyNotEmpty(self, column, res_dict):
        result = {}
        print(res_dict[column])
        if res_dict[column] != '':
            result['verifyNotEmpty'] = True
        else:
            result['verifyNotEmpty'] = False
        return result

    def verifyAllowance(self, res_dict, all_dict):
        result = {}
        if res_dict['IIS_Remain_Allowance_Amt'] == all_dict['IA_Remain_Allowance_Amt']:
            result['verifyRemainAllowance'] = True
        else:
            result['verifyRemainAllowance'] = False
        return result

