import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper


class actgetMacValue(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI',
                                                                feature_name='getMacValue')
        hash_key = self.feature_conf['HashKey132']
        hash_iv = self.feature_conf['HashIV132']
        APIHelper.__init__(self, hash_key, hash_iv)
        
        
    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        return req

    def createCheckMacValueByRequest(self, req_info):
        form_act = self.feature_conf['getMacValue_API']
        response = requests.post(form_act, req_info)
        print((response.text))
        return response.text

    def genCheckMacValue(self, req_info):
        hashKey = ''
        hashIV = ''
        if req_info['MerchantID'] == '2000132':
            hashKey = self.feature_conf['HashKey132']
            hashIV = self.feature_conf['HashIV132']
        elif req_info['MerchantID'] == '2000933':
            hashKey = self.feature_conf['HashKey933']
            hashIV = self.feature_conf['HashIV933']
        APIHelper.__init__(self, hashKey, hashIV)
        print(('hashKey= ' + hashKey))
        print(('hashIV= ' + hashIV))
        chksum = self.genChkMacVal(req_info, mode='local')
        print(chksum)
        return chksum
