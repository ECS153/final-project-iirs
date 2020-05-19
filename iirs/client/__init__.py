from getpass import getpass

# use usernmame and password to generate keys / do encryption
def login():
    username = input("Enter username:")
    password = getpass(prompt="Enter password:")

def valid_user():
    dest = input("Enter username of user you want to talk to or q to quit:")
    return dest != "q"
