from PyQt5 import QtWidgets, uic
import re


#Initializing the interface
intrf = QtWidgets.QApplication([])
csl = uic.loadUi("affine_cypher.ui")

a_iscorrect = "ok"
b_iscorrect = "ok"
a_iswrong = "a must be an odd integer different than 13"
b_iswrong = "b must be between 0 and 25 included"
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

 
#Check if "a" is a usable value       
def is_a():
    try:
        a = int(csl.a_value.text())
        if (a%2==0 or a==13) :
            csl.a_check.setText(a_iswrong) 
        else :
            csl.a_check.setText(a_iscorrect) 
    except:
        csl.a_check.setText(a_iswrong)
    return a


#Check if "b" is a usable value       
def is_b() :
    try:
        b = int(csl.b_value.text())
        if (b>-1 and b<26) :
            csl.b_check.setText(b_iscorrect) 
        else :
            csl.b_check.setText(b_iswrong)      
    except:
        csl.b_check.setText(b_iswrong) 
    return b


#Find the inverse of a for decryption
def is_inva(a):
    inv_a = 0
    i = 0
    while ((a*i)%26 != 1):
        i += 1
    inv_a = i
    return inv_a
        

#Encrypt function
def encrypt() : 
    csl.output_msg_value.setText("")
    try:
        a = is_a()
        b= is_b()
    except:
        return
    try:
        msg = csl.input_msg_value.text()
        msg = msg.upper()
        msg= msg.replace(" ", "XSPACEX")
        msg = re.sub(r'[.,"\'-?:!;]', '', msg)
        encrypted_msg = ""
        for i in range (len(msg)) :
            encrypted_msg += alph[(alph.find(msg[i])*a+b)%26]
            if ((i+1)%5 == 0) :
                encrypted_msg += " "
        csl.output_msg_value.setText(str(encrypted_msg))
    except:
        return


#Starts the encryption function while clicking on it    
csl.encrypt_button.clicked.connect(encrypt) 
  

#Decrypt function
def decrypt() :
    csl.output_msg_value.setText("")
    try:
        a = is_a()
        b = is_b()
    except:
        return
    try:
        msg = csl.input_msg_value.text()
        msg = msg.upper()
        msg = msg.replace(" ","")
        decrypted_msg = ""
        inv_a = is_inva(a)
        for i in range (len(msg)):
            decrypted_msg += alph[(((alph.find(msg[i]))-b)*inv_a)%26]
        decrypted_msg = decrypted_msg.replace("XSPACEX", " ")
        csl.output_msg_value.setText(str(decrypted_msg))
    except:
        return

    
#Starts the decryption function while clicking on it  
csl.decrypt_button.clicked.connect(decrypt) 
    
 
#plot the interface
csl.show()
intrf.exec()

