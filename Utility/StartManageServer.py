import os
import sys
import subprocess
from configparser import ConfigParser as parser
from LibGeneral.GetConfigValue import getConfig
import LibGeneral.GeneralHelper as gen_helper

PJOIN = os.path.join
FRAME_CONF = getConfig()
CONF = parser()
CONF_HELPER = gen_helper.configHelper()
ROOTDIR = FRAME_CONF.getRootDir()
SC_CONFIG_PATH = PJOIN(ROOTDIR, 'Conf', 'Agent.ini')
CONF.read(SC_CONFIG_PATH)
SVC_HELPER = gen_helper.ServiceHelper()


SVC_HELPER.startServices(CONF, rootdir=ROOTDIR)

    
    