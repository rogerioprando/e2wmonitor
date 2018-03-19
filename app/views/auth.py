from flask import Blueprint, render_template, request, session, redirect, url_for
auth = Blueprint('auth', __name__)


@auth.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('auth/login.html')


@auth.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'POST':
        if request.form['password'] == '123':
            session['logged_in'] = request.form['username']
            return redirect(url_for('website.send_message_to_device'))
        else:
            return home()
    return home()
