# -*- coding:utf-8 -*-
import time
import json
import os
import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actTradeWithBindingCardID(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='TradeWithBindingCardID')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()

    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genBindingRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req['MerchantMemberID'] = self.gen_uid(with_dash=False)[0:20]
        chksum = self.genChkMacVal(req, mode='local', codec='sha256')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req
    
    def bindingByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Binding_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def inputCreditInfo(self, card_no, cvv):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        op.inputTextBox('CardPart1', cno_parts[0])
        op.inputTextBox('CardPart2', cno_parts[1])
        op.inputTextBox('CardPart3', cno_parts[2])
        op.inputTextBox('Card4No', cno_parts[3])
        op.clickElem('//*[@id="AuthExpireDateMM"]/option[7]', findby='xpath')
        op.clickElem('//*[@id="AuthExpireDateYY"]/option[22]', findby='xpath')
        op.inputTextBox('AuthCode', cvv)
        op.clickElem('btn_submit')

    def inputOTP(self, OTP):
        op = self.webop
        op.handleAlert()
        op.clickElem('GetOTPPwd')
        time.sleep(3)
        op.inputTextBox('OTP', OTP)
        time.sleep(2)
        op.clickElem('OTPSend')
    def GetInfoFromServerReplyUrl(self, merchant_trade_no):
        serverReplyUrl = 'http://192.168.150.131:5000/?IdentCol=MerchantTradeNo&IdentVal=' + merchant_trade_no
        print(serverReplyUrl)
        response = requests.get(serverReplyUrl, headers={'Connection': 'close'})
        self.log.INFO("response msg: " + response.text)
        self.log.INFO("status code: " + str(response.status_code))
        return response

    def GetInfoFromClientRedirectUrl(self):
        op = self.webop
        divText = op.drv.find_element_by_tag_name('body').text
        self.log.INFO(divText)
        return divText

    def GetInfoFromPageWithoutClientURL(self):
        op = self.webop
        divText = op.drv.find_element_by_tag_name('h2').text
        self.log.INFO(divText)
        return divText

    def redirectStrToDict(self, res_text):
        res_list = res_text.split('\n')
        res_dict = {}
        for ele in res_list:
            res_dict[ele.split(':')[0]] = ele.split(':')[1]
        return res_dict
