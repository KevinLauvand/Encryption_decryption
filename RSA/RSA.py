import random
import sympy
from sympy import randprime
import math
from PyQt5 import QtWidgets, uic


#Intilazing the interface
intrf = QtWidgets.QApplication([])
csl = uic.loadUi("RSA.ui")


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


#Change the input string message to a list of int
#for the encryption function
def string_toInt(msg):
    try:
        n_split = 7
        len_bits = 8
        msg = list(msg)
        encrypted_msg = []
        binary_list=[]
        int_list=[]
        for ele in msg:
            encrypted_msg.extend(ord(num) for num in ele)
        for i in range(len(encrypted_msg)):
            binary_list.append(bin(encrypted_msg[i]))
        binary_list = [s.replace('0b', '') for s in binary_list]
        for i in range(len(binary_list)):
            binary_list[i] = str(binary_list[i]).zfill(len_bits)
        binary_list = [binary_list[i:i + n_split] for i in range(0, len(binary_list), n_split)]
        for i in range(len(binary_list)):
            binary_list[i] = ''.join(binary_list[i])
            int_list.append(int(binary_list[i],2))
        return(int_list)
    except:
        return



#Encrypt function
def encrypt_Msg():
    csl.output_msg.setText("")
    try:
        msg = csl.input_msg.toPlainText()
        n = int(csl.n_inputvalue.text())
        e = int(csl.e_inputvalue.text())
        encrypted_msg = string_toInt(msg)
        for i in range (len(encrypted_msg)):
            encrypted_msg[i] = pow(encrypted_msg[i],e,n)
        csl.output_msg.setText(str(encrypted_msg))
    except:
        return


#Starts the function while clicking on the encryption button
csl.button_encrypt.clicked.connect(encrypt_Msg)    


#Change the list of int encrypted to a string
#for the decryption function
def int_toString(msg):
        try:
            split_list = []
            ascii_list = []
            char_list = []
            n_split = 7
            len_bits = 8
            encrypted_msg = [str(x) for x in msg]
            encrypted_msg = [s.replace('0b', '') for s in encrypted_msg]
            for i in range(len(encrypted_msg)-1):
                encrypted_msg[i] = str(encrypted_msg[i]).zfill(n_split*len_bits)
            while(len(encrypted_msg[-1])%len_bits != 0):
                i = 1
                x = '0'*i
                encrypted_msg[-1] = x + encrypted_msg[-1]
            for i in range(len(encrypted_msg)):
                a = encrypted_msg[i]
                for idx in range(0, len(a), len_bits):
                    split_list.append(a[idx : idx + len_bits])
            for i in range(len(split_list)):
                ascii_list.append(int(split_list[i],2))
            for i in range(len(ascii_list)):
                char_list.append(chr(ascii_list[i]))
            final_msg = ''.join(char_list)
            return final_msg
        except:
            return


#Decryption function
def decrypt_Msg():
    try:
        csl.output_msg.setText("")
        encrypted_msg = csl.input_msg.toPlainText()
        n = int(csl.n_inputvalue.text())
        d = int(csl.d_inputvalue.text())
        encrypted_msg = list(encrypted_msg)
        encrypted_msg.remove("[")
        encrypted_msg.remove("]")
        encrypted_msg = "".join(encrypted_msg)
        encrypted_msg = encrypted_msg.split(", ")
        encrypted_list = [eval(x) for x in encrypted_msg]
        for i in range (len(encrypted_list)):
            encrypted_list[i] = pow(encrypted_list[i],d,n)
            encrypted_list[i] = bin(encrypted_list[i])
        decrypted_msg = int_toString(encrypted_list)
        csl.output_msg.setText(str(decrypted_msg))
    except:
        return
    

#Starts the function while clicking on the decryption button    
csl.button_decrypt.clicked.connect(decrypt_Msg)
    
    
#Launch the interface   
csl.show()
intrf.exec()