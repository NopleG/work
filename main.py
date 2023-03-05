from flask import Flask, render_template, request, redirect, url_for, sessions, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import sqlite3
import os
from sqlalchemy import desc
from config import DB_CONNECTION

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONNECTION
db = SQLAlchemy()
db.init_app(app)


class PriceList(db.Model):
    tablename = 'price_list'
    id = db.Column(db.Integer, primary_key=True)
    good_id = db.Column(db.Integer(), db.ForeignKey('goods.id'), nullable=True)
    created_on = db.Column(db.DateTime())
    price = db.Column(db.Float, nullable=False)

class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    recommend_price = db.Column(db.Float, nullable=True)
    url1 = db.Column(db.String, db.ForeignKey('goods.url'), nullable=True)
    url2 = db.Column(db.String, db.ForeignKey('goods.url'), nullable=True)
    url3 = db.Column(db.String, db.ForeignKey('goods.url'), nullable=True)
    url4 = db.Column(db.String, db.ForeignKey('goods.url'), nullable=True)
    my_url = db.Column(db.String, nullable=True)

    url_1 = db.relationship("Goods", foreign_keys=url1, lazy='select', backref=db.backref('listing1', lazy='select'))
    url_2 = db.relationship("Goods", foreign_keys=url2, lazy='select', backref=db.backref('listing2', lazy='select'))
    url_3 = db.relationship("Goods", foreign_keys=url3, lazy='select', backref=db.backref('listing3', lazy='select'))
    url_4 = db.relationship("Goods", foreign_keys=url4, lazy='select', backref=db.backref('listing4', lazy='select'))

# with app.app_context():
#     db.create_all()

class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    site = db.Column(db.String, nullable=False)





@app.route("/view", methods=["GET", "POST"])
@app.route("/view/<int:page>", methods=["GET", "POST"])
def view(page=1):

    info = Listing.query.paginate(page=page, per_page=3)
    return render_template('view.html', info=info)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = f"%{request.form['name']}%"
        result = Goods.query.filter(Goods.name.like(name)).all()

        return render_template('login.html', info=result)


    else:
        return render_template('login.html')


@app.route("/addNote", methods=["GET", "POST"])
def addNote():
    if request.method == "POST":
        name = request.form['name']
        url1 = request.form['url1']
        url2 = request.form['url2']
        url3 = request.form['url3']
        url4 = request.form['url4']
        data = Listing(name=name, url1=url1, url2=url2, url3=url3, url4=url4)
        db.session.add(data)
        db.session.commit()
        return render_template('addNote.html')
    else:
        return render_template('addNote.html')





@app.route("/editNote/<int:id>/", methods=["GET", "POST"])
def editNote(id):
    if id > 0:
        row = Listing.query.filter(Listing.id == id).first()
        if request.method == 'POST':
            row.name = request.form['name']
            row.url1 = request.form['url1']
            row.url2 = request.form['url2']
            row.url3 = request.form['url3']
            row.url4 = request.form['url4']
            db.session.commit()
            return redirect(url_for('editNote', id=row.id))
        return render_template('editNote.html', info=row)
    else:
        return render_template('index.html')


@app.route("/priceList/<int:id>/", methods=["GET", "POST"])
def priceList(id):
    if request.method == 'POST':
        pass
    result = PriceList.query.filter(PriceList.good_id == id).order_by(desc(PriceList.created_on)).all()

    for i in result:
        print(i.price)
        print(i.created_on)
    return render_template('priceList.html', info=result, id=id)


if __name__ == "__main__":
    app.run(debug=True)
