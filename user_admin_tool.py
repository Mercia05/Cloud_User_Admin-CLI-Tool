import mysql.connector

# Database configuration
db_config = {
    "host": "awsmysql-db6.c5ak8gaqwbjk.eu-north-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Jbgsjn8!",
    "database": "sql_system",
    "port": 3306
}

# Menu options
def show_menu():
    print("\n User Admin Menu:")
    print("1. View all users")
    print("2. Add new user")
    print("3. Update user role")
    print("4. Delete user")
    print("5. Exit")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-5):")
        if choice == '1':
            view_users()
        elif choice == '2':
            add_user()
        elif choice == '3':
            update_user() # type: ignore
        elif choice == '4':
            delete_user() # type: ignore
        elif choice == '5':
            print("Existing... Goodbye !")
            break
        else:
            print("Invalid choice. Please try again.")

def add_user():
    try:
        full_name = input("Enter full name: ")
        email = input("Enter email address: ")
        password = input("Enter password: ")
        role = input("Enter role (admin/user): ").lower()

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = """
        INSERT INTO user (full_name, email, password, role)
        VALUES (%s, %s, %s, %s)
        """
        values = (full_name, email, password, role)

        cursor.execute(query, values)
        connection.commit()

        print("User added successfully!")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def update_user():
    try:
        user_id = input("Enter the ID of the user you want to update:")
        new_role = input("Enter the new role(admin/user):").lower()

        if new_role not in ['admin', 'user']:
            print("Invalid role. Must be 'admin' or 'user'.")
            return
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "UPDATE user SET role = %s WHERE id %s"
        values = (new_role, user_id)

        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount == 0:
            print("No user found with that ID.")
        else:
            print("User role updated successfully !")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error:{err}")


def delete_user():
    try:
        user_id = input("Enter the ID of the user you want to delete:")
        confirm = input(f"Are you sure you want to delete user ID {user_id}? (yes/no):").lower()
        
        if confirm != 'yes':
            print("Deletion cancelled.")
            return
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "DELETE FROM user WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()

        if cursor.rowcount == 0:
            print("No user found with that ID.")
        else:
            print("User deleted successfully")
                  
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# ---Functions---
def view_users():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        print("\n All Users:")
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[4]}, Created: {user[5]}")
        
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Run the app
if __name__ == "__main__": 
    main()