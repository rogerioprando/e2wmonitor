from app import db


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    device = db.Column(db.String)
    prefix = db.Column(db.String)
    instant = db.Column(db.DateTime) # timestamp
    xvm = db.Column(db.String)
    client = db.Column(db.String)

    def __init__(self, device, prefix, instant, xvm, client):
        self.device = device
        self.prefix = prefix
        self.instant = instant
        self.xvm = xvm
        self.client = client

    def __repr__(self):
        return '<Event {}>' .format(self.xvm)
        # retorna a representação do objeto no formato texto
