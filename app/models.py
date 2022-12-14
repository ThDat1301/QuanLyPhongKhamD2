import datetime
import hashlib

from sqlalchemy import Column, String, Integer, Boolean, Date, Float, ForeignKey, func, Enum
from enum import Enum as UserEnum
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from app import app, db


class UserRole(UserEnum):
    NURSE = 1
    DOCTOR = 2
    CASHIER = 3
    ADMIN = 4


class NguoiDung(db.Model):
    __tablename__ = 'nguoidung'
    id = Column(Integer, primary_key=True, autoincrement=True)
    namSinh = Column(Integer, nullable=False)
    diaChi = Column(String(100), nullable=False)
    hoTen = Column(String(50), nullable=False)
    sdt = Column(String(10), nullable=False)
    taiKhoan = relationship('TaiKhoan', backref='nguoidung', lazy=True, uselist=False)


class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'taikhoan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vaiTro = Column(Enum(UserRole), default=UserRole.NURSE, nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    nguoiDungId = Column(Integer, ForeignKey(NguoiDung.id), nullable=False, unique=True)

    def isDoctor(self):
        if self.vaiTro == UserRole.DOCTOR:
            return True

    def isNurse(self):
        if self.vaiTro == UserRole.NURSE:
            return True

    def isAdmin(self):
        if self.vaiTro == UserRole.ADMIN:
            return True

    def isCashier(self):
        if self.vaiTro == UserRole.CASHIER:
            return True

    def __str__(self):
        return self.username


class BacSi(NguoiDung):
    chuyenKhoa = Column(String(50))


benhnhan_lichkham = db.Table('benhnhan_lichkham',
                           Column('benhNhanId', Integer,
                                  ForeignKey('benhnhan.id'),
                                  primary_key=True, nullable=False),
                           Column('lichKhamId', Integer,
                                  ForeignKey('lichkham.id'),
                                  primary_key=True, nullable=False)
                           )


class LichKham(db.Model):
    __tablename__ = 'lichkham'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayKham = Column(Date, default=datetime.date.today(), nullable=False, unique=True)
    soLuong = Column(Integer, default=40)
    tienKham = Column(Integer, default=100000)


class BenhNhan(db.Model):
    __tablename__ = 'benhnhan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50), nullable=False)
    sdt = Column(String(10), nullable=False)
    ngaySinh = Column(Date, nullable=False)
    gioiTinh = Column(String(10), nullable=False)
    diaChi = Column(String(100))
    cccd = Column(String(12), nullable=False, unique=True)
    phieuKhamBenh = relationship('PhieuKhamBenh', backref='benhnhan', lazy=True)
    lichKham = relationship('LichKham', secondary='benhnhan_lichkham', lazy='subquery',
                            backref=backref('benhnhan', lazy='joined'))

    def __str__(self):
        return self.hoTen


class PhieuKhamBenh(db.Model):
    __tablename__ = 'phieukhambenh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayKhamBenh = Column(Date, nullable=False)
    trieuChung = Column(String(200), nullable=False)
    duDoanBenh = Column(String(200), nullable=False)
    benhNhanId = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    thuoc = relationship('PhieuKhamBenh_Thuoc', backref='phieukhambenh')

    def __str__(self):
        return self.id


class Thuoc(db.Model):
    __tablename__ = 'thuoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    donVi = Column(String(50), nullable=False)
    donGia = Column(Float, nullable=False)
    soLuong = Column(Integer, default=100, nullable=False)
    image = Column(String(200))
    active = Column(Boolean, default=True)
    phieuKhamBenh = relationship('PhieuKhamBenh_Thuoc', backref='thuoc')


class PhieuKhamBenh_Thuoc(db.Model):
    __table_name = 'phieukhambenh_thuoc'
    phieukhambenh_id = Column(ForeignKey(PhieuKhamBenh.id), primary_key=True)
    thuoc_id = Column(ForeignKey(Thuoc.id), primary_key=True)
    soLuong = Column(Integer, nullable=False)
    cachDung = Column(String(200))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        bs = BacSi(namSinh=2002, diaChi='B??nh T??n', hoTen='L?? Minh ?????c', sdt='0123456790', chuyenKhoa='Mat')
        tkbs = TaiKhoan(vaiTro=UserRole.DOCTOR, username='bacsi', password=password, nguoiDungId=1)
        yta = NguoiDung(namSinh=2002, diaChi='B??nh T??n', hoTen='Tr????ng Th??nh ?????t', sdt='0123456790')
        tkyta = TaiKhoan(vaiTro=UserRole.NURSE, username='yta', password=password, nguoiDungId=2)
        ad = NguoiDung(namSinh=2002, diaChi='B??nh T??n', hoTen='V??n Tr??c Vy', sdt='0123456790')
        tkad = TaiKhoan(vaiTro=UserRole.ADMIN, username='admin', password=password, nguoiDungId=3)
        tn = NguoiDung(namSinh=2002, diaChi='Binh Tan', hoTen='Nguyen Van A', sdt='015123213')
        tktn = TaiKhoan(vaiTro=UserRole.CASHIER, username='thungan', password=password, nguoiDungId=4)
        db.session.add_all([bs, tkbs, yta, tkyta, ad, tkad, tn, tktn])
        db.session.commit()
