# -*- coding: utf-8 -*-

import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections

class actInvQueryChkMobBarCode(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI',
                                                                feature_name='InvQueryChkMobBarCode')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv, inject_value=''):
        req = self.genArgsDictFromCSV(param_csv)
        for key in req:
            if req[key] == 'AUTO_INJECT_KEY':
                req[key] = inject_value
                break
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvQueryChkMobBarCode_API']
        print('BEFORE DO SORT:', req_info)
        od_arg_dict = collections.OrderedDict(sorted(req_info.items()))
        print('DID SORT:', od_arg_dict)
        query_order = self.postRequestToAPI(self.raw_sess, od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(query_order.decode('utf-8'))
        return query_order

    def strToDict(self, res_info):
        res_dict = {}
        str_to_list = res_info.split('&')
        for item in str_to_list:
            tmp = item.split('=')
            res_dict[tmp[0]] = tmp[1]
        print(res_dict)
        return res_dict
    
