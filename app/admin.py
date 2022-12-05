from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import Thuoc, LichKham
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user
from flask import redirect
admin = Admin(app, name='Quản trị phòng khám', template_mode='bootstrap4')

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
        return self.render('admin/stats.html')

class LogoutAdmin(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

admin.add_view(xemThuoc(Thuoc, db.session, name='Quản lý thuốc'))
admin.add_view(ModelView(LichKham, db.session, name='Quản lý danh sách khám'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutAdmin(name='Đăng xuất'))