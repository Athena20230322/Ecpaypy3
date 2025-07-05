import time
import json
import LibGeneral.funcGeneral as funcGen
from LibGeneral.GetConfigValue import getConfig
from LibGeneral.TestHelper import classTestHelper
from APIOperate.APIOperate import APIHelper
from APIOperate.APIOperate import HtmlHelper
from UIOperate import WebOperate

class verifyCreateHiLifeTestData(APIHelper):
    def __init__(self):
        self.conf = getConfig()
        self.category = 'ECpayAPI'
        self.fea_name = 'CreateHiLifeTestData'
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

    def enableWebOperate(self, webdrv):
        self.webop = WebOperate.webOperate(webdrv)

    def verifyStatusResult(self, res_info, match_str):
        result = {}
        if res_info.find(match_str) != -1:
            result['verifyStatusResult'] = True
            return result
        else:
            result['verifyStatusResult'] = False
            return result

    def verifyCreateHiLifeTestDataResult(self):
        op = self.webop
        tag_body = op.getElem('body', find_by='tag')
        result = {}
        print(tag_body.text)
        tag_str = tag_body.text
        #print type(tag_str)
        tag_str= tag_str.split('|')
        #print tag_str[0]
        if tag_str[0].find('1') != -1:
            result['verifyCreateHiLifeTestDataResult'] = True
            return result
        else:
            self.log.WARN('verifyCreateHiLifeTestDataResult: result is not 1|return_message!')
            result['verifyCreateHiLifeTestDataResult'] = False
            return result

    def verifyCreateHiLifeTestDataDownload(self, merc_id):
        op = self.webop
        print('####test_merchantid####')
        print(merc_id)
        tag_body = op.getElem('body', find_by='tag')
        result = {}
        print(tag_body.text)
        tag_str = tag_body.text
        tag_str = tag_str.split('|')
        print(tag_str)
        if tag_str[0].find('1') != -1:
            tag_str = ''.join(tag_str[1])
            print(tag_str)
            if tag_str.find(merc_id) != -1:
                result['verifyCreateHiLifeTestDataDownload'] = True
                return result
        else:
            self.log.WARN('verifyCreateHiLifeTestDataResult: result is not 1|return_message!')
            result['verifyCreateHiLifeTestDataDownload'] = False
            return result

    def verifyColumn(self, res_dict, case_id):
        all_verify_data = self.t_helper.getTestDataIniSections(self.category, self.fea_name, case_id,
                                                               'Verification.ini')
        if 'verifyReturnColumn' in all_verify_data:
            expect_args_dict = all_verify_data['verifyReturnColumn']
        else:
            raise ValueError("verifyColumn: Secion 'verifyReturnColumn' not found in Verification.ini")
        print((list(expect_args_dict.keys())))
        print((list(res_dict.keys())))
        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(expect_args_dict) == len(res_dict):
                    result['verifyColumnNumber'] = True
                else:
                    raise ValueError("verifyColumn: the amount of columns is not equal to the expected result.")
                for key in expect_args_dict:
                    if key in res_dict:
                        result['verifyColumns'] = True
                        continue
                    else:
                        result['verifyColumns'] = False
                        break
                return result
            else:
                raise ValueError("verifyColumn: Length of expected result cannot be zero.")
        else:
            raise TypeError("verifyColumn: Received expect_args_dict is not a dictionary.")

    def verifyCreateHiLifeTestDataCheck(self, req_info):
        expect_args_dict = self.returnBodyToDic(req_info)
        tamp_dic = {}
        tamp_dic['AllPayLogisticsID'] = expect_args_dict['1|AllPayLogisticsID']
        expect_args_dict.pop('1|AllPayLogisticsID')
        expect_args_dict['AllPayLogisticsID'] = tamp_dic['AllPayLogisticsID']
        query_dict = {}
        for key in expect_args_dict:
            query_dict[key] = expect_args_dict[key]
        query_dict.pop('CheckMacValue')
        query_chksum = self.genChkMacVal(query_dict)
        query_dict['CheckMacValue'] = query_chksum

        result = {}
        if type(expect_args_dict) is dict:
            if len(expect_args_dict) > 0:
                if len(query_dict) != 0:
                    if query_dict['RtnCode'] == '2001':

                        result['verifyCreateHiLifeTestDataCheck'] = self.verifyRtnData(query_dict,
                                                                                       expect_args_dict,
                                                                                       datatype='dictionary')
                        return result
                    else:
                        self.log.WARN("RtnCode is not '2001'!%s" % query_dict)
                        result['verifyCreateHiLifeTestDataCheck'] = False
                        return result

            else:
                raise ValueError("verifyCreateHiLifeTestDataCheck: Length of expected result dic cannot be zero.")
        else:
            raise TypeError("verifyCreateHiLifeTestDataCheck: Received expect_args_dict is not an dictionary.")
