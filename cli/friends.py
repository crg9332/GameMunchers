def friend(curs, username):
    userEmail = input("Enter email of friend: ")
    try:
        curs.execute("SELECT username FROM users WHERE email = %s",(userEmail,))
        friendUsername = curs.fetchone()
        if friendUsername == None:
            print(f"User with email '{userEmail}' does not exist.")
            return
        
        # Check if user is already friends with friendUsername
        curs.execute("SELECT * FROM friends WHERE friendee = %s AND friender = %s", (friendUsername, username))
        friends = curs.fetchone()
        if friends != None:
            print(f"You are already friends with {friendUsername[0]}")
            return
        
        curs.execute("INSERT INTO friends VALUES (%s, %s)", (username, friendUsername))
        curs.execute("COMMIT")
        print(f"Friended {friendUsername[0]}")
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

def unfriend(curs, username):
    unfriendUsername = input("Enter username of friend: ")
    try:
        curs.execute("SELECT * FROM friends WHERE friendee = %s AND friender = %s", (unfriendUsername, username))
        friends = curs.fetchone()
        if friends == None:
            print("You are not friends with %s" % unfriendUsername)
            return
        curs.execute("DELETE FROM friends WHERE friendee = %s AND friender = %s", (unfriendUsername, username))
        curs.execute("COMMIT")
        print(f"Unfriended {unfriendUsername}")
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
