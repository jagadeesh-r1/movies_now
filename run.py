#! /media/pavan/Data/Work/Work_Github/env/bi_server_env/bin/python
import os
import time
import json
from flask import request, g, jsonify
from app import create_app

app = create_app()

@app.errorhandler(404) 
  
# inbuilt function which takes error as parameter 
def not_found(e): 
  
# defining function 
  return jsonify(
      {
        "message": "Not Found",
        "error": {
            "status": 404
        }
    }), 404

@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    g.request_start_time = time.time()

    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = {'ip': request.environ['REMOTE_ADDR']}
    else:
        ip_address = {'ip': request.environ['HTTP_X_FORWARDED_FOR']}

    print("***** Request ip ----->",ip_address)
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Credentials'] = 'true'
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers[
            'Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        h['Content-Type'] = 'application/json'
        #  print("type of request" + str(type(h['Access-Control-Allow-Origin'])))
        #  We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    # print(resp.get_data())
    h = resp.headers
    resp.add_etag()

    
    
    h['X-XSS-Protection'] = "1; mode=block"
    h['X-Content-Type-Options'] = "nosniff"
    h['X-Download-Options'] = "noopen"

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Credentials'] = 'true'

    else:
        try:
            body = json.loads(resp.get_data())
        except:
            body = {}
        if body:
            response_data = body
            if not "error" in body:
                status = body.get("status")
                if status is not None:

                    del body["status"]
                    
                    response_data["status"] = status


        else:
            response_data = {
                "status":False,
                "error_obj":{
                    "error_code":"unknown",
                    "message":"There is some problem. PLease try again after sometime"
                }
            }
        response_data = json.dumps(response_data)
        resp.set_data(response_data)

    elapsed = time.time() - g.request_start_time
    elapsed = '{}ms'.format(round(1000 * elapsed,2))
    h['X-Response-Time'] = elapsed

    return resp
