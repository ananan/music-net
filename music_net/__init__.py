#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 15:21
# @Author  : Peter Yang
# @Contact : 13yhyang1@gmail.com
# @File    : __init__.py

from music_net import config
from flask import Flask


app = Flask(__name__)
app.config.from_object(config)
