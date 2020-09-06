import json
import pymysql
from pymongo import MongoClient
from flask import jsonify

#mongodb connection
database = MongoClient("mongodb+srv://---@cluster0-u9pbg.mongodb.net/test?retryWrites=true&w=majority")
db = database.JustGrab
coupons_data = db["coupons_data"]

#main function
def retreive_only_coupon_codes_fxn(res_id):
    resturant_id = res_id
    try:
        coupons = []
        for i in coupons_data.find({"coupon_active_status":1,"resturant_id":resturant_id}):
            i.pop('_id')
            coupons.append(i['coupon_code'])
        final_return_message = {
            "total_coupons":len(coupons),
            "coupon_data":coupons,
            "status":200
            }
        return jsonify(final_return_message)
    except:
        final_return_message = {
            "message":"resturant id not found",
            "status":202
            }
        return jsonify(final_return_message)
