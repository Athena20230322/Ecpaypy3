import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyPrintUniMartC2COrder(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'PrintUniMartC2COrder'
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

    def __hiddenCode(self, str, mode='name'):
        #Vera -> V**a
        if mode == 'name':
            return str[0] + '*'*(len(str)-2) + str[-1]
        elif mode == 'phone':
            print((str[0:3] + '*'*(len(str)-5) + str[-2:]))
            return str[0:3] + '*'*(len(str)-5) + str[-2:]

    def verifyExistance(self, ele):
        result = {}
        if ele != None:
            result['verifyExist'] = True
        else:
            result['verifyExist'] = False
        return result

    def verifyPrintInfo(self, print_dict, order_dict, cvs_payment_no, cvs_validation_no, case_id):
        result = {}
        if print_dict['serv_no'] == cvs_payment_no + cvs_validation_no:
            result['verifyCVSPaymentNo&CVSValidationNo'] = True
        else:
            result['verifyCVSPaymentNo&CVSValidationNo'] = False
        if print_dict['recver'] == order_dict['ReceiverName']:
            result['verifyReceiverName'] = True
        else:
            result['verifyReceiverName'] = False
        if print_dict['sender'] == self.__hiddenCode(order_dict['SenderName'], mode='name'):
            result['verifySenderName'] = True
        else:
            result['verifySenderName'] = False
        verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name,
                                                           case_id, 'Verification.ini')
        expect_dict = verify_data['verifyReturn']
        print(('expect_dict', expect_dict))
        print(('print result: ' + print_dict['shop']))
        print(('expect result: ' + expect_dict['shop'].decode('big5')))
        if type(expect_dict) is dict:
            if len(expect_dict) > 0:
                if print_dict['shop'] == expect_dict['shop'].decode('big5'):
                    result['verifyShop'] = True
                else:
                    result['verifyShop'] = False
            else:
                raise ValueError("verifyPaymentReturn: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyPaymentReturn: Recieved expect_args_dict is not an dictionary")
        return result
