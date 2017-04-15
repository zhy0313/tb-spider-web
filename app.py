#!/usr/bin/env python
# -*-  coding: utf-8 -*-

import json
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import make_response
from datetime import datetime as date

from mongo import tb_industry_top as industry_top_dao
from excel import export


app = Flask(__name__)


def response(data):
    resp = make_response(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test",methods=["post", "get"])
def test():
    return response(jsonify(name="xm"))


@app.route("/industry/item", methods=["POST", "GET"])
def item():
    model = {
        "type": request.form["type"],
        "id": request.form['id'],
        "pay_cri": request.form['pay_cri'],
        "growth_rate": request.form["growth_rate"],
        "price": request.form['price'],
        "shop": request.form['shop'],
        "shop_url": request.form['shop_url'],
        "sub_orders": request.form['sub_orders'],
        "url": request.form['url'],
        "index": request.form['index'],
        "day": date.now().strftime("%Y-%m-%d"),
        "ts": int(time.time() * 1000)
    }
    # print(model)
    industry_top_dao.insert(model)
    return response(jsonify(code=0, message="Insert item success"))


@app.route("/industry/flow",methods=["POST"])
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
    response_ = make_response(export.create_industry_excel(day_items))
    response_.headers['Content-Disposition'] = "attachment;filename=%s.xls;" % (day)
    response_.headers["Content-type"] = 'application/vnd.ms-excel'
    response_.headers['Transfer-Encoding'] = 'chunked'
    return response_

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

