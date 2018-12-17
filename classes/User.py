from flask_login import UserMixin

class UserObj(UserMixin):
    def __init__(self, user_id, person_id, username, pass_hash, email, reg_date, active, admin):
        self.id = user_id
        self.person_id = person_id
        self.username = username
        self.email = email
        self.password_hash = pass_hash
        self.reg_date = reg_date
        self.active = active
        self.is_admin = admin
