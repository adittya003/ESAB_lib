from datetime import date, timedelta

from . import db
from . import bcrypt
from .helper import *
from sqlalchemy import Integer, String,Boolean


class AdminUser(db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(32), unique=True, nullable=False)
    password = db.Column(String(256), nullable=False)
    
    def set_password(self, data):
        self.password = bcrypt.generate_password_hash(data).decode('utf-8')

    def check_password(self, data):
        return bcrypt.check_password_hash(self.password, data)
    
    def __repr__(self) -> str:
        return f"<AdminUser {self.username}>" 


class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String(32), nullable=False)
    last_name= db.Column(String(32), nullable=False)
    qr=db.Column(String(256),unique=True, nullable=False)
    active=db.Column(Boolean,nullable=False,default=True)

    
class Books(db.Model):
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(256), nullable=False)
    author = db.Column(String(256), nullable=False)
    qr=db.Column(String(256),unique=True, nullable=False)
    issue=db.Column(Boolean,nullable=False,default=False)


class Transaction(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(Integer, db.ForeignKey('books.id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False, default=date.today)
    due_date=db.Column(db.DateTime,nullable=False, default=due_date_calculator)
    return_date = db.Column(db.DateTime)
    returned=db.Column(Boolean,nullable=False,default=False)


