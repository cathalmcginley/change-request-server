import re

from collections import OrderedDict
import datetime

import yaml
from flask import Flask, request
from flask_cors import CORS
from jsons.exceptions import UnfulfilledArgumentError

from changerequest.server import (
    Application,
    name,
    version,
    PingResponseBody,
    PingErrorBody
)


app = Flask(__name__)
print("CREATING APP")
print(app)
cors = CORS(app)
## cors = CORS(app, resources={"/clipboard": {"origins": "http://localhost"}})


def check_for_auth_header(headers, clipboard_util):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return (False, "Authorization required")
    else:
        auth_match = re.match(r"^Basic\s([\d\w\+\/]+={0,2}$)", auth_header)
        if auth_match:
            auth_key = auth_match[1]
            if clipboard_util.auth_key_matches(auth_key):
                return (True, auth_key)
            else:
                return (False, "Authentication key was invalid")
        else:
            return (False, "Authorization scheme must be 'Basic'")


@app.route("/ping", methods=["GET"])
def ping():
    # global app
    auth_is_valid, message = check_for_auth_header(
        request.headers, app.config["clipboard_util"]
    )
    if auth_is_valid:
        database = app.config['database']    
        cr = database.load("/home/cathal/change-requests/cr/2022-04-20--ACE--a972b4c7-79ce-412f-ba0e-ac384cc6de3e.yaml")
        # return PingResponseBody(f"{name} {version}").dump()
        return cr.dump()
    else:
        return PingErrorBody(message).dump(), 401

def get_application(app_code):
    return Application(app_code, "ACE", "ACE - Production")



@app.route("/changerequests", methods=["POST"])
def picreate_change_requestng2():
    # global app
    auth_is_valid, message = check_for_auth_header(
        request.headers, app.config["clipboard_util"]
    )
    archetypes = app.config['archetypes']
    database = app.config['database']
    if auth_is_valid:

        body = request.get_json()
        application= get_application(body["app"])
        scheduled = body["scheduled"]
        start_date = None
        if "start-date" in body:
            start_date = datetime.date.fromisoformat(body["start-date"])
        cr = None
        if scheduled:
            cr = archetypes.create_scheduled_change_request(application, start_date)
        else:
            cr = archetypes.create_off_cycle_change_request(application, start_date)


        

                
        #     return cr.dump()
        #return PingResponseBody(f"{name} {version} {cr.uuid}").dump()
        headers = {'Location': f"/changerequest/{cr.uuid}"}
        database.save(cr)
        return (cr.dump(), 201, headers)
    else:
        return {"error", "not authorized"}, 401



@app.route("/changerequest/<id>", methods=['GET'])
def get_change_request(id):
    print(app)
    return {"id": id}
