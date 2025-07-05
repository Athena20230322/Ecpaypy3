import time
import json
import requests
from selenium.webdriver.common.keys import Keys
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate



class actQueryCreditTrade(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='QueryCreditTrade')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
    def genQueryRequestInfo(self, param_csv, MerchantTradeNo):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if len(req['MerchantTradeNo']) == 0:
            req['MerchantTradeNo'] = MerchantTradeNo
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def inputPaymentPageCreditInfo(self, card_no, exp_year, exp_month, cvv, cell_no,testname):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        op.inputTextBox('CCHolderTemp', testname)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        op.inputTextBox('creditMM', exp_month)
        op.inputTextBox('creditYY', exp_year)
        op.inputTextBox('CreditBackThree', cvv)
        op.inputTextBox('CellPhoneCheck', cell_no)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')

    def inputPaymentPageCreditInfoE(self, card_no, exp_year, exp_month, cvv, cell_no,email, testname):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        op.inputTextBox('CCHolderTemp', testname)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        op.inputTextBox('creditMM', exp_month)
        op.inputTextBox('creditYY', exp_year)
        op.inputTextBox('CreditBackThree', cvv)
        op.inputTextBox('EmailTemp', email)
        op.inputTextBox('CellPhoneCheck', cell_no)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')


    def queryCreditOTP(self, phone_no):
        time.sleep(20)
        dic_otp_queryinfo = {
            'CellNo': phone_no,
            'OTPType': 'ECpay_Credit_Payment'
        }

        otp_query = self.getRequestFromAPI(dic_otp_queryinfo, self.feature_conf['OtpCollectorAddr'])
        if otp_query != 'Not_Found':
            otp_data = json.loads(otp_query)
            return otp_data

    # def inputOTP(self, otp_data):
    #     op = self.webop
    #     passcode = otp_data['OTP']
    #     print passcode
    #     op.inputTextBox('SMSAuthCode', passcode)
    #     op.clickElem('Submit')
    #     op.handleAlert()

    def inputOTP(self):
        time.sleep(2)
        op = self.webop
        passcode = op.getElemValue('HightlightOTP', find_by='id')
        # print passcode
        sms_code = op.resolveSMSAuthCode(passcode)
        op.inputTextBox('SMSAuthCode', sms_code)
        op.clickElem('btnSendOtpValidate')

    def queryCreditCardPeriodInfo(self, req_info):
        form_actQueryCreditTrade = self.feature_conf['Query_API']
        response = requests.post(url=form_actQueryCreditTrade, data=req_info)
        self.log.INFO(response.json())
        return response.json()

    def createOrderByRequest(self, req_info):
        pass

