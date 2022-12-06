from app import app, dao, login
from flask import render_template, url_for, request, redirect, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.models import LichKham, BenhNhan, UserRole


@app.route("/dang-ky-kham-truc-tuyen", methods=['GET', 'POST'])
def make_appointment():
    msg = ''
    success = None
    if request.method.__eq__('POST'):
        day = request.form.get('date')
        if not dao.get_id_lichkham_by_date(day):
            dao.add_lichKham(day)
        if dao.chk_patient(day):
            ho_ten = request.form.get('hoten')
            cccd = request.form.get('cccd')
            sdt = request.form.get('tel')
            ngay_sinh = request.form.get('birthdate')
            gioi_tinh = request.form.get('sex')
            dia_chi = request.form.get('address')
            try:
                dao.add_patient(hoTen=ho_ten,
                                cccd=cccd,
                                sdt=sdt,
                                ngaySinh=ngay_sinh,
                                gioiTinh=gioi_tinh,
                                diaChi=dia_chi,
                                lichKhamId=dao.get_id_lichkham_by_date(day),
                                )
            except Exception as ex:
                msg = "Lỗi hệ thống!"
                return render_template('appointment.html', msg=msg, success=success)
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
        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            # print(current_user.vaiTro)
            if current_user.vaiTro == UserRole.ADMIN:
                return  redirect('/admin')
            else:
                return redirect('/')
        else:
            err_msg = 'Sai tài khoản hoặc mật khẩu!!! Vui lòng nhập lại'

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
        cccd = request.form.get('cccd')
        patient = dao.get_patient_by_cccd(cccd)
        ngayKham = request.form.get('date')
        trieuChung = request.form.get('trieu-chung')
        duDoanBenh = request.form.get('du-doan')
        medicines_in_list = session.get('medicines')
        if not medicines_in_list:
            medicines_in_list = {}
        if patient:
            try:
                dao.add_report(patient=patient,
                               ngayKhamBenh=ngayKham,
                               trieuChung=trieuChung,
                               duDoanBenh=duDoanBenh)
                phieuKham = dao.get_phieu_kham_by_date_patient_id(ngayKham, patient.id)
                dao.add_medicines_to_report(medicines_in_list, phieuKham)
            except:
                msg = "Lỗi hệ thống"
                del session['medicines']
                return render_template('/doctor/lapphieukham.html',
                                       medicines=medicines,
                                       msg=msg,
                                       success=success)
            success = True
            msg = 'Lập phiếu thành công'
            del session['medicines']
        else:
            msg = 'Bệnh nhân không tồn tại'
            success = False

    return render_template('/doctor/lapphieukham.html',
                           medicines=medicines,
                           msg=msg,
                           success=success)


@app.route('/ds-benh-nhan')
def xem_ds_benh_nhan():
    patients = dao.load_patient()
    ds = dao.load_lichkham()
    return render_template('/nurse/danh-sach-benh-nhan.html',
                           patients=patients,
                           ds=ds)


@app.route('/ds-benh-nhan/<string:ngayKham>')
def chi_tiet_ds(ngayKham):
    ds = dao.load_lichkham_by_date(ngayKham)
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
            'soLuongThem': 1,
            'cachDung': ''
        }
    session['medicines'] = medicines
    return jsonify(dao.count_medicines(medicines))


@app.route('/api/update-medicines', methods=['put'])
def update_number_medicines():
    data = request.json
    id = str(data.get('id'))
    soLuongThem = data.get('soLuongThem')
    medicines = session.get('medicines')
    if medicines and id in medicines:
        medicines[id]['soLuongThem'] = soLuongThem
        session['medicines'] = medicines

    return jsonify(dao.count_medicines(medicines))


@app.route('/api/update-use-medicines', methods=['put'])
def update_use_medicines():
    data = request.json
    cachDung = data.get('cachDung')
    id = str(data.get('id'))
    medicines = session.get('medicines')
    if medicines and id in medicines:
        medicines[id]['cachDung'] = cachDung
        session['medicines'] = medicines

    return jsonify(dao.count_medicines(medicines))


@app.route('/api/delete-medicines/<medicine_id>', methods=['delete'])
def delete_medicines(medicine_id):
    medicines = session.get('medicines')
    if medicines and medicine_id in medicines:
        del medicines[medicine_id]
        session['medicines'] = medicines
    return jsonify(dao.count_medicines(medicines))


@app.route('/xem-lich-su-benh-nhan')
def history_patients():
    patients = dao.load_patient(patient_name=request.args.get('patient_name'))
    return render_template('/doctor/xemdanhsachlichsubenhnhan.html',
                           patients=patients)


@app.route('/xem-lich-su-benh-nhan/<int:patient_id>')
def history_patient(patient_id):
    patient = dao.get_patient_by_id(patient_id)
    report_patient = dao.get_phieu_kham_by_patient_id(patient_id)
    medicines_use = []
    for r in report_patient:
        medicines_use.append(dao.load_medicines_in_report(r.id))
    print(medicines_use)
    for m in medicines_use:
        print(m)
    return render_template('/doctor/xemlichsubenhnhan.html',
                           patient=patient,
                           report_patient=report_patient,
                           medicines_use=medicines_use
                           )


@app.route('/chi-tiet-phieu-kham/<int:report_id>')
def report_details(report_id):
    report = dao.get_report_by_id(report_id)
    patient = dao.get_patient_by_id(report.benhNhanId)
    medicines = dao.load_medicines_in_report(report_id)
    return render_template('/doctor/chitietphieukham.html',
                           report=report,
                           medicines=medicines,
                           name_patient=patient
                           )

@app.route("/")
def home():
    return render_template('index.html')


if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)
