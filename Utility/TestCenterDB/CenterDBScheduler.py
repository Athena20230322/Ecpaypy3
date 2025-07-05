from TestCenterDB.CenterDB import scheduleTask
import time

i = 0
CDB = scheduleTask()

while i == 0:
    CDB.ExecScheduleJob()
    time.sleep(33)
    