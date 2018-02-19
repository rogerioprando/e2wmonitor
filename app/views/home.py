from flask import Blueprint, render_template

mod = Blueprint('home', __name__, url_prefix='/home', template_folder='templates')


@mod.route('/', defaults={'page': 'index'})
@mod.route('/<page>')
def index(page):
        return render_template('home/%s.html' % page)