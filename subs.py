import random

key = {'1':'a', '2':'i', '3':'l', '4':'u',
    '5':'j', '6':'r', '7':'o', '8':'t', '9':'v'}
door = 'bcdefghkmnpqswxyz'

def decrypt(text):
    """Decrypt string to number"""
    text = text[7:11] + text[27:]
    decripted = ""
    for char in text:
        if char in door:
            decripted += "0"
        else:
            s = [n for n, c in key.items() if c == char]
            decripted += str(s[0])
    return decripted

def encrypt(text):
    """Encrypt number to string"""
    text = str(text)
    add = ""
    for _ in range(7 - len(text)):
        text = "0" + text
    for char in text:
        if char == "0":
            add += random.choice(door)
        else:
            add += key[char]
    encripted = ""
    for _ in range(7):
        encripted += chr(random.randrange(97, 123))
    encripted += add[:4]
    for _ in range(16):
        encripted += chr(random.randrange(97, 123))
    encripted += add[4:]
    return encripted
