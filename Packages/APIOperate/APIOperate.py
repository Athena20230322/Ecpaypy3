# -*- coding: utf-8 -*-
import os
import collections
import time
import datetime
import uuid
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from binascii import b2a_hex, a2b_hex
from PyDataSet.pyDataSet import classPyDataSet
import LibGeneral.funcGeneral as funcGen
from LibGeneral.TestHelper import classTestHelper
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urlencode
from urllib.parse import unquote_plus
from urllib.parse import quote_plus
from Crypto.Util.Padding import pad
#from urllib.parse import urlparse
import urllib.parse
from html.parser import HTMLParser
from hashlib import md5
import hashlib
import hmac
import requests
import re
import json
import LibGeneral.AddLog as Addlog

import rsa
import numpy as np

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5 as Sig_PK
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from selenium import webdriver
from  UIOperate import WebOperate


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)
    
    
class APIHelper():
    def __init__(self, hash_key, hash_iv):
    #def __init__(self):
        self.hkey = hash_key
        self.hiv = hash_iv
        self.log = Addlog.customLog()
        self.gen_uid = funcGen.genRandomUuid
        self.ds = classPyDataSet()
        self.thelper = classTestHelper()
        self.genChkMacUrl = 'http://payment-stage.allpay.com.tw/AioHelper/GenCheckMacValue'

    def genSession(self):
        sess = requests.session()
        return sess

    def genSimpleHtmlForm(self, arg_dict):
        pass

    def createHtmlFormJs(self, form_id, param_dict, method='POST', action='', submit=True):
        js_stmts = []
        gen_form = """
            var form = document.createElement("form");
            form.method = "%s";
            form.action = "%s"; 
        """ % (method, action)
        js_stmts.append(gen_form)
        params = list(param_dict.keys())
        for pa in params:
            
            create_input = """
            var elem = document.createElement("input"); 
            elem.name="elem";
            elem.value="%s";
            form.appendChild(elem);
            """ % (param_dict[pa])
            
            create_input = create_input.replace('elem', pa)
            js_stmts.append(create_input)
        
        form_add = 'document.body.appendChild(form);'
        submit_stmt = 'form.submit();'
        js_stmts.append(form_add)
        if submit is True:
            js_stmts.append(submit_stmt)
        str_stmt = ''.join(js_stmts)
        
        return str_stmt
    
    def genMercTradeNo(self):
        trade_no = self.gen_uid(with_dash=False)[0:19]
        self.log.INFO("MerchantTradeNo generated : %s." % (trade_no))
        return trade_no
        
    def urlEncodePyToNet(self, querystr):
        correspond = {
                        '%21':'!',
                        '%2A':'*',
                        '%28':'(',
                        '%29':')'
                      }
        codes = list(correspond.keys())
        querystr = str(querystr)
        for c in codes:
            querystr = querystr.replace(c, correspond[c])
        
        return querystr
    
    
    def genArgsDictFromCSV(self, csv_path, de_strip=False):
        dset = self.ds
        self.log.INFO("Import argument data from csv file %s" %(csv_path))
        raw_args = dset.importCSV(csv_path)
        arg_values = dset.queryDataSet(raw_args, ['Argument', 'Value'], withHeader=False)
        arg_dict = {}
        for argv in arg_values:
            argv_list = list(argv)
            v = argv_list[1]
            if v.startswith('AUTO_'):
                if v == 'AUTO_GEN_MERC_ID':
                    argv_list[1] = self.genMercTradeNo()
                elif v == 'AUTO_GEN_DATETIME':
                    curr_dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    argv_list[1] = curr_dt
                elif v == 'AUTO_GEN_DATE':
                    curr_dt = datetime.datetime.now().strftime("%Y/%m/%d")
                    argv_list[1] = curr_dt
                elif v == 'AUTO_GEN_UNIXSTAMP':
                    t_stamp = funcGen.getCurrentDatetimeStamp()
                    argv_list[1] = str(t_stamp[1])
                elif v == 'AUTO_GEN_GUID':
                    guid = uuid.uuid4().hex
                    argv_list[1] = guid
            elif v.startswith('CUSTOM_'):
                if v == 'CUSTOM_MID_DEFINED_IN_CONF':
                    uinfo = self.thelper.getCustomUserInfo()
                    mid = uinfo['MERCID']
                    argv_list[1] = mid
                    
            if de_strip is False:
                arg_dict[argv_list[0].strip(' ')] = argv_list[1].strip(' ')
            elif de_strip is True:
                arg_dict[argv_list[0].strip(' ')] = argv_list[1]
            else:
                raise ValueError("genArgsDictFromCSV: Unreconized 'de_strip' option")
                
        self.log.INFO("Generated argument dictionary: %s" %(arg_dict))

        return arg_dict

    def genhashhmac(self, arg_dict, case='sensitive'):
        od_arg_dict = {}
        hmacs=''
        if case == "insensitive":
            for key,value in sorted(list(arg_dict.items()), key=lambda x: x[0]):
                hmacs=hmacs+key+value


            #od_arg_dict = collections.OrderedDict(sorted(arg_dict.items(), key=lambda i: i[0].lower()))
        else:
            od_arg_dict = collections.OrderedDict(sorted(arg_dict.items()))
        print(('OD:', hmacs))

        #print to_req
        message = hmacs
        print (message)
        secret = "tL06r5Yo4BhpbA2r"
        h = hmac.new(secret, message, digestmod=hashlib.sha256)
        result = h.hexdigest()
        print((result.lower()))
        res = result.upper().lower()
        self.log.INFO("MacValue generating result : %s." % (res))
        return res
    
        
    def genChkMacVal(self, arg_dict, mode='local', codec='md5', case='sensitive'):
        od_arg_dict = {}
        if case == "insensitive":
            od_arg_dict = collections.OrderedDict(sorted(list(arg_dict.items()), key=lambda i: i[0].lower()))
        elif case == "insensitive1":
            od_arg_dict = collections.OrderedDict(sorted(list(arg_dict.items()), key=lambda i: i[0].lower()))
            self.hkey = 'spPjZn66i0OhqJsQ'
            self.hiv = 'hT5OJckN45isQTTs'
        else:
            od_arg_dict = collections.OrderedDict(sorted(arg_dict.items()))
        print(('OD:', od_arg_dict))
        to_req = urlencode(od_arg_dict)
        print (to_req)
        
        if mode == 'local':
            src_str = unquote_plus(to_req)        
            key_str = '='.join(['HashKey', self.hkey])
            iv_str = '='.join(['HashIV', self.hiv])
            src_str = '&'.join([key_str, src_str, iv_str])
            encoded = self.urlEncodePyToNet(quote_plus(src_str))
            #encoded = urllib.quote_plus(src_str)
            print (encoded)
            low = encoded.lower().encode("utf8")
            self.log.INFO("Parameter string to be encode: %s" %(low))
            ## Determine encoding method
            if codec == 'md5':
                md5_obj = md5(low)
                result = md5_obj.hexdigest()
            elif codec == 'sha256':
                result = hashlib.sha256(low).hexdigest()
            
        elif mode == 'api':
            header = {'Content-Type':'application/x-www-form-urlencoded'}
            self.log.INFO("Query GenCheckMacValue API for MacValue.")
            req = requests.post(url=self.genChkMacUrl, data=to_req, headers=header)
            #print req.content
            result = req.text
        else:
            raise ValueError("genChkMacVal: Unknown 'mode' argument.") 
        
        res = result.upper()
        self.log.INFO("MacValue generating result : %s." % (res))
        return res

    def genChkMacVal3D(self, arg_dict, mode='local', codec='md5', case='sensitive'):
        od_arg_dict = {}
        if case == "insensitive":
            od_arg_dict = collections.OrderedDict(sorted(list(arg_dict.items()), key=lambda i: i[0].lower()))
        else:
            od_arg_dict = collections.OrderedDict(sorted(arg_dict.items()))
        print(('OD:', od_arg_dict))
        to_req = urlencode(od_arg_dict)
        print (to_req)

        if mode == 'local':
            self.hkey = 'pwFHCqoQZGmho4w6'
            self.hiv = 'EkRm7iFT261dpevs'
            src_str = unquote_plus(to_req)
            key_str = '='.join(['HashKey', self.hkey])
            iv_str = '='.join(['HashIV', self.hiv])
            src_str = '&'.join([key_str, src_str, iv_str])
            encoded = self.urlEncodePyToNet(quote_plus(src_str))
            # encoded = urllib.quote_plus(src_str)
            print (encoded)
            low = encoded.lower().encode("utf8")
            self.log.INFO("Parameter string to be encode: %s" % (low))
            ## Determine encoding method
            if codec == 'md5':
                md5_obj = md5(low)
                result = md5_obj.hexdigest()
            elif codec == 'sha256':
                result = hashlib.sha256(low).hexdigest()

        elif mode == 'api':
            header = {'Content-Type': 'application/x-www-form-urlencoded'}
            self.log.INFO("Query GenCheckMacValue API for MacValue.")
            req = requests.post(url=self.genChkMacUrl, data=to_req, headers=header)
            # print req.content
            result = req.text
        else:
            raise ValueError("genChkMacVal: Unknown 'mode' argument.")

        res = result.upper()
        self.log.INFO("MacValue generating result : %s." % (res))
        return res

    def aesEncrypt(self, plaintext, encode='base64'):
        cryptor = AES.new(self.hkey.encode(encoding = 'UTF-8'), AES.MODE_CBC, self.hiv.encode(encoding = 'UTF-8'))
        plaintext_padded = self.__pkcs7Padding(plaintext)
        ciphered = cryptor.encrypt(plaintext_padded.encode(encoding = 'UTF-8'))
        #ciphered = cryptor.encrypt(pad(plaintext.encode(encoding = 'UTF-8'), AES.block_size))
        if encode == 'base64':
            return b64encode(ciphered)
        elif encode == 'hex':
            return b2a_hex(ciphered)

    def aesEncryptB2C(self, plaintext, encode='base64'):
        cryptor = AES.new('5294y06JbISpM5x9', AES.MODE_CBC, 'v77hoKGq4kWxNNIS')
        plaintext_padded = self.__pkcs7Padding(plaintext)
        ciphered = cryptor.encrypt(plaintext_padded)
        if encode == 'base64':
            return b64encode(ciphered)
        elif encode == 'hex':
            return b2a_hex(ciphered)
    def aesEncryptPID(self, plaintext, encode='base64'):
        cryptor = AES.new('spPjZn66i0OhqJsQ', AES.MODE_CBC, 'hT5OJckN45isQTTs')
        plaintext_padded = self.__pkcs7Padding(plaintext)
        ciphered = cryptor.encrypt(plaintext_padded)
        if encode == 'base64':
            return b64encode(ciphered)
        elif encode == 'hex':
            return b2a_hex(ciphered)

    def aesDecrypt(self, cypher_text, encode='base64', captcha=''):
        if captcha == '':
            cryptor = AES.new(self.hkey.encode(encoding = 'UTF-8'), AES.MODE_CBC, self.hiv.encode(encoding = 'UTF-8'))
            if encode == 'base64':
                plaintext = cryptor.decrypt(b64decode(cypher_text)).decode("utf-8")
            elif encode == 'hex':
                plaintext = cryptor.decrypt(a2b_hex(cypher_text)).decode("utf-8")
            else:
                plaintext = None
        elif captcha == 'cap':
            cryptor = AES.new('3jkd93mgtgsd4alb', AES.MODE_CBC, 'n8gf2joslrmcvnbq')
            if encode == 'base64':
                plaintext = cryptor.decrypt(b64decode(cypher_text)).decode("utf-8")
            elif encode == 'hex':
                plaintext = cryptor.decrypt(a2b_hex(cypher_text)).decode("utf-8")
            else:
                plaintext = None
        pad = plaintext[-1:]
        plaintext = self.urlDecode(plaintext.rstrip(pad))
        return plaintext

    def aesDecryptB2C(self, cypher_text, encode='base64', captcha=''):
        if captcha == '':
            cryptor = AES.new('5294y06JbISpM5x9', AES.MODE_CBC, 'v77hoKGq4kWxNNIS')
            if encode == 'base64':
                plaintext = cryptor.decrypt(b64decode(cypher_text))
            elif encode == 'hex':
                plaintext = cryptor.decrypt(a2b_hex(cypher_text))
            else:
                plaintext = None
        elif captcha == 'cap':
            cryptor = AES.new('3jkd93mgtgsd4alb', AES.MODE_CBC, 'n8gf2joslrmcvnbq')
            if encode == 'base64':
                plaintext = cryptor.decrypt(b64decode(cypher_text))
            elif encode == 'hex':
                plaintext = cryptor.decrypt(a2b_hex(cypher_text))
            else:
                plaintext = None
        pad = plaintext[-1:]
        plaintext = self.urlDecode(plaintext.rstrip(pad))
        return plaintext
    def aesDecryptPID(self, cypher_text, encode='base64', captcha=''):
        if captcha == '':
            cryptor = AES.new('spPjZn66i0OhqJsQ', AES.MODE_CBC,'hT5OJckN45isQTTs')
            if encode == 'base64':
                plaintext = cryptor.decrypt(b64decode(cypher_text))
            elif encode == 'hex':
                plaintext = cryptor.decrypt(a2b_hex(cypher_text))
            else:
                plaintext = None
        elif captcha == 'cap':
            cryptor = AES.new('spPjZn66i0OhqJsQ', AES.MODE_CBC, 'hT5OJckN45isQTTs')
            if encode == 'base64':
                plaintext = cryptor.decrypt(b64decode(cypher_text))
            elif encode == 'hex':
                plaintext = cryptor.decrypt(a2b_hex(cypher_text))
            else:
                plaintext = None
        pad = plaintext[-1:]
        plaintext = self.urlDecode(plaintext.rstrip(pad))
        return plaintext

    def aesEncryptforAPP(self, plaintext,key,iv, encode='base64'):
        cryptor = AES.new(key, AES.MODE_CBC,iv)
        plaintext_padded = self.__pkcs7Padding(plaintext)
        ciphered = cryptor.encrypt(plaintext_padded)
        if encode == 'base64':
            return b64encode(ciphered)
        elif encode == 'hex':
            return b2a_hex(ciphered)
    def aesDecryptforAPP(self, cypher_text,key,iv, encode='base64', captcha=''):
        if captcha == '':
            cryptor = AES.new(key, AES.MODE_CBC, iv)
            if encode == 'base64':
                plaintext = cryptor.decrypt(b64decode(cypher_text))
            elif encode == 'hex':
                plaintext = cryptor.decrypt(a2b_hex(cypher_text))
            else:
                plaintext = None
        elif captcha == 'cap':
            cryptor = AES.new('3jkd93mgtgsd4alb', AES.MODE_CBC, 'n8gf2joslrmcvnbq')
            if encode == 'base64':
                plaintext = cryptor.decrypt(b64decode(cypher_text))
            elif encode == 'hex':
                plaintext = cryptor.decrypt(a2b_hex(cypher_text))
            else:
                plaintext = None
        pad = plaintext[-1:]
        plaintext = self.urlDecode(plaintext.rstrip(pad))
        return plaintext

    def rsaDecrpt(self,msg):
        # 密文
        #msg = 'vEkVjsYPIoe3h+LBnvrHkyTwMrFy7kaoHlEUf2onXpnOdRdNS47NO8EnLTD+VWZIT/BYQuzNDYoljqEnQdiN5xCIKvvVkiccHR6t8JNgqaJcbIZukSB51Ajg577E/CNLvqbOqMjPh2IwyNjllNT9fzyh/XbWNQGzwpmBYhoAHe7rYylO9NIeVi3cP/PC6hVoTTzrrBJZsvVx887BAQLpSnCByl35JFMh9UZ77pUbyFDjiAIIewwzZ27fgpW1TgjhsQDmPgpZd5a8IKtMAGOx4hIxQKHOjruyinXlGvBno88lHpFZ8ALdIqqJXrb5Fiu707wV7i2VrPqrmDvBAb1jAv/Xd97Y+xl/su1LID7UWW9ub2qCEdUk+aX9D+Ls02hbQVIffZTvWC1jahBnWQU6NuDFPMA0stO5PrIkNh0/G/8DfuNhgB0txGDl4+I3cungJ/DOQphgrSCyzyatFSSTBcp4kK+xFiGLgpWrH9DUo9B9qU2pyTQRo9aRkmSSnzgMvkaM6RhqgJp4zh7xqps6HT2JHKwSBfR6cv/Ippn7W9GpCiVd7T5GqITUY3Kl+8Bqvttzv0jGMdeWSYwDK5VH8ksFz+Yfsom7O3nbWNkgrEp11PLuzE79ckHpYy1jdCbnlFGXqFR2npJbQHPthXZmYOlYnNyTW7eSGSdN5b0fO88='

        # base64解码
        msg = base64.b64decode(msg)
        # 获取私钥
        # privatekey = open('private_key.pem').read()

        # print (privatekey)
        pppp = '''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQBbrA8fqLh0JFLjxcASfW7wjTUiEST+ps2OE68+ZY193rGABIV/
MzQ/Y5zSHO8feN/1HMpVOHusTGtTH0FuXptrRUutyJywDS3G/la5+sdb8sBFxIOt
l8pW5ZL4S3xAwNqCY1EfOnaaL6zaM1+8Vhg9uxRdGhbU9ZgjgT4k9ATcP6K68R1I
uTE4COoI4CehDWUKpupFfQo3GQz/L+HQBRe1WwR/0DSpq8jGp8xZqhGEoxqZHRK8
SBXXfyhvSul4x8e8J5+A/ECdA6kcnmXimNNrWP4iO8wFrAcapW5mJjdBuSgX/Nlv
BFYy/otZb9IQYkb1kQSUxuVLOdvFOXtex1jNAgMBAAECggEADf9kw8nIeHt/aKYu
YORkRzjYjx4dDwE7S+F3lch95WVWpxyJodWYucElFfQzExQq5kuCHaclQzbcAHI6
VHb/tk57csq6Giu4/LSjW3yOalzTvRN3o88Up1YgrecgzuZjtxshLOqJZ5u2Ag9s
I97ljq99OYYdTGE/3NQEQDI+d77U3AtM296N3hFC2HJTumkC4PIE1358NHMdfXuy
iwLSj3sP5M2nXcyryuBV5Y3vxpZxanb9tO7R5fcUl99PbYin/Tz1B2O1VimkpfWV
EbjYeXXPghYHutbIKRr31nwdRRjcZJ51EfagXQjpmiLeRzZB3KgtENDnYbcvZtC+
+rLQpQKBgQCkjV1yUtWHtrWFGdIUmtx3HTx3SbGDV2Baxq7CHKYjjcKbef/QwrDN
OS+sv7oHhpBt6L7ugd3/PjpK3ZayWov28suzml21q+Qf9YCgS9KUlFvctVHJ5Jk7
mzFsEmaGpKUyugWFSyfCaasn7Tg5zlwsPuvNLeq1SNh+gwCH+9dIewKBgQCOniJK
W7IKI2+qKpsNgVMMbCBk+h+zG2V0Hh/cK+D5DwVHLlj+iM/PfHq9FmYXiZ4fWajc
x4MCcg1dGNtMDFmAxLrmpc0O2LFbx8QUjZe05LGJSphArkYCoVIQJ8zLUN2Vf6lc
xqyAC7RG7EtvlJBFdpzICwv4RpFT5Udo7MD1VwKBgQCQG+nRvG+a2k1gUrukJfec
LbONuLFImFYfSc802og5rOXY6eA6wLa8FDAHdyWBf7yvNN053exApAvDEwruCdR4
Iix5j2AwQWiZAJV0TNMQIlnNEdKeIKB+Di0bO4Yktr6ijT1WffpFDevCHMNYBLy+
VyCFYYgi2bgYG7x0Wv8wTwKBgAQwZudyPA+KLOx9peJGqy7ROj5dDnNPWbKIc/0e
mNQX+dq2ZMzNLfV1PZGyR7tnQmq/UnNxtMpsmTHj2gUo07Qxkx/VPOmzubntazgD
VLJuiTx0IXa857eKD4QD90L9lBShFFNyTnzQWzI+HJUhcv9nVYGWuXpIcFpbgLZ3
Rc+vAoGADpF8qIJXimzkimKj/rUId/4k0U3K4KxUmrkj4zMJVbIgZW1gAx8INy0/
Crk3TqBT7WQZT0w8nJp8YxgmSXndmLuF4WQ1+f3ty6YX7+IX4NlQn/ubyF0gmEuu
es9ruxt8kMcEO62DM6CbIbf9SFEq5tUIUzpSlvW53vhGwNWU6qQ=
        -----END RSA PRIVATE KEY-----'''
        print (pppp)
        rsakey = RSA.importKey(pppp)
        # 进行解密
        cipher = PKCS1_v1_5.new(rsakey)
        text = cipher.decrypt(msg, 'DecryptError')
        # 解密出来的是字节码格式，decodee转换为字符串
        print((text.decode()))
        print ('4231451352645773')
        return text.decode()

    def rsaServerPub(self, msg,skey):
        #msg = '{"key":"nTpUcgFRwVG8ld4nta823odiF8LzoAl5","iv":"sVp2W0cyOIzXTiHD"}'
        print (skey)
        pppp = '''-----BEGIN RSA PUBLIC KEY-----'''+'\n'+skey+'''-----END RSA PUBLIC KEY-----'''

        print(pppp)

        # 读取文件中的公钥
        # key = open('public_key.pem').read()
        print ('456')
        publickey = RSA.importKey(pppp)
        print ('123')
        # 进行加密
        pk = PKCS1_v1_5.new(publickey)
        print ('123456')
        encrypt_text = pk.encrypt(msg.encode())
        print ('123789')
        # 加密通过base64进行编码
        result = base64.b64encode(encrypt_text)
        print(result)
        return result
    def rsaServerPubn(self, msg,skey):
        #msg = '{"key":"nTpUcgFRwVG8ld4nta823odiF8LzoAl5","iv":"sVp2W0cyOIzXTiHD"}'
        print (skey)
        pppp = '''-----BEGIN RSA PUBLIC KEY-----'''+'\n'+skey+'\n'+'''-----END RSA PUBLIC KEY-----'''

        print(pppp)

        # 读取文件中的公钥
        # key = open('public_key.pem').read()
        print ('456')
        publickey = RSA.importKey(pppp)
        print ('123')
        # 进行加密
        pk = PKCS1_v1_5.new(publickey)
        print ('123456')
        encrypt_text = pk.encrypt(msg.encode())
        print ('123789')
        # 加密通过base64进行编码
        result = base64.b64encode(encrypt_text)
        print(result)
        return result
    def rsaClientPri(self,msg):
        #msg = '{"key":"nTpUcgFRwVG8ld4nta823odiF8LzoAl5","iv":"sVp2W0cyOIzXTiHD"}'
        pppp = '''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQBbrA8fqLh0JFLjxcASfW7wjTUiEST+ps2OE68+ZY193rGABIV/
MzQ/Y5zSHO8feN/1HMpVOHusTGtTH0FuXptrRUutyJywDS3G/la5+sdb8sBFxIOt
l8pW5ZL4S3xAwNqCY1EfOnaaL6zaM1+8Vhg9uxRdGhbU9ZgjgT4k9ATcP6K68R1I
uTE4COoI4CehDWUKpupFfQo3GQz/L+HQBRe1WwR/0DSpq8jGp8xZqhGEoxqZHRK8
SBXXfyhvSul4x8e8J5+A/ECdA6kcnmXimNNrWP4iO8wFrAcapW5mJjdBuSgX/Nlv
BFYy/otZb9IQYkb1kQSUxuVLOdvFOXtex1jNAgMBAAECggEADf9kw8nIeHt/aKYu
YORkRzjYjx4dDwE7S+F3lch95WVWpxyJodWYucElFfQzExQq5kuCHaclQzbcAHI6
VHb/tk57csq6Giu4/LSjW3yOalzTvRN3o88Up1YgrecgzuZjtxshLOqJZ5u2Ag9s
I97ljq99OYYdTGE/3NQEQDI+d77U3AtM296N3hFC2HJTumkC4PIE1358NHMdfXuy
iwLSj3sP5M2nXcyryuBV5Y3vxpZxanb9tO7R5fcUl99PbYin/Tz1B2O1VimkpfWV
EbjYeXXPghYHutbIKRr31nwdRRjcZJ51EfagXQjpmiLeRzZB3KgtENDnYbcvZtC+
+rLQpQKBgQCkjV1yUtWHtrWFGdIUmtx3HTx3SbGDV2Baxq7CHKYjjcKbef/QwrDN
OS+sv7oHhpBt6L7ugd3/PjpK3ZayWov28suzml21q+Qf9YCgS9KUlFvctVHJ5Jk7
mzFsEmaGpKUyugWFSyfCaasn7Tg5zlwsPuvNLeq1SNh+gwCH+9dIewKBgQCOniJK
W7IKI2+qKpsNgVMMbCBk+h+zG2V0Hh/cK+D5DwVHLlj+iM/PfHq9FmYXiZ4fWajc
x4MCcg1dGNtMDFmAxLrmpc0O2LFbx8QUjZe05LGJSphArkYCoVIQJ8zLUN2Vf6lc
xqyAC7RG7EtvlJBFdpzICwv4RpFT5Udo7MD1VwKBgQCQG+nRvG+a2k1gUrukJfec
LbONuLFImFYfSc802og5rOXY6eA6wLa8FDAHdyWBf7yvNN053exApAvDEwruCdR4
Iix5j2AwQWiZAJV0TNMQIlnNEdKeIKB+Di0bO4Yktr6ijT1WffpFDevCHMNYBLy+
VyCFYYgi2bgYG7x0Wv8wTwKBgAQwZudyPA+KLOx9peJGqy7ROj5dDnNPWbKIc/0e
mNQX+dq2ZMzNLfV1PZGyR7tnQmq/UnNxtMpsmTHj2gUo07Qxkx/VPOmzubntazgD
VLJuiTx0IXa857eKD4QD90L9lBShFFNyTnzQWzI+HJUhcv9nVYGWuXpIcFpbgLZ3
Rc+vAoGADpF8qIJXimzkimKj/rUId/4k0U3K4KxUmrkj4zMJVbIgZW1gAx8INy0/
Crk3TqBT7WQZT0w8nJp8YxgmSXndmLuF4WQ1+f3ty6YX7+IX4NlQn/ubyF0gmEuu
es9ruxt8kMcEO62DM6CbIbf9SFEq5tUIUzpSlvW53vhGwNWU6qQ=
                -----END RSA PRIVATE KEY-----'''
        print(pppp)


        # 读取文件中的公/私钥
        # key = open('public_key.pem').read()

        key = RSA.importKey(pppp)
        h = SHA256.new(msg)
        signer = Sig_PK.new(key)
        signature = signer.sign(h)
        result= base64.b64encode(signature)

        print (result)
        return result




        #5
        # private =RSA.importKey(pppp)
        # signature = Sig_pk.new(private)
        # hash_msg = SHA256.new(msg.encode("utf-8"))
        # signature_bytes = signature.sign(hash_msg)
        # signature_text = base64.b64encode((signature_bytes))
        # print signature_text
        # return signature_text

        #4
        # private = RSA.importKey(pppp)
        # signer = Sig_pk.new(private)
        # digest = SHA256.new(msg)
        # digest.update(msg)
        # sign =signer.sign(digest)
        # signature =base64.b64encode(sign)
        # print signature
        # return signature


        #3
        # private = RSA.importKey(pppp)
        # data =SHA256.new(msg.encode())
        # sign_pk =Sig_pk.new(private)
        # sign =sign_pk.sign(data)
        # result = base64.b64encode(sign)
        # data = result.decode()
        # print data
        # print '47239084709123'
        # return data

        #2
        # private = RSA.importKey(pppp)
        # pk = PKCS1_v1_5.new(private)
        # encrypt_text = pk.encrypt(msg.encode("utf-8"))
        # result =base64.b64encode(encrypt_text)
        # print (result)
        # return result


        # 进行加密
        # private = RSA.importKey(pppp)
        # pk = PKCS1_cipher.new(private)
        # rsa_text = base64.b64encode(pk.encrypt(bytes(msg.encode("utf8"))))
        # print(rsa_text.decode('utf-8'))
        # print '47239084709123'
        # return rsa_text.decode('utf-8')

        #1
        # pk = PKCS1_v1_5.new(private)
        # encrypt_text = pk.encrypt(msg.encode())
        # # 加密通过base64进行编码
        # result = base64.b64encode(encrypt_text)
        # print(result)
        #         # return result



    def urlEncode(self, text):
        return self.urlEncodePyToNet(quote_plus(text))

    def urlDecode(self, text):
        #if type(text) == type(b'xx'):
        #    return unquote_plus(text.decode("utf-8"))
        #else:
        #    return unquote_plus(text)
        return unquote_plus(text)

    def __pkcs7Padding(self, text):
        block_size = 16
        count = len(text)
        pad = block_size - (count % block_size)
        print (pad)
        text += (chr(pad) * pad)
        return text

    def __pkcs5Padding(self, text):
        block_size = 8
        count = len(text)
        pad = block_size - (count % block_size)
        print (pad)
        text += (chr(pad) * pad)
        return text

    def postRequestToAPI(self, session_obj, request_dict, api_url, is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type':'application/x-www-form-urlencoded'}
        sess = session_obj
        if is_json is False:
            payload = urlencode(request_dict)
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
                
            #req = requests.post(api_url, data=payload, headers=header)
            req = sess.post(api_url, data=payload, headers=header)
            print((req.status_code))
            return req.content


    def postRequestToAPIb2cL(self, session_obj, request_dict, api_url, is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json'}
        sess = session_obj
        if is_json is False:
            payload = urlencode(request_dict)
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            print (request_dict)
            print((json.dumps(request_dict)))
            req = sess.post(api_url, data=json.dumps(request_dict, separators=(',', ':')), headers=header)
            print((req.status_code))
            return req.content


    def postRequestToAPIj(self, session_obj, request_dict, api_url, is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json'}
        sess = session_obj
        if is_json is False:
            payload = urlencode(request_dict)
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)

            # req = requests.post(api_url, data=payload, headers=header)
            req = sess.post(api_url, data=payload, headers=header)
            print((req.status_code))
            return req.content

    def postRequestToAPIforShopify(self, session_obj, request_dict, api_url, is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json'}
        sess = session_obj
        if is_json is False:
            # payload = urllib.urlencode(request_dict)
            # if trencode_dotnet is True:
            #     payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            print (request_dict)
            print((json.dumps(request_dict, separators=(',', ':')).replace(' ','')))
            req = sess.post(api_url, data=json.dumps(request_dict, separators=(',', ':')).replace(' ',''), headers=header)
            print((req.status_code))
            return req.content

    def postRequestToAPIforWordSettingNumber(self, session_obj, request_dict, api_url, is_json=False, trencode_dotnet=False):
            ret_dic = {}
            header = {'Content-Type': 'application/json'}
            sess = session_obj
            if is_json is False:
                # payload = urllib.urlencode(request_dict)
                # if trencode_dotnet is True:
                #     payload = self.urlEncodePyToNet(payload)
                # req = requests.post(api_url, data=payload, headers=header)
                print (request_dict)
                print((json.dumps(request_dict, separators=(',', ':')).replace(' ', '')))
                req = sess.post(api_url, data=json.dumps(request_dict, separators=(',', ':')).replace(' ', ''),
                                headers=header)
                print((req.status_code))
                return req.content

    def postRequestToAPIb2c(self, session_obj, request_dict, api_url, is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json'}
        sess = session_obj
        if is_json is False:
            payload = urlencode(request_dict)
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            #print (json.dumps(request_dict))
            req = sess.post(api_url, data=json.dumps(request_dict, cls=MyEncoder, separators=(',', ':')), headers=header)
            print((req.status_code))
            return req.content

    def postRequestToAPIb2cNoheader(self, session_obj, request_dict, api_url,domain,id,version, is_json=False, trencode_dotnet=False):
        ret_dic = {}
        print ('5223452')
        header = {'Content-Type': 'application/json', 'Shopify-Shop-Domain': domain, 'Shopify-Request-Id': id, 'Shopify-Api-Version': version}
        print ('5223452')
        #header = {'Content-Type': 'application/json'}
        sess = session_obj
        if is_json is False:
            payload = urlencode(request_dict)
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            print (request_dict)
            print((json.dumps(request_dict)))
            req = sess.post(api_url, data=json.dumps(request_dict, separators=(',', ':')), headers=header)
            print((req.status_code))
            return req.content

    def postRequestToAPIb2c2(self, session_obj, request_dict, api_url, is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json'}
        sess = session_obj
        if is_json is False:
            payload = urlencode(request_dict)
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            print (request_dict)
            print((json.dumps(request_dict)))
            req = sess.post(api_url, data=json.dumps(request_dict, separators=(',', ':')), headers=header)
            print((req.status_code))
            return req.content
    def postRequestToAPIkeyexchange(self, session_obj, request_dict, api_url, UUID,AppName,AppInfo,is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json','UUID':UUID,'AppName':AppName,'AppInfo':AppInfo}
        sess = session_obj
        if is_json is False:
            #payload = urllib.urlencode(request_dict)
            payload = request_dict
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            print (request_dict)
            print((json.dumps(request_dict)))
            req = sess.post(api_url, data=request_dict, headers=header)
            print((req.status_code))
            print((req.headers))
            ddd={}
            ddd['header']=req.headers
            ddd['content']=req.content
            return ddd
    def postRequestToAPIQuery(self, session_obj, request_dict, api_url, UUID,AppName,AppInfo,KeyInfo,Signature,KeyID,is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json','UUID':UUID,'AppName':AppName,'AppInfo':AppInfo,'KeyInfo':KeyInfo,'Signature':Signature,'KeyID':KeyID}
        sess = session_obj
        if is_json is False:
            #payload = urllib.urlencode(request_dict)
            payload = request_dict
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            print (request_dict)
            print (header)
            req = sess.post(api_url, data=request_dict, headers=header)
            print((req.status_code))
            return req.content
    def postRequestToAPIQueryL(self, session_obj, request_dict, api_url,Language,UUID,AppName,AppInfo,KeyInfo,Signature,KeyID,is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json','Language':Language,'UUID':UUID,'AppName':AppName,'AppInfo':AppInfo,'KeyInfo':KeyInfo,'Signature':Signature,'KeyID':KeyID}
        sess = session_obj
        if is_json is False:
            #payload = urllib.urlencode(request_dict)
            payload = request_dict
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            print (request_dict)
            print (header)
            req = sess.post(api_url, data=request_dict, headers=header)
            print((req.status_code))
            print((req.headers))
            print((req.content))
            return req
    def postRequestToAPIQueryQ(self, session_obj, request_dict, api_url,Language,UUID,AppName,AppInfo,KeyInfo,Signature,KeyID,is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json','Language':Language,'UUID':UUID,'AppName':AppName,'AppInfo':AppInfo,'KeyInfo':KeyInfo,'Signature':Signature,'KeyID':KeyID}
        sess = session_obj
        if is_json is False:
            #payload = urllib.urlencode(request_dict)
            payload = request_dict
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            print (request_dict)
            print (header)
            req = sess.post(api_url, data=request_dict, headers=header)
            print((req.status_code))
            print((req.headers))
            return req.content
    def postRequestToAPIThreeD(self, session_obj, request_dict, api_url, is_json=False, trencode_dotnet=False):
        ret_dic = {}
        header = {'Content-Type': 'application/json'}
        sess = session_obj
        if is_json is False:
            payload = urlencode(request_dict)
            if trencode_dotnet is True:
                payload = self.urlEncodePyToNet(payload)
            # req = requests.post(api_url, data=payload, headers=header)
            print (request_dict)
            print((json.dumps(request_dict)))
            req = sess.post(api_url,data=json.dumps(request_dict, separators=(',', ':')), headers=header)
            print((req.status_code))
            return req.content
    def getRequestFromAPI(self, request_dict, api_url):
        print(api_url)
        req = requests.get(api_url, params=request_dict, timeout=5)
        return req.text

    def returnBodyToDic(self, rtn_body):
        print((rtn_body, type(rtn_body)))
        rtn_list = rtn_body.decode().split('&')
        rdict = {x.split('=')[0] : x.split('=')[1] for x in rtn_list} 
        return rdict
    def returnBodyToDicb2c(self, rtn_body):
        rtn_body=rtn_body.replace('{','').replace('}','').replace('"','').replace('Items:[','').replace(']','').replace('[','').replace(' ','').replace('Items:','')
        #print rtn_body
        rtn_list = rtn_body.split(',')
        print (rtn_list)
        rdict = {x.split(':')[0] : x.split(':')[1] for x in rtn_list}
        #print rdict
        return rdict
    def returnBodyToDicb2cA(self, rtn_body):
        rtn_body=rtn_body.replace('{','').replace('}','').replace('"','').replace('Items:[','').replace(']','').replace('[','').replace(' ','').replace('Items:','').replace('AllowanceInfo:','')
        #print rtn_body
        rtn_list = rtn_body.split(',')
        print (rtn_list)
        rdict = {x.split(':')[0] : x.split(':')[1] for x in rtn_list}
        #print rdict
        return rdict
    def returnBodyToDicb2c2(self, rtn_body):
        rtn_body=rtn_body.replace('{','').replace('}','').replace('"','')
        #print rtn_body
        rtn_list = rtn_body.split(',')
        print (rtn_list)
        rdict = {x.split(':')[0] : x.split(':')[1] for x in rtn_list}
        #print rdict
        return rdict
    def returnBodyToDicb2b(self, rtn_body):
        rtn_body = rtn_body.replace('{', '').replace('}', '').replace('"', '').replace('Items:[', '').replace(']',
                                                                                                              '').replace(
            '[', '').replace(' ', '').replace('Items:', '')
        # print rtn_body
        rtn_list = rtn_body.split(',')
        print (rtn_list)
        rdict = {x.split(':')[0]: x.split(':')[1] for x in rtn_list}
        # print rdict
        return rdict
    def returnBodyToDicb2b2(self, rtn_body):
        rtn_body = rtn_body.replace('{', '').replace('}', '').replace('"', '').replace(']','').replace('[', '').replace(' ', '').replace('RtnData:', '')
        # print rtn_body
        rtn_list = rtn_body.split(',')
        print (rtn_list)
        rdict = {x.split(':')[0]: x.split(':')[1] for x in rtn_list}
        # print rdict
        return rdict
    def verifyRtnData(self, ret_dat, expect_val_dic, re_match_dict={}, datatype='addr_option'):
        result = {}
        if datatype is 'addr_option':
            rtn_body_dic = self.returnBodyToDic(ret_dat)
        elif datatype is 'dictionary':
            rtn_body_dic = ret_dat



        print (ret_dat)
        print (rtn_body_dic)
        ans_keys = list(expect_val_dic.keys())
        sample_dic = {}
        for key in ans_keys:
            sample_dic[key] = rtn_body_dic[key]
        if expect_val_dic == sample_dic:
            result['FixValueCompare'] = True
        else:
            self.log.WARN("Return string comparing not match, return body : %s \n Sample Dict : %s \n Expected Dict: %s." % (rtn_body_dic, sample_dic, expect_val_dic))
            result['FixValueCompare'] = False
            
        if len(re_match_dict) > 0:
            unmatch = {}
            key_for_match = list(re_match_dict.keys())
            for key in key_for_match:
                pattern = re_match_dict[key]
                value = rtn_body_dic[key]
                match = re.search(pattern, value)
                if match is not None:
                    self.log.INFO("Matching return data '%s' (value: %s) success with regex pattern '%s', matched result : %s." % (key, value, pattern, match.group()))
                else:
                    self.log.WARN("Matching return data '%s' (value: %s) Fail with regex pattern '%s'" % (key, value, pattern))
                    unmatch[key] = (value, pattern)
            if len(unmatch) > 0:
                result['RegexMatching'] = False
            elif len(unmatch) == 0:
                result['RegexMatching'] = True
                self.log.INFO("All regex matching correct.")
                
        all_res = list(result.values())
        #if all_res.__contains__(False):
        if False in all_res:
            return False
        else:
            return True
                    
            
    

class HtmlHelper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tags = []
        self.urljoin = urllib.parse.urljoin
        
    def clearCurrentTag(self):
        self.tags = []
        
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        tag_info = [tag, attr_dict]
        self.tags.append(tag_info)

    def handle_endtag(self, tag):
        tag_info = [tag, {'Ending':True}]
        self.tags.append(tag_info)
    
    def retrieve_FormTag(self):
        form_grp = {}
        form_elems = []
        curr_form = ''
        for t in self.tags:
            tag_attr = t[1]
            if t[0] == 'form' and list(tag_attr.keys()).__contains__('Ending') is False:
                if list(tag_attr.keys()).__contains__('id') is True:
                    curr_form = tag_attr['id']
                elif list(tag_attr.keys()).__contains__('action') is True:
                    curr_form = tag_attr['action']
                form_act = tag_attr['action']
            elif t[0] == 'input' and list(tag_attr.keys()).__contains__('Ending') is False:
                if curr_form != '':
                    form_elems.append(tag_attr)
                    #print tag_attr
            elif t[0] == 'form' and list(tag_attr.keys()).__contains__('Ending') is True:
                form_grp[curr_form] = {'Elems':form_elems, 'Action':form_act}
                curr_form = ''
                form_elems = []
        print(('Number of form found:', len(form_grp)))
        forms = list(form_grp.keys())
        for fo in forms:
            print(('%s' % (fo), len(form_grp[fo])))
        return form_grp
    
    def formToPOSTDict(self, formident):
        forms_dict = self.retrieve_FormTag()
        if list(forms_dict.keys()).__contains__(formident) is True:
            form = forms_dict[formident]
            args = form['Elems']
            res = collections.OrderedDict()
            #res = {}
            for a in args:
                if list(a.keys()).__contains__('value') is False:
                    val = ''
                else:
                    val = a['value']
                    
                keyn = a['name']
                res[keyn] = val
                print (res)
            return res
        else:
            raise ValueError('formToPOSTDict: Specified Form identifier not found in source html.')
                    
    def getFormAct(self, formident, urlroot=''):
        forms_dict = self.retrieve_FormTag()
        if list(forms_dict.keys()).__contains__(formident) is True:
            form = forms_dict[formident]
            action = form['Action']
            if action.startswith('http') is False and urlroot is not '':
                action = self.urljoin(urlroot, action)
            elif action.startswith('http') is True and urlroot is not '':
                raise ValueError('formToPOSTDict: urlroot is specified on an action begin with "http".') 
            return action
        else:
            raise ValueError('formToPOSTDict: Specified Form identifier not found in source html.')        

              
        
                
