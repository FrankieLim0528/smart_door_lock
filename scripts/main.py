import enchant

def check_passphrase(passphrase):
    dictionary = enchant.Dict("en_US")

    words = passphrase.split()

    if len(words) <= 2:
        if all(dictionary.check(word) for word in words):
            return True
    return False

passphrase = raw_input("Please enter your passphrase: ")
if check_passphrase(passphrase):
    print("Valid passphrase")
    file_path = r"/home/mustar/catkin_ws/src/smart_door_lock/passphrase.txt"
    with open(file_path, "w") as f:
        f.write(passphrase)
else:
    print("Invalid passphrase.")