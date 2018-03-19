from flask import Blueprint, render_template, request, jsonify, flash, redirect, session, abort
from app.SocketServer import *
from collections import defaultdict
from app.testing_db import *


website = Blueprint('website', __name__)
xvm_connection = SocketServer()
xvm_connection.start_process()
answer = defaultdict(list)


@website.route('/send', methods=['GET', 'POST'])
def send_message_to_device():
    if not session.get('logged_in'):
        return render_template('auth/login.html')
    else:
        user = session['logged_in']
        cookie_value = request.cookies.get('session')
        print('cookie: {}'.format(cookie_value))
        if request.method == 'POST':
            json = request.get_json()
            id_xvm = json['id_xvm']
            cmd_xvm = json['cmd_xvm']
            mdt_xvm = json['mdt_xvm']
            timeout_xvm = json['timeout_xvm']
            request_id = xvm_connection.send_command(id_xvm, cmd_xvm, mdt_xvm)
            if request_id == 'busy':
                answer[cookie_value].append('busy')
            else:
                temp = xvm_connection.wait_response(id_xvm, int(timeout_xvm))
                answer[cookie_value].append(temp)
            return jsonify(ans_request=answer[cookie_value])
        if bool(xvm_connection.addr_devices_list.keys()) is False:
            devices = 0
        else:
            devices = xvm_connection.addr_devices_list.keys()
        return render_template('website/send.html', online_devices=devices, user=user)

# guardar essa "ideia"
#@website.route('/show_devices')
#def show_devices_online():
#    online_devices = xvm_connection.get_online_devices()
#    # se passar o self.addrs_devices_list
#    # erro: <DictProxy object, typeid 'dict' at 0x7f2dab829f60> is not JSON serializable
#    return jsonify(devices_list=online_devices)


@website.route('/cancel', methods=['POST'])
def cancel_message():
    json = request.get_json()
    id_xvm = json['id_xvm']
    xvm_connection.cancel_request(id_xvm)
    print('ID {} solicitou cancelamento do pedido!' .format(id_xvm))
    return jsonify(id_cancelled=id_xvm)


@website.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return render_template('auth/login.html')
    else:
        if request.method == 'POST':
            client = request.json['client']
            device = request.json['wplex_id']
            prefix = request.json['prefix']
            start_dt = request.json['start_dt']
            end_dt = request.json['end_dt']
            q_str = ('select * from event where {} and {} and {} and instant between {} and {} .. ' .format(
                device, client, prefix, start_dt, end_dt))
            print(q_str)
            return jsonify(q_str)
        return render_template('website/dashboard.html')
