# -*- coding: utf-8 -*-


# Static Import Area
import argparse
from LibGeneral.TestHelper import classTestHelper
from SeleniumHelper.SeleniumHelper import clsWebDriverHelper
import time
import os

#Feature related test package import
from ECpay.ProdActions.ActECpayAPI.ActInvIssue import actInvIssue
from ECpay.Verification.VerifyECpayAPI.VerifyInvIssue import verifyInvIssue
# from ECpay.ProdActions.ActECpayAPI.ActInvIssueInvalid import actInvIssueInvalid
# from ECpay.Verification.VerifyECpayAPI.VerifyInvIssueInvalid import verifyInvIssueInvalid
from ECpay.ProdActions.ActECpayAPI.ActInvAllowance import actInvAllowance
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowance import verifyInvAllowance
from ECpay.ProdActions.ActECpayAPI.ActInvAllowanceInvalid import actInvAllowanceInvalid
from ECpay.Verification.VerifyECpayAPI.VerifyInvAllowanceInvalid import verifyInvAllowanceInvalid
from ECpay.ProdActions.ActECpayAPI.ActInvNotify import actInvNotify
from ECpay.Verification.VerifyECpayAPI.VerifyInvNotify import verifyInvNotify


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
ACT_ISS_API = actInvIssue()
VER_ISS_API = verifyInvIssue()
# ACT_ISSIV_API = actInvIssueInvalid()
# VER_ISSIV_API = verifyInvIssueInvalid()
ACT_ALL_API = actInvAllowance()
VER_ALL_API = verifyInvAllowance()
ACT_ALLIV_API = actInvAllowanceInvalid()
VER_ALLIV_API = verifyInvAllowanceInvalid()
ACT_API = actInvNotify()
VER_API = verifyInvNotify()

# Testing exec

# precondition-Issue

ISS_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotify', 'Initial_Data', 'InvIssue.csv')

exclusive_list = ['InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

revert_list = ['CustomerName', 'CustomerAddr', 'CustomerEmail', 'InvoiceRemark', 'ItemName', 'ItemWord', 'ItemRemark']

iss_info = EXEC_ACT(ACT_ISS_API.genOrderRequestInfo, ISS_INFO_CSV, exclusive_list, revert_list)

iss_info_res = EXEC_ACT(ACT_ISS_API.genPostRequestToAPI, iss_info)

iss_res_dict = EXEC_ACT(ACT_ISS_API.strToDict, iss_info_res)

# precondition-Issue Verify

VERIFY(VER_ISS_API.verifyColumn, iss_res_dict, 'InvIssue_RAT_0001')

'''
# precondition-IssueInvalid

ISSIV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotify', 'Initial_Data', 'InvIssueInvalid.csv')

revert_list = ['Reason']

issiv_info = EXEC_ACT(ACT_ISSIV_API.genOrderRequestInfo, ISSIV_INFO_CSV, iss_res_dict['InvoiceNumber'], revert_list)

issiv_info_res = EXEC_ACT(ACT_ISSIV_API.genPostRequestToAPI, issiv_info)

print 'Issiv_info_res: ', issiv_info_res

issiv_res_dict = EXEC_ACT(ACT_ISSIV_API.strToDict, issiv_info_res)

# precondition-IssueInvalid Verify

VERIFY(VER_ISSIV_API.verifyColumn, issiv_res_dict, 'InvIssueInvalid_RAT_0001')

'''

# precondition-Allowance

ALL_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotify', 'Initial_Data', 'InvAllowance.csv')

exclusive_list = ['ItemName', 'ItemWord']

revert_list = ['CustomerName', 'NotifyMail', 'ItemName', 'ItemWord']

all_info = EXEC_ACT(ACT_ALL_API.genOrderRequestInfo, ALL_INFO_CSV, iss_res_dict, exclusive_list, revert_list)

all_info_res = EXEC_ACT(ACT_ALL_API.genPostRequestToAPI, all_info)

all_res_dict = EXEC_ACT(ACT_ALL_API.strToDict, all_info_res)

# precondition-Allowance Verify

VERIFY(VER_ALL_API.verifyColumn, all_res_dict, 'InvAllowance_RAT_0001')

# precondition-AllowanceInvalid

ALLIV_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotify', 'Initial_Data', 'InvAllowanceInvalid.csv')

exclusive_list = ['Reason']

revert_list = ['Reason']

alliv_info = EXEC_ACT(ACT_ALLIV_API.genOrderRequestInfo, ALLIV_INFO_CSV, all_res_dict, exclusive_list, revert_list)

alliv_info_res = EXEC_ACT(ACT_ALLIV_API.genPostRequestToAPI, alliv_info)

alliv_res_dict = EXEC_ACT(ACT_ALL_API.strToDict, alliv_info_res)

# precondition-AllowanceInvalid Verify

VERIFY(VER_ALLIV_API.verifyColumn, alliv_res_dict, 'InvAllowanceInvalid_RAT_0001')

# InvNotify

NOTIFY_INFO_CSV = os.path.join(ROOTDIR, 'Test_Data', 'ECpayAPI', 'InvNotify', CASE_NAME, 'OrderInfo.csv')

revert_args = ['NotifyMail']

notify_info = EXEC_ACT(ACT_API.genOrderRequestInfo, NOTIFY_INFO_CSV, all_res_dict, revert_args)

notify_info_res = EXEC_ACT(ACT_API.genPostRequestToAPI, notify_info)

notify_res_dict = EXEC_ACT(ACT_API.strToDict, notify_info_res)

# InvNotify Verify

VERIFY(VER_API.verifyInvNotifyRequestInfo, notify_res_dict, CASE_NAME)

# (DO NO Edit) Result processing
HELPER.processResult(caserun_uid=RUN_UID)