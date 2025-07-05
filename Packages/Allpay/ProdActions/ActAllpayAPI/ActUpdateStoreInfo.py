import time
import json
import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actUpdateStoreInfo(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI',
                                                                feature_name='UpdateStoreInfo')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
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
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = merchant_trade_no
        req['MerchantTradeDate'] = merchant_trade_date
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        print(req['MerchantTradeDate'])
        return req

    def createOrderByRequest(self, req_info):
        form_act = self.feature_conf['Shipment_Order_API']
        response = requests.post(form_act, data=req_info)
        print((response.text))
        return response.text

    def getRtnMsg(self, response):
        result = response.split('|')[1]
        return result

    def genUpdateStoreInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        req['AllPayLogisticsID'] = ''
        req['CVSPaymentNo'] = ''
        req['CVSValidationNo'] = ''
        print(req)
        return req

    def genCheckMacValue(self, req):
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def updateStoreInfoByRequest(self, req_info):
        form_act = self.feature_conf['Update_Store_API']
        response = requests.post(form_act, data=req_info)
        print((response.text))
        return response.text

