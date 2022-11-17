from app import app, dao, login
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user





@app.route("/dang-ky-kham-truc-tuyen")
def make_appointment():
    return render_template('appointment.html')

@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)

@app.route("/dang-nhap", methods=['get', 'post'])
def login():
    err_msg=''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        # return redirect('/')
        user = dao.check_login(username=username, password=password)

        if user:
            login_user(user=user)
            return redirect('/')
        else:
            err_msg = 'Sai tài khoản hoặc mật khẩu!!! vui lòng nhập lại'

    return render_template('login.html', err_msg=err_msg)
@app.route('/logout')
def logout():
    logout_user()
    return redirect('dang-nhap')
@app.route("/tra-cuu-thuoc")
def tra_cuu_thuoc():
    medicines = dao.load_medicine(medicine=request.args.get('medicine'))
    return render_template('/doctor/tracuuthuoc.html',
                           medicines=medicines)

@app.route("/")
def home():
    return render_template('index.html')
if __name__ == '__main__':
    # app.secret_key='super secret_key'
    app.run(debug=True)
