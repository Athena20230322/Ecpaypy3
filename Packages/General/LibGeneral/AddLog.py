import logging
import os
import LibGeneral.GetConfigValue as getConf
import LibGeneral.funcGeneral as funcGen

class customLog():
    def __init__(self):
        self.conf = getConf.getConfig()
        self.rootdir = self.conf.getRootDir()
        self.log_level = self.conf.getLogSetting()['LogLevel']
        self.log_dir = self.conf.getLogSetting()['LogDir']
        self.is_console_out = self.conf.getLogSetting()['IsConsoleOut']
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')        

    def createLogger(self, path, fullpath=False):
        is_console_out = self.is_console_out
        if fullpath is True:
            self.log_file_path = path
        else:
            self.log_file_path = os.path.join(self.rootdir, self.log_dir, path)
        if len(self.logger.handlers) == 0 and path != '':
            if is_console_out == '1':
                self.shandler = logging.StreamHandler()
                self.shandler.setLevel(self.log_level)
                self.shandler.setFormatter(self.formatter)
                self.logger.addHandler(self.shandler)
                self.logger.handlers
            elif is_console_out == '0':
                pass
            else:
                raise TypeError("Setting is not an valid string: %r" % is_console_out)
            
            funcGen.testFilePath(self.log_file_path)
            self.fhandler = logging.FileHandler(self.log_file_path)
            self.fhandler.setLevel(self.log_level)
            self.fhandler.setFormatter(self.formatter)
            self.logger.addHandler(self.fhandler)
        else:
            print ("No path specified or logger already exist")
        #print "Logger: %i" % (len(self.logger.handlers))        

        
    
    def INFO(self, msg):
        self.logger.info(msg)
        
    def DEBUG(self, msg):
        self.logger.debug(msg)
        
    def ERROR(self, msg):
        self.logger.error(msg)
        
    def WARN(self, msg):
        self.logger.warning(msg)
        
    def EXCEPT(self, msg):
        self.logger.exception(msg)
    
        
    
class dummyLog():
    
    def __init__(self):
        pass
    
    def INFO(self, msg):
        pass
    
    def DEBUG(self, msg):
        pass
        
    def ERROR(self, msg):
        pass
        
    def WARN(self, msg):
        pass
        
    def EXCEPT(self, msg):
        pass
    
