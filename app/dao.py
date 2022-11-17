import hashlib
from app.models import User, UserRole, BacSi, NguoiDung

from app.models import Thuoc
from app import db


def load_medicine(medicine=None):
    query = Thuoc.query.filter(Thuoc.active.__eq__(True))
    if medicine:
        query = query.filter(Thuoc.tenThuoc.contains(medicine))
    return query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)
def check_login(username, password):
     if username and password:
         # password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
         return BacSi.query.filter(BacSi.username.__eq__(username.strip()),
                                  BacSi.password.__eq__(password),).first()