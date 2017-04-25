#!/usr/bin/env python
# -*-  coding: utf-8 -*-
# author = xm

from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from io import BytesIO

COLS_NAME = [{"name": "id", "desc": "编号"},
             {"name": "day", "desc": "日期"},
             {"name": "price", "desc": "价格"},
             {"name": "ljpj", "desc": "累计评价"},
             {"name": "sales", "desc": "销量"},
             {"name": "url", "desc": "链接"},
             {"name": "nick", "desc": "店铺"}]


def write_sheet_row(work_sheet, row, col, data):
    style = XFStyle()
    style.font = Font()
    work_sheet.write(row, col, data)


def create__excel(topx_items):
    """
    生成行业指数数据表
    """
    work_book = Workbook(encoding="utf-8")
    work_sheet = work_book.add_sheet('sheet-1')
    # 生成列头
    cols_name = COLS_NAME
    for index in range(0, len(cols_name)):
        write_sheet_row(work_sheet, 0, index, cols_name[index]["desc"])

    # 生成标准内容
    for index in range(0, len(topx_items)):
        item = topx_items[index]
        for col_index in range(0, len(cols_name)):
            col = cols_name[col_index]
            write_sheet_row(work_sheet, index + 1, col_index, item[col["name"]])
    byte_io = BytesIO()
    work_book.save(byte_io)
    return byte_io.getvalue()

