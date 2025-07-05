#-*- coding: utf-8 -*-
import requests
import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actCapture(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='Capture')
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
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_actCapture = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_actCapture, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def queryTradeInfo(self, req_info):
        query_trade_info_url = self.feature_conf['QueryOrder_API']
        print(query_trade_info_url)
        query_req = {}
        query_req.update({'MerchantID': req_info['MerchantID'],
                          'MerchantTradeNo': req_info['MerchantTradeNo'],
                          'TimeStamp': str(funcGen.getCurrentDatetimeStamp()[1])
                          })
        checksum = self.genChkMacVal(query_req, mode='local')
        query_req.update({'CheckMacValue': checksum})
        response = requests.post(url=query_trade_info_url, data=query_req)
        print((response.text))
        res_dict = self.strToDict(response.text)
        return res_dict

    def payMoney(self):
        op = self.webop
        time.sleep(3)
        op.maximizeWindow()
        op.clickElem('//input[@value="10001@2000@WebATM_TAISHIN"]', findby='xpath')
        # op.clickElem('/html/body/div/div[5]/div/div/div[3]/div/div/div[3]/ul/li[10]/input',
        #              findby='xpath')
        op.clickElem('WebAtmPaySubmit')
        op.handleAlert()
        op.clickElem('WebAtmPaySubmit')
        op.handleAlert()
        time.sleep(2)
        op.clickElem('/html/body/form/fieldset/p/input', findby='xpath')

    def genCaptureRequestInfo(self, param_csv, merchantTradeNo):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req['MerchantTradeNo'] = merchantTradeNo
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def captureResult(self, req_info):
        form_actCapture = self.feature_conf['Capture_API']
        response = requests.post(url=form_actCapture, data=req_info)
        print((response.text))
        return response.text

    def strToDict(self, req_str):
        result = {}
        for ele in req_str.split('&'):
            tmp_list = ele.split('=')
            result[tmp_list[0]] = tmp_list[1]
        print(result)
        return result

    def queryCaptureResult(self, browser_drv, acct, pw, merchant_trade_no):
        op = self.webop
        form_act = self.feature_conf['Query_API']
        form_genorder = self.createHtmlFormJs('FormQueryCapture', {}, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        time.sleep(1)
        op.inputTextBox('Account', acct)
        op.inputTextBox('Password', pw)
        captcha_code = op.resolveLoginCaptcha('_mvcCaptchaGuid')
        op.inputTextBox('allpayCaptchaValue', captcha_code)
        op.clickElem('LoginAllpay')
        time.sleep(2)
        leftFrame = browser_drv.find_element_by_id('leftFrame')
        browser_drv.switch_to_frame(leftFrame)
        op.clickElem('//*[@id="accordion-2"]/li[9]/a', findby='xpath')
        time.sleep(1)
        op.clickElem('//*[@id="accordion-2"]/li[9]/ul/li[5]/a', findby='xpath')
        time.sleep(2)
        browser_drv.switch_to_default_content()
        contentFrame = browser_drv.find_element_by_id('contentFrame')
        browser_drv.switch_to_frame(contentFrame)
        op.inputTextBox('MerchantTradeNo', merchant_trade_no)
        op.clickElem('ListTradeSubmit')
        time.sleep(3)
        result_ele = op.getElem('//*[@id="divAio"]/div/div/div/div[2]/div[1]/table/tbody/tr[2]/td[6]/span', find_by='xpath')
        return result_ele.text
