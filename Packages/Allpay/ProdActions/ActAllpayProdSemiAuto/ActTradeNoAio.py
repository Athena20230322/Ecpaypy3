import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actTradeNoAio(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='TradeNoAio')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        #print req['MerchantTradeNo']
        return req

    def genOrderRequestInfoPlatformID(self, param_csv, plat_id=''):
        req = self.genArgsDictFromCSV(param_csv)
        req['PlatformID'] = plat_id
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        #print req['MerchantTradeNo']
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_actTradeNoAio = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_actTradeNoAio, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def createOrderByRequest(self, req_info):
        pass

    def genpostRequestToAPI(self, order_info_crt_res, api_url):
        query_order = self.postRequestToAPI(self.raw_sess, order_info_crt_res, api_url)
        return query_order
    
