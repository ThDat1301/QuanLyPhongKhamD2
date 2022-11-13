from app import app, dao
from flask import render_template, url_for, request


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/dang-ky-kham-truc-tuyen")
def make_appointment():
    return render_template('appointment.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/tra-cuu-thuoc")
def tra_cuu_thuoc():
    medicines = dao.load_medicine(medicine=request.args.get('medicine'))
    return render_template('/doctor/tracuuthuoc.html',
                           medicines=medicines)


if __name__ == '__main__':
    app.run(debug=True)
