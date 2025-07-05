import collections
import time
import json
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actMobileCreateServerOrder(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='MobileCreateServerOrder')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['MobileCreateServerOrder_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['MobileCreateServerOrder_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def strToDict(self, res_info):
        print('str1: ' + res_info)
        # res_info = self.urlDecode(res_info)
        # print 'str2: ' + res_info
        res_dict = json.loads(res_info)
        print(res_dict)
        return res_dict

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