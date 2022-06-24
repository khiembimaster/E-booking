from socket import *
from threading import Thread
import tkinter


def Main_menu():
    """Login or Register"""
    msg = client_socket.recv(BUFSIZE).decode("utf8")
    label_greeting_from_server = tkinter.Label(master=frame_start, text = msg)
    label_greeting_from_server.pack()
    frame_login.pack()
    frame_register.pack()

def Login():
    """Login"""

def Register():
    """Register"""


#Inter-face
window = tkinter.Tk()
window.title("E-booking")
frame_start = tkinter.Frame()
label_greeting = tkinter.Label(master=frame_start, text = "Please connect to server...")
label_greeting.pack()
frame_login = tkinter.Frame()
button_login = tkinter.Button(master=frame_login, text = "Login", command=Login)
button_login.pack()
frame_register = tkinter.Frame()
button_register = tkinter.Button(master=frame_register, text = "Register", command=Register)
button_register.pack()

frame_start.pack()




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