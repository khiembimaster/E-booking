from socket import *
from threading import Thread
import tkinter
import json


def Main_menu():
    """Login or Register"""
    msg = client_socket.recv(BUFSIZE).decode("utf8")
    label_greeting.destroy()
    frame_start.pack_forget()
    label_greeting_from_server = tkinter.Label(master=frame_main_menu, text = msg)
    label_greeting_from_server.pack()
    frame_main_menu.pack()
        
def Login():
    """Login"""
    frame_main_menu.pack_forget()
    #require Login modul
    client_socket.send(bytes("Logg","utf8"))
    #Get confirm
    msg = (client_socket.recv(BUFSIZE)).decode("utf8")
    print(msg)
    #Generate login information from user
    log_info = {}
    log_info["name"] = input("Enter username: ")
    log_info["password"] = input("Enter password: ")
    #dump log_info into string and send it to server 
    msg = json.dumps(log_info)
    client_socket.send(bytes(msg,"utf8"))
    #Wait for server acception
    msg = client_socket.recv(BUFSIZE).decode("utf8")
    #handle msg
    print(msg)
    if msg != "Login success!":
        frame_main_menu.pack()

def Register():
    """Register"""
    frame_main_menu.pack_forget() 
    #require Register modul
    client_socket.send(bytes("Register","utf8"))
    #Get confirm
    msg = (client_socket.recv(BUFSIZE)).decode("utf8")
    print(msg)
    #Generate login information from user
    reg_info = {}
    reg_info["name"] = input("Enter username: ")
    reg_info["password"] = input("Enter password: ")
    reg_info["ID"] = input("Enter Bank Account: ")
    #dump reg_info into string and send it to server 
    msg = json.dumps(reg_info)
    client_socket.send(bytes(msg,"utf8"))
    #Wait for server acception
    msg = client_socket.recv(BUFSIZE).decode("utf8")
    #handle msg
    print(msg)
    if msg == "Register success!":
        Login()
    else :
        frame_main_menu.pack()



#Inter-face
window = tkinter.Tk()
window.title("E-booking")
frame_start = tkinter.Frame()
label_greeting = tkinter.Label(master=frame_start, text = "Please connect to server...")
label_greeting.pack()
frame_start.pack()

frame_main_menu = tkinter.Frame()
button_login = tkinter.Button(master=frame_main_menu, text = "Login", command=Login)
button_login.pack()
button_register = tkinter.Button(master=frame_main_menu, text = "Register", command=Register)
button_register.pack()




#Socket
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZE = 1024
ADDR = (HOST,PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=Main_menu)
receive_thread.start()

window.mainloop()