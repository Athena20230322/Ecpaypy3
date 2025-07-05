# -*- coding: utf-8 -*-
import time
import json
import os
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from base64 import b64encode, b64decode
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actGetUserInfo(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='GetUserInfo')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        self.key = hash_key
        self.iv = hash_iv
        self.mode = AES.MODE_CBC
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def GetQuerMemberInfoUrl(self):
        op = self.webop
        divText = op.drv.find_element_by_tag_name('body').text
        self.log.INFO(divText)
        return divText

    def genOrderRequestInfo(self, param_csv, token):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if req['OpenKey'] == 'AUTO_GEN_OPENKEY':
            req['OpenKey'] = self.feature_conf['OpenKey']
        if req['Token'] == 'GET_OPENIDLOGIN_TOKEN':
            req['Token'] = token
        temp_dic = {}
        temp_dic['MerchantID'] = req['MerchantID']
        req.pop('MerchantID')
        json2string = json.JSONEncoder().encode(req)
        print(json2string)
        encode_jsonstring = self.encrypt(json2string)
        print(encode_jsonstring)
        temp_dic['OpenData'] = encode_jsonstring
        print(temp_dic)
        return temp_dic
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['GetUserInfo_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        # 在這密鑰key and iv 16（AES-128）、24（AES-192）、或32（AES-256）Bytes長度，目前AES-128足夠用
        amount_to_pad = 0
        count = len(text)
        print("Before add padding len: ", count)
        print("AES block size: ", AES.block_size)
        if count < AES.block_size:
            amount_to_pad = (AES.block_size - count)
        elif count > AES.block_size:
            if count % AES.block_size == 0:
                amount_to_pad = 16
            else:
                amount_to_pad = (AES.block_size - (count % AES.block_size))
        text += (chr(amount_to_pad) * amount_to_pad)
        print("After added pad len: ", len(text))
        ciphertext = cryptor.encrypt(text)
        # 因為AES加密時得到的字串不一定是ascii字串集的，輸出到終端或者保存的時候可能存在問題
        # 所以這裡統一把加密後的字串轉為Base64字串
        return b64encode(ciphertext)

    # 解密後，去掉補足的padding
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(b64decode(text))
        pad = plain_text[-1]
        self.log.INFO(plain_text.decode('utf-8'))
        if ord(pad) <= 16:
            return plain_text.rstrip(pad)
        else:
            return plain_text.rstrip(' ')

    def strToDict(self, res):
        res_list = res
        replace_list = ['{', '}', '"', '\r\n', ' ']
        for replace_args in replace_list:
            if replace_args == '{' or replace_args == '}' or replace_args == '"' or replace_args == '\r\n' or \
                            replace_args == ' ':
                res_list = res_list.replace(replace_args, '')
        res_list = res_list.split(',')
        res_dict = {}
        for item in res_list:
            res_dict[item.split(':')[0]] = item.split(':')[1]
        print(res_dict)
        self.log.INFO(res_dict)
        return res_dict