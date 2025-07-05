# -*- coding: utf-8 -*-
import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actBindingTrade(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='BindingTrade')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        if req['MerchantID'] == '2001867':
            hash_key = self.feature_conf['JumpKey']
            hash_iv = self.feature_conf['JumpIV']
            APIHelper.__init__(self, hash_key, hash_iv)
        if req['MerchantID'] == '1063694':
            hash_key = self.feature_conf['SuntoryKey']
            hash_iv = self.feature_conf['SuntoryIV']
            APIHelper.__init__(self, hash_key, hash_iv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info, mode):
        op = self.webop
        form_act = self.feature_conf[mode]
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def inputOTPCredit(self, OTP):
        op = self.webop
        op.handleAlert()
        op.clickElem('GetOTPPwd')
        time.sleep(3)
        op.inputTextBox('OTP', OTP)
        time.sleep(2)
        op.clickElem('OTPSend')

    def inputPaymentPageCreditInfoSP(self, card_no, exp_year, exp_month, cvv, tellphone,testname,mode='normal'):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode == 'normal':
            op.clickElem('nav-section3')
            time.sleep(2)
        op.inputTextBox('CCHolderTemp', testname)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        op.inputTextBox('creditMM', exp_month)
        op.inputTextBox('creditYY', exp_year)

        op.inputTextBox('CreditBackThree', cvv)
        op.inputTextBox('CellPhoneCheck', tellphone)

        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        # op.clickElem('a.readySubmit.btn', findby='css')

    def inputPaymentPageCreditInfoE(self, card_no, exp_year, exp_month, cvv, tellphone,email,name, mode='normal'):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode == 'normal':
            op.clickElem('nav-section3')
            time.sleep(5)
        op.inputTextBox('CCHolderTemp', name)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        op.inputTextBox('creditMM', exp_month)
        op.inputTextBox('creditYY', exp_year)

        op.inputTextBox('CreditBackThree', cvv)
        op.inputTextBox('CellPhoneCheck', tellphone)
        op.inputTextBox('EmailTemp', email)

        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        # op.clickElem('a.readySubmit.btn', findby='css')

    def inputPaymentPageCreditInfo(self, card_no, exp_year, exp_month, cvv, tellphone, mode='normal'):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode == 'normal':
            op.clickElem('nav-section3')
            time.sleep(2)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        op.inputTextBox('creditMM', exp_month)
        op.inputTextBox('creditYY', exp_year)

        op.inputTextBox('CreditBackThree', cvv)
        op.inputTextBox('CellPhoneCheck', tellphone)

        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        # op.clickElem('a.readySubmit.btn', findby='css')
    def inputPaymentPageCreditInfo(self, card_no, exp_year, exp_month, cvv, tellphone, mode='normal'):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode == 'normal':
            op.clickElem('nav-section3')
            time.sleep(2)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        op.inputTextBox('creditMM', exp_month)
        op.inputTextBox('creditYY', exp_year)

        op.inputTextBox('CreditBackThree', cvv)
        op.inputTextBox('CellPhoneCheck', tellphone)

        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        # op.clickElem('a.readySubmit.btn', findby='css')

    def genQueryRequestInfo(self, param_csv, order_info):
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = order_info['MerchantTradeNo']
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genPostRequestToAPI(self, req_info, mode):
        form_act = self.feature_conf[mode]
        print(form_act)
        response = self.postRequestToAPI(self.genSession(), req_info, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def strToDict(self, res):
        res_list = res.split('&')
        res_dict = {}
        for item in res_list:
            res_dict[item.split('=')[0]] = item.split('=')[1]
        self.log.INFO(res_dict)
        return res_dict

    def genBindingRequestInfo(self, param_csv, query_dict, punctuation):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req['MerchantTradeNo'] = query_dict['MerchantTradeNo']
        req['AllpayTradeNo'] = query_dict['TradeNo']
        if req['MerchantMemberID'] == 'GEN_MEM_ID':
            if punctuation == 'Chinese':
                req['MerchantMemberID'] = self.gen_uid(with_dash=False)[0:28] + '哈'
            elif punctuation != '':
                req['MerchantMemberID'] = self.gen_uid(with_dash=False)[0:29] + punctuation
            else:
                req['MerchantMemberID'] = self.gen_uid(with_dash=False)[0:30]
        chksum = self.genChkMacVal(req, mode='local', codec='sha256')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def createOrderByRequest(self, req_info):
        pass