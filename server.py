from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from flask.ext.api import status
from OpenSSL import SSL
import requests
import json
from flask import *
import random
import string
import sqlite3

app = Flask(__name__)

api_token = ''
user_create = ''


def crossdomain(origin=None, methods=None, headers="Content-Type",
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)
    return decorator


def verify_user_create_key(content):
    token = content['token']['id']

    if token == user_create:
        return True
    else:
        return False


def api_key_verify(content):
    token = content['token']['id']
    command = "select uid from users where token='{}';".format(token)
    try:
        c.execute(command)
        uid = c.fetchone()[0]
        return True, uid
    except:
        return False, None


@app.route("/user_api", methods=["POST"])
@crossdomain(origin='*')
def generate_api_token():
    content = request.get_json()
    if verify_user_create_key(content):
        token = id_generator()
        uid = content['user']['uid']
        try:
            command = "INSERT INTO users VALUES('{uid}','{token}');".format(uid=uid, token=token)
            c.execute(command)
            db.commit()
            return_status = (jsonify({'uid': uid,
                                      'token': token}), status.HTTP_200_OK)
            return return_status
        except sqlite3.IntegrityError:
            command = "select token from users where uid='{}';".format(uid)
            c.execute(command)
            token = c.fetchone()[0]
            return jsonify(user={'uid': uid,
                                 'token': token}), status.HTTP_200_OK
    else:
            return jsonify(status={'success': False, 'error': "Incorrect API Key"}), status.HTTP_401_UNAUTHORIZED


@app.route("/lounge/projector", methods=["GET"])
@crossdomain(origin='*')
def lounge_projector_status():
    data = requests.get("http://lforlounge.csh.rit.edu:5000/lounge/projector")
    device = json.loads(data.text)

    power_command = "select function, state from device_log where device='projector' and function='power' ORDER BY date DESC LIMIT 1;"
    input_command = "select function, state from device_log where device='projector' and function!='power' and function!='blank' ORDER BY date DESC LIMIT 1;"
    blank_command = "select function, state from device_log where device='projector' and function='blank' ORDER BY date DESC LIMIT 1;"

    c.execute(power_command)
    power = bool(c.fetchone()[1])

    c.execute(input_command)
    input = c.fetchone()[0]

    c.execute(blank_command)
    blank = bool(c.fetchone()[1])

    if power == device['projector']['power']:
        pass
    else:
        command = "INSERT INTO device_log('device','function','state','user') VALUES('projector','power',{},'sync');".format(int(device['projector']['power']))
        c.execute(command)
        db.commit()

    if input == device['projector']['input']:
        pass
    else:
        command = "INSERT INTO device_log('device','function','state','user') VALUES('projector','{}',1,'sync');".format(device['projector']['input'])
        c.execute(command)
        db.commit()

    if blank == device['projector']['blank']:
        pass
    else:
        command = "INSERT INTO device_log('device','function','state','user') VALUES('projector','blank',{},'sync');".format(int(device['projector']['blank']))
        c.execute(command)
        db.commit()

    if device['status']['success']:
        return_status = jsonify(status={'success': True}, projector={'power': device['projector']['power'],
                                                                     'input': device['projector']['input'],
                                                                     'hours': int(device['projector']['hours']),
                                                                     'sources': {'HDMI1': None,
                                                                                 'HDMI2': 'Receiver',
                                                                                 'Computer1': 'Aux VGA',
                                                                                 'Computer2': None,
                                                                                 'Composite': None},
                                                                     'blank': device['projector']['blank']
                                                                     })
    else:
        return_status = jsonify(status={'success': False,
                                        'error': "Cannot communicate with projector."}), \
                        status.HTTP_400_BAD_REQUEST
    return return_status