# T???o b???ng

        t1 = Thuoc(tenThuoc="Tobrex", donVi="L???", donGia="42798", image="https://res.cloudinary.com/dgyytgkae/image/upload/v1668356628/medicine/tobrex_tuhk3d.jpg")
        t2 = Thuoc(tenThuoc="Natri Colorid thu???c nh??? m???t", donVi="L???", donGia="1617", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/natriclorid_wqho0t.jpg')
        t3 = Thuoc(tenThuoc="Dentuz", donVi="L???", donGia="126000", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/dentuz_js7bgg.jpg')
        t4 = Thuoc(tenThuoc="Espumisan", donVi="L???", donGia="57030", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/espumisan_ewagvp.jpg')
        t5 = Thuoc(tenThuoc="Flumetholon", donVi="L???", donGia="32177", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358414/medicine/20220329_082951_725761_Flumetholon.max-1800x1800_lxluud.jpg')
        t6 = Thuoc(tenThuoc="Iodine 30ml", donVi="L???", donGia="6291", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/iodine_a36q8c.webp')
        t7 = Thuoc(tenThuoc="Klacid", donVi="L???", donGia="108296", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/klacid_wttgqi.jpg')
        t8 = Thuoc(tenThuoc="Lantus", donVi="L???", donGia="530250", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/lantus-100iuml-10ml-lo-17147_xv64j6.webp')
        t9 = Thuoc(tenThuoc="Laforin", donVi="L???", donGia="101115", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/laforin_qxcn2f.jpg')
        t10 = Thuoc(tenThuoc="Mixtard 30", donVi="L???", donGia="70619", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/00004976-mixtard-100iuml-8681-5f28_large_imkw3r.jpg')
        t11 = Thuoc(tenThuoc="Acetazolamid", donVi="Vi??n", donGia="1150", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/20200111_013058_854007_acetazolamid-250mg-.max-1800x1800_xahhcg.jpg')
        t12 = Thuoc(tenThuoc="Alphachymotrypsin", donVi="Vi??n", donGia="839", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/ALPHACHYMOTRYPSIN_v4glik.jpg')
        t13 = Thuoc(tenThuoc="Albuglucan", donVi="Vi??n", donGia="28364", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/ALBUGLUCAN_zauekf.png')
        t14 = Thuoc(tenThuoc="Licotan", donVi="Vi??n", donGia="5885", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/Licotan_yn9zzv.jpg')
        t15 = Thuoc(tenThuoc="Cordarone", donVi="Vi??n", donGia="7222", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/20220605_085302_864175_Cordarone_-200mg.max-1800x1800_c1i2lz.jpg')
        t16 = Thuoc(tenThuoc="Digorich", donVi="Vi??n", donGia="678", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/digorich_jpcgja.jpg')
        t17 = Thuoc(tenThuoc="Epclusa", donVi="Vi??n", donGia="281137", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668359578/medicine/Epclusa_oblviw.jpg')
        t18 = Thuoc(tenThuoc="Fluconazol", donVi="Vi??n", donGia="11770", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/00003097-fluconazol-150mg-3318-5b6d_large_oj8epo.webp')
        t19 = Thuoc(tenThuoc="Glucophage", donVi="Vi??n", donGia="4073", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/20220215_141017_242436_thuoc-glucophage.max-1800x1800_vqdzhp.jpg')
        t20 = Thuoc(tenThuoc="Imexime 200", donVi="Vi??n", donGia="7383", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/20220613_003441_863812_Imexime_-200.max-1800x1800_uwksaq.jpg')
        t21 = Thuoc(tenThuoc="BB M Mocagos", donVi="G??i", donGia="2750", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/MOCAGOS_eztwf3.jpg')
        t22 = Thuoc(tenThuoc="Benokid colos", donVi="G??i", donGia="14445", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/Th%E1%BB%B1c-ph%E1%BA%A9m-b%E1%BB%95-sung-Benokid-Colos-1_vqfh6n.jpg')
        t23 = Thuoc(tenThuoc="B??ng g???c", donVi="G??i", donGia="11235", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/bonggac_sewlcf.jpg')
        t24 = Thuoc(tenThuoc="Didicera", donVi="G??i", donGia="4180", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/didicera_trw2ts.jpg')
        t25 = Thuoc(tenThuoc="Duphalac", donVi="G??i", donGia="3000", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/DUPHALAC_a80wab.jpg')
        t26 = Thuoc(tenThuoc="Egaruta", donVi="G??i", donGia="6419", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/EGARUTA_l233ky.jpg')
        t27 = Thuoc(tenThuoc="Eroleucin", donVi="G??i", donGia="31458", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/EROLEUCIN_vi9moe.jpg')
        t28 = Thuoc(tenThuoc="Forlax", donVi="G??i", donGia="4702", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/FORLAX_eacyqx.jpg')
        t29 = Thuoc(tenThuoc="Hydrite gra", donVi="G??i", donGia="2795", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/HYDRITE_zgund9.jpg')
        t30 = Thuoc(tenThuoc="Nabifar", donVi="G??i", donGia="772", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/NABIFAR_isrzhq.jpg')

        db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10,
                           t11, t12, t13, t14, t15, t16, t17, t18, t19, t20,
                           t21, t22, t23, t24, t25, t26, t27, t28, t29, t30])

        db.session.commit()

