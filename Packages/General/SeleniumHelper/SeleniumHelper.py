import os
import LibGeneral.funcGeneral as funcGen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

PJOIN = os.path.join


class clsWebDriverHelper():
    def __init__(self):
        tmp = ''


    
    def initWebDriver(self, browser):
        self.browser = browser

        br = self.browser
        br = 'Chrome'
        if br == 'IE':
            self.drv = webdriver.Ie()
        elif br == 'Chrome':
            chrome_options = Options()


            #chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920x3000")
            #chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--hide-scrollbars")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("blink-settings=imagesEnabled=false")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_argument("--disable-javascript")




            self.drv = webdriver.Chrome(executable_path='D:\ECpayAutoFramework\Packages\chromedriver.exe', chrome_options=chrome_options)
            #self.drv = webdriver.Chrome(executable_path='/home/shihyu/chromedriver', chrome_options=chrome_options)
        elif br == 'Firefox':
            self.drv= webdriver.Firefox()
        elif br == 'Edge':
            self.drv = webdriver.Edge()
        elif br == 'mChrome':

            mobileEmulation = {'deviceName': 'iPhone 6'}
            options = webdriver.ChromeOptions()
            options.add_argument('blink-settings=imagesEnabled=false')
            options.add_experimental_option('mobileEmulation', mobileEmulation)

            self.drv = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
        else:
            err_msg = "Specified browser is not supported."
            raise ValueError(err_msg)
        return self.drv

    def initWebDriverHilife(self, browser):
        self.browser = browser

        br = self.browser
        if br == 'IE':
            self.drv = webdriver.Ie()
        elif br == 'Chrome':
            chrome_options = Options()

            #chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920x3000")
            # chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--hide-scrollbars")
            chrome_options.add_argument("blink-settings=imagesEnabled=false")
            # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_argument("-first run")
            chrome_options.add_argument("--disable-javascript")

            self.drv = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
        elif br == 'Firefox':
            self.drv = webdriver.Firefox()
        elif br == 'Edge':
            self.drv = webdriver.Edge()
        elif br == 'mChrome':

            mobileEmulation = {'deviceName': 'iPhone 6'}
            options = webdriver.ChromeOptions()
            options.add_argument('blink-settings=imagesEnabled=false')
            options.add_experimental_option('mobileEmulation', mobileEmulation)

            self.drv = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
        else:
            err_msg = "Specified browser is not supported."
            raise ValueError(err_msg)
        return self.drv

    def minitWebDriver(self, browser):
        self.browser = browser
        br = self.browser
        if br == 'IE':
            self.drv = webdriver.Ie()
        elif br == 'Firefox':
            self.drv = webdriver.Firefox()
        elif br == 'Edge':
            self.drv = webdriver.Edge()
        elif br == 'Chrome':

            mobileEmulation = {'deviceName': 'iPhone 6'}
            options = webdriver.ChromeOptions()
           # options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--incognito")
            options.add_argument("blink-settings=imagesEnabled=false")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('mobileEmulation', mobileEmulation)
            self.drv = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
        elif br == 'mChrome':
            mobileEmulation = {'deviceName': 'iPhone 6'}
            options = webdriver.ChromeOptions()
           # options.add_argument('blink-settings=imagesEnabled=false')
           # options.add_argument("--headless")
            options.add_experimental_option('mobileEmulation', mobileEmulation)
            self.drv = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
        else:
            err_msg = "Specified browser is not supported."
            raise ValueError(err_msg)
        return self.drv

    def genElemScreenshot(self, drv, elem, folderpath):
        gen_uuid = funcGen.genRandomUuid
        size = elem.size
        location = elem.location
        print (size)
        print (location)
        scr_fname = gen_uuid(with_dash=False)
        scr_file = '.'.join(('scrnshot_' + scr_fname, 'png'))
        scr_fullpath = PJOIN(folderpath, scr_file)
        drv.save_screenshot(scr_fullpath)
        scr = Image.open(scr_fullpath)
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        output = scr.crop((left, top, right, bottom))
        out_file = '.'.join(('Elem_' + scr_fname, 'png'))
        out_fullpath = PJOIN(folderpath, out_file)
        output.save(out_fullpath)
        return out_fullpath
