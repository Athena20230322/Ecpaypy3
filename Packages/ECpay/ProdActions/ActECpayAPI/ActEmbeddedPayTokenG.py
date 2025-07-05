# -*- coding: utf-8 -*-
import textwrap
import time
import json
import os
import urllib.request, urllib.parse, urllib.error
import re
import collections
import hashlib
import hmac
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actEmbeddedpaytokenG(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='EmbeddedPayTokenG')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
    def genOrderRequestInfoTokenGet(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        OrderInfo = self.genArgsDictFromCSV(param_csv)
        ConsumerInfo = self.genArgsDictFromCSV(param_csv)
        req={}
        # if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
        #     data['RelateNumber'] = self.gen_uid(with_dash=False)[0:20]
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID']='3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('MerchantTradeNo')
        data.pop('MerchantTradeDate')
        data.pop('TotalAmount')
        # data.pop('TradeDesc')
        data.pop('Email')
        data.pop('Phone')
        data.pop('Name')
        data.pop('CountryCode')





        rqHeader.pop('MerchantID')
        rqHeader.pop('UseType')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('TotalAmount')
        # rqHeader.pop('TradeDesc')
        rqHeader.pop('Email')
        rqHeader.pop('Phone')
        rqHeader.pop('Name')
        rqHeader.pop('CountryCode')
        rqHeader.pop('AppStoreName')

        OrderInfo.pop('MerchantID')
        OrderInfo.pop('UseType')
        OrderInfo.pop('Timestamp')
        OrderInfo.pop('Revision')
        OrderInfo.pop('Email')
        OrderInfo.pop('Phone')
        OrderInfo.pop('Name')
        OrderInfo.pop('CountryCode')
        OrderInfo.pop('AppStoreName')

        ConsumerInfo.pop('MerchantID')
        ConsumerInfo.pop('Timestamp')
        ConsumerInfo.pop('Revision')
        ConsumerInfo.pop('MerchantTradeNo')
        ConsumerInfo.pop('MerchantTradeDate')
        ConsumerInfo.pop('TotalAmount')
        ConsumerInfo.pop('AppStoreName')





        data['OrderInfo'] = OrderInfo
        data['ConsumerInfo'] = ConsumerInfo
        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')

        print(data)
        data = self.urlEncode(data)
        #print data
        data = self.aesEncrypt(data)
        #print data
        print(rqHeader)
        req['Data'] = data
        req['RqHeader'] = rqHeader
        print(req)
        return req
    def genOrderRequestInfoThreeD2(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        OrderInfo = self.genArgsDictFromCSV(param_csv)
        CardInfo = self.genArgsDictFromCSV(param_csv)
        ATMInfo = self.genArgsDictFromCSV(param_csv)
        CVSInfo = self.genArgsDictFromCSV(param_csv)
        BarcodeInfo = self.genArgsDictFromCSV(param_csv)
        ConsumerInfo = self.genArgsDictFromCSV(param_csv)
       # Gwinfo = self.genArgsDictFromCSV(param_csv)

        req = {}
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('MerchantTradeDate')
        data.pop('MerchantTradeNo')
        data.pop('TotalAmount')
        data.pop('ReturnURL')
        data.pop('TradeDesc')
        data.pop('ItemName')
        data.pop('Redeem')
        data.pop('PeriodAmount')
        data.pop('PeriodType')
        data.pop('Frequency')
        data.pop('ExecTimes')
        data.pop('OrderResultURL')
        data.pop('PeriodReturnURL')
        data.pop('CreditInstallment')
        data.pop('TravelStartDate')
        data.pop('TravelEndDate')
        data.pop('TravelCounty')
        data.pop('ExpireDate')
        data.pop('ATMBankCode')
        data.pop('StoreExpireDate')
        data.pop('CVSCode')
        data.pop('Desc_1')
        data.pop('Desc_2')
        data.pop('Desc_3')
        data.pop('Desc_4')
        data.pop('MerchantMemberID')
        data.pop('Email')
        data.pop('Phone')
        data.pop('Name')
        data.pop('CountryCode')
        data.pop('Address')

        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('RememberCard')
        rqHeader.pop('PaymentUIType')
        rqHeader.pop('ChoosePaymentList')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('ReturnURL')
        rqHeader.pop('TradeDesc')
        rqHeader.pop('ItemName')
        rqHeader.pop('Redeem')
        rqHeader.pop('PeriodAmount')
        rqHeader.pop('PeriodType')
        rqHeader.pop('Frequency')
        rqHeader.pop('ExecTimes')
        rqHeader.pop('OrderResultURL')
        rqHeader.pop('PeriodReturnURL')
        rqHeader.pop('CreditInstallment')
        rqHeader.pop('TravelStartDate')
        rqHeader.pop('TravelEndDate')
        rqHeader.pop('TravelCounty')
        rqHeader.pop('ExpireDate')
        rqHeader.pop('ATMBankCode')
        rqHeader.pop('StoreExpireDate')
        rqHeader.pop('CVSCode')
        rqHeader.pop('Desc_1')
        rqHeader.pop('Desc_2')
        rqHeader.pop('Desc_3')
        rqHeader.pop('Desc_4')
        rqHeader.pop('MerchantMemberID')
        rqHeader.pop('Email')
        rqHeader.pop('Phone')
        rqHeader.pop('Name')
        rqHeader.pop('CountryCode')
        rqHeader.pop('Address')
        rqHeader.pop('CustomField')

        OrderInfo.pop('Timestamp')
        OrderInfo.pop('RqID')
        OrderInfo.pop('Revision')
        OrderInfo.pop('MerchantID')
        OrderInfo.pop('PlatformID')
        OrderInfo.pop('RememberCard')
        OrderInfo.pop('PaymentUIType')
        OrderInfo.pop('ChoosePaymentList')
        OrderInfo.pop('Redeem')
        OrderInfo.pop('PeriodAmount')
        OrderInfo.pop('PeriodType')
        OrderInfo.pop('Frequency')
        OrderInfo.pop('ExecTimes')
        OrderInfo.pop('OrderResultURL')
        OrderInfo.pop('PeriodReturnURL')
        OrderInfo.pop('CreditInstallment')
        OrderInfo.pop('TravelStartDate')
        OrderInfo.pop('TravelEndDate')
        OrderInfo.pop('TravelCounty')
        OrderInfo.pop('ExpireDate')
        OrderInfo.pop('ATMBankCode')
        OrderInfo.pop('StoreExpireDate')
        OrderInfo.pop('CVSCode')
        OrderInfo.pop('Desc_1')
        OrderInfo.pop('Desc_2')
        OrderInfo.pop('Desc_3')
        OrderInfo.pop('Desc_4')
        OrderInfo.pop('MerchantMemberID')
        OrderInfo.pop('Email')
        OrderInfo.pop('Phone')
        OrderInfo.pop('Name')
        OrderInfo.pop('CountryCode')
        OrderInfo.pop('Address')
        OrderInfo.pop('CustomField')

        CardInfo.pop('Timestamp')
        CardInfo.pop('RqID')
        CardInfo.pop('Revision')
        CardInfo.pop('MerchantID')
        CardInfo.pop('PlatformID')
        CardInfo.pop('RememberCard')
        CardInfo.pop('PaymentUIType')
        CardInfo.pop('ChoosePaymentList')
        CardInfo.pop('MerchantTradeDate')
        CardInfo.pop('MerchantTradeNo')
        CardInfo.pop('TotalAmount')
        CardInfo.pop('ReturnURL')
        CardInfo.pop('TradeDesc')
        CardInfo.pop('ItemName')
        CardInfo.pop('ExpireDate')
        CardInfo.pop('ATMBankCode')
        CardInfo.pop('StoreExpireDate')
        CardInfo.pop('CVSCode')
        CardInfo.pop('Desc_1')
        CardInfo.pop('Desc_2')
        CardInfo.pop('Desc_3')
        CardInfo.pop('Desc_4')
        CardInfo.pop('MerchantMemberID')
        CardInfo.pop('Email')
        CardInfo.pop('Phone')
        CardInfo.pop('Name')
        CardInfo.pop('CountryCode')
        CardInfo.pop('Address')
        CardInfo.pop('CustomField')

        ATMInfo.pop('Timestamp')
        ATMInfo.pop('RqID')
        ATMInfo.pop('Revision')
        ATMInfo.pop('MerchantID')
        ATMInfo.pop('PlatformID')
        ATMInfo.pop('RememberCard')
        ATMInfo.pop('PaymentUIType')
        ATMInfo.pop('ChoosePaymentList')
        ATMInfo.pop('MerchantTradeDate')
        ATMInfo.pop('MerchantTradeNo')
        ATMInfo.pop('TotalAmount')
        ATMInfo.pop('ReturnURL')
        ATMInfo.pop('TradeDesc')
        ATMInfo.pop('ItemName')
        ATMInfo.pop('Redeem')
        ATMInfo.pop('PeriodAmount')
        ATMInfo.pop('PeriodType')
        ATMInfo.pop('Frequency')
        ATMInfo.pop('ExecTimes')
        ATMInfo.pop('OrderResultURL')
        ATMInfo.pop('PeriodReturnURL')
        ATMInfo.pop('CreditInstallment')
        ATMInfo.pop('TravelStartDate')
        ATMInfo.pop('TravelEndDate')
        ATMInfo.pop('TravelCounty')
        ATMInfo.pop('StoreExpireDate')
        ATMInfo.pop('CVSCode')
        ATMInfo.pop('Desc_1')
        ATMInfo.pop('Desc_2')
        ATMInfo.pop('Desc_3')
        ATMInfo.pop('Desc_4')
        ATMInfo.pop('MerchantMemberID')
        ATMInfo.pop('Email')
        ATMInfo.pop('Phone')
        ATMInfo.pop('Name')
        ATMInfo.pop('CountryCode')
        ATMInfo.pop('Address')
        ATMInfo.pop('CustomField')

        CVSInfo.pop('Timestamp')
        CVSInfo.pop('RqID')
        CVSInfo.pop('Revision')
        CVSInfo.pop('MerchantID')
        CVSInfo.pop('PlatformID')
        CVSInfo.pop('RememberCard')
        CVSInfo.pop('PaymentUIType')
        CVSInfo.pop('ChoosePaymentList')
        CVSInfo.pop('MerchantTradeDate')
        CVSInfo.pop('MerchantTradeNo')
        CVSInfo.pop('TotalAmount')
        CVSInfo.pop('ReturnURL')
        CVSInfo.pop('TradeDesc')
        CVSInfo.pop('ItemName')
        CVSInfo.pop('Redeem')
        CVSInfo.pop('PeriodAmount')
        CVSInfo.pop('PeriodType')
        CVSInfo.pop('Frequency')
        CVSInfo.pop('ExecTimes')
        CVSInfo.pop('OrderResultURL')
        CVSInfo.pop('PeriodReturnURL')
        CVSInfo.pop('CreditInstallment')
        CVSInfo.pop('TravelStartDate')
        CVSInfo.pop('TravelEndDate')
        CVSInfo.pop('TravelCounty')
        CVSInfo.pop('ExpireDate')
        CVSInfo.pop('ATMBankCode')
        CVSInfo.pop('MerchantMemberID')
        CVSInfo.pop('Email')
        CVSInfo.pop('Phone')
        CVSInfo.pop('Name')
        CVSInfo.pop('CountryCode')
        CVSInfo.pop('Address')
        CVSInfo.pop('CustomField')

        BarcodeInfo.pop('Timestamp')
        BarcodeInfo.pop('RqID')
        BarcodeInfo.pop('Revision')
        BarcodeInfo.pop('MerchantID')
        BarcodeInfo.pop('PlatformID')
        BarcodeInfo.pop('RememberCard')
        BarcodeInfo.pop('PaymentUIType')
        BarcodeInfo.pop('ChoosePaymentList')
        BarcodeInfo.pop('MerchantTradeDate')
        BarcodeInfo.pop('MerchantTradeNo')
        BarcodeInfo.pop('TotalAmount')
        BarcodeInfo.pop('ReturnURL')
        BarcodeInfo.pop('TradeDesc')
        BarcodeInfo.pop('ItemName')
        BarcodeInfo.pop('Redeem')
        BarcodeInfo.pop('PeriodAmount')
        BarcodeInfo.pop('PeriodType')
        BarcodeInfo.pop('Frequency')
        BarcodeInfo.pop('ExecTimes')
        BarcodeInfo.pop('OrderResultURL')
        BarcodeInfo.pop('PeriodReturnURL')
        BarcodeInfo.pop('CreditInstallment')
        BarcodeInfo.pop('TravelStartDate')
        BarcodeInfo.pop('TravelEndDate')
        BarcodeInfo.pop('TravelCounty')
        BarcodeInfo.pop('ExpireDate')
        BarcodeInfo.pop('ATMBankCode')
        BarcodeInfo.pop('CVSCode')
        BarcodeInfo.pop('Desc_1')
        BarcodeInfo.pop('Desc_2')
        BarcodeInfo.pop('Desc_3')
        BarcodeInfo.pop('Desc_4')
        BarcodeInfo.pop('MerchantMemberID')
        BarcodeInfo.pop('Email')
        BarcodeInfo.pop('Phone')
        BarcodeInfo.pop('Name')
        BarcodeInfo.pop('CountryCode')
        BarcodeInfo.pop('Address')
        BarcodeInfo.pop('CustomField')

        ConsumerInfo.pop('Timestamp')
        ConsumerInfo.pop('RqID')
        ConsumerInfo.pop('Revision')
        ConsumerInfo.pop('MerchantID')
        ConsumerInfo.pop('PlatformID')
        ConsumerInfo.pop('RememberCard')
        ConsumerInfo.pop('PaymentUIType')
        ConsumerInfo.pop('ChoosePaymentList')
        ConsumerInfo.pop('MerchantTradeDate')
        ConsumerInfo.pop('MerchantTradeNo')
        ConsumerInfo.pop('TotalAmount')
        ConsumerInfo.pop('ReturnURL')
        ConsumerInfo.pop('TradeDesc')
        ConsumerInfo.pop('ItemName')
        ConsumerInfo.pop('Redeem')
        ConsumerInfo.pop('PeriodAmount')
        ConsumerInfo.pop('PeriodType')
        ConsumerInfo.pop('Frequency')
        ConsumerInfo.pop('ExecTimes')
        ConsumerInfo.pop('OrderResultURL')
        ConsumerInfo.pop('PeriodReturnURL')
        ConsumerInfo.pop('CreditInstallment')
        ConsumerInfo.pop('TravelStartDate')
        ConsumerInfo.pop('TravelEndDate')
        ConsumerInfo.pop('TravelCounty')
        ConsumerInfo.pop('ExpireDate')
        ConsumerInfo.pop('ATMBankCode')
        ConsumerInfo.pop('StoreExpireDate')
        ConsumerInfo.pop('CVSCode')
        ConsumerInfo.pop('Desc_1')
        ConsumerInfo.pop('Desc_2')
        ConsumerInfo.pop('Desc_3')
        ConsumerInfo.pop('Desc_4')
        ConsumerInfo.pop('CustomField')









        data['OrderInfo'] = OrderInfo
        data['CardInfo'] = CardInfo
        data['ATMInfo'] = ATMInfo
        data['CVSInfo'] = CVSInfo
        data['BarcodeInfo'] = BarcodeInfo
        data['ConsumerInfo'] = ConsumerInfo


        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')

        print(data)
        data = self.urlEncode(data)
        # print data
        data = self.aesEncrypt(data)
        # print data
        print(rqHeader)
        req['Data'] = data
        req['RqHeader'] = rqHeader
        print(req)
        return req

    def genOrderRequestInfoTokenQueryPlus(self, param_csv, token, aes):
        print('111111')
        data = {}
        CardInfo={}
        CardInfo['CardNumber']='4311952222222222'
        CardInfo['CardValidYY'] = '22'
        CardInfo['CardValidMM'] = '11'
        CardInfo['CardCVV2'] = '222'
        CardInfo['BindingCard'] = '0'
        token = json.loads(token)
        print(token)
        print(aes)
        aesdata = aes
        aes = json.loads(aes)
        print(aes)
        print(aes['key'])
        print(aes['iv'])
        data['Token'] = token['Token']
        print(data['Token'])
        data['CardInfo'] = CardInfo
        data['CreditInstallment'] = '0'

        print(data)
        print('22222')
        data = json.dumps(data)
        data = data.replace(' ', '')
        data = data.encode('utf-8')
        print(data)
        print('11111')
        data = self.urlEncode(data)
        # print data
        data = self.aesEncryptforAPP(data, aes['key'], aes['iv'])
        # print data
        print(data)
        print('2333')
        return data


    def genOrderRequestInfoTokenQuery(self, param_csv,token,aes):
        print('111111')
        data ={}
        token = json.loads(token)
        print(token)
        print(aes)
        aesdata=aes
        aes=json.loads(aes)
        print(aes)
        print(aes['key'])
        print(aes['iv'])
        data['Token']=token['Token']
        print(data['Token'])
        data = json.dumps(data)
        data = data.encode('utf-8')
        print(data)
        data = self.urlEncode(data)
        #print data
        data = self.aesEncryptforAPP(data,aes['key'],aes['iv'])
        #print data
        print(data)
        return data

    def genOrderRequestInfoKeyExchange(self, param_csv):
        req = {}
        req['ClientPublicKey'] = 'MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBbrA8fqLh0JFLjxcASfW7wjTUiEST+ps2OE68+ZY193rGABIV/MzQ/Y5zSHO8feN/1HMpVOHusTGtTH0FuXptrRUutyJywDS3G/la5+sdb8sBFxIOtl8pW5ZL4S3xAwNqCY1EfOnaaL6zaM1+8Vhg9uxRdGhbU9ZgjgT4k9ATcP6K68R1IuTE4COoI4CehDWUKpupFfQo3GQz/L+HQBRe1WwR/0DSpq8jGp8xZqhGEoxqZHRK8SBXXfyhvSul4x8e8J5+A/ECdA6kcnmXimNNrWP4iO8wFrAcapW5mJjdBuSgX/NlvBFYy/otZb9IQYkb1kQSUxuVLOdvFOXtex1jNAgMBAAE='
        req = json.dumps(req)
        print(req)
        return req

    def genPostRequestToAPIQuery(self, req_info, keyinfo, data2):
        rqq = {}
        form_act = self.feature_conf['AppsdkSearch_API']
        print(req_info)
        req_info1 = {}
        req_info1['Data'] = req_info
        req_info1 = json.dumps(req_info1)
        req_info1 = req_info1.replace(' ', '')
        print(req_info1)
        # req_info1=self.urlEncode(req_info1)
        # hsobj = hashlib.sha256()
        # hsobj.update(req_info1.encode("utf-8"))
        # req_info2 = hsobj.hexdigest().upper()
        # print'456'
        # print req_info2
        # od_arg_dict = collections.OrderedDict(req_info.items)
        # print od_arg_dict
        data2=json.loads(data2)
        Language = 'en-US'
        UUID = 'ae81566dc1e70479'
        AppName = 'com.ecpay.appsdk'
        AppInfo = '{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        KeyInfo = keyinfo
        Signature = self.rsaClientPri(req_info1)
        KeyID = data2['KeyID']
        print(Signature)


        req = json.dumps(req_info)
        print('213123124')
        response = self.postRequestToAPIQueryL(self.genSession(), req_info1, form_act, Language, UUID, AppName, AppInfo, KeyInfo,
                                              Signature, KeyID,
                                              trencode_dotnet=True)
        print('2131231256')
        print(response.headers)
        print(response.content)
        #self.log.INFO(response.decode('utf-8'))
        return response







    # def genPostRequestToAPIQuery(self, req_info,keyinfo,data2):
    #     rqq ={}
    #     form_act = self.feature_conf['AppsdkSearch_API']
    #     print req_info
    #     req_info1={}
    #     req_info1['Data']=req_info
    #     req_info1 = json.dumps(req_info1)
    #     req_info1 = req_info1.replace(' ', '')
    #     print  req_info1
    #     # od_arg_dict = collections.OrderedDict(req_info.items)
    #     # print od_arg_dict
    #     UUID = 'ae81566dc1e70479'
    #     AppName = 'com.ecpay.appsdk'
    #     AppInfo = '{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
    #     KeyInfo = keyinfo
    #     Signature = self.rsaClientPri(req_info1)
    #     KeyID = data2
    #
    #     req = json.dumps(req_info)
    #
    #     response = self.postRequestToAPIQuery(self.genSession(), req_info, form_act, UUID, AppName, AppInfo,KeyInfo,Signature,KeyID,
    #                                                 trencode_dotnet=True)
    #     print '213123124'
    #     print response
    #     self.log.INFO(response.decode('utf-8'))
    #     return response

    def genPostRequestToAPIToken(self, req_info):
        form_act = self.feature_conf['Appsdktoken_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genPostRequestToAPIkeyexchange(self, req_info):
        form_act = self.feature_conf['Appsdk_API']
        print(req_info)
        # od_arg_dict = collections.OrderedDict(req_info.items)
        # print od_arg_dict
        UUID = 'ae81566dc1e70479'
        AppName = 'com.ecpay.appsdk'
        AppInfo = '{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        req = json.dumps(req_info)

        response = self.postRequestToAPIkeyexchange(self.genSession(), req_info, form_act, UUID, AppName, AppInfo,
                                                    trencode_dotnet=True)
        self.log.INFO(response['content'].decode('utf-8'))
        return response
    def strToDictAppsdk(self, res_info1):
        res_info=res_info1['content']
        res_info = self.urlEncode(res_info)
        print('str1: ' + res_info)
        res_dict = {}
        res_info = self.urlDecode(res_info)
        print('str2: ' + res_info)
        # str_to_list = res_info.split('&')
        # for item in str_to_list:
        #     tmp = item.split('=')
        #     res_dict[tmp[0]] = tmp[1]

        res_dict = eval(res_info)

        print(res_dict)


        return res_dict

    def strToDict(self, res_info):
        res_info = self.urlEncode(res_info)
        print('str1: ' + res_info)
        res_dict = {}
        res_info = self.urlDecode(res_info)
        print('str2: ' + res_info)
        # str_to_list = res_info.split('&')
        # for item in str_to_list:
        #     tmp = item.split('=')
        #     res_dict[tmp[0]] = tmp[1]

        print('432141234')

        res_dict = json.loads(res_info)

        print(res_dict)

        return res_dict

    def strToDictrsa(self, KeyInfo):
        res_info1 = self.rsaDecrpt(KeyInfo)
        print(res_info1)
        res_dict1 = {}


        print('432141234')

        res_dict1 = json.loads(res_info1)

        print(res_dict1)

        return res_dict1



    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['Appsdktoken_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def quote_item(self, res_dict, revert_list):
        for key in revert_list:
            res_dict[key] = urllib.parse.quote_plus(res_dict[key]).lower()
        return res_dict
    def decryptDatab2b(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def decryptDatapppsdk(self, data):
        # data = self.urlDecode(data)

        print(data['header'])
        res = {}
        res = data['header']
        print(res)
        print(res['KeyInfo'])
        return self.rsaDecrpt(res['KeyInfo'])

    def decryptDatappprsa(self, data):
        # data = self.urlDecode(data)

        print(data['header'])
        res = {}
        res = data['header']
        print(res)
        print(res['KeyInfo'])
        return self.rsaDecrpt(res['KeyInfo'])

    def encryptDatapppsdk(self, data,skey):
        # data = self.urlDecode(data)

        print(data)
        print('888877777776666')

        skey=json.loads(skey)
        print(skey['ServerPublicKey'])

        skey['ServerPublicKey'] = skey['ServerPublicKey'].replace(" ", "+").replace("\\/", "/")

        print(skey['ServerPublicKey'])

        print('88887777777333')
        res = {}
        res = data

        print(res)
        print('999999999999999')
        return self.rsaServerPub(res, skey['ServerPublicKey'])

    def encryptDatapppsdkn(self, data, skey):
        # data = self.urlDecode(data)

        print(data)
        print('888877777776666')

        skey = json.loads(skey)
        print('888877777755555')
        print(skey['ServerPublicKey'])

        skey['ServerPublicKey'] = skey['ServerPublicKey'].replace(" ", "+").replace("\\/", "/")

        s = skey['ServerPublicKey']
        s='\n'.join(textwrap.wrap(s, 64))
        print(s)


        print('88887777777333')
        res = {}
        res = data

        print(res)
        print('999999999999999')
        return self.rsaServerPubn(res, s)

    def decryptDatarsa(self, data):
        # data = self.urlDecode(data)
        headers = data.headers
        content = data.content
        content = eval(content)
        print(headers['KeyInfo'])
        print(content['Data'])
        aes = self.rsaDecrpt(headers['KeyInfo'])
        print(aes)
        aes = json.loads(aes)

        print(aes['key'])
        print(aes['iv'])

        return self.aesDecryptforAPP(content['Data'], aes['key'], aes['iv'])


    def decryptDatab2b2(self, data):
        #data = self.urlDecode(data)
        print(data)
        print('9999991111')
        return self.aesDecrypt(data)

    def decryptDatab2bAppsdk(self, data,aes):
        #data = self.urlDecode(data)
        print(aes)
        aesdata={}
        aesdata=aes
        aes=json.loads(aes)

        print(aes['key'])
        print(aes['iv'])
        print(data)
        print(data)

        return self.aesDecryptforAPP(data,aes['key'],aes['iv'])

    def decryptDatarsa(self, data):
        # data = self.urlDecode(data)
        headers=data.headers
        content=data.content
        content=eval(content)
        print(headers['KeyInfo'])
        print(content['Data'])
        aes=self.rsaDecrpt(headers['KeyInfo'])
        print(aes)
        aes = json.loads(aes)

        print(aes['key'])
        print(aes['iv'])

        return self.aesDecryptforAPP(content['Data'], aes['key'], aes['iv'])

