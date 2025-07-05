# -*- coding: utf-8 -*-

import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
import collections
import urllib.request, urllib.parse, urllib.error




class actInvDelay(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='InvDelay')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv, revert_args, exclusive_args):
        req = self.genArgsDictFromCSV(param_csv)
        print(repr(req))

        if req['RelateNumber'] == 'AUTO_GEN_RELATENO':
            req['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]

        if req['Tsr'] == 'AUTO_GEN_TSR':
            req['Tsr'] = self.gen_uid(with_dash=False)[0:30]

        for key in req:
            req[key] = req[key].encode('utf-8')

        exclusive_dict = {}
        for param in exclusive_args:
            exclusive_dict[param] = req[param]
            req.pop(param)

        chksum = self.genChkMacVal(req, case='insensitive')
        print(chksum)

        for param in exclusive_args:
            req[param] = exclusive_dict[param]

        for revert_key in revert_args:
            req[revert_key] = urllib.parse.unquote(req[revert_key])

        req['CheckMacValue'] = chksum
        return req

    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvDelay_API']
        od_arg_dict = collections.OrderedDict(sorted(list(req_info.items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    def strToDict(self, res):
        res_list = res.split('&')
        res_dict = {}
        for item in res_list:
            res_dict[item.split('=')[0]] = item.split('=')[1]
        return res_dict


