# -*- coding: utf-8 -*-


#Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActEmbeddedCreatePaymentWeb import actEmbeddedcreatepaymentweb
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedCreatePaymentWeb import verifyEmbeddedcreatepaymentweb

from ECpay.ProdActions.ActECpayAPI.ActEmbeddedtoken import actEmbeddedtoken
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedtoken import verifyEmbeddedtoken


from ECpay.ProdActions.ActECpayAPI.ActEmbedded import actEmbedded
from ECpay.Verification.VerifyECpayAPI.VerifyEmbedded import verifyEmbedded

from ECpay.ProdActions.ActECpayAPI.ActEmbeddedPayToken import actEmbeddedpaytoken
from ECpay.Verification.VerifyECpayAPI.VerifyEmbeddedPayToken import verifyEmbeddedpaytoken


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
ACT_API = actEmbeddedcreatepaymentweb()
VER_API = verifyEmbeddedcreatepaymentweb()

ACT_API1 = actEmbeddedtoken()
VER_API1 = verifyEmbeddedtoken()
ACT_API2 = actEmbedded()
VER_API2 = verifyEmbedded()
ACT_API3 = actEmbeddedpaytoken()
VER_API3 = verifyEmbeddedpaytoken()
ACT_API5 = actEmbeddedpaytoken()
VER_API5 = verifyEmbeddedpaytoken()

#Testing exec


INV_INFO_CSV2 = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedCreatePaymentWeb', CASE_NAME, 'Tokenget.csv')

print('6563535')
inv_info = EXEC_ACT(ACT_API1.genOrderRequestInfoThreeD2, INV_INFO_CSV2)



api_response = EXEC_ACT(ACT_API1.genPostRequestToAPI, inv_info)
res_dict = EXEC_ACT(ACT_API1.strToDict, api_response)

data8 = EXEC_ACT(ACT_API1.decryptDatab2b2, res_dict['Data'])

print("1232413413531")

print(data8)

print("1232413413533")





INV_INFO_CSV1 = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedCreatePaymentWeb', CASE_NAME, 'Keyexchange.csv')

info1 = EXEC_ACT(ACT_API2.genOrderRequestInfoKeyExchange, INV_INFO_CSV1)

api_response = EXEC_ACT(ACT_API2.genPostRequestToAPIkeyexchange,info1)


data1 = EXEC_ACT(ACT_API2.decryptDatapppsdk,api_response )
print(data1)

res_dict1 = EXEC_ACT(ACT_API2.strToDict, api_response)
print(res_dict1)

data2 = EXEC_ACT(ACT_API2.decryptDatab2b, res_dict1['Data'],data1)
print('12222')
print(data2)
print('22333')



QUERY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedCreatePaymentWeb', CASE_NAME, 'Query.csv')

time.sleep(3)

query_info = EXEC_ACT(ACT_API5.genOrderRequestInfoTokenQueryPlus, QUERY_INFO_CSV, data8,data1)

data3 = EXEC_ACT(ACT_API5.encryptDatapppsdkn, data1,data2)
print(data3)

query_rtn = EXEC_ACT(ACT_API5.genPostRequestToAPIQuery, query_info,data3,data2)
print('9999')
print(query_rtn)
#query_rtn_dict = EXEC_ACT(ACT_API.strToDict, query_rtn)

data5 = EXEC_ACT(ACT_API5.decryptDatarsa,query_rtn )
print(data5)


datam = EXEC_ACT(ACT_API1.decryptDatab2b2, inv_info['Data'])

INV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'EmbeddedCreatePaymentWeb', CASE_NAME, 'GetCreatepayment.csv')



inv_info1 = EXEC_ACT(ACT_API.genOrderRequestInfoCreatePaymentWeb, INV_INFO_CSV,data5,datam)
print('64567474')

api_response = EXEC_ACT(ACT_API.genPostRequestToAPI, inv_info1)

res_dict = EXEC_ACT(ACT_API.strToDict, api_response)

print('5265465765676')

data8 = EXEC_ACT(ACT_API1.decryptDatab2b2, res_dict['Data'])
#data = EXEC_ACT(ACT_API.decryptDatab2b2, res_dict['Data'])

print(data8)





VERIFY(VER_API.verifyResponseValuesforcreatepaymentOrd,CASE_NAME,data8)
time.sleep(3)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)
