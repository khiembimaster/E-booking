from socket import *
from threading import Thread
import tkinter


def Main_menu():
    """Login or Register"""
    msg = client_socket.recv(BUFSIZE).decode("utf8")
    label_greeting.destroy()
    label_greeting_from_server = tkinter.Label(master=frame_main_menu, text = msg)
    label_greeting_from_server.pack()
    frame_start.pack_forget()
    frame_main_menu.pack()
    

def Login():
    """Login"""
    frame_main_menu.pack_forget()
    client_socket.send(bytes("Logg","utf8"))
    msg = (client_socket.recv(BUFSIZE)).decode("utf8")
    print(msg)
    return
    # log_info = {}
    # log_info["name"] = input()
    # log_info["password"] = input()
    

def Register():
    """Register"""
    frame_main_menu.destroy() 
    client_socket.send(bytes("Resgister","utf8"))

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