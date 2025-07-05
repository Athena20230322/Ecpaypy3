import time
import json
import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actPrintHILIFEC2COrder(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI',
                                                                feature_name='PrintHILIFEC2COrder')
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
        op.handleAlert()
        return browser_drv

    def genC2COrderRequestInfo(self, param_csv, merchant_trade_no, merchant_trade_date):
        req = self.genArgsDictFromCSV(param_csv)
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
        rtnMsg = response.split('|')[1]
        print(rtnMsg)
        return rtnMsg

    def genPrintInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        req['AllPayLogisticsID'] = ''
        req['CVSPaymentNo'] = ''
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
        alert = browser_drv.switch_to_alert()
        alert_text = alert.text
        print(alert_text)
        op.handleAlert()
        return alert_text
