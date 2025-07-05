# -*- coding:utf-8 -*-
import json
import urllib.request, urllib.parse, urllib.error
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyCrossMap(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'CrossMap'
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

    def verifyExpressFAMIMap(self, driver):
        op = WebOperate.webOperate(driver)
        verify_obj = op.getElem('FamilyPost', find_by='id')
        result = {}
        if verify_obj == False:
            result['verifyExpressFAMIMap'] = False
            return result
        result['verifyExpressFAMIMap'] = True
        return result

    def verifyCrossReturnResult(self, response, case_id):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            res_dict = {}
            for ele in res_list:
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
            print(res_dict)
            res_dict['MerchantTradeNo'] = res_dict['MerchantTradeNo'].encode('utf-8')
            all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                                   'Verification.ini')
            expect_args_dict = all_verify_data['verifyServerReplyRtnData']
            print(expect_args_dict)
            # if type(expect_args_dict) is dict:
            #     if len(expect_args_dict) > 0:
            #         result['verifyRtnData'] = self.verifyRtnData(res_dict, expect_args_dict, datatype='dictionary')
            #         # if res_dict['MerchantTradeNo'] == m_trade_no:
            #         #     result['verifyMerchantTradeNo'] = True
            #         # else:
            #         #     self.log.WARN('MerchantTradeNo not match!\nexpect: %s\nreply: %s' % (m_trade_no, res_dict['MerchantTradeNo']))
            #         #     result['verifyMerchantTradeNo'] = False
            #         # if res_dict['MerchantMemberID'] == m_mid:
            #         #     result['verifyMerchantMemberID'] = True
            #         # else:
            #         #     self.log.WARN('MerchantMemberID not match!\nexpect: %s\nreply: %s' % (m_mid, res_dict['MerchantMemberID']))
            #         #     result['verifyMerchantMemberID'] = False
            #         # if res_dict['process_date'] is not False:
            #         #     result['verifyProcessDate'] = True
            #         # else:
            #         #     self.log.WARN("process_date is empty!")
            #         #     result['verifyProcessDate'] = False
            #         return result
            #     else:
            #         raise ValueError("verifyServerReplyValues: Length of expected result dic cannot be zero.")
            # else:
            #     raise TypeError("verifyServerReplyValues: Received expect_args_dict is not a dictionary.")

    def verifyCrossReturnResult11(self, response, map_req_info):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            res_dict = {}
            print (res_dict)
            # for ele in res_list:
            #     res_dict[ele.split('=')[0]] = ele.split('=')[1]
            # print(res_dict)
            if res_dict['MerchantTradeNo'] != map_req_info['MerchantTradeNo']:
                 self.log.WARN('MerchantTradeNo is different!')
                 result['verifyCrossReturnResult'] = True
            # elif res_dict['MerchantTradeNo'] != map_req_info['MerchantTradeNo']:
            #     self.log.WARN('MerchantTradeNo is different!')
            #     result['verifyCrossReturnResult'] = False
        #     elif res_dict['LogisticsType'] != map_req_info['LogisticsType']:
        #         self.log.WARN('LogisticsType is different!')
        #         result['verifyCrossReturnResult'] = False
        #     elif res_dict['LogisticsSubType'] != map_req_info['LogisticsSubType']:
        #         self.log.WARN('LogisticsSubType is different!')
        #         result['verifyCrossReturnResult'] = False
        #     elif res_dict['ExtraData'] != map_req_info['ExtraData']:
        #         self.log.WARN('ExtraData is different!')
        #         result['verifyCrossReturnResult'] = False
        #     elif res_dict['Country'] != map_req_info['Country']:
        #         self.log.WARN('Country is different!')
        #         result['verifyCrossReturnResult'] = False
        #     elif res_dict['StoreID'] != map_req_info['StoreID']:
        #         self.log.WARN('StoreID is different!')
        #         result['verifyCrossReturnResult'] = False
        #     elif res_dict['StoreZipCode'] != map_req_info['StoreZipCode']:
        #         self.log.WARN('StoreZipCode is different!')
        #         result['verifyCrossReturnResult'] = False
        #     elif res_dict['StoreName'] != map_req_info['StoreName']:
        #         self.log.WARN('StoreName is different!')
        #         result['verifyCrossReturnResult'] = False
        #     elif res_dict['StoreAddress'] != map_req_info['StoreAddress']:
        #         self.log.WARN('StoreAddress is different!')
        #         result['verifyCrossReturnResult'] = False
        #     else:
        #         result['verifyCrossReturnResult'] = True
        # elif response.status_code == 204:
        #     self.log.WARN('status code: 204, cannot found the serverReplyURL value')
        #     result['verifyCrossReturnResult'] = False
        # else:
        #     self.log.WARN('other status code: %d' % response.status_code)
        #     result['verifyCrossReturnResult'] = False
        return result



    def verifyFAMIReturnResult(self, response, map_req_info):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            res_dict = {}
            for ele in res_list:
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
            print(res_dict)
            if res_dict['MerchantID'] != map_req_info['MerchantID']:
                self.log.WARN('MerchantID is different!')
                result['verifyFAMIReturnResult'] = False
            elif res_dict['MerchantTradeNo'] != map_req_info['MerchantTradeNo']:
                self.log.WARN('MerchantTradeNo is different!')
                result['verifyFAMIReturnResult'] = False
            elif res_dict['LogisticsSubType'] != map_req_info['LogisticsSubType']:
                self.log.WARN('LogisticsSubType is different!')
                result['verifyFAMIReturnResult'] = False
            elif res_dict['ExtraData'] != map_req_info['ExtraData']:
                self.log.WARN('ExtraData is different!')
                result['verifyFAMIReturnResult'] = False
            elif res_dict['CVSStoreID'] != '006598':
                self.log.WARN('StoreID is different!')
                result['verifyFAMIReturnResult'] = False
            elif res_dict['CVSStoreName'] != urllib.parse.urlencode({'name': '台醫店'}).split('=')[1]:
                self.log.WARN('StoreName is different!')
                result['verifyFAMIReturnResult'] = False
            elif res_dict['CVSAddress'] != urllib.parse.urlencode({'name': '台北市中正區中山南路７號１樓'}).split('=')[1]:
                self.log.WARN('Address is different!')
                result['verifyFAMIReturnResult'] = False
            elif res_dict['CVSTelephone'] != '02-24326001':
                self.log.WARN('Telephone is different!')
                result['verifyFAMIReturnResult'] = False
            else:
                result['verifyFAMIReturnResult'] = True
        elif response.status_code == 204:
            self.log.WARN('status code: 204, cannot found the serverReplyURL value')
            result['verifyFAMIReturnResult'] = False
        else:
            self.log.WARN('other status code: %d' % response.status_code)
            result['verifyFAMIReturnResult'] = False
        return result

    def verifyUniMartReturnResult(self, response, map_req_info):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            res_dict = {}
            for ele in res_list:
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
            print(res_dict)
            if res_dict['MerchantID'] != map_req_info['MerchantID']:
                self.log.WARN('MerchantID is different!')
                result['verifyMerchantID'] = False
            elif res_dict['MerchantTradeNo'] != map_req_info['MerchantTradeNo']:
                self.log.WARN('MerchantTradeNo is different!')
                result['verifyMerchantTradeNo'] = False
            elif res_dict['LogisticsSubType'] != map_req_info['LogisticsSubType']:
                self.log.WARN('LogisticsSubType is different!')
                result['verifyLogisticsSubType'] = False
            elif res_dict['ExtraData'] != map_req_info['ExtraData']:
                self.log.WARN('ExtraData is different!')
                result['verifyExtraData'] = False
            elif res_dict['CVSStoreID'] != '991182':
                self.log.WARN('StoreID is different!')
                result['verifyCVSStoreID'] = False
            elif res_dict['CVSStoreName'] != urllib.parse.urlencode({'name': '馥樺門市'}).split('=')[1]:
                self.log.WARN('StoreName is different!')
                result['verifyCVSStoreName'] = False
            elif res_dict['CVSAddress'] != urllib.parse.urlencode({'name': '台北市南港區三重路23號1樓'}).split('=')[1]:
                self.log.WARN('Address is different!')
                result['verifyCVSAddress'] = False
            else:
                result['verifyUniMartReturnResult'] = True
        elif response.status_code == 204:
            self.log.WARN('status code: 204, cannot found the serverReplyURL value')
            result['verifyUniMartReturnResult'] = False
        else:
            self.log.WARN('other status code: %d' % response.status_code)
            result['verifyUniMartReturnResult'] = False
        return result

    def verifyHiLifeReturnResult(self, response, map_req_info):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            res_dict = {}
            for ele in res_list:
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
            print(res_dict)
            if res_dict['MerchantID'] != map_req_info['MerchantID']:
                self.log.WARN('MerchantID is different!')
                result['verifyMerchantID'] = False
            elif res_dict['MerchantTradeNo'] != map_req_info['MerchantTradeNo']:
                self.log.WARN('MerchantTradeNo is different!')
                result['verifyMerchantTradeNo'] = False
            elif res_dict['LogisticsSubType'] != map_req_info['LogisticsSubType']:
                self.log.WARN('LogisticsSubType is different!')
                result['verifyLogisticsSubType'] = False
            elif res_dict['ExtraData'] != map_req_info['ExtraData']:
                self.log.WARN('ExtraData is different!')
                result['verifyExtraData'] = False
            elif res_dict['CVSStoreID'] != '2001':
                self.log.WARN('StoreID is different!')
                result['verifyCVSStoreID'] = False
            elif res_dict['CVSStoreName'] != urllib.parse.urlencode({'name': '北市杭州店'}).split('=')[1]:
                self.log.WARN('StoreName is different!')
                result['verifyCVSStoreName'] = False
            elif res_dict['CVSAddress'] != urllib.parse.urlencode({'name': '台北市大安區杭州南路二段５號'}).split('=')[1]:
                self.log.WARN('Address is different!')
                result['verifyCVSAddress'] = False
            elif res_dict['CVSTelephone'] != urllib.parse.urlencode({'name': '02-23579306'}).split('=')[1]:
                self.log.WARN('Telephone is different!')
                result['verifyTelephone'] = False
            else:
                result['verifyUniMartReturnResult'] = True
        elif response.status_code == 204:
            self.log.WARN('status code: 204, cannot found the serverReplyURL value')
            result['verifyUniMartReturnResult'] = False
        else:
            self.log.WARN('other status code: %d' % response.status_code)
            result['verifyUniMartReturnResult'] = False
        return result

    def verifyIsCollection(self):
        result = {}
        result['verifyIsCollection'] = False
        return result

    def verifyDevice(self, element):
        result = {}
        if element is not None:
            print(element)
            result['verifyDevice'] = True
        else:
            result['verifyDevice'] = False
        return result

    def verifyExtraData(self, response):
        result = {}
        if response.status_code != 200:
            self.log.WARN('response status code = ' + str(response.status_code))
            result['verifyStatusCode'] = False
        extraData = response.text.split('&')[8].split('=')[1].split('\"')[0]
        print(extraData)
        if extraData == urllib.parse.urlencode({'name': 'ｔｅｓｔ'}).split('=')[1]:
            print(extraData)
            result['verifyExtraData'] = True
        elif extraData == 'eql2TwentyCharacters':
            print(extraData)
            result['verifyExtraData'] = True
        else:
            result['verifyExtraData'] = False
        return result
