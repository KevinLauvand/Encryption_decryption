import random
import sympy
from sympy import randprime
import math
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import os


#Intilazing the interface
intrf = QtWidgets.QApplication([])
csl = uic.loadUi("DSA.ui")

#Function to get a prime number between 10**1 and (10**17)-1
def get_RandomPrime():
    n = randprime(10**16, (10**17)-1)
    return n


#Find e for the decryption
def get_e(phi_n):
    e = random.randint(1,phi_n)
    while math.gcd(e,phi_n) != 1:
        e = random.randint(1,phi_n)
    return e


#Find keys on the GUI if the user doesn't have is own
def find_Keys():
    p = get_RandomPrime()
    q = get_RandomPrime()
    while (p == q):
        q = random.randint(10**16,(10**17)-1)
    n = p*q
    phi_n = (p-1)*(q-1)
    e = get_e(phi_n)
    d = pow(e,-1,phi_n)
    csl.n_get_publickeyvalue.setText(str(n))
    csl.e_get_publickeyvalue.setText(str(e))
    csl.n_get_privatekeyvalue.setText(str(n))
    csl.d_get_privatekeyvalue.setText(str(d))

    
csl.button_getkey.clicked.connect(find_Keys)


#Open the file
def open_File():
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ReadOnly
    file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open a file", "", "All Files (*);;Text Files (*.txt)", options=options)
    
    if file_name:
        name = os.path.basename(file_name)
        path = file_name
        stat = os.stat(path)
        size = stat.st_size
        format = os.path.splitext(path)[1]
       
        with open(file_name, 'r', encoding='latin-1') as f:
            file_contents = f.read()     
       
        csl.txt_filevalue.setText(str(name))
        csl.txt_locationvalue.setText(str(path))
        csl.txt_sizevalue.setText(str(size))
        csl.txt_typevalue.setText(str(format))
        csl.txt_fileinfo.setText(str(file_contents))

csl.button_loadfile.clicked.connect(open_File)


# Sign the message
def sign_Message():
    n = int(csl.n_get_privatekeyvalue.text())
    d = int(csl.d_get_privatekeyvalue.text())
    message = csl.txt_fileinfo.text()
    hash_msg = hash(message) # Hash the message
    signature = pow(hash_msg, d, n)
    csl.output_signature.setText(str(signature))

csl.button_signfile.clicked.connect(sign_Message)

# Verify the signature
def verify_Signature():
    n = int(csl.n_get_publickeyvalue.text())
    e = int(csl.e_get_publickeyvalue.text())
    message = csl.txt_fileinfo.text()
    signature = int(csl.output_signature.text())
    hash_msg = hash(message) # Hash the message
    verified = pow(signature, e, n) == hash_msg
    if verified:
        csl.txt_verification.setText("Signature verified")
    else:
       csl.txt_verification.setText("Signature not verified")

csl.button_verification.clicked.connect(verify_Signature)


#Launch the interface   
csl.show()
intrf.exec()
