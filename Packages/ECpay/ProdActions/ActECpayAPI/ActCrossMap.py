# -*- coding:utf-8 -*-
import time
import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
from rest_framework.utils import json


class actCrossMap(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI',
                                                                feature_name='CrossMap')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
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
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req['MerchantTradeNo'] = merchant_trade_no
        return req

    def genOrderRequestInfoB2c(self, param_csv):
        # data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
       # Items = self.genArgsDictFromCSV(param_csv)
        req = {}
        # if data['RelateNumber'] == 'AUTO_GEN_RELATENO':
        #     data['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        # req['MerchantID'] = data['MerchantID']
       # req['PlatformID'] = ''
       #  data.pop('Timestamp')
       #  data.pop('PlatformID')
       #  data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('LogisticsType')
        rqHeader.pop('LogisticsSubType')
        rqHeader.pop('Destination')
        rqHeader.pop('ServerReplyURL')

        #data['Items'] = [Items]

        time.sleep(1)
        data = json.dumps(rqHeader)
        data = data.encode('utf-8')

        print(data)
        data = self.urlEncode(data)
        # print data
        data = self.aesEncrypt(data)
        # print data
        print(rqHeader)
        # req['Data'] = data
        req['RqHeader'] = rqHeader
        print(req)
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
    
    def CrossMapByBrowser(self, browser_drv, req_info, device=-1):
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

    def ChooseCrossLog(self):
            op = self.webop
           # op.clickElem("btn-Confirm")
            op.clickElem('/html/body/div/div[1]/div[2]/div/div[1]/div/div/p[4]', findby='xpath')
            time.sleep(1)
            op.clickElem("btn-Confirm")

    def ChooseFAMIStore(self):
        op = self.webop
        op.clickElem("FamilyPost")
        # op.clickElem('/html/body/div/div[2]/center/input', findby='xpath')
        time.sleep(1)

    def ChooseUniMartStore(self, web_driver):
        op = self.webop
        op.clickElem('byID')
        time.sleep(1)
        web_driver.switch_to.frame('frmMain')
        op.inputTextBox('storeIDKey', '991182')
        op.clickElem('serach_name')
        time.sleep(1)
        web_driver.switch_to.default_content()
        op.clickElem('sevenDataBtn')
        time.sleep(1)
        op.clickElem('AcceptBtn')
        time.sleep(1)
        op.clickElem('submit_butn')

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
        self.log.INFO("response msg: " + response.text)
        self.log.INFO("status code: " + str(response.status_code))
        return response



