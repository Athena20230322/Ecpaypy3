import requests
import datetime
from datetime import timedelta
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper


class actUpdateShipInfo(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI',
                                                                feature_name='UpdateShipInfo')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.htm_helper = HtmlHelper()
        
    def genB2COrderRequestInfo(self, param_csv, merchant_trade_no, merchant_trade_date):
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = merchant_trade_no
        req['MerchantTradeDate'] = merchant_trade_date
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def createOrderByRequest(self, req_info):
        form_act = self.feature_conf['Shipment_Order_API']
        response = requests.post(form_act, data=req_info)
        print((response.text))
        return response.text

    def getRtnMsg(self, response):
        result = (response.split('|')[1])
        return result

    def genUpdateShipInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        req['AllPayLogisticsID'] = ''
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

