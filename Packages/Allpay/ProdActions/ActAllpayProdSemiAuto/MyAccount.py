# -*- coding: utf-8 -*-

from UIOperate.WebOperate import webOperate
import time



class myAccountPage(webOperate):
    
    def __init__(self, drv, log_file):

        webOperate.__init__(self, drv)
        
    def gotoRetrieve(self):
        
        
        self.clickElem('a.table_btn_blue.margin_l0.margin_t5', findby='css')
        
    def gotoAcctDetail(self):
        self.clickElem("[href='/BaseMember/AccountDetail']", findby='css')
        time.sleep(3)
       
    def selectTransCategory(self, data):
        self.selectDropboxList('text', data, 'TypeName', find_by='name')
        
    def specifyStartDate(self, *args):
        if len(args) == 3:
            self.clickElem('startDate')
            self.operateCalendar(args)

    def specifyEndDate(self, *args):
        if len(args) == 3:
            self.clickElem('endDate')
            self.operateCalendar(args)
            
    def submitQuery(self):
        self.clickElem('fomeSubmit')