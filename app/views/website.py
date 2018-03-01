from flask import Blueprint, render_template, request, jsonify, json
from app.SocketServer import *


website = Blueprint('website', __name__)
xvm_connection = SocketServer()
xvm_connection.start_process()
ans_request = []


@website.route('/send', methods=['GET', 'POST'])
def send_message_to_device():
    if request.method == 'POST':
        json = request.get_json()
        id_xvm = json['id_xvm']
        cmd_xvm = json['cmd_xvm']
        mdt_xvm = json['mdt_xvm']
        request_id = xvm_connection.send_command(id_xvm, cmd_xvm, mdt_xvm)
        if request_id == 'busy':
            ans_request.append('busy')
        else:
            ans_request.append(xvm_connection.wait_response(request_id, timeout=5))
        print('ans_request: {}' .format(ans_request))
        return jsonify(ans_request=ans_request)
    return render_template('website/send.html', online_devices=xvm_connection.addr_devices_list.keys())

# guardar essa "ideia"
#@website.route('/show_devices')
#def show_devices_online():
#    online_devices = xvm_connection.get_online_devices()
#    # se passar o self.addrs_devices_list
#    # erro: <DictProxy object, typeid 'dict' at 0x7f2dab829f60> is not JSON serializable
#    return jsonify(devices_list=online_devices)


@website.route('/dashboard')
def dashboard():
    return render_template('website/dashboard.html')

