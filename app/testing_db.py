from app import db
from app.models import Event


def read_db_event(id):
    q = Event.query.filter_by(id=id).first()
    print('id {}'.format(q.id))
    print('device {}'.format(q.device))
    print('prefix {}'.format(q.prefix))
    print('instant {}'.format(q.instant))
    print('xvm {}'.format(q.xvm))
    return q


def search_mdt_disconnect():
    q = Event.query.filter_by(prefix='RUV1122').first()
    q2 = Event.query.filter_by(prefix='RUV1122').all()
    print('q2: {}'.format(q2))
    print('id {}'.format(q2[0].id))
    print('device {}'.format(q2[0].device))
    print('prefix {}'.format(q2[0].prefix))
    print('instant {}'.format(q2[0].instant))
    print('xvm {}'.format(q2[0].xvm))
    return q2
