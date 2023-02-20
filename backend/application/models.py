import datetime as d
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db=SQLAlchemy()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) 
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('User', lazy='dynamic'))
    lists=db.relationship('List', backref=db.backref('User'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class List(db.Model):
    __tablename__ = 'list'
    list_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    list_name= db.Column(db.String(101),nullable=False)
    list_description = db.Column(db.String(255))
    l_timestamp=db.Column(db.Date(), default=d.date.today())
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    
    cards=db.relationship('Card', backref=db.backref('List'))

class Card(db.Model):
    __tablename__="cards"
    card_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    card_name=db.Column(db.String(255), nullable=False)
    card_content=db.Column(db.String(255), nullable=False)   
    deadline_date = db.Column(db.Date(), nullable = False, default = d.date.today())
    created_date = db.Column(db.Date(), nullable = False, default=d.date.today())
    last_updated = db.Column(db.Date(), nullable = False, default=d.date.today())
    completion_date = db.Column(db.Date)
    list_id=db.Column(db.Integer, db.ForeignKey('list.list_id'), nullable=False)

class Completed(db.Model):
    __tablename__='completed'
    list_id=db.Column(db.Integer, db.ForeignKey('list.list_id'), primary_key=True)
    completion_date=db.Column(db.Date, db.ForeignKey('cards.card_id'), primary_key=True)
    count=db.Column(db.Integer)

class CompletedStats(db.Model):
    __tablename__='stats'
    list_id=db.Column(db.Integer, db.ForeignKey('list.list_id'), primary_key=True)
    total_cards=db.Column(db.Integer, default=0)
    completed_cards=db.Column(db.Integer, default=0)
    passed_deadline=db.Column(db.Integer, default=0)
    incomplete_cards=db.Column(db.Integer, default=0)