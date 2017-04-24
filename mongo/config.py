#!/usr/bin/env python
# -*-  coding: utf-8 -*-
# author: xm

import pymongo

CLIENT = pymongo.MongoClient("mongodb://192.168.100.101:27017")
DB = CLIENT['tb']