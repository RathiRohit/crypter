import os
import random
import hashlib
import struct
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import askdirectory
from Crypto.Cipher import AES


'''Encrypting function'''
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


'''Decrypting function'''
def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

'''Start encryption'''
def startEncrypter(password, choice):
    Tk().withdraw()
    dirpath = askdirectory()
    key = hashlib.sha256(password).digest()
    for x in os.walk(dirpath):
        for filename in x[2]:
            encrypt_file(key, x[0]+'/'+filename, x[0]+'/'+filename+'.enc')
            if choice=='y' or choice=='Y':
                os.remove(x[0]+'/'+filename)


def startDecrypter(password, choice):
    Tk().withdraw()
    dirpath = askdirectory()
    key = hashlib.sha256(password).digest()
    for x in os.walk(dirpath):
        for filename in x[2]:
            decrypt_file(key, x[0]+'/'+filename, x[0]+'/'+os.path.splitext(filename)[0])
            if choice=='y' or choice=='Y':
                os.remove(x[0]+'/'+filename)


print('Choose option:\nE : Encrypt\nD : Decrypt\nCtrl+C : Exit\n\nOption:\n')
cmd = raw_input()
if cmd=='E':
    print('Encryption key:')
    key = raw_input()
    print('Delete original files (y/n):')
    choice = raw_input()
    startEncrypter(key, choice)
elif cmd=='D':
    print('Decryption key:')
    key = raw_input()
    print('Delete encrypted files (y/n):')
    choice = raw_input()
    startDecrypter(key, choice)
else:
    exit()
