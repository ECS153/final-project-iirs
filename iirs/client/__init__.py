from getpass import getpass

# use usernmame and password to generate keys / do encryption
def login():
    username = input("Enter username:")
    # XXX not really useful currently
    #password = getpass(prompt="Enter password:")
    password = ''
    return (username, password)

def valid_user():
    dest = input("Enter username of user you want to talk to or q to quit:")
    if dest == "q":
        return None
    else:
        return dest
