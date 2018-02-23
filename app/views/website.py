from flask import Blueprint, render_template, request, json, jsonify, abort
from app.SocketServer import *

website = Blueprint('website', __name__)
conect_xvm = SocketServer()
conect_xvm.init_queues()


@website.route('/send', methods=['GET', 'POST'])
def send_message_to_device():
    if request.method == 'POST':
        ans_request = None
        id = request.form['id_xvm']
        cmd = request.form['cmd_xvm']
        request_id = conect_xvm.send_command(id, cmd)
        print('request_id {}' .format(request_id))
        '''try:
            if request_id == 'busy':
                ans_request = 'busy'
            else:
                ans_request = conect_xvm.wait_response(request_id, timeout=5)
        except Exception:
            ans_request = 'Exception timeout '
        '''
        if request_id == 'busy':
            ans_request = 'busy'
        else:
            ans_request = conect_xvm.wait_response(request_id, timeout=5)
        print('ans_request :{}' .format(ans_request))
        return render_template('website/send.html', ans_xvm=ans_request)
    return render_template('website/send.html')


@website.route('/dashboard')
def dashboard():
    print('to no dashboard')
    return render_template('website/dashboard.html')



