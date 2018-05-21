#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 15:30
# @Author  : Peter Yang
# @Contact : 13yhyang1@gmail.com
# @File    : config.py

import os
import subprocess

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    # 从系统环境变量获取key,运行前先export一下
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGODB_SETTING = {
        'db': 'dev',
        'host': 'localhost',
        'port': 27017
    }


class ProductionConfig(BaseConfig):
    DEBUG = True
    MONGODB_SETTING = {
        'db': 'music',
        'host': 'localhost',
        'port': 27017
    }