from sqlalchemy import Column, String, Integer, Boolean, Date, Float, ForeignKey, func, Enum
from enum import Enum as UserEnum
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import app, db


class UserRole(UserEnum):
    USER = 1
    NURSE = 2
    DOCTOR = 3
    CASHIER = 4
    ADMIN = 5


class NguoiDung(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    namSinh = Column(Integer, nullable=False)
    diaChi = Column(String(100), nullable=False)
    hoTen = Column(String(50), nullable=False)
    sdt = Column(String(10), nullable=False)
    vaiTro = Column(Enum(UserRole), default=UserRole.USER)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
class BenhNhan(NguoiDung):
    gioiTinh = Column(Boolean, default=True, nullable=False)
    cmnd = Column(String(12), nullable=False)


class BacSi (NguoiDung):
    chuyenKhoa = Column(String(50))
    active = Column(Boolean, default=True)

class YTa(NguoiDung):
    pass


class ThuNgan(NguoiDung):
    pass


class PhieuKhamBenh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayKhamBenh = Column(Date, nullable=False)
    trieuChung = Column(String(200), nullable=False)
    duDoanBenh = Column(String(200), nullable=False)


class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    donVi = Column(String(50), nullable=False)
    donGia = Column(Float, nullable=False)
    image = Column(String(200))
    active = Column(Boolean, default=True)


class HoaDon(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tienKham = Column(Float, nullable=False)
    tienThuoc = Column(Float, nullable=False)
    ngayBan = Column(Date, nullable=False)

class quanTri(NguoiDung):
    pass

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
if __name__ == '__main__':
    with app.app_context():
        # Tạo bảng
        db.create_all()

        t1 = Thuoc(tenThuoc="Tobrex", donVi="Lọ", donGia="42798", image="https://res.cloudinary.com/dgyytgkae/image/upload/v1668356628/medicine/tobrex_tuhk3d.jpg")
        t2 = Thuoc(tenThuoc="Natri Colorid thuốc nhỏ mắt", donVi="Lọ", donGia="1617", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/natriclorid_wqho0t.jpg')
        t3 = Thuoc(tenThuoc="Dentuz", donVi="Lọ", donGia="126000", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/dentuz_js7bgg.jpg')
        t4 = Thuoc(tenThuoc="Espumisan", donVi="Lọ", donGia="57030", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/espumisan_ewagvp.jpg')
        t5 = Thuoc(tenThuoc="Flumetholon", donVi="Lọ", donGia="32177", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358414/medicine/20220329_082951_725761_Flumetholon.max-1800x1800_lxluud.jpg')
        t6 = Thuoc(tenThuoc="Iodine 30ml", donVi="Lọ", donGia="6291", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/iodine_a36q8c.webp')
        t7 = Thuoc(tenThuoc="Klacid", donVi="Lọ", donGia="108296", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/klacid_wttgqi.jpg')
        t8 = Thuoc(tenThuoc="Lantus", donVi="Lọ", donGia="530250", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/lantus-100iuml-10ml-lo-17147_xv64j6.webp')
        t9 = Thuoc(tenThuoc="Laforin", donVi="Lọ", donGia="101115", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358415/medicine/laforin_qxcn2f.jpg')
        t10 = Thuoc(tenThuoc="Mixtard 30", donVi="Lọ", donGia="70619", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/00004976-mixtard-100iuml-8681-5f28_large_imkw3r.jpg')
        t11 = Thuoc(tenThuoc="Acetazolamid", donVi="Viên", donGia="1150", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/20200111_013058_854007_acetazolamid-250mg-.max-1800x1800_xahhcg.jpg')
        t12 = Thuoc(tenThuoc="Alphachymotrypsin", donVi="Viên", donGia="839", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/ALPHACHYMOTRYPSIN_v4glik.jpg')
        t13 = Thuoc(tenThuoc="Albuglucan", donVi="Viên", donGia="28364", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/ALBUGLUCAN_zauekf.png')
        t14 = Thuoc(tenThuoc="Licotan", donVi="Viên", donGia="5885", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/Licotan_yn9zzv.jpg')
        t15 = Thuoc(tenThuoc="Cordarone", donVi="Viên", donGia="7222", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/20220605_085302_864175_Cordarone_-200mg.max-1800x1800_c1i2lz.jpg')
        t16 = Thuoc(tenThuoc="Digorich", donVi="Viên", donGia="678", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/digorich_jpcgja.jpg')
        t17 = Thuoc(tenThuoc="Epclusa", donVi="Viên", donGia="281137", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668359578/medicine/Epclusa_oblviw.jpg')
        t18 = Thuoc(tenThuoc="Fluconazol", donVi="Viên", donGia="11770", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358418/medicine/00003097-fluconazol-150mg-3318-5b6d_large_oj8epo.webp')
        t19 = Thuoc(tenThuoc="Glucophage", donVi="Viên", donGia="4073", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/20220215_141017_242436_thuoc-glucophage.max-1800x1800_vqdzhp.jpg')
        t20 = Thuoc(tenThuoc="Imexime 200", donVi="Viên", donGia="7383", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/20220613_003441_863812_Imexime_-200.max-1800x1800_uwksaq.jpg')
        t21 = Thuoc(tenThuoc="BB M Mocagos", donVi="Gói", donGia="2750", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/MOCAGOS_eztwf3.jpg')
        t22 = Thuoc(tenThuoc="Benokid colos", donVi="Gói", donGia="14445", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/Th%E1%BB%B1c-ph%E1%BA%A9m-b%E1%BB%95-sung-Benokid-Colos-1_vqfh6n.jpg')
        t23 = Thuoc(tenThuoc="Bông gạc", donVi="Gói", donGia="11235", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/bonggac_sewlcf.jpg')
        t24 = Thuoc(tenThuoc="Didicera", donVi="Gói", donGia="4180", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/didicera_trw2ts.jpg')
        t25 = Thuoc(tenThuoc="Duphalac", donVi="Gói", donGia="3000", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/DUPHALAC_a80wab.jpg')
        t26 = Thuoc(tenThuoc="Egaruta", donVi="Gói", donGia="6419", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358417/medicine/EGARUTA_l233ky.jpg')
        t27 = Thuoc(tenThuoc="Eroleucin", donVi="Gói", donGia="31458", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/EROLEUCIN_vi9moe.jpg')
        t28 = Thuoc(tenThuoc="Forlax", donVi="Gói", donGia="4702", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/FORLAX_eacyqx.jpg')
        t29 = Thuoc(tenThuoc="Hydrite gra", donVi="Gói", donGia="2795", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/HYDRITE_zgund9.jpg')
        t30 = Thuoc(tenThuoc="Nabifar", donVi="Gói", donGia="772", image='https://res.cloudinary.com/dgyytgkae/image/upload/v1668358416/medicine/NABIFAR_isrzhq.jpg')

        db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10,
                           t11, t12, t13, t14, t15, t16, t17, t18, t19, t20,
                           t21, t22, t23, t24, t25, t26, t27, t28, t29, t30])

        db.session.commit()

        # id = Column(Integer, primary_key=True, autoincrement=True)
        # namSinh = Column(Integer, nullable=False)
        # diaChi = Column(String(100), nullable=False)
        # hoTen = Column(String(50), nullable=False)
        # sdt = Column(String(10), nullable=False)
        # vaiTro = Column(Enum(UserRole), default=UserRole.USER)
        # username = Column(String(50), nullable=False)
        # password = Column(String(50), nullable=False)
        # ad = User(username="admin", password="123")
        # db.session.add(ad)
        # db.session.commit()
        bs = BacSi(namSinh=2000, diaChi='HCM', hoTen='Văn Trúc Vy', sdt='0366004732', vaiTro=UserRole.DOCTOR, username='string', password='string')
        db.session.add(bs)
        db.session.commit()







