# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssueb2c import actInvIssueb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueb2c import verifyInvIssueb2c
from ECpay.ProdActions.ActECpayAPI.ActInvIssueInvalidb2c import actInvIssueInvalidb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueInvalidb2c import verifyInvIssueInvalidb2c
# from ECpay.ProdActions.ActECpayAPI.ActInvAllowance import actInvAllowance
# from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowance import verifyInvAllowance
# from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceInvalid import actInvAllowanceInvalid
# from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowanceInvalid import verifyInvAllowanceInvalid
from ECpay.ProdActions.ActECpayAPI.ActInvNotifyb2c import actInvNotifyb2c
from ECpay.Verification.VerifyECpayAPI.VerifyInvNotifyb2c import verifyInvNotifyb2c


#(DO NO Edit) Static declare

ARGP = argparse.ArgumentParser(description='Script for exec test.')
ARGP.add_argument('--logdir', type=str, help='Specify the log dir')
ARGP.add_argument('--package', type=str, help='Specify the package name')
ARGP.add_argument('--runid', type=str, default='', help = 'Specify the runtime guid for this run.')
ARGS = ARGP.parse_args()
LOG_DIR = ARGS.logdir
PKG = ARGS.package
RUN_UID = ARGS.runid
CASE_NAME = str(os.path.basename(__file__)).rstrip('.py')
SUM_LOG = os.path.join(LOG_DIR, CASE_NAME, 'Summary.log')
HELPER = classTestHelper(SUM_LOG)
# DRIVER = clsWebDriverHelper().initWebDriver(PKG)
ROOTDIR = HELPER.rootdir
EXEC_ACT = HELPER.execTestAction
VERIFY = HELPER.execTestVerify

# Declare feature testing instances
ACT_ISS_API = actInvIssueb2c()
VER_ISS_API = verifyInvIssueb2c()
ACT_ISSIV_API = actInvIssueInvalidb2c()
VER_ISSIV_API = verifyInvIssueInvalidb2c()
# ACT_ALL_API = actInvAllowance()
# VER_ALL_API = verifyInvAllowance()
# ACT_ALLIV_API = actInvAllowanceInvalid()
# VER_ALLIV_API = verifyInvAllowanceInvalid()
ACT_API = actInvNotifyb2c()
VER_API = verifyInvNotifyb2c()

# Testing exec

# precondition-Issue

ISS_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotifyb2c', 'Initial_Data', 'InvIssue.csv')

# exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']
#
# revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

iss_info = EXEC_ACT(ACT_ISS_API.genOrderRequestInfoB2c, ISS_INFO_CSV)

data1 = EXEC_ACT(ACT_ISS_API.decryptDatab2c, iss_info['Data'])

iss_info_res = EXEC_ACT(ACT_ISS_API.genPostRequestToAPI, iss_info)

iss_res_dict = EXEC_ACT(ACT_ISS_API.strToDict, iss_info_res)

data = EXEC_ACT(ACT_ISS_API.decryptDatab2c, iss_res_dict['Data'])
print(data)


# precondition-Issue Verify

VERIFY(VER_ISS_API.verifyColumn, 'InvIssueb2c_RAT_0001',data)

# precondition-IssueInvalid

ISSIV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotifyb2c', 'Initial_Data', 'InvIssueInvalid.csv')

revert_list = ['Reason']

issiv_info = EXEC_ACT(ACT_ISSIV_API.genOrderRequestInfoB2c, ISSIV_INFO_CSV,data,data1)

issiv_info_res = EXEC_ACT(ACT_ISSIV_API.genPostRequestToAPIb2c, issiv_info)

print('Issiv_info_res: ', issiv_info_res)

res_dict = EXEC_ACT(ACT_ISSIV_API.strToDict, issiv_info_res)


data = EXEC_ACT(ACT_ISSIV_API.decryptDatab2c, res_dict['Data'])
print(data)

# precondition-IssueInvalid Verify

VERIFY(VER_ISSIV_API.verifyColumn, 'InvIssueInvalidb2c_RAT_0001',data)


# InvNotify

NOTIFY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotifyb2c', CASE_NAME, 'OrderInfo.csv')

revert_args = ['NotifyMail']

notify_info = EXEC_ACT(ACT_API.genOrderRequestInfoB2c, NOTIFY_INFO_CSV, data)

notify_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, notify_info)

notify_res_dict = EXEC_ACT(ACT_API.strToDict, notify_info_res)

# InvNotify Verify

VERIFY(VER_API.verifyInvNotifyRequestInfob2c, CASE_NAME,data)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)