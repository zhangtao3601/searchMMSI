from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException
import time
import fileinput

import datetime

driver = webdriver.Chrome()   #打开chrome浏览器
driver.get('http://www.shipxy.com')   #chrome浏览器转至船讯网网站
wait = WebDriverWait(driver,10)

while True:
    report = open(datetime.date.today().isoformat() + r'.txt','a')
    report.write('---------------------------------------我是分割线-----------------------------------\n')
    report.write(datetime.datetime.now().isoformat())
    report.write("更新\n\n")
    for mmsi_shipname in fileinput.input(files = 'mmsi.csv'):
        for i in range(3):
            try:
                mmsi = mmsi_shipname.split(',')[1]
                shipname = mmsi_shipname.split(',')[0]
                element_MMSI = wait.until(EC.presence_of_element_located((By.ID,"txtKey")))
                element_MMSI.clear()
                element_MMSI.send_keys(mmsi)

                element_butnQuery = wait.until(EC.visibility_of_element_located((By.ID,"butnQuery")))
                time.sleep(1)
                element_butnQuery.click()

                element_si_mmsi = wait.until(EC.visibility_of_element_located((By.ID,"si_mmsi")))
                time.sleep(1)
                
                si_mmsi_title = element_si_mmsi.text
                if si_mmsi_title == mmsi.strip('\n'):
                    element_time = wait.until(EC.visibility_of_element_located((By.ID,"si_lastTime")))
                    time.sleep(1)
                    
                    report.write(shipname + ' mmsi:' + mmsi.strip('\n')+' 于')
                    report.write(element_time.get_attribute('title') )
                    
                    report.write(' 航迹向'+driver.find_element_by_id('si_course').text)
                                
                    report.write(' 航速'+driver.find_element_by_id('si_speed').text)
                                
                    report.write(' 纬度'+driver.find_element_by_id('si_lat').text)
                                
                    report.write(' 经度'+driver.find_element_by_id('si_lng').text)
                    report.write('\n\n\n')
                    #report.close()
                    break;
            except TimeoutException as err1:
                print(datetime.datetime.now())
                print(mmsi)
                print(format(err1))
            finally:                
                #report.close()                
                print('finally')
    report.close()
    time.sleep(10)
