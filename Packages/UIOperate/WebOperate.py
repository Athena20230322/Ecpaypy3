import urllib.request, urllib.parse, urllib.error
from base64 import b64decode
from binascii import a2b_hex
from selenium.webdriver.common.by import By

import selenium.webdriver as webdriver
import selenium.webdriver.common.alert as WEBALERT
import SeleniumHelper.SeleniumHelper as SHELPER
import CaptchaResolve.CaptchaResolve as CAPRE
from Crypto.Cipher import AES
from selenium.webdriver import ActionChains
import selenium.webdriver.support.expected_conditions as EXPD_COND
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import unquote_plus
import LibGeneral.GetConfigValue as getConf
import LibGeneral.funcGeneral as funcGen
import time
import os


class webOperate():
    def __init__(self, drv):
        self.conf = getConf.getConfig()
        self.rootdir = self.conf.getRootDir() 
        self.drv = drv
        self.drv_wait = webdriver.support.ui.WebDriverWait
        self.select = webdriver.support.ui.Select
        self.alert = WEBALERT.Alert(self.drv)
        self.origin_handle = self.drv.window_handles[0]
        self.except_noelem = NoSuchElementException

        
    def goToURL(self, url):
        self.drv.get(url)
    
    def getElem(self, elem_ident, find_by='id'):
        if find_by == 'id':
            #elem = self.drv.find_element_by_id(elem_ident)
            elem = self.drv.find_element(By.ID, elem_ident)
        elif find_by == 'class':
            elem = self.drv.find_element_by_class_name(elem_ident)
        elif find_by == 'css':
            elem = self.drv.find_element_by_css_selector(elem_ident)
        elif find_by == 'xpath':
            elem = self.drv.find_element(By.XPATH, elem_ident)
        elif find_by == 'tag':
            elem = self.drv.find_element_(By.TAG_NAME,elem_ident)
        elif find_by == 'name':
            elem = self.drv.find_element_by_name(elem_ident)
        elif find_by == 'text':
            elem = self.drv.find_element_by_link_text(elem_ident)
        else:
            err_msg = "getElem: Specified 'findby' argument is not correct."
            raise ValueError(err_msg)
        if elem.location != None:
            return elem
        else:
            return False
        
    def getSubElem(self, elem, elem_ident, find_by='id'):
        if find_by == 'id':
            #elem = elem.find_element_by_id(elem_ident)
            elem = elem.find_element(By.ID, elem_ident)
        elif find_by == 'class':
            elem = elem.find_element_by_class_name(elem_ident)
        elif find_by == 'css':
            elem = elem.find_element_by_css_selector(elem_ident)
        elif find_by == 'xpath':
            elem = elem.find_element(By.XPATH, elem_ident)
        elif find_by == 'tag':
            elem = elem.find_element_(By.TAG_NAME,elem_ident)
        elif find_by == 'name':
            elem = elem.find_element_by_name(elem_ident)
        elif find_by == 'text':
            elem = elem.find_element_by_link_text(elem_ident)            
        else:
            err_msg = "getSubElem: Specified 'findby' argument is not correct."
            raise ValueError(err_msg)
        return elem
        
        
    def getMultipleElem(self, elem_ident, find_by='id'):
        if find_by == 'id':
            elem = self.drv.find_elements_by_id(elem_ident)
        elif find_by == 'class':
            elem = self.drv.find_elements_by_class_name(elem_ident)
        elif find_by == 'css':
            elem = self.drv.find_elements_by_css_selector(elem_ident) 
        elif find_by == 'text':
            elem = self.drv.find_elements_by_link_text(elem_ident) 
        elif find_by == 'tag':
            elem = self.drv.find_elements_by_tag_name(elem_ident)        
        else:
            err_msg = "getMultipleElem: Specified 'findby' argument is not correct."
            raise ValueError(err_msg)
        
    def getMultipleSubElems(self, elem, elem_ident, find_by='id'):
        if find_by == 'id':
            elem = elem.find_elements_by_id(elem_ident)
        elif find_by == 'class':
            elem = elem.find_elements_by_class_name(elem_ident)
        elif find_by == 'css':
            elem = elem.find_elements_by_css_selector(elem_ident)
        elif find_by == 'xpath':
            elem = elem.find_elements_by_xpath(elem_ident)
        elif find_by == 'tag':
            elem = elem.find_elements_by_tag_name(elem_ident)
        elif find_by == 'name':
            elem = elem.find_elements_by_name(elem_ident)
        elif find_by == 'text':
            elem = elem.find_elements_by_link_text(elem_ident)            
        else:
            err_msg = "getSubElem: Specified 'findby' argument is not correct."
            raise ValueError(err_msg)
        return elem

    def maximizeWindow(self):
        self.drv.maximize_window()

    def executeScript(self, script):
        self.drv.execute_script(script)
    
    def inputTextBox(self, elem_identifer, value, findby='id'):
        element = self.getElem(elem_identifer, findby)
        if element is not False:
            element.send_keys(value)
        
    def clickElem(self, elem_identifer, findby='id'):
        element = self.getElem(elem_identifer, findby)
        if element is not False:
            #self.drv.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
            element.click()

    def resolveLoginCaptcha(self, login_cap_ident):
        cap_re = CAPRE.DBC()
        
        captcha = self.getElem(login_cap_ident)
        cap_guid = captcha.get_attribute('value')
        img_elem = self.getElem(cap_guid)
    
        helper = SHELPER.clsWebDriverHelper
        png_container = os.path.join(self.rootdir, 'Tmp')
        capt = helper.genElemScreenshot(helper(), self.drv, img_elem, png_container)  
        i = 0
        while i < 3:
            out = cap_re.resolveFile(capt)
            if out == None or out == '':
                i += 1
            else:
                break
        return out
    
    def resolveCaptchaElem(self, elem):
        cap_re = CAPRE.DBC()
        helper = SHELPER.clsWebDriverHelper
        png_container = os.path.join(self.rootdir, 'Tmp')
        capt = helper.genElemScreenshot(helper(), self.drv, elem, png_container)  
        i = 0
        while i < 3:
            out = cap_re.resolveFile(capt)
            if out == None or out == '':
                i += 1
            else:
                break
        return out        
    
    def mouseHoverElem(self, element, x_offset=0, y_offset=0):
        
        # element = self.getElem(elem_ident, findby)
        hover = ActionChains(self.drv).move_to_element_with_offset(element, x_offset, y_offset)
        hover.perform()
        time.sleep(2)
        
    def handleAlert(self, msg=None, action='Accept'):
        print ("HANDLE ALERT")
        try:
            self.drv_wait(self.drv, 1).until(EXPD_COND.alert_is_present())
            
        except TimeoutException:
            return 'No_Alert'
        else:
            page_alert = self.alert
            if msg is None:
                pass
            else:
                alert_text = page_alert.text
                if msg == alert_text:
                    pass
                else:
                    return 'Text_Not_Match'
            
            if action == 'Accept':
                page_alert.accept()
                return True
            elif action == 'Dismiss':
                page_alert.dismiss()
                return True
                
    def filterElemsByAttr(self, elems, criteria, attr='value', partial=False):
        if partial is False:
            res_elems = [x for x in elems if x.get_attribute(attr) == criteria]
        elif partial is True:
            res_elems = []
            for x in elems:
                if x.get_attribute(attr) is not None and str(x.get_attribute(attr)).__contains__(criteria) is True:
                    res_elems.append(x)
        return res_elems

    def getElemDisplayStat(self, elem_ident, find_by='id', parent_elem=None, ignore_nfound=False):
        try:
            if parent_elem is None:
                style_str = self.getElem(elem_ident, find_by).get_attribute('style')
            else:
                style_str = self.getSubElem(parent_elem, elem_ident, find_by).get_attribute('style')
        except Exception:
            if ignore_nfound is True:
                return False
            elif ignore_nfound is False:
                raise NoSuchElementException("getElemDisplayStat: Elem not found")
        else:
            style_dict = funcGen.resolveElemStyle(style_str)
            return style_dict['display']
    
    def operateCalendar(self, date_list):
        year = date_list[0]
        month = date_list[1]
        day = date_list[2]
        iframe = self.getElem('iframe', 'tag')
        print (iframe)
        time.sleep(1)
        self.drv.switch_to.frame(iframe)
        calendar = self.getElem('div.wdatediv', 'css')
        input_boxes = calendar.find_elements_by_css_selector('input.yminput')
        for box in input_boxes:
            box.click()
            time.sleep(1)
            monthmenu_setting = self.getElemDisplayStat('div.menusel.mmenu', find_by='css', parent_elem=calendar)
            
            if monthmenu_setting == 'block':
                # send month value
                box.send_keys(month)
            elif monthmenu_setting == 'none':
                # send year
                box.send_keys(year)

        td_elems = self.getMultipleSubElems(calendar, 'td', find_by='tag')
        
        close_ylist_attr = 'hide($d.yD);$d.yI.blur();'
        close_btn = [x for x in td_elems if x.get_attribute('onmousedown') == close_ylist_attr]
        close_btn[0].click()
        
        day_attr = "day_Click(%s,%s,%s);" % (year, month, day)
        es = [x for x in td_elems if x.get_attribute('onclick') == day_attr]
        es[0].click()
        self.drv.switch_to_window(self.origin_handle)

    def selectDropboxList(self, select_by, val, elem_ident, find_by='id'):
        drop_list = self.getElem(elem_ident, find_by)
        sel_list = self.select(drop_list)
        if select_by == 'text':
            sel_list.select_by_visible_text(val)
        elif select_by == 'value':
            sel_list.select_by_value(val)
        elif select_by == 'index':
            sel_list.select_by_index(val)
        else:
            raise ValueError("selectDropboxList : Unknown select_by argument recieved. Current argument: %s" % (select_by))
    
    def getDropboxItems(self):
        pass
    
    def formElemToDict(self, elem):
        #inps = elem.find_elements_by_tag_name('input')
        inps = elem.find_elements(By.TAG_NAME, "input")


        return_dict = {}
        for i in inps:
            input_name = i.get_attribute('name')
            input_value = i.get_attribute('value')
            if input_value is None:
                input_value = ''
            return_dict[input_name] = input_value
        return return_dict

    def ElemisDisplay(self, elem, find_by='id'):
        if find_by == 'id':
             return self.drv.find_element(By.ID,elem).is_displayed()
        elif find_by == 'css':
            return self.drv.find_element_by_css_selector(elem).is_displayed()

    def ElemisExist(self, elem, find_by='id'):
        try:
            self.drv.find_element(By.ID, elem)
            return True
        except NoSuchElementException:
            print(('Element not exists : "%s" .' % elem))
            return False

    def changeFrame(self):
        iframe = self.getElem('iframe', 'tag')
        print (iframe)
        time.sleep(1)
        self.drv.switch_to.frame(iframe)

    def changetab(self, tab):
        self.drv.switch_to_window(self.drv.window_handles[tab])

    def getElemValue(self, elem, find_by='id'):
        return self.drv.find_element(By.ID,elem).get_attribute('value')

    def urlDecode(self, text):
        return unquote_plus(text)

    def resolveSMSAuthCode(self, sms_auth_code):
        out = self.aesDecrypt(sms_auth_code)
        print (out)
        out = out[:4]
        return out

    def aesDecrypt(self, cypher_text, encode='base64'):
        cryptor = AES.new(b'ezquL9eE4hivNCdM', AES.MODE_CBC, b'QHyU6o2dKdUz4zhD')
        if encode == 'base64':
            plaintext = cryptor.decrypt(b64decode(cypher_text)).decode("utf-8") 
        elif encode == 'hex':
            plaintext = cryptor.decrypt(a2b_hex(cypher_text))
        else:
            plaintext = None
        pad = plaintext[-1:]
        plaintext = self.urlDecode(plaintext.rstrip(pad))
        return plaintext

