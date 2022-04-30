from cryptography.fernet import Fernet, InvalidToken
import base64
import hashlib

print("Password manager. By J3ldo")
print("Github: http://github.com/J3ldo")

with open("key.key", "rb+") as f:
    if f.read() == b"":
        masterpass = input("What do you want the master password to be: ")
        f.write(hashlib.md5(base64.urlsafe_b64encode(hashlib.md5(masterpass.encode()).hexdigest().encode())).hexdigest().encode())


with open("key.key", "rb") as f:
    keyhashed = f.read()

while True:
    masterpass = input("What is your password: ")
    if hashlib.md5(base64.urlsafe_b64encode(hashlib.md5(masterpass.encode()).hexdigest().encode())).hexdigest().encode() == keyhashed:
        key = base64.urlsafe_b64encode(hashlib.md5(masterpass.encode()).hexdigest().encode())
        break
    else:
        print("Wrong password please try again")

f = Fernet(key)


def add_pass(user: str, passw: str):
    with open("passwords.txt", "a") as b:
        b.write(f"\n{f.encrypt(user.encode()).decode()}|{f.encrypt(passw.encode()).decode()}")


def view_pass():
    with open("passwords.txt", "r") as b:
        print("   Name\tPassword")
        for i, item in enumerate(b.read().split("\n")):
            try:
                print(f"{i}) {f.decrypt(item.split('|')[0].encode()).decode()} | {f.decrypt(item.split('|')[1].encode()).decode()}")
            except IndexError:
                pass
            except InvalidToken:
                print("   Something went wrong. Maybe the list is empty or you are trying to decode with an invalid key")
                return


def remove_pass(index):
    with open("passwords.txt", "r") as b:
        information = b.readlines()

    information.pop(index)
    newinformation = ""

    for i in information:
        if i.isspace():
            continue

        newinformation += i

    newinformation = "\n" + newinformation

    with open("passwords.txt", "w") as b:
        b.write(newinformation)

    print("Succesfully removed the item from the list.")


print("Type help for a lists of commands. Type q or quit to quit")
cmd = ""
while cmd != "q" or cmd != "quit":
    cmd = input("> ")

    if cmd == "help":
        print("The available commands are: \n"
              "view - To view all your passwords.\n"
              "add - To add a password.\n"
              "remove - To remove a password\n"
              "help - To show all commands\n"
              "quit - To quit this program.")

    elif cmd == "view":
        view_pass()

    elif cmd == "add":
        add_pass(input("Username: "), input("Password: "))

    elif cmd == "remove":
        remove_pass(int(input("Index of password: ")))

    elif cmd == "q" or cmd == "quit":
        print("Quitting")
        break

    else:
        print("You didn't put in a valid command please try again")
