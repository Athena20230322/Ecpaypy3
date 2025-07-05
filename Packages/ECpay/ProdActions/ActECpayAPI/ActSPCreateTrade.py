# -*- coding: utf-8 -*-
import collections
import time
import json
import os
from webbrowser import browser

from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actSPCreateTrade(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='SPCreateTrade')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfoPID(self, param_csv, chkmac='local'):
        req = self.genArgsDictFromCSV(param_csv)
        self.hkey = 'spPjZn66i0OhqJsQ'
        self.hiv = 'hT5OJckN45isQTTs'
        chksum = self.genChkMacVal(req, mode=chkmac, codec='sha256')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genOrderRequestInfo(self, param_csv, chkmac='local'):
        req = self.genArgsDictFromCSV(param_csv)
        if req['MerchantID'] == '3002607':
            hash_key = 'pwFHCqoQZGmho4w6'
            hash_iv = 'EkRm7iFT261dpevs'
            APIHelper.__init__(self, hash_key, hash_iv)
            chksum = self.genChkMacVal3D(req, mode=chkmac, codec='sha256', case='insensitive')  # 驗證
            print(chksum)
            req['CheckMacValue'] = chksum  # 檢查碼
        else:
            chksum = self.genChkMacVal(req, mode=chkmac, codec='sha256', case='insensitive')  # 驗證
            print(chksum)
            req['CheckMacValue'] = chksum  # 檢查碼
        print(req['MerchantTradeNo'])  # 廠商交易編號
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['SPCreateTrade_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def createOrderByRequest(self, req_info):
        form_act = self.feature_conf['SPCreateTrade_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8-sig'))
        return response


    def strToDict(self, res_info):
        print('str1: ' + res_info)
        # res_info = self.urlDecode(res_info)
        print('str2: ' + res_info)
        res_dict = json.loads(res_info,'utf-8-sig')
        print(res_dict)
        return res_dict

    def makeHtmlFile(self, save_path, data_dict, PType, PName):
        op = self.webop
        html_tmp = os.path.join(save_path, 'tmp.html')
        time.sleep(5)
        with open(html_tmp, mode='w') as html_test:
            time.sleep(5)
            js_src = self.feature_conf['SPCreateTrade_JS']

            html = """
            <!DOCTYPE html>
            <html>
            <head>
            <script src = "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js">
            </script>
            </head>
            <body>
                <h1 id="res">test</h1>
                <script src = "%s"
                    data-MerchantID = %s
                    data-SPToken = %s
                    data-PaymentType="%s"
                    data-PaymentName="%s">
                </script>
                <script>
                $(function(){
                window.addEventListener('message', function(e){
                document.getElementById("res").innerHTML = e.data;
                });
                });
                </script>
            </body>
            </html>
            """ % (js_src, data_dict['MerchantID'], data_dict['SPToken'], PType, PName)

            html_test.write(html)

        op.goToURL('file:///' + html_tmp)

        # op.clickElem('html/body/button', findby='xpath')
        op.clickElem('Btn_Pay', findby='id')


    def makeHtmlFileNew(self, save_path, data_dict, PType, PName, CBtn):
        op = self.webop
        html_tmp = os.path.join(save_path, 'tmp.html')
        with open(html_tmp, mode='w') as html_test:
            js_src = self.feature_conf['SPCreateTrade_JS']

            html = """
            <!DOCTYPE html>
            <html>
            <head>
            <script src = "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js">
            </script>
            </head>
            <body>
                <h1 id="res">test</h1>
                <script src = "%s"
                    data-MerchantID = %s
                    data-SPToken = %s
                    data-PaymentType="%s"
                    data-PaymentName="%s"
                    data-CustomerBtn="%s">
                </script>
                <button id="Customer_Btn_CVS" onclick="checkOut('CVS')">CVS Pay</button>
                <button id="Customer_Btn_ATM" onclick="checkOut('ATM')">ATM Pay</button>
                <button id="Customer_Btn_CREDIT" onclick="checkOut('CREDIT')">CREDIT Pay</button>
                <script>
                $(function(){
                window.addEventListener('message', function(e){
                document.getElementById("res").innerHTML = e.data;
                });
                });
                </script>
                <script>               
                var customer_btn = %s;
                if(customer_btn == "0"){
                    document.all["Customer_Btn_CVS"].style.display = "none";
                    document.all["Customer_Btn_ATM"].style.display = "none";
                    document.all["Customer_Btn_CREDIT"].style.display = "none";
                }
                </script>
            </body>
            </html>
            """ % (js_src, data_dict['MerchantID'], data_dict['SPToken'], PType, PName, CBtn, CBtn)
            html_test.write(html)
        op.goToURL('file:///' + html_tmp)
        # op.clickElem('html/body/button', findby='xpath')
        if CBtn != '':
            if CBtn == '1' and PType == 'CVS':
                print('Customer CVS')
                op.clickElem('Customer_Btn_CVS', findby='id')
            elif CBtn == '1' and PType == 'ATM':
                print('Customer ATM')
                op.clickElem('Customer_Btn_ATM', findby='id')
            elif CBtn == '1' and PType == 'CREDIT':
                print('Customer CREDIT')
                op.clickElem('Customer_Btn_CREDIT', findby='id')
            elif CBtn == '0':
                print('BUTTON: Btn_Pay')
                op.clickElem('Btn_Pay', findby='id')
            else:
                raise ValueError('Button does not exist.')

    def inputPaymentInfo(self, card_no, exp_year, exp_month, cvv, cell_no, card_owner):
        op = self.webop
        op.changeFrame()
        cno_part = card_no.split('-')
        op.inputTextBox('CardHolderTemp', card_owner)
        op.inputTextBox('CardNoPart1', cno_part[0])
        op.inputTextBox('CardNoPart2', cno_part[1])
        op.inputTextBox('CardNoPart3', cno_part[2])
        op.inputTextBox('CardNoPart4', cno_part[3])
        op.inputTextBox('CreditMM', exp_month)
        op.inputTextBox('CreditYY', exp_year)
        op.inputTextBox('CreditAuth', cvv)
        op.inputTextBox('CellPhoneCheck', cell_no)
        op.clickElem('CreditPaySubmit', findby='id')

    def inputPaymentInfoE(self, card_no, exp_year, exp_month, cvv, cell_no,email,card_owner):
        op = self.webop
        op.changeFrame()
        cno_part = card_no.split('-')
        op.inputTextBox('CardHolderTemp', card_owner)
        op.inputTextBox('CardNoPart1', cno_part[0])
        op.inputTextBox('CardNoPart2', cno_part[1])
        op.inputTextBox('CardNoPart3', cno_part[2])
        op.inputTextBox('CardNoPart4', cno_part[3])
        op.inputTextBox('CreditMM', exp_month)
        op.inputTextBox('CreditYY', exp_year)
        op.inputTextBox('CreditAuth', cvv)
        op.inputTextBox('CellPhoneCheck', cell_no)
        op.inputTextBox('EmailTemp', email)
        op.clickElem('CreditPaySubmit', findby='id')

    def mobilesubmitinputPaymentInfo(self, card_no, exp_year, exp_month, cvv, cell_no, card_owner):
        op = self.webop
        op.changetab(1)
        cno_part = card_no.split('-')
        op.inputTextBox('CardHolderTemp', card_owner)
        op.inputTextBox('CardNoPart1', cno_part[0])
        op.inputTextBox('CardNoPart2', cno_part[1])
        op.inputTextBox('CardNoPart3', cno_part[2])
        op.inputTextBox('CardNoPart4', cno_part[3])
        op.inputTextBox('CreditMM', exp_month)
        op.inputTextBox('CreditYY', exp_year)
        op.inputTextBox('CreditAuth', cvv)
        op.inputTextBox('CellPhoneCheck', cell_no)

        time.sleep(2)
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(2)
        print("333")
        op.clickElem('CreditPaySubmit', findby='id')
        print("55555")
        time.sleep(10)
        op.handleAlert()
        time.sleep(20)
    def inputPaymentPageCreditInfoBind(self, card_no, exp_year, exp_month, cvv, cell_no, card_owner ,mode, rebind=False):
        op = self.webop
        cno_parts = card_no.split('-')
        op.changeFrame()
        if mode != 'divide':
            op.clickElem('nav-section3')
            time.sleep(2)
            op.handleAlert()
        op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
        op.ElemisDisplay('CreditCardDelete')
        time.sleep(2)
        if rebind is False:
            if op.ElemisDisplay('CreditCardDelete') is False:
                print('Elem not exists')
                time.sleep(2)
                op.inputTextBox('CardHolderTemp', card_owner)
                op.inputTextBox('CardNoPart1', cno_parts[0])
                op.inputTextBox('CardNoPart2', cno_parts[1])
                op.inputTextBox('CardNoPart3', cno_parts[2])
                op.inputTextBox('CardNoPart4', cno_parts[3])
                # op.inputTextBox('CreditMM', exp_month)
                # op.inputTextBox('CreditYY', exp_year)
                op.inputTextBox('CreditMM', exp_month)
                op.inputTextBox('CreditYY', exp_year)
                op.inputTextBox('CreditAuth', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)
                op.inputTextBox('CellPhoneCheck', cell_no)
                op.clickElem('CreditPaySubmit')
                op.handleAlert()
            elif op.ElemisDisplay('CreditCardDelete') == True:
                print('Elem exists')
                op.executeScript('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(2)
                op.clickElem('CreditPaySubmit')
        elif rebind == True:
            if op.ElemisDisplay('CreditCardDelete') == True:
                print('Rebinding')
                op.clickElem('CreditCardDelete')
                time.sleep(2)
                op.handleAlert()
                time.sleep(5)
                op.inputTextBox('CardHolderTemp', card_owner)
                op.inputTextBox('CardNoPart1', cno_parts[0])
                op.inputTextBox('CardNoPart2', cno_parts[1])
                op.inputTextBox('CardNoPart3', cno_parts[2])
                op.inputTextBox('CardNoPart4', cno_parts[3])
                # op.inputTextBox('CreditMM', exp_month)
                # op.inputTextBox('CreditYY', exp_year)
                op.inputTextBox('CreditMM', exp_month)
                op.inputTextBox('CreditYY', exp_year)
                op.inputTextBox('CreditAuth', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)
                op.inputTextBox('CellPhoneCheck', cell_no)
                op.clickElem('CreditPaySubmit')
            elif op.ElemisDisplay('CreditCardDelete') == False:
                time.sleep(2)
                op.inputTextBox('CardHolderTemp', card_owner)
                op.inputTextBox('CardNoPart1', cno_parts[0])
                op.inputTextBox('CardNoPart2', cno_parts[1])
                op.inputTextBox('CardNoPart3', cno_parts[2])
                op.inputTextBox('CardNoPart4', cno_parts[3])
                # op.inputTextBox('CreditMM', exp_month)
                # op.inputTextBox('CreditYY', exp_year)
                op.inputTextBox('CreditMM', exp_month)
                op.inputTextBox('CreditYY', exp_year)
                op.inputTextBox('CreditAuth', cvv)
                # op.inputTextBox('tmpIDNO', citizenid)
                op.inputTextBox('CellPhoneCheck', cell_no)
                op.clickElem('CreditPaySubmit', findby='id')
                print('TE46')
            print('TE5')
    def inputPaymentInfo1(self, card_no, exp_year, exp_month, cvv, cell_no):
        op = self.webop
        op.changeFrame()
        cno_part = card_no.split('-')
        op.inputTextBox('CardNoPart1', cno_part[0])
        op.inputTextBox('CardNoPart2', cno_part[1])
        op.inputTextBox('CardNoPart3', cno_part[2])
        op.inputTextBox('CardNoPart4', cno_part[3])
        op.inputTextBox('CreditMM', exp_month)
        op.inputTextBox('CreditYY', exp_year)
        op.inputTextBox('CreditAuth', cvv)
        op.inputTextBox('CellPhoneCheck', cell_no)
        op.clickElem('CreditPaySubmit', findby='id')

        def inputPaymentInfoE(self, card_no, exp_year, exp_month, cvv, cell_no):
            op = self.webop
            op.changeFrame()
            cno_part = card_no.split('-')
            op.inputTextBox('CardNoPart1', cno_part[0])
            op.inputTextBox('CardNoPart2', cno_part[1])
            op.inputTextBox('CardNoPart3', cno_part[2])
            op.inputTextBox('CardNoPart4', cno_part[3])
            op.inputTextBox('CreditMM', exp_month)
            op.inputTextBox('CreditYY', exp_year)
            op.inputTextBox('CreditAuth', cvv)
            op.inputTextBox('CellPhoneCheck', cell_no)
            op.clickElem('CreditPaySubmit', findby='id')
    def queryCreditOTP(self, phone_no):
        time.sleep(20)
        dic_otp_queryinfo = {
            'CellNo': phone_no,
            'OTPType': 'ECpay_Credit_Payment'
        }

        otp_query = self.getRequestFromAPI(dic_otp_queryinfo, self.feature_conf['OtpCollectorAddr'])
        if otp_query != 'Not_Found':
            otp_data = json.loads(otp_query)
            return otp_data

    # def inputOTP(self, otp_data):
    #     op = self.webop
    #     passcode = otp_data['OTP']
    #     print passcode
    #     op.inputTextBox('SMSAuthCode', passcode)
    #     op.clickElem('Submit')

    def inputOTP(self):
        time.sleep(20)
        op = self.webop
        passcode = op.getElemValue('HightlightOTP', find_by='id')
        # print passcode
        sms_code = op.resolveSMSAuthCode(passcode)

        op.inputTextBox('SMSAuthCode', sms_code)

        op.clickElem('Submit')
    def mobileinputOTP(self):
        time.sleep(10)
        op = self.webop

        # op.clickElem('CreditPaySubmit', findby='id')
        time.sleep(10)
        passcode = op.getElemValue('HightlightOTP', find_by='id')
        # print passcode


        sms_code = op.resolveSMSAuthCode(passcode)

        op.inputTextBox('SMSAuthCode', sms_code)


        op.clickElem('Submit')



        time.sleep(10)
        op.changetab(0)
        time.sleep(10)
    def getResultfromBrowser(self, Type=''):
        op = self.webop
        op.handleAlert()
        time.sleep(5)
        self.webop.drv.switch_to_default_content()
        if Type != '':
            op.clickElem('iframeECPayClose_%s' %Type)
        res = op.getElem('h1', find_by='tag').text
        return res

    def cleanHtmlTmp(self, html_path):
        time.sleep(5)
        file = os.path.join(html_path, 'tmp.html')
        time.sleep(5)
        os.remove(file)
        return 'Html tmp file removed ...'

    def submitCVSPayment(self):
        op = self.webop
        op.changeFrame()
        op.clickElem('.btn.default.btnCVS', findby='css')

    def submitATMPayment(self):
        op = self.webop
        op.changeFrame()
        op.selectDropboxList('value', '10002@8@ATM_CHINATRUST', 'PaymentName')
        op.clickElem('.btn.default.btnATM', findby='css')

    def submitATMPaymentPanhsin(self):
         op = self.webop
         op.changeFrame()
         op.selectDropboxList('value', '10002@17@ATM_PANHSIN', 'PaymentName')
         op.clickElem('.btn.default.btnATM', findby='css')

    def mobilesubmitCVSPayment(self):
        op = self.webop
        op.changetab(1)
        op.clickElem('.btn.default.btnCVS', findby='css')
        qrurl = op.getElem('img', find_by='tag').get_attribute('src')
        if '.png' in qrurl:
            print('QR is fine')
        else:
            raise ValueError('QRCode Error')
        op.changetab(0)
        op.handleAlert()

    def mobilesubmitATMPayment(self):
        op = self.webop
        op.changetab(1)
        op.selectDropboxList('value', '10002@8@ATM_CHINATRUST', 'PaymentName')
        op.clickElem('.btn.default.btnATM', findby='css')
        op.changetab(0)
        op.handleAlert()

    def mobileGetResult(self):
        op = self.webop
        time.sleep(2)
        res = op.getElem('h1', find_by='tag').text

        #op.clickElem('CreditPaySubmit', findby='id')
        return res

    def simulatePay(self, mer_id):
        op = self.webop
        op.goToURL('https://vendor-stage.ecpay.com.tw/Frame/Index')