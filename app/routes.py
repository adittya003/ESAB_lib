from flask import render_template,redirect,url_for,request
from . import app
from .form import * 
from .models import *
from datetime import date, timedelta

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user_qrscan_borrow', methods=["POST","GET"])
def user_qrscan_borrow():
    form=UserQrScan()
    if form.validate_on_submit():
        user = User.query.filter_by(
            qr=form.data.get('qr')
        ).first()
        if user is None:
            return "Invalid QR"
        
        return redirect(url_for('book_qrscan_borrow',userid=user.id))
    return render_template('user_qr_borrow.html',form=form)


@app.route('/book_qrscan_borrow', methods=["POST","GET"])
def book_qrscan_borrow():
    form=BookQrScan()

    user_id = request.args.get('userid')
    if user_id is None:
        return "No User ID Present"
    
    if form.validate_on_submit():
        book_qr = form.data.get("qr")

        user = User.query.filter_by(
            id = user_id
        ).first()

        book = Books.query.filter_by(
            qr = book_qr
        ).first()

        if user is None or book is None:
            return "Error"
        
        if book.issue:
            return "Book Already Issued"
        
        trans = Transaction()
        trans.user_id = user.id
        trans.book_id = book.id
        book.issue=True

        db.session.add(trans)
        db.session.commit()

        return "Issued",trans.id
    
    return render_template('book_qr_borrow.html',form=form,userid=user_id)




@app.route('/user_qrscan_return', methods=["POST","GET"])
def user_qrscan_return():
    form=UserQrScan()
    if form.validate_on_submit():
        user = User.query.filter_by(
            qr=form.data.get('qr')
        ).first()
        if user is None:
            return "Invalid QR"
        
        return redirect(url_for('book_qrscan_return',userid=user.id))
    return render_template('user_qr_return.html',form=form)


@app.route('/book_qrscan_return', methods=["POST","GET"])
def book_qrscan_return():
    form=BookQrScan()

    user_id = request.args.get('userid')
    if user_id is None:
        return "No User ID Present"
    
    if form.validate_on_submit():
        book_qr = form.data.get("qr")

        user = User.query.filter_by(
            id = user_id
        ).first()

        book = Books.query.filter_by(
            qr = book_qr
        ).first()

        if user is None or book is None:
            return "Error"
        
        if not book.issue:
            return "Book Already Returned"
        
        trans=Transaction.query.filter_by(user_id=user.id,book_id=book.id,return_date=None).first()
        if trans:
            trans.return_date = date.today()
            trans.returned=True
            book.issue=False
            db.session.add(trans)
            db.session.commit()
            return "Returned"
        
        else:
            return "No Transaction Found"
    
    return render_template('book_qr_return.html',form=form,userid=user_id)

