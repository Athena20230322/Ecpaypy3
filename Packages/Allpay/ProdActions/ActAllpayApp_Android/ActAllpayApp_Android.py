import os
import MobileOperate.modMobileOperate as MOP
from selenium.common.exceptions import NoSuchElementException


UIAct = MOP.ClassMobileOperate()

def ActAndroidAppLogin():
    try:
        UIAct.clickAppElement('id', '/welcome_btn_login')

    except NoSuchElementException:
        print('Element not found')
        
ActAndroidAppLogin()