# -*-coding: utf-8 -*-
import time
import json
import os
from Crypto.Cipher import AES
from binascii import a2b_hex, b2a_hex
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actRemoveMemberInfo(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='RemoveMemberInfo')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)
        
    def genRemoveInfo(self, param_csv, ID):
        req_data = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if req_data['ID'] == 'GEN_ID':
            req_data['ID'] = self.gen_uid(with_dash=False)[:30]
            req_data['ID'] = self.gen_uid(with_dash=False)[:20]
        elif req_data['ID'] != '':
            pass
        else:
            req_data['ID'] = ID
        req = {}
        req['PlatformID'] = req_data['PlatformID']
        req_data.pop('PlatformID')
        json2String = json.JSONEncoder().encode(req_data)
        print(json2String)
        AES_result = self.__AESencrypt(json2String)
        req['PlatformData'] = AES_result
        print(req)
        return req
    
    def createRemovingByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['Remove_API']
        form_genorder = self.createHtmlFormJs('FormGenRemoving', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        return browser_drv

    def fillInLoginInfo(self, browser_drv, account, pw):
        op = self.webop
        op.inputTextBox('UserCode', account, findby='id')
        op.inputTextBox('Pwd', pw, findby='id')
        imgs = op.drv.find_elements_by_tag_name('img')
        captcha_result = ''
        for img in imgs:
            if img.get_attribute('title') == '刷新驗證碼':
                captcha_result = op.resolveCaptchaElem(img)
                break
            else:
                continue
        op.inputTextBox('login-captcha', captcha_result, findby='id')
        op.clickElem('btnSubmit', findby='id')

    def getDataFromBrowser(self, browser_drv):
        op = self.webop
        body = op.drv.find_element_by_tag_name('body').text
        self.log.INFO(body)
        return body

    def strToDict(self, remove_return):
        item_list = remove_return.split('\n')
        res_dict = {}
        for item in item_list:
            res_dict[item.split(':')[0]] = item.split(':')[1]
        self.log.INFO(res_dict)
        return res_dict

    def decodeResult(self, res_dict):
        cyphertext = res_dict['PlatformData']
        result = self.__AESdecrypt(cyphertext)
        res_dict = json.loads(result)
        for key in res_dict:
            if type(res_dict[key]) is int:
                res_dict[key] = str(res_dict[key]).decode('utf-8')
        print(result)
        self.log.INFO(res_dict)
        return res_dict

    def __AESencrypt(self, text):
        cryptor = AES.new(self.hkey, AES.MODE_CBC, self.hiv)
        print(text)
        length = 16
        pad = 0
        count = len(text)
        print(count)
        if count < length:
            pad = (length - count)
        elif count > length:
            if count % length == 0:
                pad = 16
                print(pad)
            else:
                pad = length - (count % length)
        text += (chr(pad) * pad)
        print(len(text))
        ciphertext = cryptor.encrypt(text)
        hexCipherText = b2a_hex(ciphertext)
        return hexCipherText

    def __AESdecrypt(self, text):
        cryptor = AES.new(self.hkey, AES.MODE_CBC, self.hiv)
        plaintext = cryptor.decrypt(a2b_hex(text))
        padding = plaintext[-1:]
        if ord(padding) <= 16:
            return plaintext.rstrip(padding).decode('utf-8')
        else:
            return plaintext.rstrip(' ').decode('utf-8')
