"""my_code"""

import redis

from flask import Flask
from flask_script import Manager
from flask_session import Session

from bakc.models import db
from bakc.views import blue, blueweb

app = Flask(__name__)
app.register_blueprint(blueprint=blue, url_prefix='/back')
app.register_blueprint(blueprint=blueweb, url_prefix='/web')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lhy213lhy@47.95.9.84:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = '123456789qwertyuiop'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='47.95.9.84', port=6379)
Session(app)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
