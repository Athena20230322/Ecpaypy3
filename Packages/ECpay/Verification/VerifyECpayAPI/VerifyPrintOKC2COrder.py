import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyPrintOKC2COrder(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'PrintOKC2COrder'
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

    def verifyExistance(self, element):
        result = {}
        if element is not None:
            result['verifyExist'] = True
        else:
            result['verifyExist'] = False
        return result

    def verifyPrintInfo(self, expect_dict, res_dict, sender, receiver):
        result = {}
        # if res_dict['orderID'][-5:] == expect_dict['AllPayLogisticsID']:
        #     result['verifyAllPayLogisticsID'] = True
        # else:
        #     result['verifyAllPayLogisticsID'] = False
        if res_dict['CVSPaymentNo'] == expect_dict['CVSPaymentNo']:
            result['verifyCVSPaymentNo'] = True
        else:
            result['verifyCVSPaymentNo'] = False
        if res_dict['sender'] == sender:
            result['verifySenderName'] = True
        else:
            result['verifySenderName'] = False
        if res_dict['receiver'] == receiver:
            result['verifyReceiverName'] = True
        else:
            result['verifyReceiverName'] = False
        return result
