# -*-coding: utf-8 -*-
import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actOpenIDLogin(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='OpenIDLogin')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
        
    def genLoginRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        print(req)
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['OpenIDLogin_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        return browser_drv

    def login(self, account, pw):
        op = self.webop
        op.inputTextBox('UserCode', account)
        op.inputTextBox('Pwd', pw)
        imgs = op.drv.find_elements_by_tag_name('img')
        capt_code = ''
        for img in imgs:
            if img.get_attribute('title') == '刷新驗證碼':
                capt_code = op.resolveCaptchaElem(img)
                break
        op.inputTextBox('login-captcha', capt_code)
        op.clickElem('SubmitLogin')

    def getResultFromBrowser(self):
        op = self.webop
        body = op.drv.find_elements_by_tag_name('body')
        res_dict = {}
        for item in body:
            body = item.text.encode('utf-8')
        body = body.split('\n')
        for ele in body:
            res_dict[ele.split(':')[0]] = ele.split(':')[1]
        self.log.INFO(res_dict)
        return res_dict
