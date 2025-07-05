# -*- coding: utf-8 -*-

from UIOperate.WebVerify import  webVerification
import LibGeneral.GetConfigValue as getConf
import os

class myAccountVerify(webVerification):
    def __init__(self):
        self.conf = getConf.getConfig()
        self.rootdir = self.conf.getRootDir()        
        self.elem_list = os.path.join(self.rootdir, 'Conf', 'Element_Corresponding', 'AllpayWeb', 'LoginPage.csv')
        webVerification.__init__(self, input_drv, self.elem_list, log_file_relat_path)        
    
    def verifyAcctQueryDetailTable(self):
        result_table = self.getElem("table.list.margin_b15", find_by='css')
        tb_head = result_table.find_elements_by_tag_name("th")
    
        value = '查詢'.decode('utf-8').encode('big5')
    
        res = self.chkHTMLTableContent(result_table, value, typ='header')
        print(res)
        print(list(res.keys())[0].decode('big5').encode('big5'))    