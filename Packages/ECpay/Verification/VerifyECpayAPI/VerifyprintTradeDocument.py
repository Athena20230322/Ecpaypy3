# -*- coding: utf-8 -*-

import time
import datetime
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyprintTradeDocument(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'printTradeDocument'
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo',
                                                                feature_cat=self.category,
                                                                feature_name=self.fea_name)
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']        
        APIHelper.__init__(self, hash_key, hash_iv)
        self.hkey = hash_key
        self.hiv = hash_iv
        self.htm_helper = HtmlHelper()
        self.raw_sess = self.genSession()

    def enableWebOperate(self, webdrv):
        self.webop = WebOperate.webOperate(webdrv)

    def verifyStatusResult(self, query_str, match_str):
        result = {}
        print(query_str)
        if query_str.find(match_str) != -1:
            result['verifyStatusResult'] = True
            return result
        else:
            self.log.WARN('verifyStatusResult: result is not match')
            result['verifyStatusResult'] = False
            return result

    def verifyprintTradeDocumentResult(self):
        op = self.webop
        tbody = op.getElem('/html/body/div/div[2]/table/tbody', find_by='xpath')
        result = {}
        for tbody_element in op.getMultipleSubElems(tbody, 'samp', find_by='tag'):
            print(tbody_element.text)
            tbody_elements_str = tbody_element.text
            if tbody_elements_str != '':
                result['verifyprintTradeDocumentResult'] = True
                return result
            else:
                self.log.WARN("verifyprintTradeDocumentResult: result is not found!")
                result['verifyprintTradeDocumentResult'] = False
                return result

    def verifyprintTradeDocFAMI(self, recei_name, recei_sid, logis_id, merct_no):
        op = self.webop
        tbody = op.getElem('//table[1]/tbody/tr/td/table[1]/tbody', find_by='xpath')
        info_chek_count = 0
        result = {}
        for tbody_element in op.getMultipleSubElems(tbody, 'samp', find_by='tag'):
            print(tbody_element.text)
            #print type(tbody_element.text)
            tbody_elements_str = tbody_element.text
            if tbody_elements_str.find(recei_name) != -1:
                #print tbody_elements_str, recei_name
                info_chek_count += 1
            elif tbody_elements_str.find(recei_sid) != -1:
                #print tbody_elements_str, recei_sid
                info_chek_count += 1
            elif tbody_elements_str.find(logis_id) != -1:
                #print tbody_elements_str, logis_id
                info_chek_count += 1
            elif tbody_elements_str.find(merct_no) != -1:
                #print tbody_elements_str, merct_no
                info_chek_count += 1
                #print info_chek_count
            else:
                pass
        if info_chek_count == 5:
            result['verifyprintTradeDocument'] = True
            return result
        else:
            self.log.WARN("verifyprintTradeDocument: result is not match!")
            result['verifyprintTradeDocument'] = False
            return result

    def verifyprintTradeDocUNIMART(self, recei_name, recei_sid, logis_id, merct_no):
        op = self.webop
        tbody = op.getElem('//table[1]/tbody/tr/td/table[1]/tbody', find_by='xpath')
        tag_img = op.getElem('img', find_by='tag')
        info_chek_count = 0
        result = {}
        # print 'info_chek_count: %d' % info_chek_count
        for tbody_element in op.getMultipleSubElems(tbody, 'samp', find_by='tag'):
            print(tbody_element.text)
            tbody_elements_str = tbody_element.text
            if tbody_elements_str.find(recei_name) != -1:
                info_chek_count += 1
                # print 'info_chek_count: %d' % info_chek_count
            elif tbody_elements_str.find(recei_sid) != -1:
                info_chek_count += 1
                # print 'info_chek_count: %d' % info_chek_count
            elif tbody_elements_str.find(merct_no) != -1:
                info_chek_count += 1
                # print 'info_chek_count: %d' % info_chek_count
            else:
                pass
        # print 'info_chek_count: %d' % info_chek_count
        print(tag_img.get_attribute('src'))
        tag_url = tag_img.get_attribute('src')
        if tag_url.find(logis_id) != -1:
            print(logis_id)
            info_chek_count += 1
        # print 'info_chek_count: %d' % info_chek_count
        if info_chek_count == 5:
            result['verifyprintTradeDocUNIMART'] = True
            return result
        else:
            self.log.WARN("verifyprintTradeDocUNIMART: result is not match!")
            result['verifyprintTradeDocUNIMART'] = False
            return result

    def verifyRtnChekHiLifeimgU(self, recei_name, recei_sid, logis_id, merct_no):
        op = self.webop
        tbody = op.getElem('//table[1]/tbody/tr/td/table[1]/tbody', find_by='xpath')
        tag_img = op.getElem('img', find_by='tag')
        info_chek_count = 0
        result = {}
        # print 'info_chek_count: %d' % info_chek_count
        for tbody_element in op.getMultipleSubElems(tbody, 'samp', find_by='tag'):
            print(tbody_element.text)
            tbody_elements_str = tbody_element.text
            if tbody_elements_str.find(recei_name) != -1:
                info_chek_count += 1
                # print 'info_chek_count: %d' % info_chek_count
            elif tbody_elements_str.find(recei_sid) != -1:
                info_chek_count += 1
                # print 'info_chek_count: %d' % info_chek_count
            elif tbody_elements_str.find(merct_no) != -1:
                info_chek_count += 1
                # print 'info_chek_count: %d' % info_chek_count
            else:
                pass
        # print 'info_chek_count: %d' % info_chek_count
        print(tag_img.get_attribute('src'))
        tag_url = tag_img.get_attribute('src')
        if tag_url.find(logis_id) != -1:
            print(logis_id)
            info_chek_count += 1
        # print 'info_chek_count: %d' % info_chek_count
        if info_chek_count == 5:
            result['verifyprintTradeDocUNIMART'] = True
            return result
        else:
            self.log.WARN("verifyprintTradeDocUNIMART: result is not match!")
            result['verifyprintTradeDocUNIMART'] = False
            return result

    def verifyRtnChekHiLifeimg(self):
        op = self.webop

        tag_img = op.getElem('embed', find_by='tag')

        result = {}
        if tag_img != None:
            result['verifyRtnChekHiLifeimg'] = True
            return result
        else:
            self.log.WARN("verifyprintTradeDocUNIMART: result is not find HiLife img!")
            result['verifyRtnChekHiLifeimg'] = False
            return result
    def verifyprintFAMIC2COrderResult(self):
        op = self.webop
        tag_print = op.getElem('button', find_by='tag')
        result = {}
        print(tag_print.text)
        tag_str = tag_print.text
        if tag_str.find('列印') != -1:
            result['verifyprintFAMIC2COrderResult'] = True
            return result
        else:
            self.log.WARN("verifyprintFAMIC2COrderResult: result is not find '列印' button!")
            result['verifyprintFAMIC2COrderResult'] = False
            return result

    def verifyprintFAMIC2COrderDownload(self):
        op = self.webop
        tag_img = op.getElem('img', find_by='tag')
        result = {}
        print(tag_img.get_attribute('src'))
        tag_url = tag_img.get_attribute('src')
        if tag_url.find('https://logistics-stage.ecpay.com.tw/Helper/FamiB2CPickupCode?') != -1:
            result['verifyprintFAMIC2COrderDownload'] = True
            return result
        else:
            self.log.WARN("verifyprintFAMIC2COrderDownload: result is not find img!")
            result['verifyprintFAMIC2COrderDownload'] = False
            return result



