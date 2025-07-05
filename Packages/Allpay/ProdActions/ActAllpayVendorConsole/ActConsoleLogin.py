# -*- coding: utf-8 -*-

from UIOperate.WebOperate import webOperate
import LibGeneral.TestHelper as Thelper
import LibGeneral.funcGeneral as funcGen
import LibGeneral.GetConfigValue as getConf
import time
import os
import sys
import re


class actConsoleLogin(webOperate):
    def __init__(self, drv, log_file):
        webOperate.__init__(self, drv)

        self.conf = getConf.getConfig()
        self.rootdir = self.conf.getRootDir()        
        self.login_elem_list = os.path.join(self.rootdir, 'Conf', 'Element_Corresponding', 'AllpayVendorConsole', 'ConsoleLogin.csv')

        self.helper = Thelper.classTestHelper(log_file)
        self.feature_conf = self.helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayVendorConsole', feature_name='ConsoleLogin')
        self.login_url = self.feature_conf['ConsoleAddr']
        self.login_identds = self.helper.generateElemDataset(self.login_elem_list)
        
    def generalLogin(self, usrn, passwd):
        
        get_ident = self.helper.getElemIdentFromDataSet
        ids = self.login_identds
        
        i = 0
        while i < 3:
            print("HANDLER:before",  self.drv.window_handles)
            self.goToURL(self.login_url)

            print("HANDLER:after",  self.drv.window_handles)
            self.inputTextBox(get_ident('Login_username', ids)['Identifier'], usrn)
            self.inputTextBox(get_ident('Login_password', ids)['Identifier'], passwd)
            capt_answer = self.resolveLoginCaptcha('_mvcCaptchaGuid')
            self.inputTextBox(get_ident('Captcha_answer', ids)['Identifier'], capt_answer)
            self.clickElem(get_ident('Submit_login_button', ids)['Identifier'])
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

    def goToCreditDetail(self):
        self.goToURL('https://creditvendor.allpay.com.tw/DumpAuth/Query')

    def abandCreditPayToday(self):
        abandoned_tid = []
        btn_value = '放棄'
        self.clickElem('btnQuery')
        time.sleep(3)
        query_result = self.getElem('queryResult')
        form_elems = self.getMultipleSubElems(query_result, 'form', find_by='tag')
        if form_elems is not None:
            for f in form_elems:
                act = f.get_attribute('action')
                print(act)
                if act.__contains__('/DumpAuth/AuthAbandon'):
                    subelems = self.getMultipleSubElems(f, 'input', find_by='tag')
                    for sub in subelems:
                        #credit_tid = ''
                        elem_val = sub.get_attribute('value')
                        print(elem_val)
                        print(sub.get_attribute('name'))
                        if sub.get_attribute('name') == 'TradeID':
                            credit_tid = sub.get_attribute('value')
                        if sub.get_attribute('type') == 'submit' and elem_val == btn_value:
                            #sub.click()
                            abandoned_tid.append(credit_tid)
                            #self.handleAlert()
        else:
            raise self.except_noelem('abandCreditPayToday: No form element found.')
        return abandoned_tid
        
    def retrieveTradeStat(self, tid_list):
        tradelinks = []
        trade_result = {}
        qresult = self.getElem('queryResult')
        tb = self.getSubElem(qresult, 'table', find_by='tag')
        print("table:" ,tb)
        links = self.getMultipleSubElems(tb, 'dialogBlock', find_by='class')
        for l in links:
            if tid_list.__contains__(l.text):
                print(l.get_attribute('href'))
                tradelinks.append(l.get_attribute('href'))
        print(tradelinks)
        if tradelinks:
            for tlink in tradelinks:
                self.goToURL(tlink)
                main = self.getElem('main')
                print("Detail", main)
                td = self.getSubElem(main, 'td', find_by='tag')
                detailhtm = ''
                detailhtm = td.get_attribute('innerHTML')
                strdetail = detailhtm.replace(' ', '').replace('<hr>', '<br>').replace('<b>', '').replace('</b>', '').replace('\n', '')
                print(strdetail)
                listdetail = re.sub('.*授權結果', '授權結果', strdetail).split('<br>')
                listdetail = [_f for _f in listdetail if _f]
                print(listdetail)
                dictdetail = {x.split(':')[0]:x.split(':')[1] for x in listdetail}
                print(dictdetail)
                tid = dictdetail['刷卡單號']
                trade_result[tid] = dictdetail

        return trade_result
                
        #for tid in tid_list:
            #link = tb.find_element_by_link_text('tid')
            #print "link:", link
            #detail_links = self.getMultipleElem('a.dialogBlock', find_by='css')
            #print detail_links
        
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


