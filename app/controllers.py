from app import app, dao, login
from flask import render_template, url_for, request, redirect, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import LichKham, BenhNhan, UserRole


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
                if dao.check_patient_by_cccd(cccd):
                    benh_nhan = dao.get_patient_by_cccd(cccd)
                    lichKham = dao.get_lichkham_by_date(day)
                    benh_nhan.lichKham.append(lichKham)
                    db.session.add(benh_nhan)
                    db.session.commit()
                else:
                    benh_nhan = BenhNhan(hoTen=ho_ten,
                                         cccd=cccd,
                                         sdt=sdt,
                                         ngaySinh=ngay_sinh,
                                         gioiTinh=gioi_tinh,
                                         diaChi=dia_chi)
                    lichKham = dao.get_lichkham_by_date(day)
                    benh_nhan.lichKham.append(lichKham)
                    db.session.add(benh_nhan)
                    db.session.commit()
            except Exception as ex:
                msg = "Lỗi hệ thống!"
                return render_template('appointment.html', msg=msg, success=success)
            msg = 'Đăng ký thành công'
            success = True
        else:
            msg = 'Số bệnh nhân đăng ký đã đạt tối đa!'
            success = False
    return render_template('appointment.html', msg=msg, success=success)


def login():
    if current_user.is_authenticated:
        return redirect('/')
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            if current_user.vaiTro == UserRole.ADMIN:
                return redirect('/admin')
            else:
                return redirect('/')
        else:
            err_msg = 'Sai tài khoản hoặc mật khẩu!!! Vui lòng nhập lại'
    return render_template('login.html', err_msg=err_msg)


def logout():
    logout_user()
    return redirect('/dang-nhap')


@login_required
def tra_cuu_thuoc():
    medicines = dao.load_medicine(medicine=request.args.get('medicine'))
    return render_template('/doctor/tracuuthuoc.html',
                           medicines=medicines)


@login_required
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
            if dao.is_make_appointment(patient.id, dao.get_id_lichkham_by_date(ngayKham)):
                try:
                    dao.add_report(patient=patient,
                                   ngayKhamBenh=ngayKham,
                                   trieuChung=trieuChung,
                                   duDoanBenh=duDoanBenh)
                    phieuKham = dao.get_phieu_kham_by_date_patient_id(ngayKham, patient.id)
                    dao.add_medicines_to_report(medicines_in_list, phieuKham)
                except:
                    msg = "Lỗi hệ thống"
                    return render_template('/doctor/lapphieukham.html',
                                           medicines=medicines,
                                           msg=msg,
                                           success=success)
                success = True
                msg = 'Lập phiếu thành công'
                del session['medicines']
            else:
                msg = 'Bệnh nhân chưa đăng ký lịch khám'
                success = False

        else:
            msg = 'Bệnh nhân không tồn tại'
            success = False

    return render_template('/doctor/lapphieukham.html',
                           medicines=medicines,
                           msg=msg,
                           success=success)


@login_required
def xem_ds_benh_nhan():
    patients = dao.load_patient()
    ds = dao.load_lichkham()
    return render_template('/nurse/danh-sach-benh-nhan.html',
                           patients=patients,
                           ds=ds)


@login_required
def chi_tiet_ds(ngayKham):
    ds = dao.load_lichkham_by_date(ngayKham)
    patients = dao.load_patients_by_date(ngayKham)
    return render_template('/nurse/danh-sach-benh-nhan-theo-ngay.html',
                           ds=ds,
                           patients=patients)


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


def update_number_medicines():
    data = request.json
    id = str(data.get('id'))
    soLuongThem = data.get('soLuongThem')
    medicines = session.get('medicines')
    if medicines and id in medicines:
        medicines[id]['soLuongThem'] = soLuongThem
        session['medicines'] = medicines

    return jsonify(dao.count_medicines(medicines))


def update_use_medicines():
    data = request.json
    cachDung = data.get('cachDung')
    id = str(data.get('id'))
    medicines = session.get('medicines')
    if medicines and id in medicines:
        medicines[id]['cachDung'] = cachDung
        session['medicines'] = medicines

    return jsonify(dao.count_medicines(medicines))


def delete_medicines(medicine_id):
    medicines = session.get('medicines')
    if medicines and medicine_id in medicines:
        del medicines[medicine_id]
        session['medicines'] = medicines
    return jsonify(dao.count_medicines(medicines))


@login_required
def history_patients():
    patients = dao.load_patient(patient_name=request.args.get('patient_name'))
    return render_template('/doctor/xemdanhsachlichsubenhnhan.html',
                           patients=patients)


@login_required
def history_patient(patient_id):
    patient = dao.get_patient_by_id(patient_id)
    report_patient = dao.get_phieu_kham_by_patient_id(patient_id)
    medicines_use = []
    for r in report_patient:
        medicines_use.append(dao.load_medicines_in_report(r.id))
    return render_template('/doctor/xemlichsubenhnhan.html',
                           patient=patient,
                           report_patient=report_patient,
                           medicines_use=medicines_use
                           )


@login_required
def report_details(report_id):
    report = dao.get_report_by_id(report_id)
    patient = dao.get_patient_by_id(report.benhNhanId)
    medicines = dao.load_medicines_in_report(report_id)
    return render_template('/doctor/chitietphieukham.html',
                           report=report,
                           medicines=medicines,
                           name_patient=patient
                           )


@login_required
def bill():
    idPhieuKham = request.args.get('bill')
    dsPhieuKham = dao.load_report(idPhieuKham)
    return render_template('/Cashier/ThanhToanHoaDon.html',
                           dsPhieuKham=dsPhieuKham)


@login_required
def get_payment(PhieuKhamBenh_id):
    patient_receipt = dao.load_report(PhieuKhamBenh_id)
    payment = dao.get_money(str(patient_receipt[0][3]))
    price_medicines = dao.get_price_medicines(PhieuKhamBenh_id)
    return render_template('/Cashier/HoaDon.html',
                           patient_receipt=patient_receipt,
                           payment=payment,
                           price_medicines=price_medicines)


def home():
    return render_template('index.html')


if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)
