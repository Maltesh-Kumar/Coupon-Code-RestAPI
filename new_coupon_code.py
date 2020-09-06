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
def new_coupon_store_fxn():
    #GET THE POSTED DATA
    posteddata = request.get_json()
    #READING THE DATA
    coupon_id = str(uuid.uuid4())[:8]
    coupon_code = str.upper(posteddata["coupon_code"])
    resturant_id = posteddata["resturant_id"]
    coupon_active_status = int(posteddata["active_status"]) # 1--> Active , 0--> Inactive
    coupon_offer_percentage = float(posteddata["offer_percentage"])
    coupon_max_cashback = float(posteddata["max_cashback"])
    coupon_min_order_value = float(posteddata["min_order_value"])
    coupon_title = posteddata["title"]
    # nota --> number of times applicable per person
    coupon_nota = int(posteddata["nota"])
    # date format = "2020-03-27 02:50:00"
    coupon_start_date_time = posteddata["start_date_time"]
    coupon_end_date_time = posteddata["end_date_time"]
    coupon_order_multiple = int(posteddata["order_multiple"])

    # checking if coupon code already existed
    try:
        coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]['coupon_code']
        final_return_message = {
            "coupon_code":coupon_code,
            "message":"coupon code already exists",
            "status":250  # If already exists
            }
        return jsonify(final_return_message)
    except:
        coupons_data.insert_one({"coupon_id":coupon_id,"resturant_id":resturant_id,"coupon_start_date_time":coupon_start_date_time,"coupon_end_date_time":coupon_end_date_time,"coupon_code":coupon_code,"coupon_active_status":coupon_active_status,"coupon_offer_percentage":coupon_offer_percentage,"coupon_max_cashback":coupon_max_cashback,"coupon_min_order_value":coupon_min_order_value,"coupon_title":coupon_title,"coupon_nota":coupon_nota,"coupon_order_multiple":coupon_order_multiple})
        final_return_message = {
            "coupon_code":coupon_code,
            "message":"coupon code successfully created",
            "status":200
            }
        return jsonify(final_return_message)
