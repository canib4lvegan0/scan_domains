import os
from typing import List
from requests import get
from threading import Thread

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy import text

from dotenv import load_dotenv
load_dotenv(".env")

from names import names, clean_names

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


def _scanner(name, th):
    print("running {} for {}".format(name, th))
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
        return cls.query.order_by(text("id DESC")).all()

    @classmethod
    def get_names(cls) -> List["RegisterModel"]:
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
        if not RegisterModel.find_by_name(name):
            if name[0] in "abcde":
                Thread(target=_scanner(name, "th1"), args=[]).start()
            if name[0] in "fghij":
                Thread(target=_scanner(name, "th2"), args=[]).start()
            if name[0] in "klmnop":
                Thread(target=_scanner(name, "th3"), args=[]).start()
            if name[0] in "qrstuvwxyz":
                Thread(target=_scanner(name, "th4"), args=[]).start()

    return redirect(url_for('clean'))

@app.route('/urls')
def get_urls():
    return {"urls": [r.to_json() for r in RegisterModel.get_urls()]}, 200

@app.route('/<string:name>')
def get_url(name):
    if (result := RegisterModel.find_by_name(name)) is None:
        return {"message": f"{name} not found."}
    return {"url": result.to_json()}, 200

@app.route('/clean')
def clean():
    clean_names(set([r.to_json()['name'] for r in RegisterModel.get_names()]), names)
    return redirect(url_for('get_urls'))


db.init_app(app)

if __name__ == '__main__':
    app.run()
