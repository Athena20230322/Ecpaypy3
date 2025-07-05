# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActEmbeddedPayToken import actEmbeddedpaytoken
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedPayToken import verifyEmbeddedpaytoken

from ECpay.ProdActions.ActECpayAPI.ActEmbeddedtoken import actEmbeddedtoken
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedtoken import verifyEmbeddedtoken

from ECpay.ProdActions.ActECpayAPI.ActEmbeddedGettokenbyTrade import actEmbeddedgettokenbytrade



from ECpay.ProdActions.ActECpayAPI.ActEmbedded import actEmbedded
from ECpay.Verification.VerifyECpayAPI.VerifyEmbedded import verifyEmbedded


#(DO NO Edit) Static declare 

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir', type=str, help='Specify the log dir')
ARGP.add_argument('--package', type=str, help='Specify the package name')
ARGP.add_argument('--runid', type=str, default='', help='Specify the runtime guid for this run.')
ARGS = ARGP.parse_args()
LOG_DIR = ARGS.logdir
PKG = ARGS.package
RUN_UID = ARGS.runid
CASE_NAME = str(os.path.basename(__file__)).rstrip('.py')
SUM_LOG = os.path.join(LOG_DIR, CASE_NAME, 'Summary.log')
HELPER = classTestHelper(SUM_LOG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_API = actEmbeddedpaytoken()
VER_API = verifyEmbeddedpaytoken()
ACT_API1 = actEmbeddedtoken()
VER_API1 = verifyEmbeddedtoken()
ACT_API2 = actEmbedded()
VER_API2 = verifyEmbedded()
ACT_API3 = actEmbeddedgettokenbytrade()

#Testing exec

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedGetBindCardPayToken', CASE_NAME, 'Tokenget1.csv')

inv_info = EXEC_ACT(ACT_API3.genOrderRequestInfoGetTokenbyBindingCard, INV_INFO_CSV)

api_response = EXEC_ACT(ACT_API3.genPostRequestToAPI, inv_info)

res_dict = EXEC_ACT(ACT_API3.strToDict, api_response)

data = EXEC_ACT(ACT_API3.decryptDatab2b2, res_dict['Data'])

print(data)





# INV_INFO_CSV1 = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedPayToken', CASE_NAME, 'Keyexchange.csv')
#
# info1 = EXEC_ACT(ACT_API2.genOrderRequestInfoKeyExchange, INV_INFO_CSV1)
#
# api_response = EXEC_ACT(ACT_API2.genPostRequestToAPIkeyexchange,info1)
#
#
# data1 = EXEC_ACT(ACT_API2.decryptDatapppsdk,api_response )
# print data1
#
# res_dict1 = EXEC_ACT(ACT_API2.strToDict, api_response)
# print res_dict1
#
# data2 = EXEC_ACT(ACT_API2.decryptDatab2b, res_dict1['Data'],data1)
# print '12222'
# print data2
# print '22333'





# QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedPayToken', CASE_NAME, 'Query.csv')
#
# query_info = EXEC_ACT(ACT_API.genOrderRequestInfoTokenQueryPlus, QUERY_INFO_CSV, data,data1)
#
# data3 = EXEC_ACT(ACT_API.encryptDatapppsdkn, data1,data2)
# print  data3
#
# query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPIQuery, query_info,data3,data2)
#
# print query_rtn
# #query_rtn_dict = EXEC_ACT(ACT_API.strToDict, query_rtn)
#
# data5 = EXEC_ACT(ACT_API.decryptDatarsa,query_rtn )
# print data5
#query_rtn_dict1 = EXEC_ACT(ACT_API.strToDictrsa, query_rtn)
#print query_rtn_dict
#print query_rtn_dict1




# verification
#VERIFY(VER_API.verifyColumn,data2, data, CASE_NAME)


# VERIFY
#VERIFY(VER_API.verifyResponseValuesforappsearch, CASE_NAME, data5)

VERIFY(VER_API.verifyResponseValuesforpaytoken,CASE_NAME,data)
time.sleep(3)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
