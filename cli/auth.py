from werkzeug.security import generate_password_hash, check_password_hash

def signup(curs, args): # add option to add first and last name (might want to use **kwargs + a base string to construct and add to query)
    if len(args) != 3:
        print("Invalid number of arguments")
        print("Usage: signup <username> <password> <email>")
        return
    username = args[0]
    password = args[1]
    password = generate_password_hash(password, method='sha256')
    email = args[2]
    try:
        curs.execute("INSERT INTO users (username, userpassword, email) VALUES (%s, %s, %s)", (username, password, email))
        print("User created")
        # print(curs.fetchall())
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

def login(curs, args):
    if len(args) != 2:
        print("Invalid number of arguments")
        print("Usage: login <username> <password>")
        return
    username = args[0]
    password = args[1]
    try:
        curs.execute("SELECT userpassword FROM users WHERE username = %s", (username,))
        result = curs.fetchall()
        if len(result) == 0:
            print("Username does not exist")
            return
        if not check_password_hash(result[0][0], password):
            print("Incorrect password")
            return
        curs.execute("COMMIT")
        curs.execute("UPDATE Users SET lastAccessedDate = NOW() WHERE username = '%s';" % username)
        user_name = username
        print("Login successful")
        # print(curs.fetchall())
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")