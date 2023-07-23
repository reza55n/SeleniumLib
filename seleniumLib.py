waitTimeout = 75  # seconds - Sometimes some countries' websites are slow!


import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])

import_or_install("selenium")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import datetime
import math



def logAdd(text, time = False, fileName = 'out.txt'):
    f = open(fileName, "a", encoding='utf-8')
    if time:
        text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\t" + text
    f.write(text + "\n")
    f.close()



def fillTextSelector(driver, selector, text):
    e = driver.find_elements(By.CSS_SELECTOR,selector)
    if len(e) == 0:
        return False
    else:
        e[0].clear()
        e[0].send_keys(text)
        return True

def submitSelector(driver, selector):
    e = driver.find_elements(By.CSS_SELECTOR,selector)
    if len(e) == 0:
        return False
    else:
        e[0].submit()
        return True

def clickSelector(driver, selector):
    e = driver.find_elements(By.CSS_SELECTOR,selector)
    if len(e) == 0:
        return False
    else:
        e[0].click()
        return True



def send_global_key(driver, key):
    driver.find_element(By.TAG_NAME,'body').send_keys(key)



# Checks if element contains intended text
# parent: driver or element
def find_element_by_text(parent, selector, text):
    e = parent.find_elements(By.CSS_SELECTOR,selector)
    for ee in e:
        if text in ee.text:
            return ee
    return False

# Checks if element's text is same as intended text
# parent: driver or element
def find_element_by_text_whole(parent, selector, text):
    e = parent.find_elements(By.CSS_SELECTOR,selector)
    for ee in e:
        if text == ee.text:
            return ee
    return False

# Uses browser's JS to find element.
# Usage: js_scroll_offseted
# retJsElemName: A desired name
# text (optional): If entered, searches inside found elements
def js_find_element_by_selector_text_whole(driver, retJsElemName, parentSelector, selector, text = ''):
    if text == '':
        driver.execute_script("window." + retJsElemName
            + "=document.querySelector('" + parentSelector + "').querySelector(\"" + selector + "\")")
        
    else:
        driver.execute_script("window.js_selenium_temp=document.querySelector('"
            + parentSelector + "').querySelectorAll(\"" + selector + "\")")
        
        driver.execute_script("for(var i=0;i<js_selenium_temp.length;i++)"
            + "{if(js_selenium_temp[i].textContent==" + text + "){window."
            + retJsElemName + "=js_selenium_temp[i];return;}}")



# Sometimes offset is needed to make element visible and clickable
# Also jsElemName can be something like this: "$('.btn-success')[0]"
def js_scroll_offseted(driver, jsElemName, offset = 100):
    driver.execute_script(jsElemName + ".scrollIntoView(); window.scrollBy(0," + str(-offset) + ");")



# Tip: You can use method `sleep([sec])`, along with below methods.

def waitTitleGone(driver, old_title):
    WebDriverWait(driver, waitTimeout).until_not(EC.title_contains(old_title))

def waitNewTitle(driver, new_title):
    WebDriverWait(driver, waitTimeout).until(EC.title_contains(new_title))

def waitElementGone(driver, selector):
    WebDriverWait(driver, waitTimeout).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

def waitElementHidden(driver, selector):
    WebDriverWait(driver, waitTimeout).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))

def waitNewElement(driver, selector):
    WebDriverWait(driver, waitTimeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

# !! Tip: Method `element_to_be_clickable` practically only checks existence (and visibility),
#         not being clickable! You can use waitElementGone for hovering element, after this method.
def waitElementClickable(driver, selector):
    WebDriverWait(driver, waitTimeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))

def waitTextGone(driver, text, selector = 'body'):
    WebDriverWait(driver, waitTimeout).until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text))

def waitNewText(driver, text, selector = 'body'):
    WebDriverWait(driver, waitTimeout).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text))



# strategy: normal, eager, none - In new version of Selenium, desired_capabilities was deprecated and there was no time to re-implement `strategy`. ...
# ... Also `normal` strategy seems to be safer
def runFirefox(strategy = 'normal'):
    options = Options()
    options.binary_location=r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(options=options)
    return driver
