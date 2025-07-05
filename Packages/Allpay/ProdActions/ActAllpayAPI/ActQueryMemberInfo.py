# -*- coding:utf-8 -*-
import time
import json
import os
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actQueryMemberInfo(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI',
                                                                feature_name='QueryMemberInfo')
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
        
    def genOrderRequestInfo(self, param_csv):
        req_data = self.genArgsDictFromCSV(param_csv, de_strip=True)
        req = {}
        req['PlatformID'] = req_data['PlatformID']
        req_data.pop('PlatformID')
        json2string = json.JSONEncoder().encode(req_data)
        print(json2string)
        encode_jsonstring = self.encrypt(json2string)
        print(encode_jsonstring)
        req['PlatformData'] = encode_jsonstring
        return req
    
    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_act = self.feature_conf['QueryMemberInfo_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_act, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        op.handleAlert()
        return browser_drv

    # 加密字串，如果text不是16的倍數[加密字串text必須為16的倍數!]，那就補足為16的倍數
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
        # 所以這裡統一把加密後的字串轉為16進制字串
        return b2a_hex(ciphertext)

    # 解密後，去掉補足的padding
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        pad = plain_text[-1]
        self.log.INFO(plain_text.decode('utf-8'))
        if ord(pad) <= 16:
            return plain_text.rstrip(pad)
        else:
            return plain_text.rstrip(' ')

    def strToDict(self, res):
        res_list = res
        replace_list = ['{', '}', '"']
        for replace_args in replace_list:
            if replace_args == '{' or replace_args == '}' or replace_args == '"':
                res_list = res_list.replace(replace_args, '')
        res_list = res_list.split(',')
        res_dict = {}
        for item in res_list:
            res_dict[item.split(':')[0]] = item.split(':')[1]
        print(res_dict)
        self.log.INFO(res_dict)
        return res_dict


    
