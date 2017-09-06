# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:58
# @Author  : Forec
# @File    : models/advice.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .. import db
from datetime import datetime
from markdown import markdown
import bleach


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    viewed = db.Column(db.Boolean, default=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i', 'br', 'strong']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags, strip=True)
        )

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from .user import User

        user_count = User.query.count()
        for i in range(count):
            u1 = User.query.offset(randint(0, user_count-1)).first()
            u2 = User.query.offset(randint(0, user_count-1)).first()
            a = Message(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                        timestamp=forgery_py.date.date(True),
                        viewed=False,
                        author=u1,
                        target=u2)
            db.session.add(a)
        db.session.commit()
