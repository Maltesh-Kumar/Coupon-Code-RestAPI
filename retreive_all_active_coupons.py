import json
import pymysql
from pymongo import MongoClient
from flask import jsonify

#mongodb connection
database = MongoClient("mongodb+srv://---@cluster0-u9pbg.mongodb.net/test?retryWrites=true&w=majority")
db = database.JustGrab
coupons_data = db["coupons_data"]

#main function
def retreive_all_active_coupons_fxn(res_id):
    resturant_id = res_id

    #checking if resturant exists
    try:
        coupons_data.find({"resturant_id":resturant_id})[0]
    except:
        final_return_message = {
            "message":"resturant id not found",
            "status":202
            }
        return jsonify(final_return_message)

    #returning coupons
    coupons = []
    for i in coupons_data.find({"coupon_active_status":1,"resturant_id":resturant_id}):
        i.pop('_id')
        coupons.append(i)
    final_return_message = {
        "total_coupons":len(coupons),
        "coupon_data":coupons,
        "status":200
        }
    return jsonify(final_return_message)
