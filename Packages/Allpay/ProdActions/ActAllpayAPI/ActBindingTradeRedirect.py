# -*- coding: utf-8 -*-
import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actBindingTradeRedirect(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='BindingTradeRedirect')
        hash_key = self.feature_conf['JumpKey']
        hash_iv = self.feature_conf['JumpIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        if req['MerchantID'] == '2000132':
            hash_key = self.feature_conf['HashKey']
            hash_iv = self.feature_conf['HashIV']
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

    def inputPaymentPageCreditInfo(self, card_no, exp_year, exp_month, cvv):
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
        op.clickElem('CreditPaySubmit')
        op.handleAlert()
        op.clickElem('#pay-confirm-popup > form > div > div.mp-btn-block > a.readySubmit.btn', findby='css')

    def inputRedirectPaymentPageCreditInfo(self, card_no, exp_year, exp_month, cvv):
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
        op.clickElem('CreditPaySubmit')
        op.handleAlert()
        op.clickElem('CreditPaySubmit')
        op.handleAlert()

    def genQueryRequestInfo(self, param_csv, order_info):
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = order_info['MerchantTradeNo']
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

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

    def genPostRequestToAPI(self, req_info, mode):
        form_act = self.feature_conf[mode]
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
