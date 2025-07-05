import time
import json
import os
import dicttoxml
import xmltodict
import re
import collections
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actBackAuthPanhsin(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='BackAuthPanhsin')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv, payment_type=1):
        data = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['PlatformID'] = data['PlatformID']
        req['MerchantID'] = data['MerchantID']
        req['Encryption'] = data['Encryption']
        req['Format'] = data['Format']
        data.pop('Encryption')
        data.pop('Format')
        if 'Version' in data:
            req['Version'] = data['Version']
            data.pop('Version')
        if data['Barcode'] == '':
            data['Barcode'] = self.getBarcode(payment_type)
        chksum = self.genChkMacVal(data, mode='local', codec='sha256', case='insensitive')
        print(chksum)
        data['CheckMacValue'] = chksum
        if req['Format'] == '2':
            data = json.dumps(data)
        elif req['Format'] == '1':
            xml = {'Data': data}
            data = dicttoxml.dicttoxml(xml, custom_root='Root', attr_type=False)
        data = data.encode('utf-8')
        print(data)
        if req['Encryption'] == '1':
            data = self.aesEncrypt(data)
        elif req['Encryption'] == '2':
            data = self.tripleDesEncrypt(data)
        data = self.urlEncode(data)
        print(data)
        req['Data'] = data
        return req

    def genOrderRequestInfoThreeD(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['MerchantID'] = data['MerchantID']
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        rqHeader.pop('MerchantID')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('TradeDesc')
        rqHeader.pop('ChoosePayment')
        rqHeader.pop('CardNo')
        rqHeader.pop('CardValidMM')
        rqHeader.pop('CardValidYY')
        rqHeader.pop('CardCVV2')
        rqHeader.pop('Remark')
        rqHeader.pop('ReturnURL')
        rqHeader.pop('Gwinfo')
        rqHeader.pop('Use3D')
        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')
        print(data)
        data = self.urlEncode(data)
        print(data)
        data = self.aesEncrypt(data)
        print(data)
        req['Data'] = data
        req['RqHeader'] = rqHeader
        return req
    def getBarcode(self, payment_type):
        get_dict = {}
        if payment_type == 1:
            get_dict['paymenttype'] = '1'
        elif payment_type == 3:
            get_dict['paymenttype'] = '3'
        elif payment_type == 4:
            get_dict['paymenttype'] = '4'
        response = self.getRequestFromAPI(get_dict, 'https://cvs-stage.opay.tw/PaymentRule/Mobile/MockGetBarCode')
        m = re.search('AP\d{3}[A-Z]{1}\d{1}\w{11}', response)
        if m:
            found = m.group()
            return found
        else:
            raise Exception('Barcode not found from https://cvs-stage.opay.tw/PaymentRule/Mobile/MockGetBarCode')

    def genOrderRequestInfoThreeD2ATM(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        ATMInfo = self.genArgsDictFromCSV(param_csv)
        OrderInfo = self.genArgsDictFromCSV(param_csv)
        # ConsumerInfo = self.genArgsDictFromCSV(param_csv)
        # Gwinfo = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('PlatformID')
        data.pop('MerchantTradeNo')
        data.pop('MerchantTradeDate')
        data.pop('TotalAmount')
        data.pop('ItemName')
        data.pop('TradeDesc')
        data.pop('Remark')
        data.pop('ReturnURL')
        data.pop('ExpireDate')
        data.pop('ATMBankCode')

        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('OrderInfo')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('ItemName')
        rqHeader.pop('TradeDesc')
        rqHeader.pop('Remark')
        rqHeader.pop('ReturnURL')
        rqHeader.pop('ChoosePayment')
        rqHeader.pop('ATMInfo')
        rqHeader.pop('CustomField')
        rqHeader.pop('ExpireDate')
        rqHeader.pop('ATMBankCode')

        ATMInfo.pop('MerchantID')
        ATMInfo.pop('PlatformID')
        ATMInfo.pop('OrderInfo')
        ATMInfo.pop('MerchantTradeNo')
        ATMInfo.pop('MerchantTradeDate')
        ATMInfo.pop('TotalAmount')
        ATMInfo.pop('ItemName')
        ATMInfo.pop('TradeDesc')
        ATMInfo.pop('Remark')
        ATMInfo.pop('ReturnURL')
        ATMInfo.pop('ChoosePayment')
        ATMInfo.pop('ATMInfo')
        ATMInfo.pop('CustomField')
        ATMInfo.pop('Timestamp')
        ATMInfo.pop('RqID')
        ATMInfo.pop('Revision')

        OrderInfo.pop('Timestamp')
        OrderInfo.pop('RqID')
        OrderInfo.pop('Revision')
        OrderInfo.pop('MerchantID')
        OrderInfo.pop('PlatformID')
        OrderInfo.pop('OrderInfo')
        OrderInfo.pop('ChoosePayment')
        OrderInfo.pop('CustomField')
        OrderInfo.pop('ATMInfo')
        OrderInfo.pop('ExpireDate')
        OrderInfo.pop('ATMBankCode')


        data['OrderInfo'] = OrderInfo
        data['ATMInfo'] = ATMInfo

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
    def genOrderRequestInfoThreeD2CVS(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        CVSInfo = self.genArgsDictFromCSV(param_csv)
        OrderInfo = self.genArgsDictFromCSV(param_csv)
        # ConsumerInfo = self.genArgsDictFromCSV(param_csv)
        # Gwinfo = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('PlatformID')
        data.pop('MerchantTradeNo')
        data.pop('MerchantTradeDate')
        data.pop('TotalAmount')
        data.pop('ItemName')
        data.pop('TradeDesc')
        data.pop('Remark')
        data.pop('ReturnURL')
        data.pop('ExpireDate')
        data.pop('CVSCode')
        data.pop('Desc_1')
        data.pop('Desc_2')
        data.pop('Desc_3')
        data.pop('Desc_4')

        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('OrderInfo')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('ItemName')
        rqHeader.pop('TradeDesc')
        rqHeader.pop('Remark')
        rqHeader.pop('ReturnURL')
        rqHeader.pop('ChoosePayment')
        rqHeader.pop('CVSInfo')
        rqHeader.pop('CustomField')
        rqHeader.pop('ExpireDate')
        rqHeader.pop('CVSCode')

        CVSInfo.pop('MerchantID')
        CVSInfo.pop('PlatformID')
        CVSInfo.pop('OrderInfo')
        CVSInfo.pop('MerchantTradeNo')
        CVSInfo.pop('MerchantTradeDate')
        CVSInfo.pop('TotalAmount')
        CVSInfo.pop('ItemName')
        CVSInfo.pop('TradeDesc')
        CVSInfo.pop('Remark')
        CVSInfo.pop('ReturnURL')
        CVSInfo.pop('ChoosePayment')
        CVSInfo.pop('CVSInfo')
        CVSInfo.pop('CustomField')
        CVSInfo.pop('Timestamp')
        CVSInfo.pop('RqID')
        CVSInfo.pop('Revision')

        OrderInfo.pop('Timestamp')
        OrderInfo.pop('RqID')
        OrderInfo.pop('Revision')
        OrderInfo.pop('MerchantID')
        OrderInfo.pop('PlatformID')
        OrderInfo.pop('OrderInfo')
        OrderInfo.pop('ChoosePayment')
        OrderInfo.pop('CustomField')
        OrderInfo.pop('CVSInfo')
        OrderInfo.pop('ExpireDate')
        OrderInfo.pop('CVSCode')
        OrderInfo.pop('Desc_1')
        OrderInfo.pop('Desc_2')
        OrderInfo.pop('Desc_3')
        OrderInfo.pop('Desc_4')


        data['OrderInfo'] = OrderInfo
        data['CVSInfo'] = CVSInfo

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


    def genOrderRequestInfoThreeD2Barcode(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        BarcodeInfo = self.genArgsDictFromCSV(param_csv)
        OrderInfo = self.genArgsDictFromCSV(param_csv)
        # ConsumerInfo = self.genArgsDictFromCSV(param_csv)
        # Gwinfo = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('PlatformID')
        data.pop('MerchantTradeNo')
        data.pop('MerchantTradeDate')
        data.pop('TotalAmount')
        data.pop('ItemName')
        data.pop('TradeDesc')
        data.pop('Remark')
        data.pop('ReturnURL')
        data.pop('ExpireDate')


        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('OrderInfo')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('ItemName')
        rqHeader.pop('TradeDesc')
        rqHeader.pop('Remark')
        rqHeader.pop('ReturnURL')
        rqHeader.pop('ChoosePayment')
        rqHeader.pop('BarcodeInfo')
        rqHeader.pop('CustomField')
        rqHeader.pop('ExpireDate')


        BarcodeInfo.pop('MerchantID')
        BarcodeInfo.pop('PlatformID')
        BarcodeInfo.pop('OrderInfo')
        BarcodeInfo.pop('MerchantTradeNo')
        BarcodeInfo.pop('MerchantTradeDate')
        BarcodeInfo.pop('TotalAmount')
        BarcodeInfo.pop('ItemName')
        BarcodeInfo.pop('TradeDesc')
        BarcodeInfo.pop('Remark')
        BarcodeInfo.pop('ReturnURL')
        BarcodeInfo.pop('ChoosePayment')
        BarcodeInfo.pop('BarcodeInfo')
        BarcodeInfo.pop('CustomField')
        BarcodeInfo.pop('Timestamp')
        BarcodeInfo.pop('RqID')
        BarcodeInfo.pop('Revision')

        OrderInfo.pop('Timestamp')
        OrderInfo.pop('RqID')
        OrderInfo.pop('Revision')
        OrderInfo.pop('MerchantID')
        OrderInfo.pop('PlatformID')
        OrderInfo.pop('OrderInfo')
        OrderInfo.pop('ChoosePayment')
        OrderInfo.pop('CustomField')
        OrderInfo.pop('BarcodeInfo')
        OrderInfo.pop('ExpireDate')



        data['OrderInfo'] = OrderInfo
        data['BarcodeInfo'] = BarcodeInfo

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

    def genOrderRequestInfoThreeD2(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        OrderInfo = self.genArgsDictFromCSV(param_csv)
        CardInfo = self.genArgsDictFromCSV(param_csv)
        ConsumerInfo = self.genArgsDictFromCSV(param_csv)
        Gwinfo = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('PlatformID')
        data.pop('MerchantTradeNo')
        data.pop('MerchantTradeDate')
        data.pop('TotalAmount')
        data.pop('ItemName')
        data.pop('TradeDesc')
        data.pop('Remark')
        data.pop('ReturnURL')
        data.pop('CardValidMM')
        data.pop('PeriodAmount')
        data.pop('PeriodType')
        data.pop('CountryCode')
        data.pop('Email')
        data.pop('Phone')
        data.pop('Redeem')
        data.pop('Address')
        data.pop('OrderResultURL')
        data.pop('ExecTimes')
        data.pop('Name')
        data.pop('CardNo')
        data.pop('CardCVV2')
        data.pop('CardValidYY')
        data.pop('CreditInstallment')
        data.pop('PeriodReturnURL')
        data.pop('Frequency')
        data.pop('Use3D')

        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('OrderInfo')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('ItemName')
        rqHeader.pop('TradeDesc')
        rqHeader.pop('Remark')
        rqHeader.pop('ReturnURL')
        rqHeader.pop('ChoosePayment')
        rqHeader.pop('CardInfo')
        rqHeader.pop('CardNo')
        rqHeader.pop('CardValidMM')
        rqHeader.pop('CardValidYY')
        rqHeader.pop('CardCVV2')
        rqHeader.pop('Redeem')
        rqHeader.pop('CreditInstallment')
        rqHeader.pop('PeriodAmount')
        rqHeader.pop('PeriodType')
        rqHeader.pop('Frequency')
        rqHeader.pop('ExecTimes')
        rqHeader.pop('PeriodReturnURL')
        rqHeader.pop('OrderResultURL')
        rqHeader.pop('ConsumerInfo')
        rqHeader.pop('Email')
        rqHeader.pop('Phone')
        rqHeader.pop('Name')
        rqHeader.pop('CountryCode')
        rqHeader.pop('Address')
        rqHeader.pop('CustomField')
        rqHeader.pop('Use3D')
        rqHeader.pop('Gwinfo')

        OrderInfo.pop('Timestamp')
        OrderInfo.pop('RqID')
        OrderInfo.pop('Revision')
        OrderInfo.pop('MerchantID')
        OrderInfo.pop('PlatformID')
        OrderInfo.pop('OrderInfo')
        OrderInfo.pop('ChoosePayment')
        OrderInfo.pop('CardInfo')
        OrderInfo.pop('CardNo')
        OrderInfo.pop('CardValidMM')
        OrderInfo.pop('CardValidYY')
        OrderInfo.pop('CardCVV2')
        OrderInfo.pop('Redeem')
        OrderInfo.pop('CreditInstallment')
        OrderInfo.pop('PeriodAmount')
        OrderInfo.pop('PeriodType')
        OrderInfo.pop('Frequency')
        OrderInfo.pop('ExecTimes')
        OrderInfo.pop('PeriodReturnURL')
        OrderInfo.pop('OrderResultURL')
        OrderInfo.pop('ConsumerInfo')
        OrderInfo.pop('Email')
        OrderInfo.pop('Phone')
        OrderInfo.pop('Name')
        OrderInfo.pop('CountryCode')
        OrderInfo.pop('Address')
        OrderInfo.pop('CustomField')
        OrderInfo.pop('Use3D')
        OrderInfo.pop('Gwinfo')

        CardInfo.pop('Timestamp')
        CardInfo.pop('RqID')
        CardInfo.pop('Revision')
        CardInfo.pop('MerchantID')
        CardInfo.pop('PlatformID')
        CardInfo.pop('OrderInfo')
        CardInfo.pop('CardInfo')
        CardInfo.pop('MerchantTradeNo')
        CardInfo.pop('MerchantTradeDate')
        CardInfo.pop('TotalAmount')
        CardInfo.pop('ItemName')
        CardInfo.pop('TradeDesc')
        CardInfo.pop('Remark')
        CardInfo.pop('ReturnURL')
        CardInfo.pop('ChoosePayment')
        CardInfo.pop('ConsumerInfo')
        CardInfo.pop('Email')
        CardInfo.pop('Phone')
        CardInfo.pop('Name')
        CardInfo.pop('CountryCode')
        CardInfo.pop('Address')
        CardInfo.pop('CustomField')
        CardInfo.pop('Use3D')
        CardInfo.pop('Gwinfo')

        ConsumerInfo.pop('Timestamp')
        ConsumerInfo.pop('RqID')
        ConsumerInfo.pop('Revision')
        ConsumerInfo.pop('MerchantID')
        ConsumerInfo.pop('PlatformID')
        ConsumerInfo.pop('OrderInfo')
        ConsumerInfo.pop('TotalAmount')
        ConsumerInfo.pop('ItemName')
        ConsumerInfo.pop('TradeDesc')
        ConsumerInfo.pop('Remark')
        ConsumerInfo.pop('ReturnURL')
        ConsumerInfo.pop('MerchantTradeNo')
        ConsumerInfo.pop('MerchantTradeDate')
        ConsumerInfo.pop('ChoosePayment')
        ConsumerInfo.pop('CardInfo')
        ConsumerInfo.pop('CardNo')
        ConsumerInfo.pop('CardValidMM')
        ConsumerInfo.pop('CardValidYY')
        ConsumerInfo.pop('CardCVV2')
        ConsumerInfo.pop('Redeem')
        ConsumerInfo.pop('CreditInstallment')
        ConsumerInfo.pop('PeriodAmount')
        ConsumerInfo.pop('PeriodType')
        ConsumerInfo.pop('Frequency')
        ConsumerInfo.pop('ExecTimes')
        ConsumerInfo.pop('PeriodReturnURL')
        ConsumerInfo.pop('OrderResultURL')
        ConsumerInfo.pop('ConsumerInfo')
        ConsumerInfo.pop('CustomField')
        ConsumerInfo.pop('Use3D')
        ConsumerInfo.pop('Gwinfo')

        Gwinfo.pop('Timestamp')
        Gwinfo.pop('RqID')
        Gwinfo.pop('Revision')
        Gwinfo.pop('MerchantID')
        Gwinfo.pop('PlatformID')
        Gwinfo.pop('OrderInfo')
        Gwinfo.pop('TotalAmount')
        Gwinfo.pop('ItemName')
        Gwinfo.pop('TradeDesc')
        Gwinfo.pop('Remark')
        Gwinfo.pop('ReturnURL')
        Gwinfo.pop('MerchantTradeNo')
        Gwinfo.pop('MerchantTradeDate')
        Gwinfo.pop('ChoosePayment')
        Gwinfo.pop('CardInfo')
        Gwinfo.pop('CardNo')
        Gwinfo.pop('CardValidMM')
        Gwinfo.pop('CardValidYY')
        Gwinfo.pop('CardCVV2')
        Gwinfo.pop('Redeem')
        Gwinfo.pop('CreditInstallment')
        Gwinfo.pop('PeriodAmount')
        Gwinfo.pop('PeriodType')
        Gwinfo.pop('Frequency')
        Gwinfo.pop('ExecTimes')
        Gwinfo.pop('PeriodReturnURL')
        Gwinfo.pop('OrderResultURL')
        Gwinfo.pop('ConsumerInfo')
        Gwinfo.pop('CustomField')
        Gwinfo.pop('Gwinfo')

        data['OrderInfo'] = OrderInfo
        data['CardInfo'] = CardInfo
        data['ConsumerInfo'] = ConsumerInfo
        data['Gwinfo'] = Gwinfo

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

    def genOrderRequestInfoThreeD3(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        OrderInfo = self.genArgsDictFromCSV(param_csv)
        CardInfo = self.genArgsDictFromCSV(param_csv)
        ConsumerInfo = self.genArgsDictFromCSV(param_csv)
        Gwinfo = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['MerchantID'] = data['MerchantID']
        #req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('PlatformID')
        data.pop('MerchantTradeNo')
        data.pop('MerchantTradeDate')
        data.pop('TotalAmount')
        data.pop('ItemName')
        data.pop('TradeDesc')
        data.pop('Remark')
        data.pop('ReturnURL')






        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('OrderInfo')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('ItemName')
        rqHeader.pop('TradeDesc')
        rqHeader.pop('Remark')
        rqHeader.pop('ReturnURL')
        rqHeader.pop('ChoosePayment')
        rqHeader.pop('CustomField')

        OrderInfo.pop('Timestamp')
        OrderInfo.pop('RqID')
        OrderInfo.pop('Revision')
        OrderInfo.pop('MerchantID')
        OrderInfo.pop('PlatformID')
        OrderInfo.pop('OrderInfo')
        OrderInfo.pop('ChoosePayment')
        OrderInfo.pop('CustomField')



        CardInfo.pop('Timestamp')
        CardInfo.pop('RqID')
        CardInfo.pop('Revision')
        CardInfo.pop('MerchantID')
        CardInfo.pop('PlatformID')
        CardInfo.pop('OrderInfo')
        CardInfo.pop('MerchantTradeNo')
        CardInfo.pop('MerchantTradeDate')
        CardInfo.pop('TotalAmount')
        CardInfo.pop('ItemName')
        CardInfo.pop('TradeDesc')
        CardInfo.pop('Remark')
        CardInfo.pop('ReturnURL')
        CardInfo.pop('ChoosePayment')
        CardInfo.pop('CustomField')





        ConsumerInfo.pop('Timestamp')
        ConsumerInfo.pop('RqID')
        ConsumerInfo.pop('Revision')
        ConsumerInfo.pop('MerchantID')
        ConsumerInfo.pop('PlatformID')
        ConsumerInfo.pop('OrderInfo')
        ConsumerInfo.pop('TotalAmount')
        ConsumerInfo.pop('ItemName')
        ConsumerInfo.pop('TradeDesc')
        ConsumerInfo.pop('Remark')
        ConsumerInfo.pop('ReturnURL')
        ConsumerInfo.pop('MerchantTradeNo')
        ConsumerInfo.pop('MerchantTradeDate')
        ConsumerInfo.pop('ChoosePayment')
        ConsumerInfo.pop('CustomField')


        Gwinfo.pop('Timestamp')
        Gwinfo.pop('RqID')
        Gwinfo.pop('Revision')
        Gwinfo.pop('MerchantID')
        Gwinfo.pop('PlatformID')
        Gwinfo.pop('OrderInfo')
        Gwinfo.pop('TotalAmount')
        Gwinfo.pop('ItemName')
        Gwinfo.pop('TradeDesc')
        Gwinfo.pop('Remark')
        Gwinfo.pop('ReturnURL')
        Gwinfo.pop('MerchantTradeNo')
        Gwinfo.pop('MerchantTradeDate')
        Gwinfo.pop('ChoosePayment')
        Gwinfo.pop('CustomField')



        data['OrderInfo'] = OrderInfo
        data['CardInfo'] = CardInfo
        data['ConsumerInfo'] = ConsumerInfo
        data['Gwinfo'] = Gwinfo

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

    def genOrderRequestInfoThreeD3ATM(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        ATMInfo = self.genArgsDictFromCSV(param_csv)
        CVSInfo = self.genArgsDictFromCSV(param_csv)
        #CardInfo = self.genArgsDictFromCSV(param_csv)
        BarcodeInfo = self.genArgsDictFromCSV(param_csv)
        #ConsumerInfo = self.genArgsDictFromCSV(param_csv)
        # Gwinfo = self.genArgsDictFromCSV(param_csv)
        req = {}
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ChoosePayment')
        data.pop('ExpireDate')
        data.pop('ATMBankCode')
        data.pop('ATMInfo')
        #data.pop('BarcodeInfo')
        data.pop('CVSInfo')
        data.pop('Desc_1')
        data.pop('Desc_2')
        data.pop('Desc_3')
        data.pop('Desc_4')
        data.pop('CVSCode')
        data.pop('CustomField')


        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('OrderInfo')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantTradeDate')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('ItemName')
        rqHeader.pop('TradeDesc')
        rqHeader.pop('Remark')
        rqHeader.pop('ReturnURL')
        rqHeader.pop('ChoosePayment')
        rqHeader.pop('ATMInfo')
        rqHeader.pop('CVSInfo')
        rqHeader.pop('ExpireDate')
        rqHeader.pop('Desc_1')
        rqHeader.pop('Desc_2')
        rqHeader.pop('Desc_3')
        rqHeader.pop('Desc_4')
        rqHeader.pop('CVSCode')
        rqHeader.pop('BarcodeInfo')
        rqHeader.pop('CustomField')
        rqHeader.pop('ATMBankCode')



        ATMInfo.pop('MerchantID')
        ATMInfo.pop('PlatformID')
        ATMInfo.pop('OrderInfo')
        ATMInfo.pop('MerchantTradeNo')
        ATMInfo.pop('MerchantTradeDate')
        ATMInfo.pop('TotalAmount')
        ATMInfo.pop('ItemName')
        ATMInfo.pop('TradeDesc')
        ATMInfo.pop('Remark')
        ATMInfo.pop('ReturnURL')
        ATMInfo.pop('CVSInfo')
        ATMInfo.pop('ExpireDate')
        ATMInfo.pop('Desc_1')
        ATMInfo.pop('Desc_2')
        ATMInfo.pop('Desc_3')
        ATMInfo.pop('Desc_4')
        ATMInfo.pop('CVSCode')
        ATMInfo.pop('BarcodeInfo')
        ATMInfo.pop('ChoosePayment')
        ATMInfo.pop('CustomField')
        ATMInfo.pop('Timestamp')
        ATMInfo.pop('RqID')
        ATMInfo.pop('Revision')


        CVSInfo.pop('MerchantID')
        CVSInfo.pop('Timestamp')
        CVSInfo.pop('RqID')
        CVSInfo.pop('Revision')
        CVSInfo.pop('PlatformID')
        CVSInfo.pop('OrderInfo')
        CVSInfo.pop('MerchantTradeNo')
        CVSInfo.pop('MerchantTradeDate')
        CVSInfo.pop('TotalAmount')
        CVSInfo.pop('ItemName')
        CVSInfo.pop('TradeDesc')
        CVSInfo.pop('Remark')
        CVSInfo.pop('ReturnURL')
        CVSInfo.pop('ChoosePayment')
        CVSInfo.pop('BarcodeInfo')
        CVSInfo.pop('ExpireDate')
        CVSInfo.pop('ATMInfo')
        CVSInfo.pop('ATMBankCode')
        CVSInfo.pop('CustomField')

        BarcodeInfo.pop('MerchantID')
        BarcodeInfo.pop('Timestamp')
        BarcodeInfo.pop('RqID')
        BarcodeInfo.pop('Revision')
        BarcodeInfo.pop('PlatformID')
        BarcodeInfo.pop('OrderInfo')
        BarcodeInfo.pop('MerchantTradeNo')
        BarcodeInfo.pop('MerchantTradeDate')
        BarcodeInfo.pop('TotalAmount')
        BarcodeInfo.pop('ItemName')
        BarcodeInfo.pop('TradeDesc')
        BarcodeInfo.pop('Remark')
        BarcodeInfo.pop('ReturnURL')
        BarcodeInfo.pop('ChoosePayment')
        BarcodeInfo.pop('CVSInfo')
        BarcodeInfo.pop('ExpireDate')
        BarcodeInfo.pop('Desc_1')
        BarcodeInfo.pop('Desc_2')
        BarcodeInfo.pop('Desc_3')
        BarcodeInfo.pop('Desc_4')
        BarcodeInfo.pop('CVSCode')
        BarcodeInfo.pop('ATMInfo')
        BarcodeInfo.pop('ATMBankCode')
        BarcodeInfo.pop('CustomField')




        data['BarcodeInfo'] = BarcodeInfo
        data['CVSInfo'] = CVSInfo
        #data['ConsumerInfo'] = ConsumerInfo
        #data['CardInfo'] = CardInfo
        data['ATMInfo'] = ATMInfo

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

    def createOrderByRequest(self, req_info):
        form_act = self.feature_conf['BackAuth_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def createOrderByRequestThreeD(self, req_info):
        form_act = self.feature_conf['BackAuth_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        #od_arg_dict = json.dumps(od_arg_dict)
        response = self.postRequestToAPIThreeD(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def strToDict(self, res_info):

        print('str1: ' + res_info)
        res_dict = {}
        res_info = self.urlDecode(res_info)
        print('str2: ' + res_info)
        str_to_list = res_info.split('&')
        for item in str_to_list:
            tmp = item.split('=')
            res_dict[tmp[0]] = tmp[1]
        print(res_dict)
        return res_dict

    def strToDictNo3D(self, res_info):
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
    def strToDict3D(self, res_info):
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

    def decryptData(self, data, encryption, data_format):
        data = self.urlDecode(data)
        print(data)
        if data_format == '1':
            if encryption == '1':
                return xmltodict.parse(self.aesDecrypt(data))['Root']['Data']
            elif encryption == '2':
                return xmltodict.parse(self.tripleDesDecrypt(data))['Root']['Data']
        elif data_format == '2':
            if encryption == '1':
                return json.loads(self.aesDecrypt(data))
            elif encryption == '2':
                return json.loads(self.tripleDesDecrypt(data))

    def decryptDataNo3D(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))
    def decryptData3D(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def ThreeURL(self, data):
        # data = self.urlDecode(data)
        data['ThreeDURL'] = str(data['ThreeDURL'])
        threeD=data['ThreeDURL']
        print(threeD)
        return threeD

    def ActthreeDVerify(self, threed):
        op=self.webop
        op.goToURL(threed)
        time.sleep(5)
    def inputOTP(self, OTP):
        op = self.webop
        op.handleAlert()
        op.clickElem('GetOTPPwd')
        time.sleep(3)
        op.inputTextBox('OTP', OTP)
        time.sleep(2)
        op.clickElem('OTPSend')
    def GetInfoFromClientRedirectUrl(self):
        op = self.webop
        divText = op.drv.find_element_by_tag_name('body').text
        #divText=json.dumps(divText)
        divText = divText.encode('utf-8')
        divText=divText.replace("ResultData:","")
        self.log.INFO(divText)
        return divText
