import datetime
import os
import re
import sys
import argparse
import re
from configparser import ConfigParser
import LibGeneral.funcGeneral as funcGen
import LibGeneral.GetConfigValue as getConf
import subprocess
import time
from LibGeneral.AddLog import customLog


def checkUserInfo():
    all_sections = UCONF._sections
    for secname in list(all_sections.keys()):
        all_sections[secname].__delitem__('__name__')
        s = all_sections[secname]
        for k in list(s.keys()):
            if not s[k]:
                print("Setting '%s' is not defined! (%s)" % (k, USERINFO_CONF_PATH))
                return False
    return True
        


def eraseUserInfo():
    with open(USERINFO_CONF_PATH, mode='r') as s:
        with open (USERINFO_TMP, mode='w') as d:
            for line in s:
                d.write(re.sub('=.*$', '=', line))
            d.close()
        s.close()
    os.remove(USERINFO_CONF_PATH)
    funcGen.fncopyfile(USERINFO_TMP, USERINFO_CONF_PATH)
    os.remove(USERINFO_TMP)



PJOIN = os.path.join
CONF = getConf.getConfig()
ROOTDIR = CONF.getRootDir() 
LOG_FOLDER = PJOIN(ROOTDIR, 'Logs')
USERINFO_CONF_PATH = PJOIN(ROOTDIR, 'Conf', 'UserInfo.ini')
USERINFO_TMP = PJOIN(ROOTDIR, 'Conf', 'UserInfo.tmp')
UCONF = ConfigParser(dict_type=dict)
UCONF.optionxform = str
UCONF.read(USERINFO_CONF_PATH)
TASK_EXE = PJOIN(ROOTDIR, 'Utility', 'ExecTestTask.py')
PROC = subprocess

if checkUserInfo():
    print('EXEC Allpay Production testing...')
    PROC.Popen(['python.exe', TASK_EXE, '--pkg', 'Chrome', '--testset', 'AllpayProduction'], shell=False).wait()
    eraseUserInfo()


