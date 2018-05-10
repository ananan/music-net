#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 16:26
# @Author  : Peter Yang
# @Contact : 13yhyang1@gmail.com
# @File    : db.py

from pymongo import MongoClient


class MongoDB:
    """
    MongoDB 的简单封装
    """
    def __init__(self, db, collection, host='localhost'):
        self.client = MongoClient(host, 27017)
        self.db = self.client[db]
        self.coll = self.db[collection]

    def insert(self, document):
        return self.coll.insert(document)

    def insert_many(self, documents):
        results = self.coll.insert_many(documents)
        return results.inserted_ids

    def __del__(self):
        self.client.close()

