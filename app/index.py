from app import app
from flask import render_template, url_for


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/dang-ky-kham-truc-tuyen")
def make_appointment():
    return render_template('appointment.html')

@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
