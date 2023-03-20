def friend(curs, username, args):
    if len(args) != 2:
        print("Usage: friend <their email>")
        return
    userEmail = args[0]
    try:
        curs.execute("SELECT username FROM user WHERE email = %s",(userEmail,))
        friendUsername = curs.fetchone()
        if friendUsername == None:
            print("%s does not exist.", userEmail)
            return
        curs.execute("INSERT INTO friends VALUES (%s, %s)", (username, friendUsername))
        curs.execute("COMMIT")
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
    
def unfriend(curs, username, args):
    if len(args) != 2:
        print("Usage: unfriend <their username>")
        return
    unfriendUsername = args[0]
    try:
        curs.execute("SELECT * FROM friends WHERE friendee = %s AND friender = %s", (unfriendUsername, username))
        friends = curs.fetchone()
        if friends == None:
            print("%s is not your friend", unfriendUsername)
            return
        curs.execute("DELETE FROM friends WHERE friendee = %s ANS friender = %s", (unfriendUsername, username))
        curs.execute("COMMIT")
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
