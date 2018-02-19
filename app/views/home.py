from flask import Blueprint, render_template

#mod = Blueprint('home', __name__, url_prefix='/', template_folder='templates')

mod = Blueprint('index', __name__)

@mod.route('/index', defaults={'page': 'index'})
@mod.route('/')
def index():
    return render_template('index.html')

#@mod.route('/', defaults={'page': 'index'})
#@mod.route('/<page>')
#def index(page):
        #return render_template('/%s.html' % page)

