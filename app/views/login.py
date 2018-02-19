from flask import Blueprint, render_template

mod = Blueprint('login', __name__, url_prefix='/', template_folder='templates')


@mod.route('/', defaults={'page': 'index'})
#@mod.route('/<page>')
def index(page):
        return render_template('/%s.html' % page)