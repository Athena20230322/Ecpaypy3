# -*- coding: utf-8 -*-

import time
import json
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actAioCheckOutV5(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='AioCheckOutV5')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv, chkmac='local'):
        print(param_csv)
        req = self.genArgsDictFromCSV(param_csv)
        if req['MerchantID'] == '3002607':
            hash_key = 'pwFHCqoQZGmho4w6'
            hash_iv = 'EkRm7iFT261dpevs'
            APIHelper.__init__(self, hash_key, hash_iv)
            chksum = self.genChkMacVal(req, mode=chkmac, codec='sha256', case='insensitive')  # 驗證
            print (chksum)
            req['CheckMacValue'] = chksum  # 檢查碼
        elif req['MerchantID'] == '3003184':
            hash_key = 'qddBncOAPMCtILqp'
            hash_iv = '3ftWaDmIbChLUtc6'
            APIHelper.__init__(self, hash_key, hash_iv)
            chksum = self.genChkMacVal(req, mode=chkmac, codec='sha256', case='insensitive')  # 驗證
            print (chksum)
            req['CheckMacValue'] = chksum  # 檢查碼
        else:
            chksum = self.genChkMacVal(req, mode=chkmac, codec='sha256', case='insensitive')  # 驗證
            print (chksum)
            req['CheckMacValue'] = chksum  # 檢查碼
        print((req['MerchantTradeNo']))  # 廠商交易編號
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print (form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def submitATMPaymentRequest(self):
        op = self.webop
        #op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        op.selectDropboxList('index',6,'selATMBank')
        op.clickElem('ATMPaySubmit')
        op.handleAlert()
        #op.clickElem('auto_BtnATM')

    def submitATMPaymentRequestOther(self):
        op = self.webop
        # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        op.selectDropboxList('index', 7, 'selATMBank')
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[5]/div/div[3]/button', findby='xpath')
        op.clickElem('ATMPaySubmit')
        op.handleAlert()
        # op.clickElem('auto_BtnATM')

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
        # time.sleep(2)
        # op.clickElem('XyzCode')
        time.sleep(2)
        op.selectDropboxList('text', '12', 'CardValidMM')
        op.selectDropboxList('value', '24', 'CardValidYY')

        op.inputTextBox('CardAuthCode', cvv)
        # op.inputTextBox('tmpIDNO', citizenid)
        op.inputTextBox('Cellphone', cell_no)
        time.sleep(2)
        op.clickElem('Agree')
        time.sleep(2)
        op.clickElem('Submit')
        # op.handleAlert()
        # op.clickElem('Submit')
        # op.handleAlert()
        # op.clickElem('a.readySubmit.btn', findby='css')

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

    def inputPaymentPageCreditInfoLanguageU(self, card_no, cvv, cell_no):
        op = self.webop
        cno_parts = card_no.split('-')
       # if op.ElemisExist('CCHolder') is True:
        op.inputTextBox('CCHolderTemp', 'AutoTester')
        op.selectDropboxList('value', 'Visa/Master/JCB', 'CreditPayType')
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        #op.inputTextBox('CardLastFourDigit', cno_parts[4])
        # time.sleep(2)
        # op.clickElem('XyzCode')
        time.sleep(2)
        op.inputTextBox('creditMM', '12')
        op.inputTextBox('creditYY', '24')

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
        # op.clickElem('Submit')
        # op.handleAlert()
        # op.clickElem('a.readySubmit.btn', findby='css')

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

    def createOrderByRequest(self, req_info):
        pass

    def WebATMpayMoney(self):
        op = self.webop
        while True:
            time.sleep(3)
            if WebDriverWait(op.drv, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/form/fieldset/p/input'))):
                op.clickElem('/html/body/form/fieldset/p/input', findby='xpath')
                break
        time.sleep(3)

    def strToDict(self, req_str):
        result = {}
        req_str = req_str.strip('{').strip('}')
        for ele in req_str.split(', '):
            tmp_list = ele.split('=')
            result[tmp_list[0]] = tmp_list[1]
        print(result)
        return result

    def getOrderResultFromPage(self):
        op = self.webop
        result = op.getElem('body', find_by='tag')
        print((result.text))
        print((self.strToDict(result.text)))
        return self.strToDict(result.text)

    def inputPaymentPageCreditInfoBindbydivisionE(self, card_no, exp_year, exp_month, cvv, cell_no, mode, testname,email, rebind=False):
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

         #time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print ('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', testname)
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

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button', findby='xpath')
                time.sleep(2)

                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #               findby='xpath')
                # op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.handleAlert()
                op.clickElem('btnConfirm')
                time.sleep(2)

            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print ('Elem exists')
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
                print ('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', testname)
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
                op.inputTextBox('CCHolderTemp', testname)
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
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')



    def inputPaymentPageCreditInfoBindbydivision(self, card_no, exp_year, exp_month, cvv, cell_no, mode, testname, rebind=False):
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

         #time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print ('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', testname)
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

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button', findby='xpath')
                time.sleep(2)

                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #               findby='xpath')
                # op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.handleAlert()
                op.clickElem('btnConfirm')
                time.sleep(2)

            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print ('Elem exists')
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
                print ('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', testname)
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
                op.inputTextBox('CCHolderTemp', testname)
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
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoFlexibleInstallment(self, card_no, exp_year, exp_month, cvv, cell_no, mode, testname,
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
        op.selectDropboxList('index', 1, 'DreamIns')
        time.sleep(2)

        # time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print ('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', testname)
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

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                             findby='xpath')
                time.sleep(2)

                # op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/button',
                #               findby='xpath')
                # op.handleAlert()
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.handleAlert()
                op.clickElem('btnConfirm')
                time.sleep(2)

            elif op.ElemisDisplay('btnChangeBindingCard') == True:
                print ('Elem exists')
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
                print ('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', testname)
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
                op.inputTextBox('CCHolderTemp', testname)
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
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

    def inputPaymentPageCreditInfoBind(self, card_no, exp_year, exp_month, cvv, cell_no, mode,testname, rebind=False):
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
       # op.selectDropboxList('index', 1, 'selectInstallments')
       # time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('btnChangeBindingCard') is False:
                print ('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CCHolderTemp', testname)
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
                #op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                #op.clickElem('labCreditBinding')

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
                print ('Elem exists')
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
                print ('Rebinding')
                op.clickElem('btnDelBindingCard')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.handleAlert()
                time.sleep(7)
                op.inputTextBox('CCHolderTemp', testname)
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
                #op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
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
                op.inputTextBox('CCHolderTemp', testname)
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
                #op.clickElem('labCreditBinding')
                #op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/label',findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')
                op.clickElem('CreditPaySubmit')
                time.sleep(2)
                op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button',
                             findby='xpath')

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

    def inputPaymentPageCreditInfoNOE(self, card_no, exp_year, exp_month, cvv, cell_no, mode):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()

        #op.inputTextBox('CCHolderTemp', testname)
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

    def inputPaymentPageCreditInfoE(self, card_no, exp_year, exp_month, cvv, cell_no,email,name, mode):
        op = self.webop
        cno_parts = card_no.split('-')
        op.handleAlert()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()

        op.inputTextBox('CCHolderTemp', name)
        op.inputTextBox('CCpart1', cno_parts[0])
        op.inputTextBox('CCpart2', cno_parts[1])
        op.inputTextBox('CCpart3', cno_parts[2])
        op.inputTextBox('CCpart4', cno_parts[3])
        op.inputTextBox('creditMM', exp_month)
        op.inputTextBox('creditYY', exp_year)

        op.inputTextBox('CreditBackThree', cvv)
        # op.inputTextBox('tmpIDNO', citizenid)
        op.inputTextBox('EmailTemp',email)

        op.inputTextBox('CellPhoneCheck', cell_no)
        # op.selectDropboxList('index', 1, 'selectInstallments')
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')
        time.sleep(2)
        op.clickElem('CreditPaySubmit')
        time.sleep(2)
        op.clickElem('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button', findby='xpath')




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
        print((elem_login_fail.get_attribute('style')))
        if elem_login_fail.get_attribute('style') == 'display: block;':
            captimg = op.getElem('reloadCaptcha', find_by='class')
            cpat_code = op.resolveCaptchaElem(captimg)
            op.inputTextBox('login-captcha', cpat_code)
            op.clickElem('aLoginSubmit')            
        
    
    def submitCVSPaymentRequest(self):
        op = self.webop
        op.maximizeWindow()
        op.handleAlert()
        print ('112255')
        op.clickElem('CVSPaySubmit')
        op.handleAlert()
       # op.clickElem('auto_BtnCVS')

    def backToShop(self):
        op = self.webop
        op.executeScript("window.scrollTo(0, document.body.scrollHeight);")
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
        return op.drv.current_url

    def ClickFamilybtnxx(self):
        op = self.webop
        op.executeScript("window.scrollTo(0, document.body.scrollHeight);")
        op.clickElem(' /html/body/div[1]/div[2]/div/div[5]/dl[2]/dd/p[3]/a', findby='xpath')
        op.clickElem('cvsUrl')
        time.sleep(3)
        nowhandle = op.drv.current_window_handle
        allhandles = op.drv.window_handles
        for handle in allhandles:
            if handle != nowhandle:
                op.drv.switch_to_window(handle)
        time.sleep(3)
        op.clickElem('/html/body/div[2]/div/div/header/nav/ul/li[2]', findby='xpath')
        time.sleep(3)
        op.clickElem('/html/body/div[1]/div/nav[1]/ul/li[1]', findby='xpath')
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

    def ClickHifeybtnxx(self):
        op = self.webop
        op.executeScript("window.scrollTo(0, document.body.scrollHeight);")
        op.clickElem('/html/body/div[1]/div[3]/div/form/div/div[1]/div[1]/ul/li[3]', findby='xpath')
        op.clickElem('CVSPaymentLinkbtn')
        time.sleep(3)
        nowhandle = op.drv.current_window_handle
        allhandles = op.drv.window_handles
        for handle in allhandles:
            if handle != nowhandle:
                op.drv.switch_to_window(handle)
        time.sleep(3)
        op.clickElem('/html/body/div[1]/div/nav[1]/ul/li[2]', findby='xpath')
        time.sleep(3)
        return op.drv.current_url


    def submitBARcodePayment(self):
        op = self.webop
        op.maximizeWindow()
        op.handleAlert()
        op.clickElem('BarCodePaySubmit')
        op.handleAlert()
        time.sleep(1)
     #   op.clickElem('auto_BtnBarCode')

    # def queryCreditOTP(self, phone_no):
    #     time.sleep(22)
    #     dic_otp_queryinfo = {
    #                         'CellNo' : phone_no,
    #                         'OTPType': 'ECpay_Credit_Payment'
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
        op.clickElem('btnSendOtpValidate')

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

    def genOrderRequestInfoPID(self, param_csv, chkmac='local'):
        req = self.genArgsDictFromCSV(param_csv)
        self.hkey = 'spPjZn66i0OhqJsQ'
        self.hiv = 'hT5OJckN45isQTTs'
        chksum = self.genChkMacVal(req, mode=chkmac, codec='sha256')
        print (chksum)
        req['CheckMacValue'] = chksum
        print((req['MerchantTradeNo']))
        return req

    def geterror(self):
        op = self.webop
        print((op.getElem('message_error', find_by='class').is_displayed()))

    def checkGooglePay(self):
        op = self.webop
        res = op.ElemisDisplay('nav-section15')
        if res == False:
            print ('Google Pay not displayed .')
        else:
            raise ValueError('Google Pay must not be supported in PC browser.')

    def checkMGooglePay(self, DeviceSource, Ignored=False):
        op = self.webop
        if DeviceSource == 'M':
            if Ignored == False:
                res = op.ElemisExist('GooglePayData')
                # res = op.getElem('slideToggleAndroidPay')
                if res:
                    dis_res = op.ElemisDisplay('imgGooglePay')
                    if dis_res:
                        print ('Google Pay supported .')
                    else:
                        raise ValueError('Google Pay not showing ...')
                else:
                    raise ValueError('Google Payment not exist .')
            elif Ignored == True:
                res = op.ElemisExist('GooglePayData')
                # res = op.getElem('slideToggleAndroidPay')
                if res:
                    raise ValueError('Google Pay should not show .')

    def checkCVSLimitAmount(self):
        op = self.webop

        res = op.ElemisDisplay('.mp-nopay-tip', find_by='css')
        if res == True:
            print (' Exceed the amount limit.')
        else:
            raise ValueError('The warning is not shown.')




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