@app.route("/lounge/receiver", methods=["GET"])
@crossdomain(origin='*')
def lounge_receiver_status():
    data = requests.get("http://lforlounge.csh.rit.edu:5000/lounge/receiver")
    device = json.loads(data.text)

    input_command = "select function, state from device_log where device='receiver' and function!='power' and function!='mute' and function!='volume' ORDER BY date DESC LIMIT 1;"
    mute_command = "select function, state from device_log where device='receiver' and function='mute' ORDER BY date DESC LIMIT 1;"
    volume_command = "select function, state from device_log where device='receiver' and function='volume' ORDER BY date DESC LIMIT 1;"

    c.execute(input_command)
    input = c.fetchone()[0]

    c.execute(mute_command)
    mute = c.fetchone()[1]

    c.execute(volume_command)
    volume = c.fetchone()[1]

    if input == device['receiver']['input']:
        pass
    else:
        command = "INSERT INTO device_log('device','function','state','user') VALUES('receiver','{}',1,'sync');".format(device['receiver']['input'])
        c.execute(command)
        db.commit()

    if bool(mute) == device['receiver']['mute']:
        pass
    else:
        command = "INSERT INTO device_log('device','function','state','user') VALUES('receiver','mute',{},'sync');".format(int(device['receiver']['mute']))
        c.execute(command)
        db.commit()

    if volume == device['receiver']['volume']:
        pass
    else:
        command = "INSERT INTO device_log('device','function','state','user') VALUES('receiver','volume',{},'sync');".format(int(device['receiver']['volume']))
        c.execute(command)
        db.commit()
    print(device['status']['success'])
    if device['status']['success']:
        return_status = jsonify(status={'success': True}, receiver={'input': device['receiver']['input'],
                                                                    'volume': device['receiver']['volume'],
                                                                    'sources': {'HDMI1': 'Media PC',
                                                                                'HDMI2': 'Aux HDMI',
                                                                                'HDMI3': 'Chromecast',
                                                                                'HDMI4': 'Raspberry Pi'},
                                                                    'mute': device['receiver']['mute']
                                                                    })
    else:
        return_status = jsonify(status={'success': False,
                                        'error': "Cannot communicate with projector."}), \
                        status.HTTP_400_BAD_REQUEST
    return return_status


@app.route("/lounge/lights", methods=["GET"])
@crossdomain(origin='*')
def lounge_lights_status():
    return_status = jsonify(status={'success': True}, lights={'L1': False, 'L2': True})
    return return_status


@app.route("/lounge/radiator", methods=["GET"])
@crossdomain(origin='*')
def lounge_radiator_status():
    return_status = jsonify(status={'success': True}, radiator={'fan': False})
    return return_status


@app.route("/lounge/projector/<function>", methods=["PUT"])
@crossdomain(origin='*')
def lounge_projector_change(function):

    if function == "power":
        content = request.get_json()
        key_verified, username = api_key_verify(content)
        if key_verified:
            try:
                print("Projector power: {}".format(content['power']['state']))
                command = "INSERT INTO device_log('device','function','state','user') VALUES('{}','{}',{},'{}');".format(
                    "projector", function, int(content['power']['state']), username)
                c.execute(command)
                db.commit()
                data = {'token': {'id': api_token}}
                return_status = (jsonify(status={'success': True}), status.HTTP_200_OK)
            except:
                return_status = (jsonify(status={'success': False}), status.HTTP_400_BAD_REQUEST)
        else:
            return_status = (jsonify(status={'success': False, 'error': "Incorrect API Key"}),
                             status.HTTP_401_UNAUTHORIZED)
        return return_status
    if function == "input":
        content = request.get_json()
        key_verified, username = api_key_verify(content)
        if key_verified:
            try:
                print("Projector input: {}".format(content['input']['select']))
                command = "INSERT INTO device_log('device','function','state','user') VALUES('{}','{}',{},'{}');".format(
                    "projector", content['input']['select'], 1, username)
                print(command)
                c.execute(command)
                db.commit()
                return_status = (jsonify(status={'success': True}), status.HTTP_200_OK)
            except:
                return_status = (jsonify(status={'success': False}), status.HTTP_400_BAD_REQUEST)
        else:
            return_status = (jsonify(status={'success': False, 'error': "Incorrect API Key"}),
                             status.HTTP_401_UNAUTHORIZED)
        return return_status
    if function == "blank":
        content = request.get_json()
        key_verified, username = api_key_verify(content)
        if key_verified:
            try:
                print("Projector blank: {}".format(content['blank']['state']))
                command = "INSERT INTO device_log('device','function','state','user') VALUES('{}','{}',{},'{}');".format(
                    "projector", function, int(content['blank']['state']), username)
                c.execute(command)
                db.commit()
                return_status = (jsonify(status={'success': True}), status.HTTP_200_OK)
            except:
                return_status = (jsonify(status={'success': False}), status.HTTP_400_BAD_REQUEST)
        else:
            return_status = (jsonify(status={'success': False, 'error': "Incorrect API Key"}),
                             status.HTTP_401_UNAUTHORIZED)
        return return_status


