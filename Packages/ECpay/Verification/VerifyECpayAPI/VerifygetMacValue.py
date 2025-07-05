from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper 
from APIOperate.APIOperate import HtmlHelper

class verifygetMacValue(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'getMacValue'
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo',
                                                                feature_cat=self.category,
                                                                feature_name=self.fea_name)
        hash_key = self.feature_conf['HashKey132']
        hash_iv = self.feature_conf['HashIV132']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.hkey = hash_key
        self.hiv = hash_iv
        self.htm_helper = HtmlHelper()
        self.raw_sess = self.genSession()

    def verifyMacValue(self, req_result, gen_result):
        result = {}
        if req_result == gen_result:
            result['verifyCheckMacValue']

    def verifyMacValueExist(self, req_result):
        result = {}
        if req_result == '' or req_result == None:
            result['VerifyResultExist'] = False
        else:
            result['VerifyResultExist'] = True
        return result

    def verifyDiffData(self, result1, result2):
        result = {}
        if result1 != result2:
            result['verifyDiffData'] = True
        else:
            result['verifyDiffData'] = False
        return result

    def verifyTwoSameDataWithApi(self, result1, result2):
        result = {}
        if result1 == result2:
            result['verifyTwoSameDataWithApi'] = True
        else:
            result['verifyTwoSameDataWithApi'] = False
        return result

    def verifyDataWithApiAndGen(self, result1, result2):
        result = {}
        if result1 == result2:
            result['verifyDataWithApiAndGen'] = True
        else:
            result['verifyDataWithApiAndGen'] = False
        return result
