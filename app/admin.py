from flask_admin import Admin, BaseView, expose
from app import app, db, dao
from app.models import Thuoc, LichKham, BenhNhan, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request
from datetime import datetime

admin = Admin(app, name='Quản trị phòng khám', template_mode='bootstrap4')

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro == UserRole.ADMIN
class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
class xemThuoc(ModelView):
    can_view_details = True
    can_export = True
    column_export_list = ['tenThuoc', 'donVi', 'donGia', 'SoLuong']
    column_searchable_list = ['tenThuoc', 'donVi']
    column_filters = ['donGia']
    column_exclude_list = ['image']
    column_labels = {
        'tenThuoc': 'Tên thuốc',
        'donVi': 'Đơn vị',
        'donGia': 'Đơn giá',
        'image': 'Ảnh',
        'soLuong': 'Số lượng',
    }
    page_size = 10


class StatsView(BaseView):
    @expose('/')
    def index(self):
        year = request.args.get('year', datetime.now().year)
        patients_stats = dao.patients_quantity_stats(year)
        medicines_stats = dao.medicines_stats()
        return self.render('admin/stats.html',
                           patients_stats=patients_stats,
                           medicines_stats=medicines_stats)


class LogoutAdmin(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')
class PatientView(ModelView):
    can_view_details = True
    can_export = True
#AuthenticatedModelView
admin.add_view(PatientView(BenhNhan, db.session, name='Bệnh nhân'))
admin.add_view(xemThuoc(Thuoc, db.session, name='Quản lý thuốc'))
admin.add_view(ModelView(LichKham, db.session, name='Quản lý danh sách khám'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutAdmin(name='Đăng xuất'))