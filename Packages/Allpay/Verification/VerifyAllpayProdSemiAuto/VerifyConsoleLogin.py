# -*- coding: utf-8 -*-

from UIOperate.WebVerify import  webVerification
import LibGeneral.GetConfigValue as getConf
import os
from LibGeneral.TestHelper import classTestHelper


class verifyConsoleLogin(webVerification):
    
    def __init__(self, input_drv, log_file_relat_path):
        
        self.category = 'AllpayProdSemiAuto'
        self.fea_name = 'ConsoleLogin'        
        self.conf = getConf.getConfig()
        self.rootdir = self.conf.getRootDir()
        
        self.t_helper = classTestHelper()
        self.elem_list = os.path.join(self.rootdir, 'Conf', 'Element_Corresponding', 'AllpayVendorConsole', 'ConsoleLogin.csv')
        webVerification.__init__(self, input_drv, self.elem_list, log_file_relat_path)
        
    def verifyTradeDetail(self, tradelist, info_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category,
                                                               self.fea_name,
                                                               case_id,
                                                               'Verification.ini') 
        expect_dict = all_verify_data['verifyTradeDetail']
        exp_dict_unicode = {x.decode('utf8'):expect_dict[x].decode('utf8') for x in list(expect_dict.keys())}
        result_dict = {}
        for trade_no in tradelist:
            detail = info_dict[trade_no]
            for k in list(exp_dict_unicode.keys()):
                print("compare %s: \n Expected: %s \n Recieved: %s \n " % (k, exp_dict_unicode[k], detail[k]))
                if exp_dict_unicode[k] == detail[k]:
                    result_dict[k] = True
                else:
                    result_dict[k] = False
        return result_dict
        
    def verifyLoginResult(self):
        get = self.helper.getElemIdentFromDataSet
        ids = self.identds  
        result = self.verifyMultipleElems('Logout_button')
        
        if len(result) is not 0:
            print('SUCCESS!!!')
            print(result)
            return result
        