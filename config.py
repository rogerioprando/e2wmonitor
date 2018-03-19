DEBUG = False

POSTGRES = {
    'user': 'rogerio',
    'pw': 'password',
    'db': 'eventlog',
    'host': 'localhost',
    'port': '5432',
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
SQLALCHEMY_TRACK_MODIFICATIONS = True
