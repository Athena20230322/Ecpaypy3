# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, urllib.error
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actBindingCardID(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='BindingCardID')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genBindingRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if req['MerchantMemberID'] != '':
            if req['MerchantMemberID'] == 'GEN_MEM_ID':
                req['MerchantMemberID'] = self.gen_uid(with_dash=False)[0:30]
            elif req['MerchantMemberID'] == 'GEN_MEM_ID_P':
                req['MerchantMemberID'] = '3003004' + self.gen_uid(with_dash=False)[0:23]
            elif req['MerchantMemberID'] == 'GEN_MEM_ID_M':
                req['MerchantMemberID'] = '2000214'+self.gen_uid(with_dash=False)[0:23]
        if 'PlatformID' in req:
            if req['PlatformID'] == '3003004':
                hash_key = self.feature_conf['PIDKey']
                hash_iv = self.feature_conf['PIDIV']
                APIHelper.__init__(self, hash_key, hash_iv)
        chksum = self.genChkMacVal(req, mode='local', codec='sha256')
        # print chksum
        req['CheckMacValue'] = chksum
        return req

    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['BindingCard_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def inputCreditCardInfo(self, card_no, exp_year, exp_month, cvv):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        op.inputTextBox('CardPart1', cno_parts[0])
        op.inputTextBox('CardPart2', cno_parts[1])
        op.inputTextBox('CardPart3', cno_parts[2])
        op.inputTextBox('Card4No', cno_parts[3])
        op.inputTextBox('AuthExpireDateMM', exp_month)
        op.inputTextBox('AuthExpireDateYY', exp_year)
        op.inputTextBox('AuthCode', cvv)
        op.clickElem('btn_submit')

    def GetInfoFromClientRedirectUrl(self):
        op = self.webop
        divText = op.drv.find_element_by_tag_name('body').text
        self.log.INFO(divText)
        return divText

    def redirectStrToDict(self, res_text):
        res_list = res_text.split('\n')
        res_dict = {}
        for ele in res_list:
            if ele != '':
                ele = ele.encode('utf-8')
                res_dict[ele.split(':')[0]] = ele.split(':')[1]
                if ele.split(':')[0] == 'BindingDate' and ele.split(':')[1] !='':
                    res_dict['BindingDate'] = ele.split(':')[1]+':'+ele.split(':')[2]+':'+ele.split(':')[3]
        res_dict['RtnMsg'] = urllib.parse.unquote_plus(res_dict['RtnMsg'])
        return res_dict
