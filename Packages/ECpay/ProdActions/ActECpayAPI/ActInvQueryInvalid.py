import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper


class actInvQueryInvalid(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvQueryInvalid')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()

    def genOrderRequestInfo(self, query_dict, issue_dict):
        req = self.genArgsDictFromCSV(query_dict, de_strip=True)
        req['RelateNumber'] = issue_dict['RelateNumber']
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def clearChkMacValue(self, query_dict):
        query_dict['CheckMacValue'] = ''
        return query_dict

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvQueryInvalid']
        response = self.postRequestToAPI(self.genSession(), req_info, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

