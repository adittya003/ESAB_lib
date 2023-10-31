from . import db
from . import bcrypt
from sqlalchemy import Integer, String


class AdminUser(db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(32), unique=True, nullable=False)
    password = db.Column(String(256), nullable=False)
    
    def set_password(self, data):
        self.password = bcrypt.generate_password_hash(data).decode('utf-8')

    def check_password(self, data):
        return bcrypt.check_password_hash(self.password, data)

# class User(db.Model):
#     pass

# class Books(db.Model):
#     pass

# class Transaction(db.Model):
#     pass


