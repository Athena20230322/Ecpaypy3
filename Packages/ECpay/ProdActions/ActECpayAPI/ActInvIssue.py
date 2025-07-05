# -*- coding: utf-8 -*-
import time
import json
import os
import urllib.request, urllib.parse, urllib.error
import collections
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote_plus
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate
from loguru import logger





class actInvIssue(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='ECpayAPI', feature_name='InvIssue')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()
        
    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    #@logger.catch
    def genOrderRequestInfo(self, param_csv, exclusive_params, revert_params):

        req = self.genArgsDictFromCSV(param_csv, de_strip=True)

        #for key in req:

           # req[key] = req[key].encode('utf-8')

        exclusive_ele = {}
        if req['RelateNumber'] == 'AUTO_GEN_RELATENO':
            req['RelateNumber'] = self.gen_uid(with_dash=False)[0:30]
        print((req['RelateNumber']))
        for param in exclusive_params:
            exclusive_ele[param] = req[param]
            req.pop(param)
        chksum = self.genChkMacVal(req, mode='local', codec='md5', case='insensitive')
        print (chksum)
        req['CheckMacValue'] = (chksum.encode('utf-8'))
        print((type(req['CheckMacValue'])))
        #print (req['CheckMacValue'])
        for param in exclusive_params:

            req[param] = exclusive_ele[param]
        for param in revert_params:
            req[param] = urllib.parse.unquote_plus(req[param])
        print (req)
        return req

    #@logger.catch
    def genPostRequestToAPI(self, req_info):
        form_act = self.feature_conf['InvIssue_API']
        od_arg_dict = collections.OrderedDict(sorted(list((req_info).items()), key=lambda x: x[0].lower()))
        response = self.postRequestToAPI(self.genSession(), od_arg_dict, form_act, trencode_dotnet=True)
        self.log.INFO(response.decode('utf-8'))
        return response

    #@logger.catch
    def strToDict(self, res_info):


        res_dict = {}


        print(res_dict)

        str_to_list = res_info.split('&'.encode(encoding='utf-8'))


        for item in str_to_list:
            tmp = item.split('='.encode(encoding='utf-8'))


            res_dict[tmp[0]] = (tmp[1])
        print('999778')
        res_dict = {key.decode(): val.decode() for key, val in list(res_dict.items())}
        print (res_dict)
        print('999777')
        return res_dict

    def quote_item(self, res_dict, revert_list):
        for key in revert_list:
            res_dict[key] = urllib.parse.unquote_plus(res_dict[key]).lower()
        return res_dict

