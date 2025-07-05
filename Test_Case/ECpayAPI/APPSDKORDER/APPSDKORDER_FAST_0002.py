# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActAppsdkorder import actAppsdkorder
from ECpay.Verification.VerifyECpayAPI.VerifyAppsdkorder import verifyAppsdkorder


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
ACT_API = actAppsdkorder()
VER_API = verifyAppsdkorder()

#Testing exec

INV_INFO_CSV2 = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'APPSDKORDER', CASE_NAME, 'Tokenget.csv')

inv_info = EXEC_ACT(ACT_API.genOrderRequestInfoTokenGet, INV_INFO_CSV2)

api_response = EXEC_ACT(ACT_API.genPostRequestToAPItoken, inv_info)

res_dict = EXEC_ACT(ACT_API.strToDict, api_response)

data = EXEC_ACT(ACT_API.decryptDatab2b2, res_dict['Data'])

print(data)


INV_INFO_CSV1 = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'APPSDKORDER', CASE_NAME, 'Keyexchange.csv')

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



# QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'APPSDKORDER', CASE_NAME, 'Query.csv')
#
# query_info = EXEC_ACT(ACT_API.genOrderRequestInfoTokenQuery, QUERY_INFO_CSV, data,data1)
#
# data3 = EXEC_ACT(ACT_API.encryptDatapppsdk, data,data2)
#
# print data3


INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'APPSDKORDER', CASE_NAME, 'Query.csv')

inv_info = EXEC_ACT(ACT_API.genOrderRequestInfoOrder, INV_INFO_CSV,data,data1)

data3 = EXEC_ACT(ACT_API.encryptDatapppsdk, data1,data2)


api_response = EXEC_ACT(ACT_API.genPostRequestToAPIkeyexchangeorder, inv_info,data3,data2)

print('12345666666')

print(api_response)

res_dict = EXEC_ACT(ACT_API.strToDict, api_response)

print(res_dict)


VERIFY(VER_API.verifyResponseValuesb2b, CASE_NAME,res_dict)


# data = EXEC_ACT(ACT_API.decryptDatab2b2, res_dict['Data'])
# print '123566'
# print data


# VERIFY
# VERIFY(VER_API.verifyStatusResult, res_dict, CASE_NAME)


#VERIFY(VER_API.verifyResponseValuesforApp, res_dict, CASE_NAME, 'success')
time.sleep(3)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)


