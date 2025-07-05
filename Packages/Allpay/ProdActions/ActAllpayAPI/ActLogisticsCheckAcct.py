import requests
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actLogisticsCheckAcct(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI',
                                                                feature_name='LogisticsCheckAcct')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()

    def getRtnMerTID(self, response):
        return_list = response.split('|')
        print(return_list)
        return return_list[0]
        
    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req['MerchantTradeNo'])
        return req

    def genRtnRequestInfo(self, param_csv, rtn_merc_t_no):
        req = self.genArgsDictFromCSV(param_csv)
        req['RtnMerchantTradeNo'] = rtn_merc_t_no
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def RtnGoodsByRequest(self, req_info):
        form_act = self.feature_conf['Rtn_API']
        response = requests.post(form_act, req_info)
        print(response.text)
        return response.text

