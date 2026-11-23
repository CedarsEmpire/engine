<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
</head>
<body>
    <h1>Admin Dashboard</h1>
    <!-- Add your admin dashboard content here -->
</body>
</html>

from views import UserView

def main():
    view = UserView()
    while True:
        print("1. Register User")
        print("2. Deposit")
        print("3. Get User Balance")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            view.register_user()
        elif choice == "2":
            view.deposit()
        elif choice == "3":
            view.get_user_balance()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
