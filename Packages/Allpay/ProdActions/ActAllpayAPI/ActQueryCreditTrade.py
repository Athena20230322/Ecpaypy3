# -*-coding:utf-8 -*-
import time
import requests
import os
import LibGeneral.funcGeneral as funcGen
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import SeleniumHelper.SeleniumHelper as SHELPER
import CaptchaResolve.CaptchaResolve as CAPRE
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

PJOIN = os.path.join

class actQueryCreditTrade(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='QueryCreditTrade')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
    def genQueryRequestInfo(self, param_csv, merchantTradeNo):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req['MerchantTradeNo'] = merchantTradeNo
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        return browser_drv

    def clickLogIn(self, driver):
        op = self.webop
        op.clickElem('//*[@id="divCheckAddMember"]/div/form/div/div/ul/li[1]/a', findby='xpath')
        while True:
            time.sleep(1)
            if WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'CreditPaySubmit'))):
                break

    def inputPaymentPageCreditInfo(self, owner_id, card_no, exp_year, exp_month, cvv, cell_no, mode='logFirst'):
        op = self.webop
        cno_parts = card_no.split('-')
        time.sleep(3)
        op.inputTextBox('CardNoPart1', cno_parts[0])
        op.inputTextBox('CardNoPart2', cno_parts[1])
        op.inputTextBox('CardNoPart3', cno_parts[2])
        op.inputTextBox('CardNoPart4', cno_parts[3])
        op.inputTextBox('CreditMM', exp_month)
        op.inputTextBox('CreditYY', exp_year)
        op.inputTextBox('CreditAuth', cvv)
        op.inputTextBox('tmpIDNO', owner_id)
        if mode != 'logFirst':
            op.inputTextBox('CellPhone_CreditPaySubmit', cell_no)
        op.clickElem('CreditPaySubmit')

    def confirmSubmitCreditInfo(self, driver):
        op = self.webop
        while True:
            time.sleep(3)
            if op.getElem('//*[@id="pay-confirm-popup"]/form/div/div[4]/a[1]', find_by='xpath').get_attribute('type') != 'hidden':
                op.clickElem('//*[@id="pay-confirm-popup"]/form/div/div[4]/a[1]', findby='xpath')
                break
        while True:
            time.sleep(3)
            if WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/h3'))):
                break

    def confirmOrderSuccess(self):
        op = self.webop
        result = op.getElem('content-title', find_by='class').text
        self.log.INFO(result)
        if result == '恭喜您！付款成功！':
            return
        else:
            raise ValueError("pay fail! msg: %s" % result)



    def login(self, driver, account, pw):
        op = self.webop
        while True:
            time.sleep(1)
            if op.getElem('m_account') is not False:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "m_account")))
                op.inputTextBox('m_account', account)
                op.inputTextBox('m_pw', pw)
                break


    def openCaptchaInNewTab(self, web_driver):
        op = self.webop
        ActionChains(web_driver).key_down(Keys.CONTROL).click(web_driver.find_element_by_id('reloadCaptcha')).perform()
        captcha_ele = web_driver.find_element_by_xpath('//*[@id="divLoginCaptcha"]/img')
        src = captcha_ele.get_attribute('src')
        web_driver.switch_to_window(web_driver.window_handles[1])
        web_driver.get(src)
        print((web_driver.current_url))
        return web_driver

    def resolveCaptchaFromNewTab(self, rootdir, web_driver):
        op = self.webop
        captcha_ele = op.getElem('/html/body/img', find_by='xpath')
        result = self.resolveLoginCaptcha(rootdir, web_driver, captcha_ele)
        web_driver.close()
        web_driver.switch_to_window(web_driver.window_handles[0])
        return result

    def inputCaptchaAndSubmit(self, driver,  captcha):
        op = self.webop
        print(captcha)
        op.inputTextBox('//*[@id="login-captcha"]', captcha, findby='xpath')
        op.inputTextBox('//*[@id="login-captcha"]', captcha, findby='xpath')
        while True:
            if op.getElem('aLoginSubmit').get_attribute('type') != 'hidden':
                op.clickElem('aLoginSubmit')
                break
        while True:
            time.sleep(1)
            if WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'checkTradeButton'))):
                op.clickElem('checkTradeButton')
                break
        while True:
            time.sleep(1)
            if op.getElem('submitbutton') is not False:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submitbutton")))
                op.clickElem('submitbutton')
                break

    def resolveLoginCaptcha(self, rootdir, drv, img_elem):
        cap_re = CAPRE.DBC()
        helper = SHELPER.clsWebDriverHelper
        png_container = os.path.join(rootdir, 'Tmp')
        capt = self.genElemScreenshot(drv, img_elem, png_container)
        i = 0
        capt_answer = 0
        while i < 3:
            out = cap_re.resolveFile(capt)
            if out == None or capt_answer == '':
                i += 1
            else:
                return out

    def genElemScreenshot(self, drv, elem, folderpath):
        gen_uuid = funcGen.genRandomUuid
        size = elem.size
        location = elem.location
        print(size)
        print(location)
        scr_fname = gen_uuid(with_dash=False)
        scr_file = '.'.join(('scrnshot_' + scr_fname, 'png'))
        scr_fullpath = PJOIN(folderpath, scr_file)
        drv.save_screenshot(scr_fullpath)
        scr = Image.open(scr_fullpath)
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        output = scr.crop((left, top, right, bottom))
        out_file = '.'.join(('Elem_' + scr_fname, 'png'))
        out_fullpath = PJOIN(folderpath, out_file)
        output.save(out_fullpath)
        return out_fullpath

    def queryCreditOTP(self, phone_no):
        for i in range(10):
            time.sleep(5)
            otp_url = self.feature_conf['OTP']
            response = requests.post(url=otp_url)
            if response.text == 'not_found':
                continue
            else:
                return response.json()['OTP']

    def inputOTP(self, otp_data):
        op = self.webop
        passcode = otp_data['OTP']
        print(passcode)
        op.inputTextBox('SMSAuthCode', passcode)
        op.clickElem('Submit')

    def queryCreditCardPeriodInfo(self, req_info):
        form_actQueryCreditTrade = self.feature_conf['Query_API']
        response = requests.post(url=form_actQueryCreditTrade, data=req_info)
        print(('status: ' + str(response.status_code)))
        self.log.INFO("queryCreditCardPeriodInfo respond: " + response.content)
        print((response.content))
        print((response.json()))
        return response.json()

    def createOrderByRequest(self, req_info):
        pass

