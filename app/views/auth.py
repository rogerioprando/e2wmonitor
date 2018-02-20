from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/', defaults={'page': 'login'})
@auth.route('/<page>')
def login(page):
    return render_template('auth/%s.html' % page)