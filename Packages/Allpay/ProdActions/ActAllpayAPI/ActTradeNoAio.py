#-*- coding:utf-8 -*-
import time
import json
import os
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate


class actTradeNoAio(APIHelper):
    def __init__(self):
        self.t_helper = classTestHelper()
        self.feature_conf = self.t_helper.getFeatureTestSetting('ModuleWideInfo', feature_cat='AllpayAPI', feature_name='TradeNoAio')
        hash_key = self.feature_conf['HashKey']
        hash_iv = self.feature_conf['HashIV']
        APIHelper.__init__(self, hash_key, hash_iv)
        self.raw_sess = self.genSession()
        self.htm_helper = HtmlHelper()

    def enableWebOperate(self, drv):
        self.webop = WebOperate.webOperate(drv)

    def genOrderRequestInfo(self, param_csv):
        req = self.genArgsDictFromCSV(param_csv)
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def genOrderRequestInfoPlatformID(self, param_csv, plat_id=''):
        req = self.genArgsDictFromCSV(param_csv)
        req['PlatformID'] = plat_id
        chksum = self.genChkMacVal(req, mode='local')
        print(chksum)
        req['CheckMacValue'] = chksum
        return req

    def createOrderByBrowser(self, browser_drv, req_info):
        op = self.webop
        form_actTradeNoAio = self.feature_conf['Chkout_API']
        form_genorder = self.createHtmlFormJs('FormGenOrder', req_info, action=form_actTradeNoAio, submit=True)
        print(form_genorder)
        browser_drv.execute_script(form_genorder)
        # op.handleAlert()
        return browser_drv

    def genpostRequestToAPI(self, order_info_crt_res):
        actTradeNoAio = self.feature_conf['Chkout_API']
        query_order = self.postRequestToAPI(self.raw_sess, order_info_crt_res, actTradeNoAio)
        self.log.INFO(query_order)
        return query_order

    def strToDict(self, res):
        res_list = res
        replace_list = ['-', '""', '=', '"', '\r']
        for replace_args in replace_list:
            if replace_args == '-' or replace_args == '""':
                res_list = res_list.replace(replace_args, '-')
            elif replace_args == '=' or replace_args == '"' or replace_args == '\r':
                res_list = res_list.replace(replace_args, '')
        res_list = res_list.split('\n')

        key_list = res_list[0].split(',')
        value_list = res_list[1].split(',')
        print(len(key_list), len(value_list))
        res_dict = {}
        for i in range(len(key_list)):
            print(key_list[i], value_list[i])
            res_dict[key_list[i]] = value_list[i]
        self.log.INFO(res_dict)
        return res_dict



