# -*- coding: utf-8 -*-
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


class actAppsdkorder(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='APPSDKORDER')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfoTokenQuery(self, param_csv, token, aes):
        print('111111')
        data = {}
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
        data = json.dumps(data)
        data = data.encode('utf-8')
        print(data)
        data = self.urlEncode(data)
        # print data
        data = self.aesEncryptforAPP(data, aes['key'], aes['iv'])
        # print data
        print(data)
        return data

    def genOrderRequestInfoOrder(self, param_csv,token,aes):
        CardInfo = self.genArgsDictFromCSV(param_csv)
        OrderInfo = self.genArgsDictFromCSV(param_csv)
        data={}
        token = json.loads(token)
          # if data['MerchantTradeNo'] == 'AUTO_GEN_RELATENO':
          #    data['MerchantTradeNo'] = self.gen_uid(with_dash=False)[0:20]
       # req['MerchantTradeNo'] = data['MerchantTradeNo']
       # req['PlatformID']='3083192'


        CardInfo.pop('MerchantTradeNo')

        OrderInfo.pop('CardNo')
        OrderInfo.pop('CardValidMM')
        OrderInfo.pop('CardValidYY')
        OrderInfo.pop('CardCVV2')


        data['OrderInfo'] = OrderInfo
        data['CardInfo'] = CardInfo

        print(aes)
        aesdata = aes
        aes = json.loads(aes)
        print(aes)
        print(aes['key'])
        print(aes['iv'])

        data['Token'] = token['Token']

        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')



        print(data)
        data = self.urlEncode(data)
        print(data)
        data = self.aesEncryptforAPP(data, aes['key'], aes['iv'])
        return data
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


    def genPostRequestToAPIorder111(self, req_info):
        form_act = self.feature_conf['Appsdkorder_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        UUID = 'ae81566dc1e70479'
        AppName = 'com.ecpay.appsdk'
        AppInfo = '{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        response = self.postRequestToAPIkeyexchange(self.genSession(), od_arg_dict, form_act, UUID, AppName, AppInfo,
                                                    trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genPostRequestToAPIQuery(self, req_info, keyinfo, data2):
        rqq = {}
        form_act = self.feature_conf['Appsdkorder_API']
        print(req_info)
        req_info1 = {}
        req_info1['Data'] = req_info
        req_info1 = json.dumps(req_info1)
        req_info1 = req_info1.replace(' ', '')
        print(req_info1)

        data2=json.loads(data2)
        UUID = 'ae81566dc1e70479'
        AppName = 'com.ecpay.appsdk'
        AppInfo = '{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        KeyInfo = keyinfo
        Signature = self.rsaClientPri(req_info1)
        KeyID = data2['KeyID']
        print(Signature)


        req = json.dumps(req_info)

        response = self.postRequestToAPIQuery(self.genSession(), req_info1, form_act, UUID, AppName, AppInfo, KeyInfo,
                                              Signature, KeyID,
                                              trencode_dotnet=True)
        print('213123124')
        print(response)
        self.log.INFO(response.decode('utf-8'))
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

    def genPostRequestToAPItoken(self, req_info):
        form_act = self.feature_conf['Appsdktoken_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response
    def genPostRequestToAPIorder(self, req_info):
        form_act = self.feature_conf['Appsdkorder_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genPostRequestToAPIkeyexchangeorderxxxx(self, req_info,data2):
        form_act = self.feature_conf['Appsdkorder_API']
        print(req_info)
        print('23434')
        od_arg_dict = collections.OrderedDict(req_info.items)
        print('23456')
        print(od_arg_dict)

        data2 = json.loads(data2)
        UUID = 'ae81566dc1e70479'
        AppName = 'com.ecpay.appsdk'
        AppInfo = '{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        KeyID = data2['KeyID']
        req = json.dumps(req_info)
        od_arg_dict=json.dumps(od_arg_dict)


        response = self.postRequestToAPIkeyexchange(self.genSession(), od_arg_dict, form_act, UUID, AppName, AppInfo,KeyID,
                                                    trencode_dotnet=True)
        self.log.INFO(response['content'].decode('utf-8'))
        return response

    def genPostRequestToAPIkeyexchangeorder(self, req_info, keyinfo, data2):
        rqq = {}
        form_act = self.feature_conf['Appsdkorder_API']
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
        data2 = json.loads(data2)
        UUID = 'ae81566dc1e70479'
        AppName = 'com.ecpay.appsdk'
        AppInfo = '{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        KeyInfo = keyinfo
        Signature = self.rsaClientPri(req_info1)
        KeyID = data2['KeyID']
        print(Signature)

        req = json.dumps(req_info)

        response = self.postRequestToAPIQuery(self.genSession(), req_info1, form_act, UUID, AppName, AppInfo, KeyInfo,
                                              Signature, KeyID,
                                              trencode_dotnet=True)
        print('213123124')
        print(response)
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


    def decryptDatab2b2(self, data):
      #  data = self.urlDecode(data)
        print(data)
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

