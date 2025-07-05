#-*- coding:utf-8 -*-
import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actReturnHiLifeCVS(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo',
                                                                 feature_cat='AllpayAPI',
                                                                  feature_name='ReturnHiLifeCVS')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestCVS(self, param_csv, alplogis_id, sel_alplogis_id=False, sel_space=False):
        req = self.genArgsDictFromCSV(param_csv, sel_space)
        if sel_alplogis_id == False:
            if alplogis_id is None:
                req['AllPayLogisticsID'] = '12345'
                # raise ValueError("genOrderRequestCVS: input alplogis_id is None")
            else:
                req['AllPayLogisticsID'] = alplogis_id
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestCreateCVS(self, param_csv, merc_tno, merc_tdate):
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = merc_tno
        req['MerchantTradeDate'] = merc_tdate
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def createOrderByBrowser(self, browser_drv, req_info, api_url):
        op = self.webop
        form_actReturnHiLifeCVS = self.feature_conf[api_url]
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_actReturnHiLifeCVS, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def genpostRequestToAPI(self, order_info_crt_res, api_url):
        form_actReturnHiLifeCVS = self.feature_conf[api_url]
        query_order = self.postRequestToAPI(self.raw_sess, order_info_crt_res, form_actReturnHiLifeCVS)
        return query_order

    def modifyAllpaylogisticsSplit(self, modify_str):
        print('####test_modify_str####')
        print(modify_str.decode('utf-8'))
        modify_str_chek = modify_str
        modify_str_chek = modify_str_chek.split('|')
        if modify_str_chek[0] != '0':
            self.log.WARN("modifyAllpaylogisticsSplit: Input str index[0] is not zero\n"
                          "The index[0] is %s" % (modify_str_chek[0]))
            raise IndexError("modifyAllpaylogisticsSplit: Input str index[0] is not zero")
        if type(modify_str) is str:
            modify_str = modify_str.split('&')
            print('####test_allpaylogistics####')
            print(modify_str[0][20:])
            return modify_str[0][20:]
        else:
            self.log.WARN("modifyAllpaylogisticsSplit: Parameter type is not a str type\n"
                          "The modify_str type is %s" % (type(modify_str)))
            raise TypeError("modifyAllpaylogisticsSplit: Parameter type is not a str type")

    def inputPaymentPageCreditInfoEC(self, card_no, exp_year, exp_month, cvv, cell_no):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()

        op.inputTextBox('CardNoPart1', cno_parts[0])
        op.inputTextBox('CardNoPart2', cno_parts[1])
        op.inputTextBox('CardNoPart3', cno_parts[2])
        op.inputTextBox('CardNoPart4', cno_parts[3])
        op.selectDropboxList('value', exp_month, 'CreditMM')
        op.selectDropboxList('value', exp_year, 'CreditYY')
        op.inputTextBox('CreditAuth', cvv)
        op.inputTextBox('CellPhoneCheck', cell_no)
        op.clickElem('CreditPaySubmit')
        op.handleAlert()
        op.clickElem('CreditPaySubmit')
        op.handleAlert()

    def inputPaymentPageCreditInfoAP(self, card_owner_id, card_no, exp_year, exp_month, cvv, cell_no):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()

        op.inputTextBox('CardNoPart1', cno_parts[0])
        op.inputTextBox('CardNoPart2', cno_parts[1])
        op.inputTextBox('CardNoPart3', cno_parts[2])
        op.inputTextBox('CardNoPart4', cno_parts[3])
        op.inputTextBox('CreditMM', exp_month)
        op.inputTextBox('CreditYY', exp_year)

        op.inputTextBox('CreditAuth', cvv)
        op.inputTextBox('tmpIDNO', card_owner_id)
        op.inputTextBox('CellPhone_CreditPaySubmit', cell_no)
        op.clickElem('CreditPaySubmit')

    def submitCVSPaymentRequest(self):
        op = self.webop
        op.handleAlert()
        op.clickElem('CvsPaySubmit')
        op.handleAlert()
        time.sleep(1)
        op.clickElem('CvsPaySubmit')

    def submitBARcodePayment(self):
        op = self.webop
        op.handleAlert()
        op.clickElem('BarcodePaySubmit')
        op.handleAlert()
        time.sleep(1)
        op.clickElem('BarcodePaySubmit')

    def queryCreditOTP(self, phone_no):
        for catch_otp in range(3):
            time.sleep(20)
            dic_otp_queryinfo = {
                'CellNo': phone_no,
                'OTPType': 'ECpay_Credit_Payment',
                'TimeRange': 300
            }

            otp_query = self.getRequestFromAPI(dic_otp_queryinfo, self.feature_conf['OtpCollectorAddr'])
            print('#######################')
            print(otp_query)
            if otp_query != 'Not_Found':
                otp_data = json.loads(otp_query)
                return otp_data

    def inputOTP(self, otp_data):
        op = self.webop
        passcode = otp_data['OTP']
        print(passcode)
        op.inputTextBox('SMSAuthCode', passcode)
        op.clickElem('Submit')

    def strToDict(self, res):
        res_list = res.split('&')
        res_dict = {}
        for item in res_list:
            res_dict[item.split('=')[0]] = item.split('=')[1]
        return res_dict
