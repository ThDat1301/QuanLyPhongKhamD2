import datetime
import hashlib

from app.models import TaiKhoan, UserRole, BacSi, NguoiDung, LichKham, BenhNhan, Thuoc, PhieuKhamBenh, \
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


def add_lichKham(ngayKham):
    lichKham = LichKham(ngayKham=ngayKham)
    db.session.add(lichKham)
    db.session.commit()


def get_lich_kham_by_id(lichKhamId):
    return LichKham.query.get(lichKhamId)


def chk_patient(day):
    num = db.session.query(BenhNhan.id).join(LichKham).filter(LichKham.ngayKham == day)
    limit = db.session.query(LichKham.soLuong).filter(LichKham.ngayKham == day).first()
    if num.count() < limit.soLuong:
        return True
    return False


def load_patients_by_list(ds):
    patients = db.session.query(BenhNhan).filter(BenhNhan.lichKhamId == ds.id).all()
    return patients


def get_patient_by_cccd(cccd):
    return BenhNhan.query.filter(BenhNhan.cccd == cccd).first()


def get_patient_by_id(patient_id):
    return BenhNhan.query.filter(BenhNhan.id == patient_id).first()


def load_lichkham():
    return LichKham.query.all()


def load_lichkham_by_date(day):
    return LichKham.query.filter(LichKham.ngayKham == day).first()


def get_id_lichkham_by_date(date):
    ds = LichKham.query.filter(LichKham.ngayKham == date).first()
    if ds:
        return ds.id
    return False


def load_patient():
    patients = db.session.query(BenhNhan).all()
    return patients


def add_patient(hoTen, sdt, ngaySinh, gioiTinh, diaChi, lichKhamId, cccd):
    benh_nhan = BenhNhan(hoTen=hoTen,
                         cccd=cccd,
                         sdt=sdt,
                         ngaySinh=ngaySinh,
                         gioiTinh=gioiTinh,
                         diaChi=diaChi,
                         lichKhamId=lichKhamId)
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
                                                 phieukhambenh_id=report.id,
                                                 cachDung=m.get('cachDung'),
                                                )
            db.session.add(report_details)
        db.session.commit()


def get_phieu_kham_by_date_patient_id(day, patient_id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.ngayKhamBenh == day
                                      and PhieuKhamBenh.benhNhanId == patient_id).first()


def get_phieu_kham_by_patient_id(patient_id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.benhNhanId == patient_id).all()


def load_patient(patient_name=None):
    query = BenhNhan.query
    if patient_name:
        query = query.filter(BenhNhan.hoTen.contains(patient_name))
    return query.all()


def load_report_medicines_by_report_id(r_id):
    return PhieuKhamBenh_Thuoc.query.filter(PhieuKhamBenh_Thuoc.phieukhambenh_id == r_id)


def load_medicines_in_report(report_id):
    return db.session.query(Thuoc.tenThuoc, Thuoc.donVi, PhieuKhamBenh_Thuoc.soLuong, PhieuKhamBenh_Thuoc.cachDung)\
              .join(Thuoc, PhieuKhamBenh_Thuoc.thuoc_id.__eq__(Thuoc.id))\
              .filter(PhieuKhamBenh_Thuoc.phieukhambenh_id == report_id).all()


def get_report_by_id(report_id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.id == report_id).first()


def get_patient_by_id(patient_id):
    return BenhNhan.query.filter(BenhNhan.id == patient_id).first()

def load_report(idPhieuKham = None):
    patient = db.session.query(PhieuKhamBenh.id, BenhNhan.hoTen, BenhNhan.sdt, PhieuKhamBenh.ngayKhamBenh).join(BenhNhan, PhieuKhamBenh.benhNhanId.__eq__(BenhNhan.id))
    if idPhieuKham:
        patient = patient.filter(BenhNhan.id.__eq__(idPhieuKham))
    return patient.all()


if __name__ == '__main__':
    with app.app_context():
        print(BenhNhan.query.all())




