# -*- coding: utf-8 -*-
import time
import json
import os
import urllib.request, urllib.parse, urllib.error
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actAuthCardIDRedirect(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='AuthCardIDRedirect')
        hash_key = self.feature_conf['JumpKey']
        hash_iv = self.feature_conf['JumpIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genAuthRequestInfo(self, param_csv, card_id):
        req = self.genArgsDictFromCSV(param_csv, de_strip=True)
        if req['CardID'] == 'GEN_BY_BINDING':
            req['CardID'] = card_id
        if req['MerchantID'] == '2001867':
            hash_key = self.feature_conf['JumpKey']
            hash_iv = self.feature_conf['JumpIV']
            APIHelper.__init__(self, hash_key, hash_iv)
        chksum = self.genChkMacVal(req, mode='local', codec='sha256')
        print(chksum)
        req['CheckMacValue'] = chksum
        print(req)
        return req

    def authPostRequest(self, req_info, mode):
        form_act = self.feature_conf[mode]
        response = self.getRequestFromAPI(req_info, form_act)
        self.log.INFO(response)
        return response

    def strToDict(self, response):
        res_list = response.split('&')
        res_dict = {}
        for ele in res_list:
            if ele != '':
                ele = ele.encode('utf-8')
                res_dict[ele.split('=')[0]] = ele.split('=')[1]
        res_dict['RtnMsg'] = urllib.parse.unquote_plus(res_dict['RtnMsg'])
        return res_dict
