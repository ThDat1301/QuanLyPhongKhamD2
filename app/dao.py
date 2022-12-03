import datetime
import hashlib

from app.models import TaiKhoan, UserRole, BacSi, NguoiDung, DanhSachKham, BenhNhan, Thuoc, PhieuKhamBenh, \
    PhieuKhamBenh_Thuoc
from sqlalchemy import func
from app import db, app
from datetime import date


def load_medicine(medicine=None):
    query = Thuoc.query.filter(Thuoc.active.__eq__(True))
    if medicine:
        query = query.filter(Thuoc.tenThuoc.contains(medicine))
    return query.all()


def get_user_by_id(user_id):
    return TaiKhoan.query.get(user_id)


def check_login(username, password):
    if username and password:
        # password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()),
                                     TaiKhoan.password.__eq__(password)).first()


def check_name_user(username):
    if username:
        result = db.session.query(NguoiDung.hoTen).join(TaiKhoan).filter(
            username.nguoiDungId == TaiKhoan.nguoiDungId).first()
        return result.hoTen


def add_dsKham(ngayKham):
    dsKham = DanhSachKham(ngayKham=ngayKham)
    db.session.add(dsKham)
    db.session.commit()


def get_ds_kham_by_id(dskhamid):
    return DanhSachKham.query.get(dskhamid)


def chk_patient(day):
    num = db.session.query(BenhNhan.id).join(DanhSachKham).filter(DanhSachKham.ngayKham == day)
    limit = db.session.query(DanhSachKham.soLuong).filter(DanhSachKham.ngayKham == day).first()
    if num.count() <= limit.soLuong:
        return True
    return False


def load_patients_by_list(ds):
    patients = db.session.query(BenhNhan).filter(BenhNhan.dsKhamId == ds.id).all()
    return patients


def get_patient_by_cccd(cccd):
    return BenhNhan.query.filter(BenhNhan.cccd == cccd).first()


def get_patient_by_id(patient_id):
    return BenhNhan.query.filter(BenhNhan.id == patient_id).first()


def load_dskham():
    return DanhSachKham.query.all()


def load_dskham_by_date(day):
    return DanhSachKham.query.filter(DanhSachKham.ngayKham == day).first()


def get_id_dskham_by_date(date):
    ds = DanhSachKham.query.filter(DanhSachKham.ngayKham == date).first()
    if ds:
        return ds.id
    return False


def load_patient():
    patients = db.session.query(BenhNhan).all()
    return patients


def add_patient(hoTen, sdt, ngaySinh, gioiTinh, diaChi, dsKhamId, cccd):
    benh_nhan = BenhNhan(hoTen=hoTen,
                         cccd=cccd,
                         sdt=sdt,
                         ngaySinh=ngaySinh,
                         gioiTinh=gioiTinh,
                         diaChi=diaChi,
                         dsKhamId=dsKhamId)
    db.session.add(benh_nhan)
    db.session.commit()


def count_medicines(medicines):
    total_quantity, total_ammount = 0, 0
    if medicines:
        for m in medicines.values():
            total_quantity += m.get('soLuongThem')
            total_ammount += m.get('soLuongThem') * m.get('donGia')
    return {
        'total_quantity': total_quantity,
        'total_ammount': total_ammount
    }


def add_report(patient, ngayKhamBenh, trieuChung, duDoanBenh):
    report = PhieuKhamBenh(benhNhanId=patient.id,
                           ngayKhamBenh=ngayKhamBenh,
                           trieuChung=trieuChung,
                           duDoanBenh=duDoanBenh)
    db.session.add(report)
    db.session.commit()


def add_medicines_to_report(medicines, report):
    if medicines:
        for m in medicines.values():
            report_details = PhieuKhamBenh_Thuoc(soLuong=m.get('soLuongThem'),
                                                 thuoc_id=m.get('id'),
                                                 phieukhambenh_id=report.id)
            db.session.add(report_details)
        db.session.commit()


def get_phieu_kham_by_date_patient_id(day, patient_id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.ngayKhamBenh == day
                                      and PhieuKhamBenh.benhNhanId == patient_id).first()


def get_phieu_kham_by_patient_id(patient_id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.benhNhanId == patient_id).all()


def load_patient():
    return BenhNhan.query.all()




