import json
import pymysql
from pymongo import MongoClient
from flask import jsonify, request
import uuid

#mongodb connection
database = MongoClient("mongodb+srv://---@cluster0-u9pbg.mongodb.net/test?retryWrites=true&w=majority")
db = database.JustGrab
coupons_data = db["coupons_data"]

#main function
def update_coupon_code_fxn():
    #GET THE POSTED DATA
    posteddata = request.get_json()
    #READING THE DATA
    resturant_id = posteddata["resturant_id"]
    try:
        coupons_data.find({"resturant_id":resturant_id})[0]
    except:
        final_return_message = {
            "message":"resturant id not found",
            "status":202
            }
        return jsonify(final_return_message)

    coupon_code = str.upper(posteddata["coupon_code"])
    try:
        coupons_data.find({"resturant_id":resturant_id,"coupon_code":coupon_code})[0]
    except:
        final_return_message = {
            "message":"coupon code does not exists in this resturant id",
            "status":203
            }
        return jsonify(final_return_message)
    #coupons_data.update("coupon_code":coupon_code,{$set:{"":}})

    #coupons_data.update({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_active_status":coupon_active_status}})

    coupon_active_status = int(posteddata["active_status"])
    coupons_data.update_one({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_active_status":coupon_active_status}})

    coupon_offer_percentage = float(posteddata["offer_percentage"])
    coupons_data.update_one({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_offer_percentage":coupon_offer_percentage}})

    coupon_max_cashback = float(posteddata["max_cashback"])
    coupons_data.update_one({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_max_cashback":coupon_max_cashback}})

    coupon_min_order_value = float(posteddata["min_order_value"])
    coupons_data.update_one({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_min_order_value":coupon_min_order_value}})

    coupon_title = posteddata["title"]
    coupons_data.update_one({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_title":coupon_title}})

    # nota --> number of times applicable per person
    coupon_nota = int(posteddata["nota"])
    coupons_data.update_one({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_nota":coupon_nota}})

    # date format = "2020-03-27 02:50:00"
    coupon_start_date_time = posteddata["start_date_time"]
    coupons_data.update_one({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_start_date_time":coupon_start_date_time}})

    coupon_end_date_time = posteddata["end_date_time"]
    coupons_data.update_one({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_end_date_time":coupon_end_date_time}})

    coupon_order_multiple = int(posteddata["order_multiple"])
    coupons_data.update_one({"coupon_code":coupon_code,"resturant_id":resturant_id},{"$set":{"coupon_order_multiple":coupon_order_multiple}})

    final_return_message = {
        "coupon_code":coupon_code,
        "message":"coupon sucessfully updated",
        "status":200
        }
    return jsonify(final_return_message)