@app.route("/lounge/receiver/<function>", methods=["PUT"])
@crossdomain(origin='*')
def lounge_receiver_change(function):

    if function == "input":
        content = request.get_json()
        key_verified, username = api_key_verify(content)
        if key_verified:
            try:
                print("Projector input: {}".format(content['input']['select']))
                command = "INSERT INTO device_log('device','function','state','user') VALUES('{}','{}',{},'{}');".format(
                    "receiver", content['input']['select'], 1, username)
                c.execute(command)
                db.commit()
                data = jsonify({'token': {'id': '<API KEY>'}, 'mute': {'power': content['input']['select']}})
                print(data)
                r = requests.put("http://lforlounge.csh.rit.edu:5000/lounge/receiver/input", data)
                print(r.text)
                return_status = (jsonify(status={'success': True}), status.HTTP_200_OK)
            except:
                return_status = (jsonify(status={'success': False}), status.HTTP_400_BAD_REQUEST)
        else:
            return_status = (jsonify(status={'success': False, 'error': "Incorrect API Key"}),
                             status.HTTP_401_UNAUTHORIZED)
        return return_status
    if function == "mute":
        content = request.get_json()
        key_verified, username = api_key_verify(content)
        if key_verified:
            try:
                print("Projector blank: {}".format(content['mute']['state']))
                command = "INSERT INTO device_log('device','function','state','user') VALUES('{}','{}',{},'{}');".format(
                    "receiver", function, int(content['mute']['state']), username)
                c.execute(command)
                db.commit()
                return_status = (jsonify(status={'success': True}), status.HTTP_200_OK)
            except:
                return_status = (jsonify(status={'success': False}), status.HTTP_400_BAD_REQUEST)
        else:
            return_status = (jsonify(status={'success': False, 'error': "Incorrect API Key"}),
                             status.HTTP_401_UNAUTHORIZED)
        return return_status


@app.route("/lounge/lights", methods=["PUT"])
@crossdomain(origin='*')
def lounge_lights_toggle():

    content = request.get_json()
    key_verified, username = api_key_verify(content)
    if key_verified:
        try:
            for light, value in content["lights"].items():
                if light == "L1":
                    print(light, value)
                    command = "INSERT INTO device_log('device','function','state','user') VALUES('{}','{}',{},'{}');".format(
                        "L1", "power", int(value), username)
                    c.execute(command)
                elif light == "L2":
                    print(light, value)
                    command = "INSERT INTO device_log('device','function','state','user') VALUES('{}','{}',{},'{}');".format(
                        "L2", "power", int(value), username)
                    c.execute(command)

            return_status = (jsonify(status={'success': True}), status.HTTP_200_OK)
        except:
            return_status = (jsonify(status={'success': False}), status.HTTP_400_BAD_REQUEST)
    else:
        return_status = (jsonify(status={'success': False, 'error': "Incorrect API Key"}),
                         status.HTTP_401_UNAUTHORIZED)
    return return_status


@app.route("/lounge/radiator", methods=["PUT"])
@crossdomain(origin='*')
def lounge_radiator_toggle():

    content = request.get_json()
    key_verified, username = api_key_verify(content)
    if key_verified:
        try:
            command = "INSERT INTO device_log('device','function','state','user') VALUES('{}','{}',{},'{}');".format(
                "radiator", "fan", int(content['radiator']['fan']), username)
            c.execute(command)
            db.commit()
            data = {'token': {'id': "<API KEY>"}, 'radiator': {'fan': content['radiator']['fan']}}
            requests.put("http://lforlounge.csh.rit.edu:5000/lounge/radiator", json=data)
            return_status = (jsonify(status={'success': True}), status.HTTP_200_OK)
        except:
            return_status = (jsonify(status={'success': False}), status.HTTP_400_BAD_REQUEST)
    else:
        return_status = (jsonify(status={'success': False, 'error': "Incorrect API Key"}),
                         status.HTTP_401_UNAUTHORIZED)
    return return_status


def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == "__main__":
    db = sqlite3.connect('state.sql')
    c = db.cursor()

    context = ('ssl.crt', 'ssl.key')

    app.run(host='0.0.0.0', port=8081)  # , ssl_context=context, threaded=True)
