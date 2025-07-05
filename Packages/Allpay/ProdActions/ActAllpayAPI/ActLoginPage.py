# -*- coding: utf-8 -*-

from UIOperate.WebOperate import webOperate
import LibGeneral.TestHelper as Thelper
import LibGeneral.funcGeneral as funcGen
import LibGeneral.GetConfigValue as getConf
import time
import os
import sys


class actLoginPage(webOperate):
    def __init__(self, drv, log_file):
        webOperate.__init__(self, drv)

        self.conf = getConf.getConfig()
        self.rootdir = self.conf.getRootDir()        
        self.login_elem_list = os.path.join(self.rootdir, 'Conf', 'Element_Corresponding', 'AllpayWeb', 'LoginPage.csv')
        self.login_url = 'https://login-stage.allpay.com.tw/Login?NextURL=https%253a%252f%252fwww-stage.allpay.com.tw%252f%252f'
        self.helper = Thelper.classTestHelper(log_file)
        self.login_identds = self.helper.generateElemDataset(self.login_elem_list)
        #self.op = WEBOP.webOperate(browser)
        
    def generalLogin(self, usrn, passwd):
        #op = self.op
        #op.goToURL(self.login_url)
        #op.inputTextBox('UserCode', 'b88612029')
        #op.inputTextBox('Pwd', 'E4vytiax5298')
        #capt_answer = op.resolveLoginCaptcha('_mvcCaptchaGuid')
        #op.inputTextBox('login-captcha', capt_answer)
        #op.clickElem('SubmitLogin')
        
        get = self.helper.getElemIdentFromDataSet
        ids = self.login_identds
        
        i = 0
        while i < 3:
            print("HANDLER:before",  self.drv.window_handles)
            self.goToURL(self.login_url)

            print("HANDLER:after",  self.drv.window_handles)
            self.inputTextBox(get('Login_username', ids)['Identifier'], usrn)
            self.inputTextBox(get('Login_password', ids)['Identifier'], passwd)
            capt_answer = self.resolveLoginCaptcha('_mvcCaptchaGuid')
            self.inputTextBox(get('Captcha_answer', ids)['Identifier'], capt_answer)
            #self.inputTextBox(get('Captcha_answer', ids)['Identifier'], '1111')
            self.clickElem(get('Submit_login_button', ids)['Identifier'])
            err_dis = self.getElemDisplayStat('div.alert_box.error.error_box.login-captcha_err', find_by='css', ignore_nfound=True)
            alert_present = self.handleAlert()
            if alert_present is True or err_dis == 'block':
                i += 1
            else:
                break
        if i == 3:
            print("LOGIN FAIL 3 TIMES")
            sys.exit(103)
        
        
        time.sleep(2)


        
    def hoverAcctSubMenu(self):
        #submenu = self.getElem('a.table_btn_blue.margin_l0.margin_t5', find_by='css')
        submenu = self.getElem('oe_menu', find_by='id')
        print(submenu)
        #self.mouseHoverElem(submenu, 60, 27)
        self.clickElem("[href='https://member.allpay.com.tw/MemberEdit/EditGeneralInfo']", findby='css')
        
    def clickForgetPwdLink(self):
        self.goToURL(self.login_url)
        #self.clickElem('/html/body/div/div[3]/div/div[1]/form/ul/li[2]/div/div[1]/span/a', findby='xpath')
        self.clickElem("[href='https://Member.allpay.com.tw/MemberPwdReset/AddPasswordReset?PwdType=1']", findby='css')
    #def facebookLogin(self):


