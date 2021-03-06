#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/10 16:16
# @Author  : Peter Yang
# @Contact : 13yhyang1@gmail.com
# @File    : crawler.py

import os
from time import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Crawler:
    """
    selenium 爬虫基类
        1. 使用上下文管理协议控制资源的释放
        2. 运行结束后输出爬虫运行的总时间
    """
    def __init__(self, driver_path='/usr/local/bin/chromedriver', headless=False, ignore_exception=False):
        self.driver_path = driver_path
        self.headless = headless
        self.ignore_exception = ignore_exception

        if not os.path.isfile(self.driver_path):
            raise Exception(self.driver_path+'is not valid, please provide webdriver path, you can download it from: \
            https://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip')

        if headless:
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            print('The Chrome is running at Headless Mode !')
            self.browser = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chrome_options)
        else:
            print('The Chrome is running at GUI Mode !')
            self.browser = webdriver.Chrome(executable_path=self.driver_path)

        # 显式等待5秒
        self.until = WebDriverWait(self.browser, 5).until
        self.EC = EC
        self.By = By
        self.Keys = Keys
        self.TimeoutException = TimeoutException

    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('爬虫运行总时间: ', time()-self.start)
        self.browser.quit()
        # 若返回True，则压制with代码库中的异常，否则with中的异常会向上一层抛出,默认设置为False
        return self.ignore_exception


def try_again(func):
    '''selenium expected_conditions 超时异常处理，最多尝试3次'''
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except TimeoutException as e:
                print(e, '--', func.__name__, '--', i, ' try_again')
        else:
            raise Exception('try again Error: has been try 3 times but still failed !')
    return wrapper
