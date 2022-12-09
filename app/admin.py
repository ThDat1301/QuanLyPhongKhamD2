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
class xemThuoc(AuthenticatedModelView):
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


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        year_patient = request.args.get('year-patient', datetime.now().year)
        patients_stats = dao.patients_quantity_stats(year_patient)
        year_revenue = request.args.get('year-revenue', datetime.now().year)
        revenue_stats = dao.revenue_stats(year_revenue)
        month_medicines = request.args.get('month-medicines', datetime.now().month)
        year_medicines = request.args.get('year-medicines', datetime.now().year)

        medicines_stats = dao.medicines_stats(month_medicines, year_medicines)
        total = 0
        for r in revenue_stats:
            total += r[1]
        return self.render('admin/stats.html',
                           patients_stats=patients_stats,
                           medicines_stats=medicines_stats,
                           revenue_stats=revenue_stats,
                           total=total)


class LogoutAdmin(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

admin.add_view(xemThuoc(Thuoc, db.session, name='Quản lý thuốc'))
admin.add_view(AuthenticatedModelView(LichKham, db.session, name='Quản lý lịch khám'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutAdmin(name='Đăng xuất'))