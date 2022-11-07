from app import app
from flask import render_template, url_for


@app.route("/")
def home():
    return render_template('index.html')


<<<<<<< HEAD
@app.route("/dang-ky-kham-truc-tuyen")
def make_appointment():
    return render_template('appointment.html')

=======
@app.route("/login")
def login():
    return render_template('login.html')
>>>>>>> 9496dad1edaf1a740e9bba089a8ab7fe45fbc278

if __name__ == '__main__':
    app.run(debug=True)
