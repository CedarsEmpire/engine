from controllers import UserController

class UserView:
    def __init__(self):
        self.controller = UserController()

    def register_user(self):
        name = input("Enter name: ")
        email = input("Enter email: ")
        region = input("Enter region: ")
        package = input("Enter package: ")
        self.controller.register_user(name, email, region, package)

    def deposit(self):
        user_id = int(input("Enter user ID: "))
        amount = float(input("Enter amount: "))
        self.controller.deposit(user_id, amount)

    def get_user_balance(self):
        user_id = int(input("Enter user ID: "))
        available_balance, reserved_balance = self.controller.get_user_balance(user_id)
        print(f"Available Balance: {available_balance}")
        print(f"Reserved Balance: {reserved_balance}")
