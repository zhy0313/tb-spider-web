#!/usr/bin/env python
# -*-  coding: utf-8 -*-
# author = xm


import json
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import make_response
from datetime import datetime as date

from mongo import tb_industry_top as industry_top_dao
from mongo import tb_topx_dao
from excel import industry_export
from excel import topx_export
from excel import data_export

app = Flask(__name__)


def response(data):
    resp = make_response(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test", methods=["post", "get"])
def test():
    return response(jsonify(name="xm"))


@app.route("/industry/item", methods=["POST", "GET"])
def item():
    model = {
        "type": request.form["type"],
        "id": request.form['id'],
        "pay_cri": int(request.form['pay_cri']),
        "growth_rate": float(request.form["growth_rate"]),
        "price": float(request.form['price']),
        "shop": request.form['shop'],
        "shop_url": request.form['shop_url'],
        "sub_orders": int(request.form['sub_orders']),
        "url": request.form['url'],
        "index": int(request.form['index']),
        "day": date.now().strftime("%Y-%m-%d"),
        "ts": int(time.time() * 1000)
    }
    # print(model)
    industry_top_dao.insert(model)
    return response(jsonify(code=0, message="Insert item success"))


@app.route("/industry/flow", methods=["POST"])
def flow():
    data_param = request.form['data']
    model = json.loads(data_param)
    if not model.get("day"):
        model['day'] = date.now().strftime("%Y-%m-%d")
    print(model)
    industry_top_dao.update_flow(model)
    return response(jsonify(code=0, message="Insert/Update flow success"))


@app.route("/industry/list", methods=["get", "post"])
def list_between():
    start_time = int(request.args.get("start_time"))
    end_time = int(request.args.get("end_time"))
    industry_items = industry_top_dao.find_between(start_time, end_time)
    # export.create_industry_excel(industry_items)
    return response(jsonify(code=0, data=industry_items))


@app.route("/industry/list/<day>")
def list_day(day):
    day_items = industry_top_dao.find_day(day)
    if len(day_items) == 0:
        return response(jsonify(code=0, data=day_items))
    response_ = make_response(industry_export.create_industry_excel(day_items))
    response_.headers['Content-Disposition'] = "attachment;filename=%s-%s.xls;" % ("Industry", day)
    response_.headers["Content-type"] = 'application/vnd.ms-excel'
    response_.headers['Transfer-Encoding'] = 'chunked'
    return response_


@app.route("/industry/<day>")
def industry_day(day):
    return list_day(day)


@app.route("/topx/<day>")
def topx_day(day):
    topx_items = tb_topx_dao.find_day(day)
    if len(topx_items) == 0:
        return response(jsonify(code=0, data=topx_items))
    print(topx_items)
    response_ = make_response(topx_export.create__excel(topx_items))
    response_.headers['Content-Disposition'] = "attachment;filename=%s-%s.xls;" % ( "Topx", day)
    response_.headers["Content-type"] = 'application/vnd.ms-excel'
    response_.headers['Transfer-Encoding'] = 'chunked'
    return response_


@app.route("/data/<day>")
def data(day):
    topx_items = tb_topx_dao.find_day(day)
    if len(topx_items) == 0:
        return response(jsonify(code=0, data=topx_items))
    industry_items = industry_top_dao.find_day(day)

    def find_by_name(name):
        for industry_item in industry_items:
            if industry_item['shop'] == name:
                return industry_item
        return {}

    result = []
    for topx_item in topx_items:
        tmp = dict(find_by_name(topx_item['nick']), **topx_item)
        result.append(tmp)
        print(tmp)
    result = sorted(result, key=lambda x: x.get('index', 1000000000))
    response_ = make_response(data_export.create__excel(result))
    response_.headers['Content-Disposition'] = "attachment;filename=%s-%s.xls;" % ("Data", day)
    response_.headers["Content-type"] = 'application/vnd.ms-excel'
    response_.headers['Transfer-Encoding'] = 'chunked'
    return response_


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)

