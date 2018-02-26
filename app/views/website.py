from flask import Blueprint, render_template, request
from app.SocketServer import *

website = Blueprint('website', __name__)
xvm_connection = SocketServer()
xvm_connection.start_process()


@website.route('/send', methods=['GET', 'POST'])
def send_message_to_device():
    if request.method == 'POST':
        ans_request = None
        id_xvm = request.form['id_xvm']
        cmd_xvm = request.form['cmd_xvm']
        mdt_xvm = request.form.get('mdt_xvm')
        request_id = xvm_connection.send_command(id_xvm, cmd_xvm, mdt_xvm)
        if request_id == 'busy':
            ans_request = 'busy'
        else:
            ans_request = xvm_connection.wait_response(request_id, timeout=5)
        return render_template('website/send.html', ans_xvm=ans_request)
    return render_template('website/send.html')


@website.route('/dashboard')
def dashboard():
    return render_template('website/dashboard.html')



