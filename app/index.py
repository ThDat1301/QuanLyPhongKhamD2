from app import app, login, controllers

app.add_url_rule('/dang-ky-kham-truc-tuyen', 'make-appointment',
                 controllers.make_appointment, methods=['GET', 'POST'])
app.add_url_rule('/dang-nhap', 'login', controllers.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', controllers.logout)
app.add_url_rule('/tra-cuu-thuoc', 'search-medicines', controllers.tra_cuu_thuoc)
app.add_url_rule('/lap-phieu-kham', 'make-report', controllers.lap_phieu_kham, methods=['get', 'post'])
app.add_url_rule('/ds-benh-nhan', 'show-list-patients', controllers.xem_ds_benh_nhan)
app.add_url_rule('/ds-benh-nhan/<string:ngayKham>', 'list-patients-details', controllers.chi_tiet_ds)
app.add_url_rule('/api/add-medicines-to-report', 'add-medicines',
                 controllers.add_medicines_to_report, methods=['post'])
app.add_url_rule('/api/update-medicines', 'update-num-medicines',
                 controllers.update_number_medicines, methods=['put'])
app.add_url_rule('/api/update-use-medicines', 'update-use-medicines',
                 controllers.update_use_medicines, methods=['put'])
app.add_url_rule('/api/delete-medicines/<medicine_id>', 'delete-medicines',
                 controllers.delete_medicines, methods=['delete'])
app.add_url_rule('/xem-lich-su-benh-nhan', 'history-patients', controllers.history_patients)
app.add_url_rule('/xem-lich-su-benh-nhan/<int:patient_id>', 'history-patient', controllers.history_patient)
app.add_url_rule('/chi-tiet-phieu-kham/<int:report_id>', 'report-details', controllers.report_details)
app.add_url_rule('/Thanh-toan', 'bill', controllers.bill)
app.add_url_rule('/Hoa-Don/<int:PhieuKhamBenh_id>', 'payment', controllers.get_payment)
app.add_url_rule('/', 'home', controllers.home)

@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)
