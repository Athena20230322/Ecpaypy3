import time
import json
import os
import requests
import collections
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from UIOperate import WebOperate

class actShopify(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='Shopify')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genOrderRequestInfo(self, param_csv, inv_info):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if len(req['RelateNumber']) == 0:
            req['RelateNumber'] = inv_info['RelateNumber']
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req
    def genOrderRequestInfoB2c(self, param_csv,invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)

        req = {}
        data['RelateNumber'] = invoice_info['RelateNumber']
       # data['AllowanceNo'] = invoice_info['IA_Allow_No']

        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'

        data.pop('MerchantID')
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')
        # data.pop('ItemName')
        # data.pop('ItemCount')
        # data.pop('ItemWord')
        # data.pop('ItemPrice')
        # data.pop('ItemTaxType')
        # data.pop('ItemAmount')
        # data.pop('ItemSeq')

        rqHeader.pop('MerchantID')
        rqHeader.pop('RelateNumber')
        # rqHeader.pop('AllowanceNo')
        # rqHeader.pop('Reason')
        # rqHeader.pop('CustomerName')
        # rqHeader.pop('NotifyMail')
        # rqHeader.pop('NotifyPhone')
        # rqHeader.pop('AllowanceAmount')
        # rqHeader.pop('ItemSeq')
        # rqHeader.pop('ItemName')
        # rqHeader.pop('ItemCount')
        # rqHeader.pop('ItemWord')
        # rqHeader.pop('ItemPrice')
        # rqHeader.pop('ItemTaxType')
        # rqHeader.pop('ItemAmount')
        # rqHeader.pop('vat')
        # rqHeader.pop('ItemName')
        # rqHeader.pop('ItemCount')
        # rqHeader.pop('ItemWord')
        # rqHeader.pop('ItemPrice')
        # rqHeader.pop('ItemTaxType')
        # rqHeader.pop('ItemAmount')
        # rqHeader.pop('ItemRemark')


        # Items.pop('CustomerPhone')
        # Items.pop('CustomerEmail')
        # Items.pop('ClearanceMark')
        # Items.pop('Print')
        # Items.pop('Donation')
        # Items.pop('LoveCode')
        # Items.pop('CarrierType')
        # Items.pop('CarrierNum')
        # Items.pop('TaxType')
        # Items.pop('SalesAmount')
        # Items.pop('InvoiceRemark')
        # Items.pop('InvType')
        # Items.pop('vat')
        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')

        print(data)
        data = self.urlEncode(data)
        # print data
        data = self.aesEncrypt(data)
        # print data
        print(rqHeader)
        req['Data'] = data
        req['RqHeader'] = rqHeader
        print(req)
        return req

    def genOrderRequestInfoB2cS(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        #print data
        #sorted(data)
        #data=sorted(data.items(), key=lambda x: x[0])
        chksum=self.genhashhmac(data,case='insensitive')
        data['x_signature'] = chksum
        print(data)
        time.sleep(1)
        print(data)
        return data
    def genOrderRequestInfoB2cSS(self, param_csv,reference,inject_value=''):

        data = self.genArgsDictFromCSV(param_csv)

        for key in data:
            if data[key] == 'AUTO_INJECT_KEY':
                data[key] = inject_value
                break
        data['x_gateway_reference'] = reference['x_gateway_reference']
        data['x_reference'] = reference['x_reference']
        data = self.genArgsDictFromCSV(param_csv)
        #print data
        #sorted(data)
        #data=sorted(data.items(), key=lambda x: x[0])
       # chksum=self.genhashhmac(data,case='insensitive')
        #data['x_gateway_reference'] = chksum
        print(data)
        time.sleep(1)
        print(data)
        return data

    def genOrderRequestInfoS(self, param_csv):
        data = self.genArgsDictFromCSV(param_csv)
        chksum=self.genhashhmac(data,case='insensitive')
        data['x_test']=1
        data['x_signature'] = chksum
        print(data)
        time.sleep(1)
        return data

    def genOrderRequestInfoSS(self, param_csv,MerchantTradeNo,TradeNo):
        data = self.genArgsDictFromCSV(param_csv)

        data['x_gateway_reference'] =TradeNo
        data['x_reference'] =MerchantTradeNo
        chksum = self.genhashhmac(data, case='insensitive')
        data['x_test'] = 1
        data['x_signature'] = chksum
        print(data)
        time.sleep(1)
        return data
    def genOrderRequestInfoShopify(self, param_csv,merchantnotrade):
        data = self.genArgsDictFromCSV(param_csv)
        data['MerchantTradeNo']='test'+merchantnotrade
        print(data)
        chksum = self.genChkMacVal(data, mode='local', codec='sha256')
        print(chksum)
        data['CheckMacValue'] = chksum

        return data


    def genOrderRequestInfoB2c2(self, param_csv,invoice_info):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
       #data['RelateNumber'] = invoice_info['RelateNumber']

        req = {}
        req['MerchantID'] = data['MerchantID']
        req['PlatformID'] = '3083192'

        data.pop('MerchantID')
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('RqID')
        data.pop('Revision')

        rqHeader.pop('MerchantID')
        rqHeader.pop('RelateNumber')
        time.sleep(1)
        data = json.dumps(data)
        data = data.encode('utf-8')

        print(data)
        data = self.urlEncode(data)
        data = self.aesEncrypt(data)
        print(rqHeader)
        req['Data'] = data
        req['RqHeader'] = rqHeader
        print(req)
        return req
    def genPostRequestToAPI(self,save_path, req_info):
        op = self.webop
        form_act = self.feature_conf['Shopify_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIforShopify(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        #self.log.INFO(response.decode('utf-8'))
        html_tmp = os.path.join(save_path, 'Shopify.html')
        time.sleep(5)
        with open(html_tmp, mode='w') as html_test:
            time.sleep(5)
            html = response
            html_test.write(html)
        op.goToURL('file:///' + html_tmp)
        #return response

    def genPostRequestToAPINohtmlrefund(self, req_info):
        form_act = self.feature_conf['Shopifyrefund_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIforShopify(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        time.sleep(5)
        return response

    def genPostRequestToAPINohtmlvoid(self, req_info):
        form_act = self.feature_conf['Shopifyvoid_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIforShopify(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        time.sleep(5)
        return response

    def genPostRequestToAPINohtml(self, req_info):
        form_act = self.feature_conf['Shopifycapture_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPIforShopify(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        time.sleep(5)
        return response
    def genPostRequestQueryToAPI(self, req_info):
        form_act = self.feature_conf['ShopifyQueryTradeInfoV4_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response
    def genPostRequestToAPIN(self, req_info):
        form_act = self.feature_conf['Shopify_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        #self.log.INFO(response.decode('utf-8'))
        return response
    def cleanHtmlTmp(self, html_path):
        time.sleep(5)
        file = os.path.join(html_path, 'Shopify.html')
        time.sleep(5)
        os.remove(file)
        return 'Html Shopify file removed ...'
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Shoify_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def createOrderByRequest(self, req_info):
        pass
    def strToDict(self, res):
        res_list = res.split('&')
        res_dict = {}
        for item in res_list:
            res_dict[item.split('=')[0]] = item.split('=')[1]
        return res_dict

    def decryptDatab2c(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))
    def decryptDatab2c2(self, data):
        #data = self.urlDecode(data)
        #print data
        return self.aesDecrypt(data)

    def inputPaymentPageCreditInfoShopify(self, card_no, exp_year, exp_month, cvv, cell_no, mode, testname, email):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
            op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(2)
        op.inputTextBox('CCHolderTemp', testname)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        op.inputTextBox('creditMM', exp_month)
        op.inputTextBox('creditYY', exp_year)

        op.inputTextBox('CreditBackThree', cvv)
        # op.inputTextBox('tmpIDNO', citizenid)
        op.inputTextBox('EmailTemp', email)

        op.inputTextBox('CellPhoneCheck', cell_no)
        # op.selectDropboxList('index', 1, 'selectInstallments')
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(4)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        # op.clickElem('a.readySubmit.btn', findby='css')

    def inputOTPCredit(self, OTP):
        op = self.webop
        op.handleAlert()
        op.clickElem('GetOTPPwd')
        time.sleep(3)
        op.inputTextBox('OTP', OTP)
        time.sleep(2)
        op.clickElem('OTPSend')
    def strToDict2(self, res_info):
        res_info = self.urlEncode(res_info)
        print('str1: ' + res_info)
        res_dict = {}
        res_info = self.urlDecode(res_info)
        print('str2: ' + res_info)
        # str_to_list = res_info.split('&')
        # for item in str_to_list:
        #     tmp = item.split('=')
        #     res_dict[tmp[0]] = tmp[1]
        res_dict = eval(res_info)
        print(res_dict)
        return res_dict

