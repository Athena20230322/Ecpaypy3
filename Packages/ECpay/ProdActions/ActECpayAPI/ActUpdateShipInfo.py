import requests
import datetime
from datetime import timedelta
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actUpdateShipInfo(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI',
                                                                feature_name='UpdateShipInfo')
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

    def genB2COrderRequestInfo(self, param_csv, merchant_trade_no, merchant_trade_date):
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = merchant_trade_no
        req['MerchantTradeDate'] = merchant_trade_date
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def createECpayOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['ECpay_Order_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def createAllpayOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Allpay_Order_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def createOrderByRequest(self, req_info):
        form_act = self.feature_conf['Shipment_Order_API']
        response = requests.post(form_act, data=req_info)
        print((response.text))
        return response.text

    def getLogisticsID(self, response):
        logisticsID = (response.split('&')[0])[20:]
        return logisticsID

    def genUpdateShipInfo(self, param_csv, allpay_logistics_id):
        req = self.genArgsDictFromCSV(param_csv)
        req['AllPayLogisticsID'] = allpay_logistics_id
        return req

    def updateShipmentDate(self, day):
        today = datetime.date.today()
        end_day = (today + timedelta(days=day)).strftime('%Y/%m/%d')
        print(end_day)
        return end_day

    def genCheckMacValue(self, req):
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req


    def updateShipInfoByRequest(self, req_info):
        form_act = self.feature_conf['Update_Shipment_API']
        response = requests.post(form_act, data=req_info)
        print((response.text))
        return response.text

