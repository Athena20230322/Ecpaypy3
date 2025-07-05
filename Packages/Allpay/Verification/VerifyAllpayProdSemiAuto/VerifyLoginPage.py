# -*- coding: utf-8 -*-

from UIOperate.WebVerify import  webVerification
import LibGeneral.GetConfigValue as getConf
import os



class loginVerify(webVerification):
    
    def __init__(self, input_drv, log_file_relat_path):

        self.conf = getConf.getConfig()
        self.rootdir = self.conf.getRootDir()        
        self.elem_list = os.path.join(self.rootdir, 'Conf', 'Element_Corresponding', 'AllpayWeb', 'LoginPage.csv')
        webVerification.__init__(self, input_drv, self.elem_list, log_file_relat_path)
        
    def verifyLoginResult(self):
        get = self.helper.getElemIdentFromDataSet
        ids = self.identds  
        result = self.verifyMultipleElems('Logout_button')
        
        if len(result) is not 0:
            print('SUCCESS!!!')
            print(result)
            return result
        