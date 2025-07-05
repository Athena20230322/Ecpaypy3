# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActAppsdksearch import actAppsdksearch
from ECpay.Verification.VerifyECpayAPI.VerifyAppsdksearch import verifyAppsdksearch


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
ACT_API = actAppsdksearch()
VER_API = verifyAppsdksearch()

#Testing exec

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'APPSDKSEARCH', CASE_NAME, 'Tokenget.csv')

inv_info = EXEC_ACT(ACT_API.genOrderRequestInfoTokenGet, INV_INFO_CSV)

api_response = EXEC_ACT(ACT_API.genPostRequestToAPIToken, inv_info)

res_dict = EXEC_ACT(ACT_API.strToDict, api_response)

data = EXEC_ACT(ACT_API.decryptDatab2b2, res_dict['Data'])

print(data)


INV_INFO_CSV1 = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'APPSDKSEARCH', CASE_NAME, 'Keyexchange.csv')

info1 = EXEC_ACT(ACT_API.genOrderRequestInfoKeyExchange, INV_INFO_CSV1)

api_response1 = EXEC_ACT(ACT_API.genPostRequestToAPIkeyexchange,info1)


data1 = EXEC_ACT(ACT_API.decryptDatapppsdk,api_response1)
print(data1)

res_dict1 = EXEC_ACT(ACT_API.strToDictAppsdk, api_response1)
print(res_dict1)


data2 = EXEC_ACT(ACT_API.decryptDatab2bAppsdk, res_dict1['Data'],data1)
print(data2)

# data5 = EXEC_ACT(ACT_API.encryptDatapppsdk, data2,data1)
#
# print '88888888'
# print data5

print('555555')




QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'APPSDKSEARCH', CASE_NAME, 'Query.csv')

query_info = EXEC_ACT(ACT_API.genOrderRequestInfoTokenQuery, QUERY_INFO_CSV, data,data1)

data3 = EXEC_ACT(ACT_API.encryptDatapppsdk, data1,data2)

query_rtn = EXEC_ACT(ACT_API.genPostRequestToAPIQuery, query_info,data3,data2)

query_rtn_dict = EXEC_ACT(ACT_API.strToDict, query_rtn)

print(query_rtn_dict)

# verification
# VERIFY(VER_API.verifyColumn,data2, data, CASE_NAME)


# VERIFY
#VERIFY(VER_API.verifyResponseValuesforappsearch, query_rtn, CASE_NAME, data3)

VERIFY(VER_API.verifyResponseValuesb2b, CASE_NAME,query_rtn_dict)
time.sleep(3)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
