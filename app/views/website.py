from flask import Blueprint, render_template


website = Blueprint('website', __name__)

@website.route('/', defaults={'page': 'login'})
@website.route('/<page>')
def login(page):
    return render_template('website/%s.html' % page)


@website.route('/<page>')
def remoto(page):
    return render_template('website/%s.html' % page)

@website.route('/<page>')
def dashboard(page):
    return render_template('website/%s.html' % page)



