# from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from . import db
# from flask.ext.script import Manager, Shell
# from sqlalchemy import Column, Integer, String

# app = Flask(__name__)
# db = SQLAlchemy(app)
# def make_shell_context():
#     return dict(app=app, db=db, User=User, School=School)
# manager = Manager(app)
# manager.add_command("shell", Shell(make_context=make_shell_context))


class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='school')
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<School %r>' % self.name
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    wxid = db.Column(db.String(64), unique=True, nullable=False, index=True)
    stuid = db.Column(db.Integer, nullable=False)
    pswd = db.Column(db.String(64), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    def __init__(self, wxid, stuid, pswd, school):
        self.wxid = wxid
        self.stuid = stuid
        self.pswd = pswd
        self.school = school
    def __repr__(self):
        return '<User %r>' % self.wxid


# if __name__ == '__main__':
#     manager.run()