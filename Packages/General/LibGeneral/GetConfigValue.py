import os
import configparser


PJOIN = os.path.join
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class getConfig():
    def __init__(self):
        self.config_file = PJOIN(SCRIPT_DIR, '..', '..', '..', 'Conf', 'Settings.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        
    def getRootDir(self):
        rootdir = self.config.get('ROOT_FOLDER', 'root_dir')
        return rootdir
    
    def getLogSetting(self):
        out = {}
        out['IsConsoleOut'] = self.config.get('LOG_SETTING', 'enable_console_output')
        out['LogLevel'] = self.config.get('LOG_SETTING', 'log_level')
        out['LogDir'] = self.config.get('LOG_SETTING', 'log_folder')
        return out
    
    def getCenterDBSetting(self):
        conf = self.config
        rtn = {}
        if conf.get('TestCenterDB', 'IsSQLExpress') == 'True':
            db_host_str = '\\'.join((conf.get('TestCenterDB', 'DBHost'), 'SQLEXPRESS'))
        else:
            db_host_str = conf.get('TestCenterDB', 'DBHost')
        
        rtn['is_enable'] = conf.get('TestCenterDB', 'Enable_CenterDB')
        rtn['user'] = conf.get('TestCenterDB', 'User')
        rtn['pwd'] = conf.get('TestCenterDB', 'Password')
        rtn['hoststr'] = db_host_str
        rtn['dbn'] = conf.get('TestCenterDB', 'DBName')
        return rtn
        
    def getRtnCollectorAddr(self):
        conf = self.config
        host = conf.get('ReturnInfoCollector', 'host')
        port = conf.get('ReturnInfoCollector', 'port')
        addr = 'http://' + host + ':' + port + '/'
        return addr
    
    def getOTPCollectorAddr(self):
        conf = self.config
        host = conf.get('OTPCollector', 'host')
        port = conf.get('OTPCollector', 'port')
        addr = 'http://' + host + ':' + port + '/'
        return addr
    
