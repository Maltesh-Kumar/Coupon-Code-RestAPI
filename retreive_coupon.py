import json
import pymysql
from pymongo import MongoClient
from flask import jsonify

#mongodb connection
database = MongoClient("mongodb+srv://---@cluster0-u9pbg.mongodb.net/test?retryWrites=true&w=majority")
db = database.JustGrab
coupons_data = db["coupons_data"]

#main function
def retreive_coupon_fxn(res_id, coupon_code):
    resturant_id = res_id
    coupon_code = coupon_code

    # checking if it exists
    try:
        coupons = []
        temp = coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]
        temp.pop('_id')
        coupons.append(temp)
        final_return_message = {
            "coupon_code":coupons,
            "message":"coupon code exists",
            "status":200
            }
        return jsonify(final_return_message)
    except:
        final_return_message = {
            "coupon_code":coupon_code,
            "message":"coupon code or resturant id does not exists",
            "status":260 # invalid coupon code
            }
        return jsonify(final_return_message)
