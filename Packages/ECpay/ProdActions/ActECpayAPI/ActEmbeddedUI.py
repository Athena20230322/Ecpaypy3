# -*- coding: utf-8 -*-
import collections
import time
import json
import urllib.request, urllib.parse, urllib.error

import requests
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actEmbeddedUI(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='EmbeddedUI')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv, chkmac='local'):
        req = self.genArgsDictFromCSV(param_csv)
        if req['MerchantID'] == '3002607':
            hash_key = 'pwFHCqoQZGmho4w6'
            hash_iv = 'EkRm7iFT261dpevs'
            APIHelper.__init__(self, hash_key, hash_iv)
            chksum = self.genChkMacVal(req, mode=chkmac, codec='sha256', case='insensitive')  # 驗證
            print(chksum)
            req['CheckMacValue'] = chksum  # 檢查碼
        else:
            chksum = self.genChkMacVal(req, mode=chkmac, codec='sha256', case='insensitive')  # 驗證
            print(chksum)
            req['CheckMacValue'] = chksum  # 檢查碼
        print(req['MerchantTradeNo'])  # 廠商交易編號
        return req

    def genOrderRequestInfoB2cLog(self, param_csv, inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        ls = self.genArgsDictFromCSV(param_csv)
        req = {}

        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value

            if data['TempLogisticsID'] == 'AUTO_GEN_RELATENO':
                data['TempLogisticsID'] = self.gen_uid(with_dash=False)[0:30]

        req['MerchantID'] = data['MerchantID']

        # req['PlatformID'] = ''
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('Revision')

        rqHeader.pop('TempLogisticsID')
        rqHeader.pop('GoodsAmount')
        rqHeader.pop('IsCollection')
        rqHeader.pop('GoodsName')
        rqHeader.pop('SenderName')
        rqHeader.pop('SenderZipCode')
        rqHeader.pop('SenderAddress')
        rqHeader.pop('Remark')
        rqHeader.pop('ServerReplyURL')
        rqHeader.pop('ClientReplyURL')
        rqHeader.pop('Temperature')
        rqHeader.pop('Specification')
        rqHeader.pop('ScheduledPickupTime')
        rqHeader.pop('PackageCount')
        rqHeader.pop('ReceiverAddress')
        rqHeader.pop('ReceiverCellPhone')
        rqHeader.pop('ReceiverPhone')
        rqHeader.pop('ReceiverName')
        rqHeader.pop('EnableSelectDeliveryTime')
        rqHeader.pop('EshopMemberID')
        rqHeader.pop('PlatformID')
        rqHeader.pop('MerchantTradeNo')
        rqHeader.pop('MerchantID')





        # data['LogisticsID'] = ""
        # print "2121213"

        #data['TempLogisticsID'] = [create['TempLogisticsID']]
        # print data
        # print "2121212"
        # data['Items'] = [Items]

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

    def genOrderRequestInfoB2cLogF(self, param_csv,create, inject_value=''):
        data = self.genArgsDictFromCSV(param_csv)
        rqHeader = self.genArgsDictFromCSV(param_csv)
        ls = self.genArgsDictFromCSV(param_csv)
        req = {}


        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value

            if data['TempLogisticsID'] == 'AUTO_GEN_RELATENO':
                data['TempLogisticsID'] = self.gen_uid(with_dash=False)[0:30]

        req['MerchantID'] = data['MerchantID']

        # req['PlatformID'] = ''
        data.pop('Timestamp')
        data.pop('PlatformID')
        data.pop('Revision')

        rqHeader.pop('TempLogisticsID')
        rqHeader.pop('MerchantTradeNo')





        # data['LogisticsID'] = ""
        # print "2121213"

        data['TempLogisticsID'] = [create["TempLogisticsID"]]

        # print data
        # print "2121212"
        # data['Items'] = [Items]

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
        req['RqHeader'] = (rqHeader)
        print(req)
        return req

    def genOrderRequestInfoPID(self, param_csv, chkmac='local'):
        req = self.genArgsDictFromCSV(param_csv)
        self.hkey = 'spPjZn66i0OhqJsQ'
        self.hiv = 'hT5OJckN45isQTTs'
        chksum = self.genChkMacVal(req, mode=chkmac, codec='sha256')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['QueryOrder_API']

        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))

        print('1233')

        response = self.postRequestToAPIb2cL(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)

        print('1255')


       # self.log.INFO(response.decode('utf-8'))

        return response
    def genPostRequestToAPI1(self, req_info,save_path):
        op = self.webop
        form_act = self.feature_conf['Chkout_API']

        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))

        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        html_tmp = os.path.join(save_path, 'create.html')
        # self.log.INFO(response.decode('utf-8'))
        with open(html_tmp, mode='w') as html_test:
            time.sleep(5)
            html = response
            html_test.write(html)
        op.goToURL('file:///' + html_tmp)
    
    def createOrderByBrowser(self):
        op = self.webop
        op.goToURL('http://127.0.0.1/embeddedweb/index.php')

        #op.getSubElem('CreditCard', findby='id')

        return
    def createOrderByBrowser132(self):
        op = self.webop
        op.goToURL('http://127.0.0.1/pythonautotest/RedirectToLogisticsSelection132.php')
        return
    def submitCVSPaymentRequestMobile(self):
        op = self.webop
        a = op.ElemisExist('slideToggle')
        b = op.ElemisExist('slideToggleAtm')
        if a or b is True:
            raise ValueError('Wrong Payment Type displayed...')
        op.clickElem('CVSPaySubmit')
        op.clickElem('btnSubmitCvs')
        time.sleep(2)
        op.clickElem('CVSPaySubmit')
        op.clickElem('btnSubmitCvs')

    def WebATMpayMoney(self):
        op = self.webop
        while True:
            time.sleep(3)
            if WebDriverWait(op.drv, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/form/fieldset/p/input'))):
                op.clickElem('/html/body/form/fieldset/p/input', findby='xpath')
                break
        time.sleep(3)

    def strToDictxx(self, req_str):
        result = {}
        req_str = req_str.strip('{').strip('}')
        for ele in req_str.split(', '):
            tmp_list = ele.split('=')
            result[tmp_list[0]] = tmp_list[1]
        print(result)
        return result

    def strToDict(self, res_info):
        #res_info = self.urlEncode(res_info)
       # print 'str1: ' + res_info
        res_dict = {}
        #res_info = self.urlDecode(res_info)
        #print 'str2: ' + res_info
        # str_to_list = res_info.split('&')
        # for item in str_to_list:
        #     tmp = item.split('=')
        #     res_dict[tmp[0]] = tmp[1]
        res_dict = json.loads(res_info)
        print(res_dict)
        return res_dict
    def strToDict1(self, res_info):
        #res_info = self.urlEncode(res_info)
       # print 'str1: ' + res_info
        res_dict = {}
        #res_info = self.urlDecode(res_info)
        #print 'str2: ' + res_info
        # str_to_list = res_info.split('&')
        # for item in str_to_list:
        #     tmp = item.split('=')
        #     res_dict[tmp[0]] = tmp[1]
        res_dict = res_info
        print(res_dict)
        return res_dict
    def strToDictF(self, res_info):
       # res_info = self.urlEncode(res_info)
        #print 'str1: ' + res_info
        res_dict = {}
        #res_info = self.urlDecode(res_info)
       # print 'str2: ' + res_info
        # str_to_list = res_info.split('&')
        # for item in str_to_list:
        #     tmp = item.split('=')
        #     res_dict[tmp[0]] = tmp[1]
        res_dict = json.loads(res_info)
        print(res_dict)
        return res_dict

    def decryptDatab2c(self, data):
        #data = self.urlDecode(data)
        print(data)
        return json.loads(self.aesDecrypt(data))

    def decryptDatab2cL(self, data):
        # data = self.urlDecode(data)
        print(data)
        return json.dumps(self.aesDecrypt(data))

    def genPostRequestToAPICre(self, req_info):
        form_act = self.feature_conf['Chkout_API']

        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))

        response = self.postRequestToAPIb2c(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        print('789')
        # self.log.INFO(response.decode('utf-8'))
        print('1111')
        return response



    def getOrderResultFromPage(self):
        op = self.webop
        result = op.getElem('body', find_by='tag')
        print(result.text)
        print(self.strToDict(result.text))
        return self.strToDict(result.text)

    def createOrderByRequest(self, req_info):
        pass

    def submitATMPaymentRequest(self):
        op = self.webop
        op.selectDropboxList('index',6, 'selATMBank')
        op.clickElem('ATMPaySubmit')
        op.handleAlert()
       # op.clickElem('AtmPaySubmit')

    def inputPaymentPageCreditInfoTrueEEE(self, card_no, exp_year, exp_month, cvv, cell_no, email, name, mode,
                                        rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)




        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)


                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)


                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)



                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoTrueE(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)


        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)


                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)


                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)



                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
    
    def inputPaymentPageCreditInfo(self, card_no, exp_year, exp_month, cvv, cell_no, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
               # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
    def inputPaymentPageCreditInfoTrueEE2(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)

                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoTrueEE3(self, card_no, exp_year, exp_month, cvv, cell_no, email, name, mode,
                                          rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/dl[1]/dd/div[2]/a[1]',
                     findby='xpath')
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)

                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                            findby='xpath')
                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoTrueEE(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)


                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)


                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoEE(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)


                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)
                op.inputTextBox('EmailTemp', email)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoE2(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/dl[2]/dd/div[2]/a[1]',
                     findby='xpath')
        time.sleep(2)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                op.clickElem('btnConfirm')
                op.handleAlert()

                # op.clickElem('CreditPaySubmit')
                # time.sleep(2)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #              findby='xpath')
                # op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
               # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
    def inputPaymentPageCreditInfoE3(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/dl[2]/dd/div[2]/a[1]',
                     findby='xpath')

        time.sleep(2)
        #op.inputTextBox('CCHolderTemp', name)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                op.clickElem('btnConfirm')
                op.handleAlert()

                # op.clickElem('CreditPaySubmit')
                # time.sleep(2)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #              findby='xpath')
                # op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
               # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoE5(self, card_no, exp_year, exp_month, cvv, cell_no, email, name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/dl[1]/dd/div[2]/a[1]',
                     findby='xpath')

        time.sleep(2)
        # op.inputTextBox('CCHolderTemp', name)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                op.clickElem('btnConfirm')
                op.handleAlert()

                # op.clickElem('CreditPaySubmit')
                # time.sleep(2)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #              findby='xpath')
                # op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')


    def inputPaymentPageCreditInfoEE1(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/dl[2]/dd/div[2]/a[1]',
                     findby='xpath')
        time.sleep(2)
        #op.inputTextBox('CCHolderTemp', name)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                op.clickElem('btnConfirm')
                op.handleAlert()

                # op.clickElem('CreditPaySubmit')
                # time.sleep(2)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #              findby='xpath')
                # op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
               # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoE(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        #op.inputTextBox('CCHolderTemp', name)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('btnConfirm')
                op.handleAlert()

                # op.clickElem('CreditPaySubmit')
                # time.sleep(2)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #              findby='xpath')
                # op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
               # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoE12(self, card_no, exp_year, exp_month, cvv, cell_no, email, name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        print('123')
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        print('222')
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        #op.clickElem('btnChangeBindingCard')
        #op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/dl[1]/dd/div[2]/a[1]',findby='xpath')
        print('456')
        time.sleep(2)
        # op.inputTextBox('CCHolderTemp', name)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                # op.clickElem('btnConfirm')

                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                # op.clickElem('CreditPaySubmit')
                # time.sleep(2)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #              findby='xpath')
                # op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                op.inputTextBox('CreditBackThree', cvv)
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
    def inputPaymentPageCreditInfoE11(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/dl[2]/dd/div[2]/a[1]',
        #              findby='xpath')

        time.sleep(2)
        #op.inputTextBox('CCHolderTemp', name)
        op.inputTextBox('EmailTemp', email)
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                op.clickElem('btnConfirm')
                op.handleAlert()

                # op.clickElem('CreditPaySubmit')
                # time.sleep(2)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #              findby='xpath')
                # op.handleAlert()
            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
               # op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def submitLogisticsRequestTCAT(self):
        op = self.webop
        # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        op.selectDropboxList('index', 2, 'LogisticsType')
        op.selectDropboxList('index', 1, 'LogisticsSubType')

        #op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[1]/dl[6]/dd/div[1]/a', findby='xpath')

        #op.clickElem('/html/body/div/div[2]/center/input', findby='xpath')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[3]/a', findby='xpath')
    def submitLogisticsRequestECAN(self):
        op = self.webop
        # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        op.selectDropboxList('index', 2, 'LogisticsType')
        op.selectDropboxList('index', 2, 'LogisticsSubType')

        #op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[1]/dl[6]/dd/div[1]/a', findby='xpath')

        #op.clickElem('/html/body/div/div[2]/center/input', findby='xpath')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[3]/a', findby='xpath')

    def submitEmbeddedUI(self):
        op = self.webop
        op.getElem('CreditCard', find_by='id')


        op.getElem('CreditInstallment', find_by='id')

        op.getElem('UnionPay', find_by='id')

        op.getElem('ApplePay', find_by='id')




        # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        #op.selectDropboxList('index', 1, 'LogisticsType')
        #op.selectDropboxList('index', 4, 'LogisticsSubType')

        #op.inputTextBox('CardCV_V2',222)

        #op.clickElem('/html/body/div/div[2]/div/div[1]/div/div/ul/li[1]/div[2]/div[1]/dl[2]/dd/input',  findby='xpath')

        #op.clickElem('/html/body/div/div[2]/div/div[3]/input', findby='xpath')

        time.sleep(5)

        #op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[3]/a', findby='xpath')

    def submitLogisticsRequestOK(self):
        op = self.webop
        # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        op.selectDropboxList('index', 1, 'LogisticsType')
        op.selectDropboxList('index', 4, 'LogisticsSubType')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[1]/dl[6]/dd/div[1]/a', findby='xpath')

        op.clickElem('/html/body/div/div[2]/center/input', findby='xpath')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[3]/a', findby='xpath')

    def submitLogisticsRequestHAI(self):
        op = self.webop
        # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        op.selectDropboxList('index', 1, 'LogisticsType')
        op.selectDropboxList('index', 3, 'LogisticsSubType')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[1]/dl[6]/dd/div[1]/a', findby='xpath')

        op.clickElem('/html/body/div/div[2]/center/input', findby='xpath')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[3]/a', findby='xpath')

    def submitLogisticsRequestFAM(self):
        op = self.webop
        # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        op.selectDropboxList('index', 1, 'LogisticsType')
        op.selectDropboxList('index', 1, 'LogisticsSubType')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[1]/dl[6]/dd/div[1]/a', findby='xpath')

        op.clickElem('/html/body/div/div[2]/center/input', findby='xpath')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[3]/a', findby='xpath')
    def submitLogisticsRequestUNI(self):
        op = self.webop
        # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        op.selectDropboxList('index', 1, 'LogisticsType')
        op.selectDropboxList('index', 2, 'LogisticsSubType')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[1]/dl[6]/dd/div[1]/a', findby='xpath')

        op.clickElem('/html/body/div/div[2]/center/form/input[1]', findby='xpath')

        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div/div/div[3]/a', findby='xpath')
    def redirectStrToDict(self, res_text):
        res_list = res_text.split('\n')
        res_dict = {}
        for ele in res_list:
            if ele != '':
               # ele = ele.encode('utf-8')
                ele =json.dumps('utf-8')
                res_dict[ele.split(':')[0]] = ele.split(':')[1]
                if ele.split(':')[0] == 'BindingDate' and ele.split(':')[1] !='':
                    res_dict['BindingDate'] = ele.split(':')[1]+':'+ele.split(':')[2]+':'+ele.split(':')[3]
        res_dict['TempLogisticsID'] = urllib.parse.unquote_plus(res_dict['TempLogisticsID'])
        res_dict['LogisticsSubType'] = urllib.parse.unquote_plus(res_dict['LogisticsSubType'])
        return res_dict

    def GetInfoFromClientRedirectUrl(self):
        op = self.webop
       # divText = op.drv.find_element_by_tag_name('body').text
        divText1 = op.drv.find_element_by_id('CreditCard')

        divText2 = op.drv.find_element_by_id('CreditInstallment')

        divText3 = op.drv.find_element_by_id('UnionPay')

        divText4 = op.drv.find_element_by_id('ApplePay')


        print("53425234")
        self.log.INFO(divText1)
        print('1')
        self.log.INFO(divText2)
        print('2')
        self.log.INFO(divText3)
        print('3')
        self.log.INFO(divText4)
        print('4')

        return divText1






        






        #op.clickElem('ATMPaySubmit')
        op.handleAlert()
        # op.clickElem('auto_BtnATM')

    def inputPaymentPageCreditInfobydivisionE(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')

        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.selectDropboxList('index', 1, 'selectInstallments')
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)

                op.inputTextBox('CCHolderTemp',name )
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)
                op.inputTextBox('EmailTemp', email)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()



            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')


    def inputPaymentPageCreditInfobydivisionE(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')

        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.selectDropboxList('index', 1, 'selectInstallments')
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)

                op.inputTextBox('CCHolderTemp',name )
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)
                op.inputTextBox('EmailTemp', email)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()



            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfobydivisionFalseE(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.selectDropboxList('index', 1, 'selectInstallments')
        time.sleep(2)

        op.inputTextBox('EmailTemp', email)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)


                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')


                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()



            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)


                op.inputTextBox('CellPhoneCheck', cell_no)

                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                op.selectDropboxList('index', 1, 'selectInstallments')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfobydivisionFalseEE(self, card_no, exp_year, exp_month, cvv, cell_no,email, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.selectDropboxList('index', 1, 'selectInstallments')
        time.sleep(2)
        op.inputTextBox('EmailTemp', email)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)
                op.inputTextBox('EmailTemp', email)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()



            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
    def inputPaymentPageCreditInfobydivisionFalseEE2(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(5)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        print("123")
        op.ElemisDisplay('btnChangeBindingCard')

        time.sleep(5)
        op.clickElem('btnChangeBindingCard')
        print("456")
        #op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/dl[2]/dd/div[2]/a[1]', findby='xpath')
        time.sleep(2)

        op.selectDropboxList('index', 1, 'selectInstallments')
        time.sleep(2)
        op.inputTextBox('EmailTemp', email)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)

                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)
               # op.inputTextBox('EmailTemp', email)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()



            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')




    def inputPaymentPageCreditInfobydivision(self, card_no, exp_year, exp_month, cvv, cell_no, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.selectDropboxList('index', 1, 'selectInstallments')
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()



            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfobydivisionFalseEEE(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('btnChangeBindingCard')
        time.sleep(2)
        op.selectDropboxList('index', 1, 'selectInstallments')
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print('Elem not exists')
                time.sleep(2)


                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)
                op.inputTextBox('EmailTemp', email)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                # op.clickElem('btnClose')
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)

                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()



            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
        elif rebind == True:
            if op.ElemisDisplay('btnChangeBindingCard') == True:
                print('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)

                op.inputTextBox('CCHolderTemp', name)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.inputTextBox('value', exp_month, 'creditMM')
                # op.inputTextBox('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                # op.clickElem('labCreditBinding')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
            elif op.ElemisDisplay('btnChangeBindingCard') == False:
                time.sleep(2)
                op.inputTextBox('CCpart1', cno_parts[0])
                op.inputTextBox('CCpart2', cno_parts[1])
                op.inputTextBox('CCpart3', cno_parts[2])
                op.inputTextBox('CCpart4', cno_parts[3])
                op.inputTextBox('creditMM', exp_month)
                op.inputTextBox('creditYY', exp_year)
                # op.selectDropboxList('value', exp_month, 'creditMM')
                # op.selectDropboxList('value', exp_year, 'creditYY')

                op.inputTextBox('CreditBackThree', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)

                op.inputTextBox('CellPhoneCheck', cell_no)
                # op.clickElem('labCreditBinding')
                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                op.selectDropboxList('index', 1, 'selectInstallments')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoLanguage(self, card_no, cvv, cell_no):
        op = self.webop
        cno_parts = card_no.split('-')
        if op.ElemisExist('CCHolder') is True:
            op.inputTextBox('CCHolder', 'AutoTester')
        op.selectDropboxList('value', 'VISA/MasterCard/JCB', 'CardType')
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CardLastFourDigit', cno_parts[3])
        time.sleep(2)
        # op.clickElem('XyzCode')
        # time.sleep(2)
        op.selectDropboxList('text', '12', 'CardValidMM')
        op.selectDropboxList('value', '24', 'CardValidYY')

        op.inputTextBox('CardAuthCode', cvv)
        # op.inputTextBox('tmpIDNO', citizenid)
        op.inputTextBox('Cellphone', cell_no)
        time.sleep(2)
        op.clickElem('Agree')
        time.sleep(2)
        op.clickElem('Submit')
        op.handleAlert()
        # op.clickElem('Submit')
        # op.handleAlert()
        # op.clickElem('a.readySubmit.btn', findby='css')

    def inputPaymentPageCreditInfoLanguageU(self, card_no, cvv, cell_no):
            op = self.webop
            cno_parts = card_no.split('-')
           # if op.ElemisExist('CCHolder') is True:
               # op.inputTextBox('CCHolder', 'AutoTester')
          #  op.selectDropboxList('value', 'VISA/MasterCard/JCB', 'CardType')

            op.inputTextBox('CCpart1', cno_parts[0])
            op.inputTextBox('CCpart2', cno_parts[1])
            op.inputTextBox('CCpart3', cno_parts[2])
            op.inputTextBox('CCpart4', cno_parts[3])
            # op.inputTextBox('creditMM', exp_month)
            # op.inputTextBox('creditYY', exp_year)

           # op.inputTextBox('CardLastFourDigit', cno_parts[4])
            time.sleep(2)
            # op.clickElem('XyzCode')
            # time.sleep(2)
            op.inputTextBox('creditMM', '12')
            op.inputTextBox('creditYY', '24')

           # op.inputTextBox('CardAuthCode', cvv)
            op.inputTextBox('CreditBackThree', cvv)
            # op.inputTextBox('tmpIDNO', citizenid)
            op.inputTextBox('CellPhoneCheck', cell_no)
            time.sleep(2)
            op.clickElem('CreditPaySubmit')
            time.sleep(2)
            op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button', findby='xpath')
            time.sleep(2)
            op.clickElem('CreditPaySubmit')
            time.sleep(2)
            op.handleAlert()
            op.clickElem('btnConfirm')
            # op.handleAlert()
            # op.clickElem('a.readySubmit.btn', findby='css')

    def inputPaymentPageCreditInfoLanguageUE(self, card_no, cvv, cell_no,email,name):
        op = self.webop
        cno_parts = card_no.split('-')
        # if op.ElemisExist('CCHolder') is True:
        # op.inputTextBox('CCHolder', 'AutoTester')
        #  op.selectDropboxList('value', 'VISA/MasterCard/JCB', 'CardType')
        op.inputTextBox('CCHolderTemp', name)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        # op.inputTextBox('creditMM', exp_month)
        # op.inputTextBox('creditYY', exp_year)

        # op.inputTextBox('CardLastFourDigit', cno_parts[4])
        time.sleep(2)
        # op.clickElem('XyzCode')
        # time.sleep(2)
        op.inputTextBox('creditMM', '12')
        op.inputTextBox('creditYY', '24')

        # op.inputTextBox('CardAuthCode', cvv)
        op.inputTextBox('CreditBackThree', cvv)
        # op.inputTextBox('tmpIDNO', citizenid)
        op.inputTextBox('EmailTemp', email)
        op.inputTextBox('CellPhoneCheck', cell_no)
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.handleAlert()
        op.clickElem('btnConfirm')
        # op.handleAlert()
        # op.clickElem('a.readySubmit.btn', findby='css')
        
    def loginPaymentPage(self, username, pwd):  
        op = self.webop
        op.handleAlert()
        op.clickElem('LoginButton')
        op.inputTextBox('m_account', username)
        op.inputTextBox('m_pw', pwd)
        captimg = op.getElem('reloadCaptcha', find_by='class')
        
        cpat_code = op.resolveCaptchaElem(captimg)
        op.inputTextBox('login-captcha', cpat_code)
        op.clickElem('aLoginSubmit')
        elem_login_fail = op.getElem('divLoginError')
        print(elem_login_fail.get_attribute('style'))
        if elem_login_fail.get_attribute('style') == 'display: block;':
            captimg = op.getElem('reloadCaptcha', find_by='class')
            cpat_code = op.resolveCaptchaElem(captimg)
            op.inputTextBox('login-captcha', cpat_code)
            op.clickElem('aLoginSubmit')            
        
    
    def submitCVSPaymentRequest(self):
        op = self.webop
        op.maximizeWindow()
        op.handleAlert()
        op.clickElem('CVSPaySubmit')
        op.handleAlert()
        #op.clickElem('CvsPaySubmit')

    def backToShop(self):
        op = self.webop
        op.executeScript("window.scrollTo(0,document.body.scrollHeight);")
        op.clickElem("//a[@href='https://www.ecpay.com.tw']", findby='xpath')
        #op.clickElem('blue_button', findby='class')
        return op.drv.current_url

    def ClickFamilybtn(self):
        op = self.webop
        op.executeScript("window.scrollTo(0, document.body.scrollHeight);")
        op.clickElem('/html/body/div[1]/div[2]/div/div[4]/dl[2]/dd/p[3]/a', findby='xpath')


        op.clickElem('cvsUrl')
        time.sleep(3)
        nowhandle = op.drv.current_window_handle
        allhandles = op.drv.window_handles
        for handle in allhandles:
            if handle != nowhandle:
                op.drv.switch_to_window(handle)
        time.sleep(3)

        op.clickElem('/html/body/div[2]/div/div/header/nav/ul/li[2]/a', findby='xpath')
        time.sleep(3)
        # op.clickElem('/html/body/div[2]/div/div/header/nav/ul/li[1]/a', findby='xpath')
        # time.sleep(3)
        #op.clickElem('/html/body/div[1]/div/nav[1]/ul/li[1]', findby='xpath')
        return op.drv.current_url

    def ClickHifeybtn(self):
        op = self.webop
        op.executeScript("window.scrollTo(0, document.body.scrollHeight);")
        op.clickElem('/html/body/div[1]/div[2]/div/div[4]/dl[2]/dd/p[3]/a', findby='xpath')
        op.clickElem('cvsUrl')
        time.sleep(3)
        nowhandle = op.drv.current_window_handle
        allhandles = op.drv.window_handles
        for handle in allhandles:
            if handle != nowhandle:
                op.drv.switch_to_window(handle)
        time.sleep(3)
        op.clickElem('/html/body/div[2]/div/div/header/nav/ul/li[3]/a', findby='xpath')
        time.sleep(3)
        return op.drv.current_url

    def Clicksevenbtn(self):
        op = self.webop
        op.executeScript("window.scrollTo(0, document.body.scrollHeight);")
        op.clickElem('/html/body/div[1]/div[2]/div/div[4]/dl[2]/dd/p[3]/a', findby='xpath')
        op.clickElem('cvsUrl')
        time.sleep(3)
        nowhandle = op.drv.current_window_handle
        allhandles = op.drv.window_handles
        for handle in allhandles:
            if handle != nowhandle:
                op.drv.switch_to_window(handle)
        time.sleep(3)
        op.clickElem('/html/body/div[2]/div/div/header/nav/ul/li[1]/a', findby='xpath')
        time.sleep(3)
        return op.drv.current_url

    def submitBARcodePayment(self):
        op = self.webop
        op.maximizeWindow()
        op.handleAlert()
        op.clickElem('BarCodePaySubmit')
        op.handleAlert()
        time.sleep(1)
       #op.clickElem('BarcodePaySubmit')
    
    
    # def queryCreditOTP(self, phone_no):
    #     time.sleep(25)
    #     dic_otp_queryinfo = {
    #                         'CellNo' : phone_no,
    #                         'OTPType': 'ECpay_Credit_Payment'
    #                         }
    #
    #     otp_query = self.getRequestFromAPI(dic_otp_queryinfo, self.feature_conf['OtpCollectorAddr'])
    #     if otp_query != 'Not_Found':
    #         otp_data = json.loads(otp_query)
    #         return otp_data
    #
    # def queryCreditOTPLanguage(self, phone_no, language):
    #     time.sleep(20)
    #     dic_otp_queryinfo = {
    #                         'CellNo' : phone_no,
    #                         'OTPType': language
    #                         }
    #
    #     otp_query = self.getRequestFromAPI(dic_otp_queryinfo, self.feature_conf['OtpCollectorAddr'])
    #     if otp_query != 'Not_Found':
    #         otp_data = json.loads(otp_query)
    #         return otp_data
        
    # def inputOTP(self, otp_data):
    #     op = self.webop
    #     passcode = otp_data['OTP']
    #     print passcode
    #     op.inputTextBox('SMSAuthCode', passcode)
    #     op.clickElem('Submit')

    def inputOTP(self):
        time.sleep(2)
        op = self.webop
        passcode = op.getElemValue('HightlightOTP', find_by='id')
        # print passcode
        sms_code = op.resolveSMSAuthCode(passcode)
        op.inputTextBox('SMSAuthCode', sms_code)
        op.clickElem('Submit')
    def inputOTPCredit(self, OTP):
        op = self.webop
        op.handleAlert()
        op.clickElem('GetOTPPwd')
        time.sleep(3)
        op.inputTextBox('OTP', OTP)
        time.sleep(2)
        op.clickElem('OTPSend')

    def postFormInHtml(self, html_str, action=''):
        pass

    #For Verify

    
    
    




#req_drv.get('https://pay-stage.allpay.com.tw/')

#print datetime.datetime.now()
#gen_order = cls_strhandler.postRequestToAPI(raw_sess, req, 'http://payment-stage.allpay.com.tw/Cashier/AioCheckOut/V2', withBrowser=req_drv)


#with open(r'd:\return.html', mode='w') as f:
    #f.write(gen_order)
    #f.close()
    



#HtmHelper.feed(gen_order)
#payment_dict = HtmHelper.formToPOSTDict('PayForm')
#payment_dict['paymentName'] = '10000@2003@Credit_GW'
#payment_dict['CardNo'] = '4311952222222222'
#payment_dict['CardValidMM'] = '05'
#payment_dict['CardValidYY'] = '22'
#payment_dict['CardAuthCode'] = '222'
#payment_dict['CellPhone'] = '0972005542'



#pay_order = cls_strhandler.postRequestToAPI(raw_sess, payment_dict, 'https://payment-stage.allpay.com.tw/Cashier/RetainPaymentType', withBrowser=req_drv)

#with open(r'd:\payment_return.html', mode='w') as f:
    #f.write(pay_order)
    #f.close()
    

#HtmHelper.clearCurrentTag()
#HtmHelper.feed(pay_order)

#CreditPayData = HtmHelper.formToPOSTDict('PostForm')
#CreditPayAct = HtmHelper.getFormAct('PostForm')
#print CreditPayData
#print CreditPayAct

#credit_post_a  = cls_strhandler.postRequestToAPI(raw_sess, CreditPayData, 'http://pay-stage.allpay.com.tw/Payment/Gateway', withBrowser=req_drv)


#with open(r'd:\credit_return_a.html', mode='w') as f:
    #f.write(credit_post_a)
    #f.close()

#HtmHelper.clearCurrentTag()
#HtmHelper.feed(credit_post_a)

#OTPform = HtmHelper.formToPOSTDict('/CreditPayment/VerifySMS')
#print OTPform

#time.sleep(20)

#dic_otp_queryinfo = {
#'CellNo' : '0972005542',
#'OTPType': 'Credit_Payment'
#}

#otp_query = cls_strhandler.getRequestFromAPI(dic_otp_queryinfo, 'http://104.214.145.51:443/')
#print "OTP Query:", otp_query

#if otp_query != 'Not_Found':
    #otp_data = json.loads(otp_query)

    #print otp_data
    
    #passcode = otp_data['OTP']
    #print passcode
    #OTPform['SMSAuthCode'] = passcode
    #OTPform['Language'] = 'lang-tw'
    
    #otp_post_res  = cls_strhandler.postRequestToAPI(raw_sess, OTPform, 'https://pay-stage.allpay.com.tw/CreditPayment/VerifySMS', trencode_dotnet=True, withBrowser=req_drv)
    
    #with open(r'd:\otp_post_res.html', mode='w') as f:
        #f.write(otp_post_res)
        #f.close()
        
    #HtmHelper.clearCurrentTag()
    #HtmHelper.feed(otp_post_res)
    #Credit_Autosubmit = HtmHelper.formToPOSTDict('PostForm')
    
    #credit_auth = cls_strhandler.postRequestToAPI(raw_sess, Credit_Autosubmit, 'https://cc-stage.allpay.com.tw/form_ssl.php', withBrowser=req_drv)
    
    #with open(r'd:\credit_auth.html', mode='w') as f:
        #f.write(credit_auth)
        #f.close()    
    



#HtmHelper.feed(pay_order)
#ATMreq_dict = HtmHelper.formToPOSTDict('PostForm')
#atm_request = cls_strhandler.postRequestToAPI(ATMreq_dict, 'http://payment-stage.allpay.com.tw/PaymentRule/ATMPaymentInfo')

#with open(r'd:\ATM_return.html', mode='w') as f:
    #f.write(atm_request)
    #f.close()