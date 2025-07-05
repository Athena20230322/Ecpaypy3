import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actAioCheckOut(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayProdSemiAuto', feature_name='AioCheckOut')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv, chkmac='local'):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode=chkmac)
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

    def createOrderByRequest(self, req_info):
        pass
    
    def selectInputCredit(self):
        op = self.webop
        op.selectDropboxList('value', '0', 'CreditID')

    
    def inputPaymentPageCreditInfo(self, card_no, exp_year, exp_month, cvv, cell_no, citizenid):
        op = self.webop
        cno_parts = card_no.split('-')
        #op.handleAlert()
        print("Before input")
        op.inputTextBox('CardNoPart1', cno_parts[0])
        op.inputTextBox('CardNoPart2', cno_parts[1])
        op.inputTextBox('CardNoPart3', cno_parts[2])
        op.inputTextBox('CardNoPart4', cno_parts[3])
        op.inputTextBox('CreditMM', exp_month)
        op.inputTextBox('CreditYY', exp_year)

        op.inputTextBox('CreditAuth', cvv)
        print("Info input")
        #op.inputTextBox('tmpIDNO', citizenid)
        
        #op.inputTextBox('CellPhone_CreditPaySubmit', cell_no)
        #op.clickElem('CreditPaySubmit')
        #op.handleAlert()
        #op.clickElem('CreditPaySubmit')
        op.handleAlert()
        submit = op.getElem('CreditPaySubmit')
        print(submit.location)
        op.clickElem('CreditPaySubmit', findby='id')
        
    def submitTrade(self):
        op = self.webop
        op.clickElem('CreditPaySubmit', findby='id')
        time.sleep(1)
        op.clickElem('a.readySubmit.btn', findby='css')
        
    def loginPaymentPage(self, username, pwd):  
        op = self.webop
        op.handleAlert()
        op.clickElem('LoginButton')
        op.inputTextBox('m_account', username)
        op.inputTextBox('m_pw', pwd)
        captimg = op.getElem('reloadCaptcha', find_by='class')
        
        cpat_code = op.resolveCaptchaElem(captimg)
        op.inputTextBox('login-captcha', cpat_code)
        op.clickElem('aLoginSubmit')
        elem_login_fail = op.getElem('divLoginError')
        print(elem_login_fail.get_attribute('style'))
        if elem_login_fail.get_attribute('style') == 'display: block;':
            captimg = op.getElem('reloadCaptcha', find_by='class')
            cpat_code = op.resolveCaptchaElem(captimg)
            op.inputTextBox('login-captcha', cpat_code)
            op.clickElem('aLoginSubmit')            
        
    
    def submitCVSPaymentRequest(self):
        op = self.webop
        op.handleAlert()
        op.clickElem('CvsPaySubmit')


    def submitBARcodePayment(self):
        op = self.webop
        '''Barcode payment is retired in Allpay'''
        #op.handleAlert()
        #op.clickElem('BarcodePaySubmit')
        #op.handleAlert()
        #time.sleep(1)
        #op.clickElem('BarcodePaySubmit')        
    
    
    def queryCreditOTP(self, phone_no):
        time.sleep(20)
        dic_otp_queryinfo = {
                            'CellNo' : phone_no,
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
    
    def postFormInHtml(self, html_str, action=''):
        pass
    
    #For Verify

    
    
    




#req_drv.get('https://pay-stage.allpay.com.tw/')

#print datetime.datetime.now()
#gen_order = cls_strhandler.postRequestToAPI(raw_sess, req, 'http://payment-stage.allpay.com.tw/Cashier/AioCheckOut/V2', withBrowser=req_drv)


#with open(r'd:\return.html', mode='w') as f:
    #f.write(gen_order)
    #f.close()
    



#HtmHelper.feed(gen_order)
#payment_dict = HtmHelper.formToPOSTDict('PayForm')
#payment_dict['paymentName'] = '10000@2003@Credit_GW'
#payment_dict['CardNo'] = '4311952222222222'
#payment_dict['CardValidMM'] = '05'
#payment_dict['CardValidYY'] = '22'
#payment_dict['CardAuthCode'] = '222'
#payment_dict['CellPhone'] = '0972005542'



#pay_order = cls_strhandler.postRequestToAPI(raw_sess, payment_dict, 'https://payment-stage.allpay.com.tw/Cashier/RetainPaymentType', withBrowser=req_drv)

#with open(r'd:\payment_return.html', mode='w') as f:
    #f.write(pay_order)
    #f.close()
    

#HtmHelper.clearCurrentTag()
#HtmHelper.feed(pay_order)

#CreditPayData = HtmHelper.formToPOSTDict('PostForm')
#CreditPayAct = HtmHelper.getFormAct('PostForm')
#print CreditPayData
#print CreditPayAct

#credit_post_a  = cls_strhandler.postRequestToAPI(raw_sess, CreditPayData, 'http://pay-stage.allpay.com.tw/Payment/Gateway', withBrowser=req_drv)


#with open(r'd:\credit_return_a.html', mode='w') as f:
    #f.write(credit_post_a)
    #f.close()

#HtmHelper.clearCurrentTag()
#HtmHelper.feed(credit_post_a)

#OTPform = HtmHelper.formToPOSTDict('/CreditPayment/VerifySMS')
#print OTPform

#time.sleep(20)

#dic_otp_queryinfo = {
#'CellNo' : '0972005542',
#'OTPType': 'Credit_Payment'
#}

#otp_query = cls_strhandler.getRequestFromAPI(dic_otp_queryinfo, 'http://104.214.145.51:443/')
#print "OTP Query:", otp_query

#if otp_query != 'Not_Found':
    #otp_data = json.loads(otp_query)

    #print otp_data
    
    #passcode = otp_data['OTP']
    #print passcode
    #OTPform['SMSAuthCode'] = passcode
    #OTPform['Language'] = 'lang-tw'
    
    #otp_post_res  = cls_strhandler.postRequestToAPI(raw_sess, OTPform, 'https://pay-stage.allpay.com.tw/CreditPayment/VerifySMS', trencode_dotnet=True, withBrowser=req_drv)
    
    #with open(r'd:\otp_post_res.html', mode='w') as f:
        #f.write(otp_post_res)
        #f.close()
        
    #HtmHelper.clearCurrentTag()
    #HtmHelper.feed(otp_post_res)
    #Credit_Autosubmit = HtmHelper.formToPOSTDict('PostForm')
    
    #credit_auth = cls_strhandler.postRequestToAPI(raw_sess, Credit_Autosubmit, 'https://cc-stage.allpay.com.tw/form_ssl.php', withBrowser=req_drv)
    
    #with open(r'd:\credit_auth.html', mode='w') as f:
        #f.write(credit_auth)
        #f.close()    
    



#HtmHelper.feed(pay_order)
#ATMreq_dict = HtmHelper.formToPOSTDict('PostForm')
#atm_request = cls_strhandler.postRequestToAPI(ATMreq_dict, 'http://payment-stage.allpay.com.tw/PaymentRule/ATMPaymentInfo')

#with open(r'd:\ATM_return.html', mode='w') as f:
    #f.write(atm_request)
    #f.close()