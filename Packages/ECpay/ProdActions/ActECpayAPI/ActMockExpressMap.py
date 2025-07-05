# -*- coding:utf-8 -*-
import time
import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actMockExpressMap(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI',
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

    def changeC2CHash(self):
        hash_key = self.feature_conf['HashKeyC2C']
        hash_iv = self.feature_conf['HashIVC2C']
        APIHelper.__init__(self, hash_key, hash_iv)

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

    def inputPaymentPageCreditInfo(self, card_owner_id, card_no, exp_year, exp_month, cvv, cell_no):
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
        op.inputTextBox('CellPhoneCheck', cell_no)
        op.clickElem('CreditPaySubmit')
        op.handleAlert()
        op.clickElem('CreditPaySubmit')
        op.handleAlert()

    def inputC2CPaymentPageCreditInfo(self, owner_name, card_no, exp_year, exp_month, cvv):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        op.inputTextBox('CardHolderTemp', owner_name)
        op.inputTextBox('CardNoPart1', cno_parts[0])
        op.inputTextBox('CardNoPart2', cno_parts[1])
        op.inputTextBox('CardNoPart3', cno_parts[2])
        op.inputTextBox('CardNoPart4', cno_parts[3])
        op.selectDropboxList('value', exp_month, 'CreditMM')
        op.selectDropboxList('value', exp_year, 'CreditYY')
        op.inputTextBox('CreditAuth', cvv)
        op.clickElem('CreditPaySubmit')
        op.handleAlert()
        op.clickElem('CreditPaySubmit')
        op.handleAlert()

    def ExpressMapByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_actExpressMap = self.feature_conf['Map_API']
        print(form_actExpressMap)
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_actExpressMap, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()

    def ChooseFAMIStore(self):
        op = self.webop
        op.clickElem('//*[@id="SubmitForm"]/input[2]', findby='xpath')
        time.sleep(1)

    def ChooseUniMartStore(self, web_driver):
        op = self.webop
        # op.clickElem('//*[@id="SubmitForm"]/input[1]', findby='xpath')
        op.clickElem('UnimartPost')
        time.sleep(1)

    def ChooseHiLifeMockStore(self):
        op = self.webop
        op.clickElem('HiLifePost')
        # op.clickElem('/html/body/div/div[2]/input', findby='xpath')
        time.sleep(1)

    def ChooseHiLifeStore(self, device=0):
        op = self.webop
        if device == 0:
            op.clickElem('lv03', findby='id')
            time.sleep(1)
            op.inputTextBox('txtShopID', '3629', findby='id')
            op.clickElem('btnSubmit3', findby='id')
            time.sleep(1)
            op.clickElem('GridView1_imgBtnDetail_0', findby='id')
            time.sleep(1)
            op.clickElem('btnSelSure', findby='id')
        else:
            op.clickElem('btnProcess2')
            time.sleep(1)
            op.inputTextBox('txtShopID', '3629')
            op.clickElem('btnSubmit3')
            time.sleep(1)
            op.clickElem('ListData_btnLink_0')
            time.sleep(1)
            op.clickElem('btnSelSure')

    def GetInfoFromServerReplyUrl(self, merchant_trade_no):
        serverReplyUrl = 'http://192.168.150.131:5000/?IdentCol=MerchantTradeNo&IdentVal=' + merchant_trade_no
        print(serverReplyUrl)
        response = requests.get(serverReplyUrl, headers={'Connection': 'close'})
        print((response.status_code))
        return response



