import os
from typing import List
import time
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from requests import get
from threading import Thread
from names import names
from dotenv import load_dotenv

load_dotenv(".env")

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


def _scanner_1(name):
    print("running scanner_3 for {}".format(name))
    if not RegisterModel.find_by_name(name):
        url = f"http://www.{name}.com"
        try:
            resp = get(url=url)
            if resp.status_code == 200:
                print(f"{url} - ok")
                RegisterModel(name=name, url=url).save_to_db()
        except:
            pass

def _scanner_2(name):
    print("running scanner_2 for {}".format(name))
    if not RegisterModel.find_by_name(name):
        url = f"http://www.{name}.com"
        try:
            resp = get(url=url)
            if resp.status_code == 200:
                print(f"{url} - ok")
                RegisterModel(name=name, url=url).save_to_db()
        except:
            pass

def _scanner_3(name):
    print("running scanner_3 for {}".format(name))
    if not RegisterModel.find_by_name(name):
        url = f"http://www.{name}.com"
        try:
            resp = get(url=url)
            if resp.status_code == 200:
                print(f"{url} - ok")
                RegisterModel(name=name, url=url).save_to_db()
        except:
            pass

def _scanner_4(name):
    print("running scanner_3 for {}".format(name))
    if not RegisterModel.find_by_name(name):
        url = f"http://www.{name}.com"
        try:
            resp = get(url=url)
            if resp.status_code == 200:
                print(f"{url} - ok")
                RegisterModel(name=name, url=url).save_to_db()
        except:
            pass


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


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/scan')
def scan_urls():

    for name in names:
        if name[0] in "abcde":
            Thread(target=_scanner_1(name), args=[]).start()
        if name[0] in "fghij":
            Thread(target=_scanner_2(name), args=[]).start()
        if name[0] in "klmnop":
            Thread(target=_scanner_3(name), args=[]).start()
        if name[0] in "qrstuvwxyz":
            Thread(target=_scanner_4(name), args=[]).start()

    return redirect(url_for('get_urls'))


@app.route('/urls')
def get_urls():
    return {"urls": [r.to_json() for r in RegisterModel.get_urls()]}, 200

db.init_app(app)

if __name__ == '__main__':
    app.run()
