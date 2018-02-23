from flask import Blueprint, render_template, request, json, jsonify, abort
from app.SocketServer import *

website = Blueprint('website', __name__)
conect_xvm = SocketServer()
conect_xvm.init_queues()


@website.route('/send', methods=['POST'])
def send_message_to_device():
    ans_request = None
    id = request.form['id_xvm']
    cmd = request.form['cmd_xvm']
    #conect_xvm.sendcommand(json.dumps({'status': 'OK', 'idwplex': id, 'command': cmd}))
    request_id = conect_xvm.send_command(id, cmd)
    print('sendcmd')
    try:
        if request_id == 'busy':
            ans_request = 'busy'
        else:
            ans_request = conect_xvm.wait_response(request_id, timeout=5)
    except Exception:
        ans_request = 'timeout'
    print('ans_request')
    #return jsonify({'ans_xvm' : ans_request})
    return render_template('website/send.html', ans_xvm=ans_request)


@website.route('/send', methods=['GET'])
def show_xvm_form():
    return render_template('website/send.html')


@website.route('/dashboard')
def dashboard():
    return render_template('website/dashboard.html')



