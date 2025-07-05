# -*- coding:utf-8 -*-
import time
import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actExpressMap(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI',
                                                                feature_name='ExpressMap')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genOrderRequestInfo(self, param_csv, merchant_trade_no):
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = merchant_trade_no
        return req

    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def ExpressMapByBrowser(self, browser_drv, req_info, device=-1):
        op = self.webop
        form_actExpressMap = self.feature_conf['Map_API']
        print(form_actExpressMap)
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_actExpressMap, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        if device == 0:
            return op.getElem('lv03')
        elif device == 1:
            return op.getElem('btnProcess2')
        else:
            pass



