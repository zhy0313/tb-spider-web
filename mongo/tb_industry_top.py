#!/usr/bin/env python
# -*-  coding: utf-8 -*-

import pymongo

client = pymongo.MongoClient("mongodb://192.168.100.101:27017")
db = client['tb']
tb_industry_top = db['tb_industry_top']


def insert(item):
    """
    新增行业排行记录
    """
    tb_industry_top.insert(item)


def update_flow(item):
    """
    依照 id 和 day 属性更新行业排行记录流量数据
    """
    tb_industry_top.update({
        "id": item['id'],
        "day": item['day']
    }, {
       "$set": {
           "flow": item['flow']
       }
    })


def find_day(day):
    cursor = tb_industry_top.find({
        "day": day
    }, {"_id": 0})
    result = []
    for i in cursor:
        result.append(i)
    return result



def find_between(start_time: int, end_time: int):
    """
    查找 [start_time, end_time] 的行业数据
    :param start_time: int 
    :param end_time: int
    """
    cursor = tb_industry_top.find({
            "ts": {"$gt": start_time, "$lt": end_time}
        }, {"_id": 0})
    result = []
    for i in cursor:
        result.append(i)
    return result
    






