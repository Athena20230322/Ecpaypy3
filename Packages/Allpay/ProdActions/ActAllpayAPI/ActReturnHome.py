import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actReturnHome(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='ReturnHome')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestHome(self, param_csv, alplogis_id):
        req = self.genArgsDictFromCSV(param_csv)
        if alplogis_id is None:
            req['AllPayLogisticsID'] = ''
            print(ValueError("genOrderRequestHome: input alplogis_id is None"))
        else:
            req['AllPayLogisticsID'] = alplogis_id
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestCVS(self, param_csv, alplogis_id):
        req = self.genArgsDictFromCSV(param_csv)
        req['AllPayLogisticsID'] = alplogis_id
        print('####test_AllPayLogisticsID####')
        print(req['AllPayLogisticsID'])
        change_address_sender = req['SenderAddress']
        change_address_receiver = req['ReceiverAddress']
        req['SenderAddress'] = change_address_sender.encode('utf-8')
        req['ReceiverAddress'] = change_address_receiver.encode('utf-8')
        print('####test_sender####')
        print(type(req['SenderAddress']))
        print('####test_receiver####')
        print(type(req['ReceiverAddress']))
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestCreateHome(self, param_csv, merc_tno, merc_tdate):
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = merc_tno
        req['MerchantTradeDate'] = merc_tdate
        for key in req:
            req[key] = req[key].encode('utf-8')
        # change_address_sender = req['SenderAddress']
        # change_address_receiver = req['ReceiverAddress']
        # req['SenderAddress'] = change_address_sender.encode('utf-8')
        # req['ReceiverAddress'] = change_address_receiver.encode('utf-8')
        print('####test_sender####')
        print(type(req['SenderAddress']))
        print('####test_receiver####')
        print(type(req['ReceiverAddress']))
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
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
        print(req['MerchantTradeNo'])
        return req

    def createOrderByBrowser(self, browser_drv, req_info, api_url):
        op = self.webop
        form_actReturnHome = self.feature_conf[api_url]
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_actReturnHome, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def genpostRequestToAPI(self, order_info_crt_res, api_url):
        query_order = self.postRequestToAPI(self.raw_sess, order_info_crt_res, api_url)
        return query_order

    def modifyAllpaylogisticsSplit(self, modify_str):
        print('####test_modify_str####')
        print(modify_str.decode('utf-8'))
        modify_str_chek = modify_str
        modify_str_chek = modify_str_chek.split('|')
        if modify_str_chek[0] != '1':
            print(IndexError("modifyAllpaylogisticsSplit: Input str index[0] is not one"))
            return None
        if type(modify_str) is str:
            modify_str = modify_str.split('&')
            print('####test_allpaylogistics####')
            # print modify_str
            print(modify_str[0][20:])
            return modify_str[0][20:]
        else:
            print('####Type_Info####')
            print(type(modify_str))
            print(TypeError("modifyAllpaylogisticsSplit: Paramter type is not a str"))
            return ''

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
        time.sleep(20)
        dic_otp_queryinfo = {
            'CellNo': phone_no,
            'OTPType': 'Credit_Payment'
        }

        otp_query = self.getRequestFromAPI(dic_otp_queryinfo, self.feature_conf['OtpCollectorAddr'])
        if otp_query != 'Not_Found':
            otp_data = json.loads(otp_query)
            return otp_data

    def inputOTP(self, otp_data):
        op = self.webop
        passcode = otp_data['OTP']
        print(passcode)
        op.inputTextBox('SMSAuthCode', passcode)
        op.clickElem('Submit')