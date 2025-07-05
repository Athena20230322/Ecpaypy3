# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import requests
import LibGeneral.funcGeneral
from LibGeneral.AddLog import dummyLog
from appium import webdriver
from appium.webdriver.webdriver import TouchAction
import re
from selenium.common import exceptions
from urllib.error import URLError
import xml.etree.cElementTree as cxml



class ClassMobileOperate():
    
    def __init__(self, deviceInfo, platform, app_pkg, app_act):

        self.desire_cap = {}
        self.desire_cap['platformName'] = platform
        self.desire_cap['platformVersion'] = '6.0'
        self.desire_cap['deviceName'] = deviceInfo
        #desire_cap['app'] = 'D:\\PyScripts\\Mobile\\AllPay.apk'
        self.desire_cap['appPackage'] = app_pkg
        #desire_cap['appPackage'] = 'com.allpay.tw'
        self.desire_cap['appActivity'] = app_act
        
        self.cellphone_no = '0963957452'
        
        self.genFunc = LibGeneral.funcGeneral
        self.otp_collect_srv = 'http://192.168.150.131:443'
        try:
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desire_cap)
        except URLError:
            print("Connect fail to Appium server.")
            raise URLError("Connect fail to Appium server.")
        else:
            pass
        self.touch = TouchAction(self.driver)
        self.NoElemEcpt = exceptions.NoSuchElementException
        time.sleep(5)
        self._logger = dummyLog()

    @property    
    def logger(self):
        return self._logger
    
    @logger.setter
    def logger(self, logobj):
        self._logger = logobj
    
    def initAndroidENV(self):
        self.desire_cap = {}
        self.desire_cap['platformName'] = 'Android'
        self.desire_cap['platformVersion'] = '6.0'
        #desire_cap['deviceName'] = 'EP7328J4HM'
        self.desire_cap['deviceName'] = 'RQ3000GT7X'
        self.desire_cap['app'] = 'D:\\PyScripts\\Mobile\\AllPay.apk'
        self.desire_cap['appPackage'] = 'com.allpay.tw'
        self.desire_cap['appActivity'] = '.Splash'


        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desire_cap)
        
    def driverReset(self):
        #self.driver.close()
        self.driver.quit
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desire_cap)
            
    def tearDown(self):
        #Quit Driver
        self.driver.quit()
        #Kill specific server process
        
    def findAppElem(self, ident, by, ignore_nfind=False):
        try:
            if by == 'id':
                elem = self.driver.find_element_by_id(ident)
            elif by == 'text':
                elem = self.driver.find_element_by_link_text(ident)
            elif by == 'name':
                elem = self.driver.find_element_by_name(ident)
        except self.NoElemEcpt:
            if ignore_nfind is True:
                return False
            else:
                raise self.NoElemEcpt
        else:
            return elem
            
            
    def findMultiAppElem(self, ident, by, ignore_nfind=False):
        try:
            if by == 'id':
                elem = self.driver.find_elements_by_id(ident)
            elif by == 'text':
                elem = self.driver.find_elements_by_link_text(ident)
            elif by == 'name':
                elem = self.driver.find_elements_by_name(ident)
            elif by == 'class':
                elem = self.driver.find_elements_by_class_name(ident)
        except self.NoElemEcpt:
            if ignore_nfind is True:
                return False
            else:
                raise self.NoElemEcpt
        else:
            return elem        
        
        
    def clickAppElement(self, By, ident):
        
        avaliable_by_arg = (
            'id',
            'text'
            )
        
        argchk = self.genFunc.chkTupleElem(avaliable_by_arg, By)
        
        if argchk:
                
            if By == 'id':
                self.driver.find_element_by_id(ident).click()
            elif By == 'text':
                self.driver.find_elements_by_link_text(ident).click()
                
        else:
            raise ValueError('clickAppElement : find BY argument error')
        
    def handleOTPSMS(self, xmlpath, usage='Unspecified_Usage'):

        xtree = cxml.parse(xmlpath)
        xroot = xtree.getroot()
        for ph in xroot.iter('phone'):
            phone_no = ph.attrib['number']
            match_msg_grp = self.findAppElem(phone_no, 'name', ignore_nfind=True)
            if match_msg_grp is not False:
                match_msg_grp.click()
                catagories = ph.iter('Catagory')
                
                relat_content = [x.text for x in ph.iter('MsgPattern')]
                
                msgs = self.findMultiAppElem('com.sonyericsson.conversations:id/message_item', 'id', ignore_nfind=True)
                if msgs is not False:
                    # print len(msgs)
                    for m in msgs:
                        post_dict = {}
                        post_dict['TEL'] = self.cellphone_no
                        try:
                            container = m.find_element_by_id('com.sonyericsson.conversations:id/message_item_body_text')
                        except Exception:
                            # print "message_item_body_text not found"
                            pass
                        for cat in catagories:
                            msg_patt = cat.find('MsgPattern').text
                            msg_cat = cat.attrib['value']
                            msg_tgt_patt = cat.find('InfoPattern').text
                            criteria = re.compile(msg_patt)
                            match = criteria.findall(container.text)
                            if match:
                                post_dict['OTPUsage'] = msg_cat
                                tgt_cri = re.compile(msg_tgt_patt)
                                tgt_mat = tgt_cri.findall(container.text)
                                if len(tgt_mat) == 1:
                                    tgt_mat = tgt_mat[0]
                                elif len(tgt_mat) == 0:
                                    tgt_mat = 'NOT_FOUND'
                                elif len(match) > 1:
                                    tgt_mat = 'MULTIPLE_MATCH'
                                post_dict['Passcode'] = tgt_mat
                                print(post_dict)
                                try:
                                    json_payload = json.dumps(post_dict, sort_keys=True, indent=4, separators=(',', ': '))
                                    requests.post(self.otp_collect_srv, json=post_dict)
                                except Exception as err:
                                    print(err.message)
                                else:
                                    self.touch.long_press(container).release().perform()
                                    del_btn = '刪除訊息'
                                    options = self.findMultiAppElem('android.widget.LinearLayout', 'class')
                                    for opt in options:
                                        txt = opt.find_element_by_id('android:id/title').text
                                        #print repr(txt)
                                        #print repr(del_btn)
                                        if txt == del_btn:
                                            opt.click()
                                            accept_btn = self.findAppElem('android:id/button1', 'id')
                                            accept_btn.click()
                                            break
                                self.driver.back()
                                break
                        break
                                #self.driver.back()
                    #self.driver.back()

        #self.driver.close()            
        

#mobile = ClassMobileOperate('RQ3000GT7X', 'Android', 'com.sonyericsson.conversations', '.ui.ConversationListActivity')
#i = 0
#while i == 0:
    ##mobile.handleOTPSMS('D:\QA\AutoTest\Utility\OTPCollector\smsconf.xml')
    #try:
        #mobile.handleOTPSMS('D:\QA\AutoTest\Utility\OTPCollector\smsconf.xml')
    #except Exception as err:
        #print "Error occurs"
        #print err.message
    #time.sleep(2)

