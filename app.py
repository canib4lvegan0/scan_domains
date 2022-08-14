import os
from typing import List

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from requests import get

from names import names

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


class RegisterModel(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=False)

    @classmethod
    def find_by_name(cls, name) -> "RegisterModel":
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def get_urls(cls) -> List["RegisterModel"]:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }


def _try_get(url):
    try:
        resp = get(url=url)
        return resp.status_code == 200
    except:
        pass


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/scan')
def scan_urls():
    for name in names:
        url = f"http://www.{name}.com"
        if _try_get(url):
            if not RegisterModel.find_by_name(name):
                RegisterModel(name=name, url=url).save_to_db()
    return redirect(url_for('get_urls'))


@app.route('/urls')
def get_urls():
    return {"urls": [r.to_json() for r in RegisterModel.get_urls()]}, 200


if __name__ == '__main__':
    db.init_app(app)
    app.run()
