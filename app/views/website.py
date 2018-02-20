from flask import Blueprint, render_template, request


website = Blueprint('website', __name__)


@website.route('/<page>', methods=['POST'])
def remoto(page):
    id = request.form['id_xvm']
    cmd = request.form['cmd_xvm']
    return render_template('website/%s.html' % page)


@website.route('/<page>')
def dashboard(page):
    return render_template('website/%s.html' % page)



