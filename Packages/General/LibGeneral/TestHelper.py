import LibGeneral.AddLog as Addlog
import LibGeneral.funcGeneral
import LibGeneral.GetConfigValue as getConf
from configparser import ConfigParser

import configparser as configparser
from TaskDB.ClassTaskDB import classTaskDB
from loguru import logger
import prettytable
import PyDataSet.pyDataSet as Pyds
import os
import sys


PJOIN = os.path.join

class classTestHelper():
    def __init__(self, result_log_path=''):
    #def __init__(self):
        self.conf = getConf.getConfig()
        self.rootdir = self.conf.getRootDir()
        self.test_data_root = PJOIN(self.rootdir, 'Test_Data')
        self.ds = Pyds.classPyDataSet()
        self.log = Addlog.customLog()
        self.log.createLogger(result_log_path)
        self.pt = prettytable.PrettyTable
        self._exec_result = []
        self._1stfailmsg = ''
        self.taskdbfile = PJOIN(self.rootdir, 'Utility', 'DB', 'TestTaskDB.db')
        self.tdb = classTaskDB(self.taskdbfile)
        
    @property
    def frame_rootdir(self):
        return self.rootdir
    
    @property
    def exec_result(self):
        return self._exec_result
    
    def getFeatureTestSetting(self, setting_sec, feature_cat='', feature_name=''):
        if feature_name != '' and feature_cat != '':
            setting_file = feature_name + '.ini'
            ini_path = PJOIN(self.test_data_root, feature_cat, feature_name, 'Initial_Data', setting_file)
            setting = ConfigParser()
            setting.optionxform = str
            setting.read(ini_path)
            if setting.has_section(setting_sec):
                all_sections = setting._sections
                rtn_dict = all_sections[setting_sec]
                return rtn_dict
            else:
                raise ValueError("getFeatureTestSetting: Specified 'setting_sec' not found in target ini file.")
        else:
            raise ValueError("getFeatureTestSetting: Parameter 'feature_name' or 'feature_cat' not specified.")
        
    def getTestDataIniSections(self, *path_args):
        ini_path = PJOIN(self.test_data_root, *path_args)
        setting = ConfigParser(dict_type=dict)
        setting.optionxform = str
        setting.read(ini_path) 

        all_sections = setting._sections
        #for sec in all_sections.keys():
        #    all_sections[sec].__delitem__('__name__')

        return all_sections


    
    def initialTest(self, module_name):
        pass
    
    def getCustomUserInfo(self):
        usr_info = os.path.join(self.rootdir, 'Conf', 'UserInfo.ini')
        conf = ConfigParser()
        conf.read(usr_info)
        ret_dict = {}
        ret_dict['CARD'] = conf.get('CardInfo', 'CardNo')
        ret_dict['CVV'] = conf.get('CardInfo', 'CVV')
        ret_dict['EXPM'] = conf.get('CardInfo', 'ExpireMM')
        ret_dict['EXPY'] = conf.get('CardInfo', 'ExpireYY')
        ret_dict['USRN'] = conf.get('UserAccount', 'Username')
        ret_dict['PW'] = conf.get('UserAccount', 'Password')
        ret_dict['MERCID'] = conf.get('TradeInfo', 'MerchantID')

        return ret_dict
    
    def addLogRecord(self, level, msg):
        if level == 'DEBUG':
            self.log.DEBUG(msg)
        elif level == 'INFO':
            self.log.INFO(msg)
        elif level == 'ERROR':
            self.log.ERROR(msg)
        elif level == 'WARN':
            self.log.WARN(msg)
        elif level == 'EXCEPT':
            self.log.EXCEPT(msg)
        else:
            raise ValueError('Specified log level is not supported. Level : %s' % (level))
        
    def getDevicePlatform(self, friendlyname, datasource='csv'):
        if datasource == 'csv':
            print ('get device platform from csv file')
            device_list_file = PJOIN(self.rootdir, 'Conf', 'DeviceList.csv')

            devlist = self.ds.importCSV(device_list_file)
            match = ("Device_Frendly_Name='%s'" % (friendlyname),)
            platform = self.ds.queryDataSet(devlist, target=('Platform',), criteria=match, 
                                      withHeader=False)
            return platform[0][0]
        elif datasource == 'db':
            print ('get device platform from test central database')
            
    def generateElemDataset(self, csv_path):
        elem_ds = self.ds.importCSV(csv_path)
        return elem_ds
    
    def getElemIdentFromDataSet(self, name, elem_ds):
        self.log.INFO("Query element name %s from dataset %s ..." % (name, elem_ds))
        ident_set = self.ds.queryDataSet(elem_ds, ['Element_identifier', 'Type'], ["Name = '%s'" % name], withHeader=False)
        if len(ident_set) > 1:
            msg = "getElemIdentFromDataSet : Queried result contains two or more records, element 'Name' might duplicate in dataset source CSV."
            self.log.ERROR(msg)
            raise ValueError(msg)
        elif len(ident_set) == 0:
            msg = "getElemIdentFromDataSet : Queried result contains NO records, element 'Name' provided might be not correct."
            self.log.ERROR(msg)
            raise ValueError(msg)
        elif len(ident_set) == 1:
            result_dict = {}
            result_dict['Identifier'] = ident_set[0][0]
            result_dict['Element_type'] = ident_set[0][1]
            return result_dict
        else:
            raise Exception("getElemIdentFromDataSet : Unexpected error occurs")
        
    def setFirstFailMsg(self, msg):
        if self._1stfailmsg == '':
            self.log.INFO("Processing exception message %s ..." % (repr(msg)))
            try:
                self._1stfailmsg = msg
            except UnicodeDecodeError:
                try:
                    self._1stfailmsg = msg
                except:
                    self.log.ERROR("Processing exception decoding FAIL. message %s ..." % (repr(msg)))
            else:
                self.log.INFO("Processing exception message complete.")

   
    def execTestAction(self, action_function, *func_args):
        act_name = action_function.__name__
        try:
            self.log.INFO("Start performing %s" % act_name)
            act_exec_res = action_function(*func_args)
        except Exception as err:
            msg = "Execute action [%s] FAIL. Error : %s" % (act_name, err)
            self.setFirstFailMsg(msg)
            self.log.ERROR(msg)
            self._exec_result.append("%s : Fail" % act_name)
            
        else:
            self._exec_result.append("%s : Success" % act_name)
            self.log.INFO("Execute action %s success." % act_name)
            return act_exec_res
        finally:
            pass
        
    def execTestVerify(self, verify_function, *func_args):
        verify_name = verify_function.__name__
        try:
            self.log.INFO("Start performing %s" % verify_name)
            verify_result = verify_function(*func_args)
        except Exception as err:
            msg = "Execute verify [%s] FAIL. Exception occurs. Error: %s" % (verify_name, err)
            #err = str(err)
            self.setFirstFailMsg(msg)
            self.log.ERROR(msg)
            self._exec_result.append("%s : Fail" % verify_name)
            #self.log.EXCEPT("Execute action '%s' FAIL. Error : " % (verify_name))
            #print str(err)
            #print err
            
        else:
            print((verify_result, type(verify_result)))
            if type(verify_result) is dict:
                keys = list(verify_result.keys())
                failed_point = [x for x in keys if verify_result[x] is False]
                #Descide if verification is pass
                if len(failed_point) > 0:
                    fail_msg = "%s : Fail" % (verify_name)
                    self.setFirstFailMsg(fail_msg)
                    self._exec_result.append(fail_msg)
                elif len(failed_point) == 0 and len(verify_result) > 0:
                    self._exec_result.append("%s : Success" % verify_name)
                    self.log.INFO("Execute verifacation %s success." % verify_name)
                    
                self.log.INFO("Fail point: %s " % (failed_point))
                return failed_point

            else:
                raise TypeError("execTestVerify : Retrieved verify result is not dictionary")
            
        finally:
            pass
        
    def getFirstFailPnt(self):
        pass

    def processResult(self, caserun_uid=''):
        steps_success = [x for x in self._exec_result if x.__contains__(': Success')]
        step_cnt = len(self._exec_result)
        result_table = self.pt(['Steps', 'Result'])
        if caserun_uid != '' and self._1stfailmsg != '':
            self.tdb.updateCaseMsg(caserun_uid, self._1stfailmsg)
            
        for e_r in self._exec_result:
            row = [x.strip(' ') for x in e_r.split(':')]
            result_table.add_row(row)
        
        tb_msg = "All action/verifacation execute complete, result: \n%s" % (result_table)
        self.log.INFO(tb_msg)

        if step_cnt > 0 and len(steps_success) == step_cnt:
            print ("SUCCESS!!")
            sys.exit(100)
        else:
            sys.exit(103)
        
