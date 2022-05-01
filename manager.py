from cryptography.fernet import Fernet
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
        b.write(f"\n{user}|{f.encrypt(passw.encode()).decode()}")


def view_pass():
    with open("passwords.txt", "r") as b:
        print("   Name\tPassword")
        for i, item in enumerate(b.read().split("\n")):
            try:
                print(f"{i}) {item.split('|')[0]} | {f.decrypt(item.split('|')[1].encode()).decode()}")
            except IndexError:
                pass


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


chars = "qwertyuiopasdfghjklzxcvbnm"
nums = "1234567890"
spec_chars = "`~!@#$%^&*()-_=+{[}]|\\:;\"',<.>/?"
all_chars = [list(chars), list(chars.upper()), list(nums), list(spec_chars)]
def check_pass(passw):
    strength = 0
    if len(passw) >= 12:
        strength += 5

    else:
        strength -= 3
    contains = {"letter": 0, "nums": 0, "chars": 0, "upper": 0}
    #letters: 10, nums: 3, char: 1, upper: 2

    for i in all_chars[0]:
        for char in list(passw):
            if i == char:
                contains["letter"] += 1

    for i in all_chars[1]:
        for char in list(passw):
            if i == char:
                contains["upper"] += 1

    for i in all_chars[2]:
        for char in list(passw):
            if i == char:
                contains["nums"] += 1

    for i in all_chars[3]:
        for char in list(passw):
            if i == char:
                contains["chars"] += 1

    if contains["letter"] >= 10:
        strength += 3

    if contains["upper"] >= 2:
        strength += 2

    if contains["nums"] >= 3:
        strength += 2

    if contains["chars"] >= 1:
        strength += 4

    if strength >= 16:
        print("Your password is super strong. It meets all requirements")

    elif strength <= 0:
        print("Your password doesn't meet any requirements. Please don't use it")

    elif strength >= 13:
        print("A nice password to use. It meets almost all requirements")

    elif strength >= 9:
        print("Medium password not to strong but also not easy to crack.")

    else:
        print("A easy/medium password. Use at your own risk")


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
              "check - To check on password strength\n"
              "quit - To quit this program.")

    elif cmd == "view":
        view_pass()

    elif cmd == "add":
        add_pass(input("Username: "), input("Password: "))

    elif cmd == "remove":
        remove_pass(int(input("Index of password: ")))

    elif cmd == "check":
        check_pass(input("Password: "))

    elif cmd == "q" or cmd == "quit":
        print("Quitting")
        break

    else:
        print("You didn't put in a valid command please try again")
