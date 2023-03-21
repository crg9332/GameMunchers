from werkzeug.security import generate_password_hash, check_password_hash

def signup(curs):
    username = input("Enter username (required): ")
    password = input("Enter password (required): ")
    password = generate_password_hash(password, method='sha256')
    email = input("Enter email (required): ")
    first_name = input("Enter first name (optional): ")
    last_name = input("Enter last name (optional): ")
    if first_name == "":
        first_name = None
    if last_name == "":
        last_name = None
    try:
        # check to see if username already exists or if email is taken
        curs.execute("SELECT username FROM users WHERE username = %s", (username,))
        result = curs.fetchall()
        if len(result) != 0:
            print("Username already exists")
            return
        curs.execute("SELECT email FROM users WHERE email = %s", (email,))
        result = curs.fetchall()
        if len(result) != 0:
            print("Email already exists")
            return
        curs.execute("INSERT INTO users (username, userpassword, email, firstName, lastName) VALUES (%s, %s, %s, %s, %s)", (username, password, email, first_name, last_name))
        curs.execute("COMMIT")
        print("User created")
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

def login(curs):
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        curs.execute("SELECT userpassword FROM users WHERE username = %s", (username,))
        result = curs.fetchall()
        if len(result) == 0:
            print("Username does not exist")
            return
        if not check_password_hash(result[0][0], password):
            print("Incorrect password")
            return
        curs.execute("UPDATE Users SET lastAccessedDate = NOW() WHERE username = %s;", (username,))
        curs.execute("COMMIT")
        print("Login successful")
        return username
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
