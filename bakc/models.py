"""my_code"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(20), unique=True, nullable=False)
    u_pass = db.Column(db.String(255), nullable=False)
    c_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean, default=1)
    __tablename__ = 'user'


class Categroy(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(50), nullable=False)
    cats = db.relationship('Article', backref='a_c')
    __tablename__ = 'cat_type'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_name = db.Column(db.String(50), nullable=False)
    sketch = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    type_id = db.Column(db.Integer, db.ForeignKey('cat_type.id'))
    __tablename__ = 'article'