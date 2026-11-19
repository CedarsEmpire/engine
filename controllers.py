from models import User, SubRegionEngine, AIEarnings
from database import session

class UserController:
    def register_user(self, name, email, region, package):
        user = User(name=name, email=email, region=region, package=package)
        session.add(user)
        session.commit()

    def deposit(self, user_id, amount):
        user = session.query(User).filter_by(id=user_id).first()
        user.available_balance += amount * 0.4
        user.reserved_balance += amount * 0.6
        session.commit()

    def get_user_balance(self, user_id):
        user = session.query(User).filter_by(id=user_id).first()
        return user.available_balance, user.reserved_balance
