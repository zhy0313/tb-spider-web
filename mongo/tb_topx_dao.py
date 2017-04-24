#!/usr/bin/env python
# -*-  coding: utf-8 -*-
# author = xm

import pymongo
from mongo.config import DB

tb_topx = DB['tb_topx']


def find_day(day):
    cursor = tb_topx.find({
        'day': day
    },{
        "_id": 0
    })
    result = []
    for i in cursor:
        result.append(i)
    return result
