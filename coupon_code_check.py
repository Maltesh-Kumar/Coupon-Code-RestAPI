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
def coupon_code_check_fxn():
    #GET THE POSTED DATA
    posteddata = request.get_json()
    #READING THE DATA
    customer_id = int(posteddata["customer_id"])
    coupon_code = str.upper(posteddata["coupon_code"])
    resturant_id = posteddata["resturant_id"]
    order_price = float(posteddata["order_price"])
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
    #print("----------------")

    # checking for minimum order criteria
    min_order_value = coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]['coupon_min_order_value']
    #print(min_order_value)
    if order_price < min_order_value:
        final_return_message = {
            "coupon_code":coupon_code,
            "min_order_value":min_order_value,
            "cart_value":order_price,
            "difference":(min_order_value-order_price),
            "message":"order value is lower",
            "status":205
            }
        return jsonify(final_return_message)

    # checking for date_time validity
    if not "" == coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]['coupon_start_date_time']:
        today = pd.to_datetime('today')
        coupon_start_date_time = coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]['coupon_start_date_time']
        coupon_end_date_time = coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]['coupon_end_date_time']
        coupon_start_date_time = pd.to_datetime(coupon_start_date_time)
        coupon_end_date_time = pd.to_datetime(coupon_end_date_time)
        if not coupon_start_date_time < today < coupon_end_date_time:
            final_return_message = {
                "coupon_code":coupon_code,
                "message":"coupon code date has been expired",
                "status":206
                }
            return jsonify(final_return_message)
    #print("date validation crossed")


    # checking for nota --> no. of times applicable pre person
    if coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]['coupon_order_multiple'] > 0:
        sql = "SELECT user_id, count(*) FROM done WHERE user_id = %s"
        cus_adr = (customer_id, )
        mycursor.execute(sql, cus_adr)
        myresult = mycursor.fetchall()
        res = dict(myresult)
        print(res)
        freq_of_order = res[str(customer_id)]
        multiple = coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]['coupon_order_multiple']
        print(freq_of_order,"---",multiple)
        if freq_of_order%multiple == 0:
            #print("INNININ")
            query =  "select User_Id, count(*) from Done_Promo where promo_code = %s and Status = 0 group by User_Id"
            cc = (coupon_code, )
            mycursor.execute(query, cc)
            myresult = mycursor.fetchall()
            res = dict(myresult)
            no_of_times_used = res[str(customer_id)]
            if no_of_times_used > coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]['coupon_nota']:
                final_return_message = {
                    "coupon_code":coupon_code,
                    "message":"you have used up coupon code",
                    "status":208
                    }
                return jsonify(final_return_message)
            else:
                final_return_message = {
                    "coupon_code":coupon_code,
                    "message":"you are eligible for coupon code",
                    "status":200
                    }
                return jsonify(final_return_message)
        else:
            final_return_message = {
            "coupon_code":coupon_code,
            "message":"coupon code not applicable as your order is not a multiple",
            "status":204
            }
            return jsonify(final_return_message)

    else:
            mycursor.execute("select User_Id, count(*) from Done_Promo where promo_code = '%s' and Status = 0 group by user_id"%coupon_code)
            myresult = mycursor.fetchall()
            res = dict(myresult)
            #print(res)
            if not bool(res):
                final_return_message = {
                    "coupon_code":coupon_code,
                    "message":"you are eligible for coupon code",
                    "status":200
                    }
                return jsonify(final_return_message)
            no_of_times_used = res[str(customer_id)]
            #print(no_of_times_used)
            if no_of_times_used > coupons_data.find({"coupon_code":coupon_code,"resturant_id":resturant_id})[0]['coupon_nota']:
                final_return_message = {
                    "coupon_code":coupon_code,
                    "message":"you have used up coupon code",
                    "status":208
                    }
                return jsonify(final_return_message)
            else:
                #print(no_of_times_used)
                final_return_message = {
                    "coupon_code":coupon_code,
                    "message":"you are eligible for coupon code",
                    "status":200
                    }
                return jsonify(final_return_message)
