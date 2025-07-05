import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actQueryLogisticsTradeInfo(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='QueryLogisticsTradeInfo')
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
        return req

    def genOrderRequestInfoWithALID(self, param_csv, alid):
        req = self.genArgsDictFromCSV(param_csv)
        req['AllpayLogisticsID'] = alid
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info, api_url):
        op = self.webop
        form_act = self.feature_conf[api_url]
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def inputOTP(self):
        time.sleep(2)
        op = self.webop
        passcode = op.getElemValue('HightlightOTP', find_by='id')
        # print passcode
        sms_code = op.resolveSMSAuthCode(passcode)
        op.inputTextBox('SMSAuthCode', sms_code)
        op.clickElem('btnSendOtpValidate')

    def inputPaymentPageCreditInfo(self, card_no, exp_year, exp_month, cvv, cell_no, mode, testname, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()

        op.inputTextBox('CCHolderTemp', testname)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        op.inputTextBox('creditMM', exp_month)
        op.inputTextBox('creditYY', exp_year)

        op.inputTextBox('CreditBackThree', cvv)
        # op.inputTextBox('tmpIDNO', citizenid)

        op.inputTextBox('CellPhoneCheck', cell_no)
        # op.selectDropboxList('index', 1, 'selectInstallments')
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')

    def createOrderByRequest(self, req_info):
        pass

    def genOrderRequestCreateCVS(self, param_csv, merc_tno, merc_tdate, mode='B2C'):
        req = self.genArgsDictFromCSV(param_csv)
        req['MerchantTradeNo'] = merc_tno
        req['MerchantTradeDate'] = merc_tdate
        if mode == 'C2C':
            hash_key = 'XBERn1YOvpM9nfZc'
            hash_iv = 'h1ONHk4P4yqbl5LK'
            APIHelper.__init__(self, hash_key, hash_iv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genPostRequestToApi(self, order_info_res, api_url):
        form_actQueryLogisticsTradeInfo = self.feature_conf[api_url]
        query_order = self.postRequestToAPI(self.raw_sess, order_info_res, form_actQueryLogisticsTradeInfo)
        return query_order

    def modifyAllpaylogisticsSplit(self, modify_str, Split=False):
        print('####test_modify_str####')
        print(modify_str.decode('utf-8'))
        modify_str_chek = modify_str
        modify_str_chek = modify_str_chek.split('|')
        if modify_str_chek[0] != '1':
            raise IndexError("modifyAllpaylogisticsSplit: Input str index[0] is not one")
        if type(modify_str) is str:
            modify_str = modify_str.split('&')
            print('####test_allpaylogistics####')
            # print modify_str
            if Split:
                data = self.strToDict(modify_str_chek[1])
                print(data)
                return data
            else:
                print(modify_str[0][20:])
                return modify_str[0][20:]
        else:
            print('####Type_Info####')
            print(type(modify_str))
            print(TypeError("modifyAllpaylogisticsSplit: Paramter type is not a str"))
            return ''

    def strToDict(self, res):
        res_list = res.split('&')
        res_dict = {}
        for item in res_list:
            res_dict[item.split('=')[0]] = item.split('=')[1]
        return res_dict
