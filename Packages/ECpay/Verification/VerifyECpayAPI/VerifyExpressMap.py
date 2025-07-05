# -*- coding:utf-8 -*-
import json
import urllib.request, urllib.parse, urllib.error
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyExpressMap(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'ExpressMap'
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

    def verifyOKMARTReturnResult(self, response, map_req_info):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            print('432432')
            print(response)
            print(res_list)
            print('542352')
            res_dict = {}
            for ele in res_list:
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
            print(res_dict)
            if res_dict['MerchantID'] != map_req_info['MerchantID']:
                self.log.WARN('MerchantID is different!')
                result['verifyOKMARTReturnResult'] = False
            elif res_dict['MerchantTradeNo'] != map_req_info['MerchantTradeNo']:
                self.log.WARN('MerchantTradeNo is different!')
                result['verifyOKMARTReturnResult'] = False
            elif res_dict['LogisticsSubType'] != map_req_info['LogisticsSubType']:
                self.log.WARN('LogisticsSubType is different!')
                result['verifyOKMARTReturnResult'] = False
            elif res_dict['ExtraData'] != map_req_info['ExtraData']:
                self.log.WARN('ExtraData is different!')
                result['verifyOKMARTReturnResult'] = False
            elif res_dict['CVSStoreID'] != '001328':
                self.log.WARN('StoreID is different!')
                result['verifyOKMARTReturnResult'] = False
            elif res_dict['CVSStoreName'] != urllib.parse.urlencode({'name': '汐止東勢店'}).split('=')[1]:
                self.log.WARN('StoreName is different!')
                result['verifyFAMIReturnResult'] = False
            elif res_dict['CVSAddress'] != urllib.parse.urlencode({'name': '新北市汐止區東勢街127號1樓'}).split('=')[1]:
                self.log.WARN('Address is different!')
                result['verifyOKMARTReturnResult'] = False
            elif res_dict['CVSTelephone'] != '02-66374630':
                self.log.WARN('Telephone is different!')
                result['verifyOKMARTReturnResult'] = False
            else:
                result['verifyOKMARTReturnResult'] = True
        elif response.status_code == 204:
            self.log.WARN('status code: 204, cannot found the serverReplyURL value')
            result['verifyOKMARTReturnResult'] = False
        else:
            self.log.WARN('other status code: %d' % response.status_code)
            result['verifyOKMARTReturnResult'] = False
        return result

    def verifyFAMIReturnResult(self, response, map_req_info):
        result = {}
        if response.status_code == 200:
            res_list = response.json()['RtnBody'].split('&')
            print('432432')
            print(response)
            print(res_list)
            print('542352')
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
            elif res_dict['CVSStoreID'] != '131386':
                self.log.WARN('StoreID is different!')
                result['verifyCVSStoreID'] = False
            elif res_dict['CVSStoreName'] != urllib.parse.urlencode({'name': '建盛門市'}).split('=')[1]:
                self.log.WARN('StoreName is different!')
                result['verifyCVSStoreName'] = False
            elif res_dict['CVSAddress'] != urllib.parse.urlencode({'name': '新竹市東區建中一路52號1樓'}).split('=')[1]:

                
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
