#importing main libraries
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json
import uuid
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)
api = Api(app)

#importing functoins
from new_coupon_code import new_coupon_store_fxn
from retreive_all_coupons import retreive_all_coupons_fxn
from retreive_all_active_coupons import retreive_all_active_coupons_fxn
from retreive_all_inactive_coupons import retreive_all_inactive_coupons_fxn
from retreive_coupon import retreive_coupon_fxn
from retreive_only_coupon_codes import retreive_only_coupon_codes_fxn
from update_coupon_code import update_coupon_code_fxn
from coupon_code_check import coupon_code_check_fxn


#routing new_coupon_store
@app.route('/cart/new_coupon_store', methods=['POST'])
def new_coupon_store():
    result = new_coupon_store_fxn()
    return result

#routing new_coupon_store
@app.route('/cart/retreive_all_coupons', methods=['GET'])
def retreive_all_coupons():
    result = retreive_all_coupons_fxn()
    return result

#routing new_coupon_store
@app.route('/cart/retreive_all_active_coupons/<res_id>', methods=['GET'])
def retreive_all_active_coupons(res_id):
    result = retreive_all_active_coupons_fxn(res_id)
    return result

#routing new_coupon_store
@app.route('/cart/retreive_all_inactive_coupons/<res_id>', methods=['GET'])
def retreive_all_inactive_coupons(res_id):
    result = retreive_all_inactive_coupons_fxn(res_id)
    return result

#routing new_coupon_store
@app.route('/cart/retreive_coupon/<res_id>/<coupon_code>', methods=['GET'])
def retreive_coupon(res_id, coupon_code):
    result = retreive_coupon_fxn(res_id, coupon_code)
    return result

#routing new_coupon_store
@app.route('/cart/retreive_only_coupon_codes/<res_id>', methods=['GET'])
def retreive_only_coupon_codes(res_id):
    result = retreive_only_coupon_codes_fxn(res_id)
    return result

#routing new_coupon_store
@app.route('/cart/update_coupon_code', methods=['POST'])
def update_coupon_code():
    result = update_coupon_code_fxn()
    return result

#routing new_coupon_store
@app.route('/cart/coupon_code_check', methods=['POST'])
def coupon_code_check():
    result = coupon_code_check_fxn()
    return result



#app.run
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
