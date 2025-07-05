import requests
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
import LibGeneral.funcGeneral as funcGen
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import SeleniumHelper.SeleniumHelper as SHELPER
import CaptchaResolve.CaptchaResolve as CAPRE
from selenium.webdriver.common.keys import Keys
from PIL import Image
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

PJOIN = os.path.join


class actCapture(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='Capture')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_actCapture = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_actCapture, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)

    def clickLogIn(self, driver):
        op = self.webop
        op.clickElem('//*[@id="divCheckAddMember"]/div/form/div/div/ul/li[1]/a', findby='xpath')
        while True:
            if WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'WebAtmPaySubmit'))):
                time.sleep(1)
                break

    def chooseBank(self, driver, cell_phone):
        op = self.webop
        op.selectDropboxList('value', '10001@2000@WebATM_TAISHIN', 'webatmPayType')
        op.inputTextBox('CellPhone_WebAtmPaySubmit', cell_phone)
        op.clickElem('WebAtmPaySubmit')
        buttons = op.drv.find_elements_by_tag_name('button')
        for button in buttons:
            if button.get_attribute('class') == 'swal2-confirm styled':
                button.click()
                break

    def login(self, driver, account, pw):
        op = self.webop
        while True:
            if op.getElem('m_account') is not False:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "m_account")))
                time.sleep(1)
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

    def inputCaptchaAndSubmit(self, driver, captcha):
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
            if WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submitbutton"))):
                op.clickElem('submitbutton')
                break
        while True:
            time.sleep(1)
            if WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/fieldset/p/input'))):
                op.clickElem('/html/body/form/fieldset/p/input', findby='xpath')
                break

    def payMoney(self, driver):
        op = self.webop
        time.sleep(5)
        op.selectDropboxList('value', '10001@2000@WebATM_TAISHIN', 'webatmPayType')
        op.clickElem('WebAtmPaySubmit')
        time.sleep(3)
        buttons = op.drv.find_elements_by_tag_name('button')
        for button in buttons:
            if button.get_attribute('class') == 'swal2-confirm styled':
                button.click()
                break
        while True:
            time.sleep(5)
            if WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/fieldset/p/input'))):
                op.clickElem('/html/body/form/fieldset/p/input', findby='xpath')
                break
        while True:
            time.sleep(3)
            if WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/h3'))):
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
            if out is None or capt_answer == '':
                i += 1
            else:
                return out

    def genElemScreenshot(self, drv, elem, folderpath):
        gen_uuid = funcGen.genRandomUuid
        size = elem.size
        location = elem.location
        # location['y'] -= 155
        # location['y'] -= 120
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


    def queryTradeInfo(self, req_info):
        query_trade_info_url = self.feature_conf['QueryOrder_API']
        print(query_trade_info_url)
        query_req = {}
        query_req.update({'MerchantID': req_info['MerchantID'],
                          'MerchantTradeNo': req_info['MerchantTradeNo'],
                          'TimeStamp': str(funcGen.getCurrentDatetimeStamp()[1])
                          })
        checksum = self.genChkMacVal(query_req, mode='local')
        query_req.update({'CheckMacValue': checksum})
        response = requests.post(url=query_trade_info_url, data=query_req)
        print((response.text))
        res_dict = self.strToDict(response.text)
        return res_dict

    def genCaptureRequestInfo(self, param_csv, MerchantTradeNo):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        for key in req:
            req[key] = req[key].encode('utf-8')
        req['MerchantTradeNo'] = MerchantTradeNo
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def captureResult(self, req_info):
        form_actCapture = self.feature_conf['Capture_API']
        response = requests.post(url=form_actCapture, data=req_info)
        print((response.text))
        return response.text

    def strToDict(self, req_str):
        result = {}
        for ele in req_str.split('&'):
            tmp_list = ele.split('=')
            result[tmp_list[0]] = tmp_list[1]
        print(result)
        return result

    def queryCaptureResult(self, browser_drv, acct, pw, merchant_trade_no):
        op = self.webop
        form_act = self.feature_conf['Query_API']
        form_genorder = self.createHtmlFormJs('FormQueryCapture', {}, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        time.sleep(1)
        op.inputTextBox('Account', acct)
        op.inputTextBox('Password', pw)
        captcha_code = op.resolveLoginCaptcha('_mvcCaptchaGuid')
        op.inputTextBox('allpayCaptchaValue', captcha_code)
        op.clickElem('LoginAllpay')
        time.sleep(2)
        leftFrame = browser_drv.find_element_by_id('leftFrame')
        browser_drv.switch_to_frame(leftFrame)
        op.clickElem('//*[@id="accordion-2"]/li[9]/a', findby='xpath')
        time.sleep(1)
        op.clickElem('//*[@id="accordion-2"]/li[9]/ul/li[7]/a', findby='xpath')
        time.sleep(2)
        browser_drv.switch_to_default_content()
        contentFrame = browser_drv.find_element_by_id('contentFrame')
        browser_drv.switch_to_frame(contentFrame)
        op.inputTextBox('MerchantTradeNo', merchant_trade_no)
        op.clickElem('ListTradeSubmit')
        time.sleep(3)
        result_ele = op.getElem('//*[@id="divAio"]/div/div/div/div[2]/div[1]/table/tbody/tr[2]/td[6]/span', find_by='xpath')
        return result_ele.text
