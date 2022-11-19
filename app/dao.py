import hashlib

from app.models import TaiKhoan, UserRole, BacSi, NguoiDung, ChiTietDSKham, DanhSachKham

from app.models import Thuoc
from app import db


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
        result = db.session.query(NguoiDung.hoTen).join(TaiKhoan).filter(username.nguoiDungId == TaiKhoan.nguoiDungId).first()
        return result.hoTen


def add_dsKham():
    dsKham = DanhSachKham()
    db.session.add(dsKham)
    db.session.commit()


def add_patient(hoTen, sdt, ngaySinh, gioiTinh):
    benh_nhan = ChiTietDSKham(hoTen=hoTen,
                              sdt=sdt,
                              ngaySinh=ngaySinh,
                              gioiTinh=gioiTinh,
                              dsKhamId=1)
    db.session.add(benh_nhan)
    db.session.commit()