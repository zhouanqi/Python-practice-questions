#!/usr/bin/python 
# -*- coding: utf-8 -*- 

import selenium
import time
import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def aotulogin():
    url = 'https://passport.lagou.com/login/login.html?ts=1528767630158&serviceId=lagou&service=https%3A%2F%2Fwww.lagou.com%2F&action=login&signature=074A3727AC575DBFF567FBE036F6216B'

    print('正在登录，请稍候...')

    optins = Options()
    optins.add_argument('-headless')

    driver = webdriver.Firefox(firefox_options=optins)
    driver.get(url)

    
    usertf = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-propertyname="username"]/input'))
    )        

    passtf = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-propertyname="password"]/input'))
    )

    loginbt = driver.find_element_by_xpath('//div[@data-propertyname="submit"]/input')
    usertf.send_keys(config.lagou_user)
        
    time.sleep(0.2)

    passtf.send_keys(config.lagou_psw)

    time.sleep(0.2)

    loginbt.click()

    time.sleep(0.2)

    try:
        #假如账号密码有误
        valid_msg = driver.find_element_by_xpath('//span[@data-valid-message=""]')
        print(valid_msg.get_attribute('innerHTML'))
        print('请在user.json中检查')
        driver.quit()
        return
    except Exception as e:
        pass
        
    print('登录成功')
    return driver
    
                
def send_resume(driver, arr):
    
    if len(arr) == 0:
        return

    url_detail = 'https://www.lagou.com/jobs/'+str(arr[0])+'.html'
    driver.get(url_detail)

    resume_btn = driver.find_element_by_xpath('//div[@class="resume-deliver"]/a')

    text = resume_btn.get_attribute('innerHTML')
    if '已' in text:
        print('已投递过: ', arr[0])
        arr.remove(arr[0])
        send_resume(driver, arr)
        driver.quit()
        
    else:
        resume_btn.click()
        print('发现目标，点击投递')
        time.sleep(1)

        #尝试获取弹窗
        try:
            cbox_loaded = driver.find_element_by_xpath('//*[@id="cboxLoadedContent"]')
        except Exception as e:
            print('获取弹窗失败: ', e)
            #没有弹窗返回
            return

        #切换当前window
        
        now = driver.current_window_handle
        driver.switch_to_window(now)

        try:
            #弹出不匹配岗位窗口
            btn = driver.find_element_by_xpath('//div[@id="cboxContent"]//table//td/a[@class="btn"]')
            btn.click()
            print('发现不匹配窗口, 点击确认投递')
        except Exception as e:
            #超时／获取不到异常不处理，继续往下走
            pass

        time.sleep(0.2)

        try:
            #弹出达到投递上限
            cancel_btn = driver.find_element_by_xpath('//div[@id="cboxContent"]//table//td/a[@class="upper_close"]')
            cancel_btn.click()
            print('发现达到投递上限窗口, 点击取消并退出')
            return
        except Exception as e:
            pass
                
        #递归请求，只有成功投递才能出来   
        send_resume(driver, arr)
