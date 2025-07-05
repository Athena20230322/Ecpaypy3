# -*- coding: utf-8 -*-
import time
import json
import os
import urllib.request, urllib.parse, urllib.error
import collections
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actEmbeddedgettokenbytrade(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='EmbeddedPayToken')
        hash_key = self.feature_conf['HashKey1']
        hash_iv = self.feature_conf['HashIV1']
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

    def genOrderRequestInfoNoThreeD2(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)

        ConsumerInfo = self.genArgsDictFromCSV(param_csv)
        # Gwinfo = self.genArgsDictFromCSV(param_csv)

        req = {}
        req['MerchantID'] = data['MerchantID']
        # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('MerchantMemberID')
        data.pop('Email')
        data.pop('Phone')
        data.pop('Name')
        data.pop('CountryCode')
        data.pop('Address')
        data['ConsumerInfo']=ConsumerInfo

        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('ConsumerInfo')
        rqHeader.pop('MerchantMemberID')
        rqHeader.pop('Email')
        rqHeader.pop('Phone')
        rqHeader.pop('Name')
        rqHeader.pop('CountryCode')
        rqHeader.pop('Address')
        rqHeader.pop('CustomField')

        ConsumerInfo.pop('Timestamp')
        ConsumerInfo.pop('RqID')
        ConsumerInfo.pop('Revision')
        ConsumerInfo.pop('MerchantID')
        ConsumerInfo.pop('PlatformID')
        ConsumerInfo.pop('CustomField')


        # data['OrderInfo'] = OrderInfo
        # data['CardInfo'] = CardInfo
        # data['ATMInfo'] = ATMInfo
        # data['CVSInfo'] = CVSInfo
        # data['BarcodeInfo'] = BarcodeInfo
        data['ConsumerInfo'] = ConsumerInfo
        # data['Gwinfo'] = Gwinfo

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

    def genOrderRequestInfoGetTokenbyBindingCard(self, param_csv, inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)

        rqHeader = self.genArgsDictFromCSV(param_csv)



        req = {}

        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value

                # req['MerchantTradeNo'] = self.gen_uid(with_dash=False)[0:30]

        req['MerchantID'] = data['MerchantID']
        data['MerchantTradeNo'] = data['MerchantTradeNo']
        # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
       # data.pop('MerchantTradeDate')


        rqHeader.pop('MerchantID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('MerchantMemberID')
        rqHeader.pop('Email')
        rqHeader.pop('Phone')
        rqHeader.pop('Name')
        rqHeader.pop('CountryCode')
        rqHeader.pop('Address')
        rqHeader.pop('BindCardResultURL')
        rqHeader.pop('CustomField')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('TotalAmount')





        # data['Gwinfo'] = Gwinfo

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



    def genOrderRequestInfoThreeD2(self, param_csv,inject_value=''):
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


        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value


                #req['MerchantTradeNo'] = self.gen_uid(with_dash=False)[0:30]


        req['MerchantID'] = data['MerchantID']
        data['MerchantTradeNo'] = data ['MerchantTradeNo']
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





        # Gwinfo.pop('Timestamp')
        # Gwinfo.pop('RqID')
        # Gwinfo.pop('Revision')
        # Gwinfo.pop('MerchantID')
        # Gwinfo.pop('PlatformID')
        # Gwinfo.pop('OrderInfo')
        # Gwinfo.pop('TotalAmount')
        # Gwinfo.pop('ItemName')
        # Gwinfo.pop('TradeDesc')
        # Gwinfo.pop('Remark')
        # Gwinfo.pop('ReturnURL')
        # Gwinfo.pop('MerchantTradeNo')
        # Gwinfo.pop('MerchantTradeDate')
        # Gwinfo.pop('ChoosePayment')
        # Gwinfo.pop('CardInfo')
        # Gwinfo.pop('CardNo')
        # Gwinfo.pop('CardValidMM')
        # Gwinfo.pop('CardValidYY')
        # Gwinfo.pop('CardCVV2')
        # Gwinfo.pop('Redeem')
        # Gwinfo.pop('CreditInstallment')
        # Gwinfo.pop('PeriodAmount')
        # Gwinfo.pop('PeriodType')
        # Gwinfo.pop('Frequency')
        # Gwinfo.pop('ExecTimes')
        # Gwinfo.pop('PeriodReturnURL')
        # Gwinfo.pop('OrderResultURL')
        # Gwinfo.pop('ConsumerInfo')
        # Gwinfo.pop('CustomField')
        # Gwinfo.pop('Gwinfo')

        data['OrderInfo'] = OrderInfo
        data['CardInfo'] = CardInfo
        data['ATMInfo'] = ATMInfo
        data['CVSInfo'] = CVSInfo
        data['BarcodeInfo'] = BarcodeInfo
        data['ConsumerInfo'] = ConsumerInfo
        # data['Gwinfo'] = Gwinfo

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

    def genOrderRequestInfoTokenQuery(self, param_csv,token):
        data = self.genArgsDictFromCSV(param_csv)
        print(token)
        data['Token']=token['Token']
        print(data['Token'])
        data = json.dumps(data)
        data = data.encode('utf-8')

        print(data)
        data = self.urlEncode(data)
        #print data
        data = self.aesEncrypt(data)
        #print data
        print(data)
        return data
    def genOrderRequestInfoB2B(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        req={}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:20]
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID']='3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ItemSeq')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemAmount')
        data.pop('ItemTax')
        data.pop('ItemRemark')

        rqHeader.pop('MerchantID')
        rqHeader.pop('ItemName')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('InvoiceTime')
        rqHeader.pop('ItemSeq')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('ClearanceMark')
        rqHeader.pop('InvType')
        rqHeader.pop('TaxType')
        rqHeader.pop('TaxRate')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('TaxAmount')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('InvoiceRemark')


        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('MerchantID')
        Items.pop('RelateNumber')
        Items.pop('InvoiceTime')
        Items.pop('CustomerIdentifier')
        Items.pop('CustomerEmail')
        Items.pop('ClearanceMark')
        Items.pop('InvType')
        Items.pop('TaxType')
        Items.pop('TaxRate')
        Items.pop('SalesAmount')
        Items.pop('TaxAmount')
        Items.pop('TotalAmount')
        Items.pop('InvoiceRemark')


        data['Items'] = [Items]

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

    def genOrderRequestInfoB2Bitem(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        Items1 = self.genArgsDictFromCSV(param_csv)
        Items2 = self.genArgsDictFromCSV(param_csv)
        req = {}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:20]
        req['MerchantID'] = data['MerchantID']
       # req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ItemSeq')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemAmount')
        data.pop('ItemTax')
        data.pop('ItemRemark')

        rqHeader.pop('MerchantID')
        rqHeader.pop('ItemName')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('InvoiceTime')
        rqHeader.pop('ItemSeq')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('ClearanceMark')
        rqHeader.pop('InvType')
        rqHeader.pop('TaxType')
        rqHeader.pop('TaxRate')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('TaxAmount')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('InvoiceRemark')

        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('MerchantID')
        Items.pop('RelateNumber')
        Items.pop('InvoiceTime')
        Items.pop('CustomerIdentifier')
        Items.pop('CustomerEmail')
        Items.pop('ClearanceMark')
        Items.pop('InvType')
        Items.pop('TaxType')
        Items.pop('TaxRate')
        Items.pop('SalesAmount')
        Items.pop('TaxAmount')
        Items.pop('TotalAmount')
        Items.pop('InvoiceRemark')

        Items1.pop('Timestamp')
        Items1.pop('RqID')
        Items1.pop('Revision')
        Items1.pop('MerchantID')
        Items1.pop('RelateNumber')
        Items1.pop('InvoiceTime')
        Items1.pop('CustomerIdentifier')
        Items1.pop('CustomerEmail')
        Items1.pop('ClearanceMark')
        Items1.pop('InvType')
        Items1.pop('TaxType')
        Items1.pop('TaxRate')
        Items1.pop('SalesAmount')
        Items1.pop('TaxAmount')
        Items1.pop('TotalAmount')
        Items1.pop('InvoiceRemark')

        Items2.pop('Timestamp')
        Items2.pop('RqID')
        Items2.pop('Revision')
        Items2.pop('MerchantID')
        Items2.pop('RelateNumber')
        Items2.pop('InvoiceTime')
        Items2.pop('CustomerIdentifier')
        Items2.pop('CustomerEmail')
        Items2.pop('ClearanceMark')
        Items2.pop('InvType')
        Items2.pop('TaxType')
        Items2.pop('TaxRate')
        Items2.pop('SalesAmount')
        Items2.pop('TaxAmount')
        Items2.pop('TotalAmount')
        Items2.pop('InvoiceRemark')


        data['Items'] = [Items,Items1,Items2]

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

    def genOrderRequestInfoB2Bitem1(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        Items = self.genArgsDictFromCSV(param_csv)
        Items1 = self.genArgsDictFromCSV(param_csv)
        Items2 = self.genArgsDictFromCSV(param_csv)
        req = {}
        if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
            data['RelateNumber'] = self.gen_uid(with_dash=False)[0:20]
        req['MerchantID'] = data['MerchantID']
        #req['PlatformID'] = '3083192'
        data.pop('Timestamp')
        data.pop('RqID')
        data.pop('Revision')
        data.pop('ItemSeq')
        data.pop('ItemName')
        data.pop('ItemCount')
        data.pop('ItemWord')
        data.pop('ItemPrice')
        data.pop('ItemAmount')
        data.pop('ItemTax')
        data.pop('ItemRemark')

        rqHeader.pop('MerchantID')
        rqHeader.pop('ItemName')
        rqHeader.pop('RelateNumber')
        rqHeader.pop('InvoiceTime')
        rqHeader.pop('ItemSeq')
        rqHeader.pop('CustomerIdentifier')
        rqHeader.pop('ClearanceMark')
        rqHeader.pop('InvType')
        rqHeader.pop('TaxType')
        rqHeader.pop('TaxRate')
        rqHeader.pop('SalesAmount')
        rqHeader.pop('TaxAmount')
        rqHeader.pop('TotalAmount')
        rqHeader.pop('InvoiceRemark')

        Items.pop('Timestamp')
        Items.pop('RqID')
        Items.pop('Revision')
        Items.pop('MerchantID')
        Items.pop('RelateNumber')
        Items.pop('InvoiceTime')
        Items.pop('CustomerIdentifier')
        Items.pop('CustomerEmail')
        Items.pop('ClearanceMark')
        Items.pop('InvType')
        Items.pop('TaxType')
        Items.pop('TaxRate')
        Items.pop('SalesAmount')
        Items.pop('TaxAmount')
        Items.pop('TotalAmount')
        Items.pop('InvoiceRemark')

        Items1.pop('Timestamp')
        Items1.pop('RqID')
        Items1.pop('Revision')
        Items1.pop('MerchantID')
        Items1.pop('RelateNumber')
        Items1.pop('InvoiceTime')
        Items1.pop('CustomerIdentifier')
        Items1.pop('CustomerEmail')
        Items1.pop('ClearanceMark')
        Items1.pop('InvType')
        Items1.pop('TaxType')
        Items1.pop('TaxRate')
        Items1.pop('SalesAmount')
        Items1.pop('TaxAmount')
        Items1.pop('TotalAmount')
        Items1.pop('InvoiceRemark')

        Items1['ItemSeq'] = '2'

        Items2.pop('Timestamp')
        Items2.pop('RqID')
        Items2.pop('Revision')
        Items2.pop('MerchantID')
        Items2.pop('RelateNumber')
        Items2.pop('InvoiceTime')
        Items2.pop('CustomerIdentifier')
        Items2.pop('CustomerEmail')
        Items2.pop('ClearanceMark')
        Items2.pop('InvType')
        Items2.pop('TaxType')
        Items2.pop('TaxRate')
        Items2.pop('SalesAmount')
        Items2.pop('TaxAmount')
        Items2.pop('TotalAmount')
        Items2.pop('InvoiceRemark')

        Items2['ItemSeq'] = '3'

        data['Items'] = [Items,Items1,Items2]

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
    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['Appsdktoken_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genPostRequestToAPIkeyexchange(self, req_info):
        form_act = self.feature_conf['Appsdktoken_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        Language = 'en-US'
        UUID ='ae81566dc1e70479'
        AppName ='com.ecpay.appsdk'
        AppInfo ='{"DeviceInfo":"SM-G955F","IsSimulator":0,"OS":2,"OSVersion":"8.0.0","Vers":"1.0.0"}'
        response = self.postRequestToAPIkeyexchange(self.genSession(), od_arg_dict, form_act, Language, UUID,AppName,AppInfo,trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response



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

        res_dict = eval(res_info)

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

    def decryptDatab2b2(self, data):
        #data = self.urlDecode(data)
        print(data)
        return self.aesDecrypt(data)



