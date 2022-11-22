from app import app, dao, login
from flask import render_template, url_for, request, redirect, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.models import DanhSachKham, BenhNhan


@app.route("/dang-ky-kham-truc-tuyen", methods=['GET', 'POST'])
def make_appointment():
    msg = ''
    success = None
    if request.method.__eq__('POST'):
        day = request.form.get('date')
        if not dao.get_id_dskham_by_date(day):
            dao.add_dsKham(day)
        if dao.chk_patient(day):
            ho_ten = request.form.get('hoten')
            sdt = request.form.get('tel')
            ngay_sinh = request.form.get('birthdate')
            gioi_tinh = request.form.get('sex')
            dia_chi = request.form.get('address')
            dao.add_patient(hoTen=ho_ten,
                            sdt=sdt,
                            ngaySinh=ngay_sinh,
                            gioiTinh=gioi_tinh,
                            diaChi=dia_chi,
                            dsKhamId=dao.get_id_dskham_by_date(day),
                            )
            msg = 'Đăng ký thành công'
            success = True
        else:
            msg = 'Số bệnh nhân đăng ký đã đạt tối đa!'
            success = False
    return render_template('appointment.html', msg=msg, success=success)


@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route("/dang-nhap", methods=['get', 'post'])
def login():
    err_msg = ''
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


@app.route('/lap-phieu-kham', methods=['get', 'post'])
def lap_phieu_kham():
    msg = ''
    success = None
    medicines = dao.load_medicine(medicine=request.args.get('medicine'))
    if request.method.__eq__('POST'):
        hoTen = request.form.get('name')
        sdt = request.form.get('sdt')
        patient = dao.get_patient_by_sdt(sdt)
        ngayKham = request.form.get('date')
        trieuChung = request.form.get('trieu-chung')
        duDoanBenh = request.form.get('du-doan')
        if patient:
            dao.add_report(patient=patient,
                           ngayKhamBenh=ngayKham,
                           trieuChung=trieuChung,
                           duDoanBenh=duDoanBenh)
            phieuKham = dao.get_phieu_kham_by_date_patient_id(ngayKham, patient.id)
            dao.add_medicines_to_report(session['medicines'], phieuKham)

            success = True
            msg = 'Lập phiếu thành công'
            del session['medicines']
        else:
            msg = 'Bệnh nhân chưa đăng ký khám'
            success = False

    return render_template('/doctor/lapphieukham.html',
                           medicines=medicines,
                           msg=msg,
                           success=success)

@app.route('/ds-benh-nhan')
def xem_ds_benh_nhan():
    patients = dao.load_patient()
    ds = dao.load_dskham()
    return render_template('/nurse/danh-sach-benh-nhan.html',
                           patients=patients,
                           ds=ds)


@app.route('/ds-benh-nhan/<string:ngayKham>')
def chi_tiet_ds(ngayKham):
    ds = dao.load_dskham_by_date(ngayKham)
    patients = dao.load_patients_by_list(ds)
    return render_template('/nurse/danh-sach-benh-nhan-theo-ngay.html',
                           ds=ds,
                           patients=patients)


@app.route('/api/add-medicines-to-report', methods=['post'])
def add_medicines_to_report():
    data = request.json
    id = str(data.get('id'))
    tenThuoc = data.get('tenThuoc')
    donVi = data.get('donVi')
    donGia = data.get('donGia')
    medicines = session.get('medicines')

    if not medicines:
        medicines = {}
    if id in medicines:
        medicines[id]['soLuongThem'] = medicines[id]['soLuongThem'] + 1
    else:
        medicines[id] = {
            'id': id,
            'tenThuoc': tenThuoc,
            'donVi': donVi,
            'donGia': donGia,
            'soLuongThem': 1
        }
    session['medicines'] = medicines
    return jsonify(dao.count_medicines(medicines))


@app.route("/")
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
