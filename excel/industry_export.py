#!/usr/bin/env python
# -*-  coding: utf-8 -*-
# author: xm

from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from io import StringIO, BytesIO

COLS_NAME = [{"name": "id", "desc": "编号"},
             {"name": "growth_rate", "desc": "交易增长"},
             {"name": "price", "desc": "价格"},
             {"name": "shop", "desc": "店铺"},
             {"name": "sub_orders", "desc": "子订单数"},
             {"name": "url", "desc": "链接"}]

COLS_EXPAND_NAME = {
    "prefix_name":  [("手淘搜索", "手淘搜索"), ("淘内免费其他", "淘内免费其他"), ("淘宝客", "淘宝客"), ("手淘首页", "手淘首页"),
                     ("我的淘宝", "我的淘宝"), ("手淘旺信", "手淘旺信"), ("购物车", "购物车"), ("直通车", "直通车"), ("钻石展位", "钻石展位"),
                     ("钻石展位", "钻石展位")],
    "cols": [("uv", "访客数"), ("uvRate", "访客数占比"), ("pv", "浏览量"),("pvRate", "浏览量占比")]
}


def expand_names():
    result = []
    for pair in COLS_NAME:
        result.append(pair['desc'])
    for name_pair in COLS_EXPAND_NAME['prefix_name']:
        prefix = name_pair[1]
        for field in COLS_EXPAND_NAME['cols']:
            result.append(prefix+"-"+field[1])
    return result


def expand_name_values(industry_item):
    result = []
    try:
        wireless = industry_item['flow']['wireless']
    except KeyError:
        return result
    def find_wireless_item(name_):
        for item_ in wireless:
            if item_['name'] == name_:
                return item_

    for name_pair in COLS_EXPAND_NAME['prefix_name']:
        name = name_pair[0]
        item = find_wireless_item(name)
        for field in COLS_EXPAND_NAME['cols']:
            if not item:
                result.append("")
            else:
                result.append(item[field[0]])
    return result


def write_sheet_row(work_sheet, row, col, data):
    style = XFStyle()
    style.font = Font()
    work_sheet.write(row, col, data)


def create_industry_excel(industry_items):
    """
    生成行业指数数据表
    """
    work_book = Workbook(encoding="utf-8")
    work_sheet = work_book.add_sheet('sheet-1')
    # 生成列头
    cols_name = expand_names()
    for index in range(0, len(cols_name)):
        write_sheet_row(work_sheet, 0, index, cols_name[index])

    # 生成标准内容
    for index in range(0, len(industry_items)):
        item = industry_items[index]

        for col_index in range(0, len(COLS_NAME)):
            col = COLS_NAME[col_index]
            write_sheet_row(work_sheet, index + 1, col_index, item[col["name"]])
        print(item)
        expand_values = expand_name_values(item)
        cols_name_length = len(COLS_NAME)
        for col_index in range(0, len(expand_values)):
            write_sheet_row(work_sheet, index + 1, cols_name_length + col_index, expand_values[col_index])
        index = index + 1

    byte_io = BytesIO()
    work_book.save(byte_io)
    return byte_io.getvalue()


if __name__ == "__main__":
    print(expand_names())
    # print(len(expand_names() + [1, 2]))
