from flask import render_template,redirect,url_for,request
from . import app
from .form import * 
from .models import *

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user_qrscan', methods=["POST","GET"])
def user_qrscan():
    form=UserQrScan()
    if form.validate_on_submit():
        user=User.query.filter_by(qr=form.data.get('qr')).first()
        if user is None:
            return "Invalid QR"
        
        return redirect(url_for('book_qrscan',userid=user.id))
    return render_template('user_qr.html',form=form)


@app.route('/book_qrscan', methods=["POST","GET"])
def book_qrscan():
    form=BookQrScan()

    if request.args.get('userid') is None:
        return "No User ID Present"
    
    if form.validate_on_submit():
        return form.data.get("qr")
    
    return render_template('book_qr.html',form=form)
