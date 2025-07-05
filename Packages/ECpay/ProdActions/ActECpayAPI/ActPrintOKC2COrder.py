import time
import json
import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actPrintOKC2COrder(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI',
                                                                feature_name='PrintOKC2COrder')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req
    
    def createAllpayOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Allpay_Order_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        #op.handleAlert()
        return browser_drv

    def createECpayOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['ECpay_Order_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def inputPaymentPageCreditInfo(self, owner_id, card_no, exp_year, exp_month, cvv, cell_no):
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
        op.inputTextBox('tmpIDNO', owner_id)
        op.inputTextBox('CellPhone_CreditPaySubmit', cell_no)
        op.clickElem('CreditPaySubmit')

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

    def genC2COrderRequestInfo(self, param_csv, merchant_trade_no, merchant_trade_date):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req['MerchantTradeNo'] = merchant_trade_no
        req['MerchantTradeDate'] = merchant_trade_date
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        print(req['MerchantTradeDate'])
        print(req)
        return req

    def createOrderByRequest(self, req_info):
        form_act = self.feature_conf['C2C_Order_API']
        print('post parameters: ')
        print(req_info)
        print(('post url: ' + form_act))
        response = requests.post(form_act, data=req_info)
        print('-----------------result-----------------')
        print((response.text))
        return response.text

    def getParamsFromResponse(self, response):
        params = {}
        params['logisticsID'] = (response.split('&')[0])[20:]
        params['CVSPaymentNo'] = (response.split('&')[3])[13:]
        print(('AllPayLogisticsId', params['logisticsID']))
        print(('CVSPaymentNo', params['CVSPaymentNo']))
        return params

    def genPrintInfo(self, param_csv, allpay_logistics_id, cvs_payment_no):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req['AllPayLogisticsID'] = allpay_logistics_id
        req['CVSPaymentNo'] = cvs_payment_no
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def printC2C(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Print_API']
        form_print = self.createHtmlFormJs('FormPrint', req_info, action=form_act, submit=True)
        print(form_print)
        browser_drv.execute_script(form_print)
        op.handleAlert()
        op.handleAlert()
        return browser_drv

    def getPrintElementExist(self):
        op = self.webop
        ele = op.getElem('form1', find_by='id')
        return ele

    def getPrintElements(self):
        op = self.webop
        eles = {}
        #op.clickElem('/html/body/embed', findby='xpath')
        test = op.getElem('/html/body/div/div[2]/iframe',find_by='xpath').click
        print(test)
        # eles['orderID'] = op.getElem('/html/body/strong/table/tbody/tr/td[2]/table/tbody/tr/td[2]',
        #                                        find_by='xpath').text
        # eles['CVSPaymentNo'] = op.getElem('/html/body/strong/table/tbody/tr/td[2]/table/tbody/tr[6]/td[2]',
        #                                   find_by='xpath').text
        # eles['sender'] = op.getElem('/html/body/strong/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]',
        #                             find_by='xpath').text
        # eles['receiver'] = op.getElem('/html/body/strong/table/tbody/tr/td[2]/table/tbody/tr[8]/td[2]',
        #                               find_by='xpath').text
        print(eles)
        return eles
