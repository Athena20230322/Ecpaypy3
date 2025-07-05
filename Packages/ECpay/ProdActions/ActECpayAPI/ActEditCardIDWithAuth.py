import time
import json
import os
import collections
import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actEditCardIDWithAuth(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='EditCardIDWithAuth')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv, binding_info, inject_value=''):
        req = self.genArgsDictFromCSV(param_csv)

        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value
                break
        req['MerchantMemberID'] = binding_info['MerchantMemberID']
        req['CardID'] = binding_info['CardID']
        chksum = self.genChkMacVal(req, mode='local', codec='sha256')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['EditCardID_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['EditCardID_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def inputOldCreditCard4NoInfo(self, card4_no):
        op = self.webop
        op.handleAlert()
        op.inputTextBox('Card4No', card4_no)
        op.clickElem('btn_submit')

    def inputEditCreditCardInfo(self, card_no, cvv):
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