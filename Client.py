from pydoc import cli
from socket import *
from threading import Thread
import tkinter
import json
import sys

from jmespath import search


def Main_menu():
    """Login or Register"""
    msg = client_socket.recv(BUFSIZE).decode("utf8")
    frame_start.pack_forget() 
    label_greeting_from_server = tkinter.Label(master=frame_main_menu, text = msg)
    label_greeting_from_server.pack()
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
    sys.stdout.flush()
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
        
def Login():
    """Login"""
    def clicked():
        name=e1.get()
        password=e2.get()
        #require Login modul
        client_socket.send(bytes("Logg","utf8"))
        #Get confirm
        msg = (client_socket.recv(BUFSIZE)).decode("utf8")
        print(msg)
        #Generate login information from user
        log_info = {}
        sys.stdout.flush()
        log_info["name"] = name
        log_info["password"] = password
        #dump log_info into string and send it to server 
        msg = json.dumps(log_info)
        client_socket.send(bytes(msg,"utf8"))
        #Wait for server acception
        msg = client_socket.recv(BUFSIZE).decode("utf8")
        #handle msg
        print(msg)
        if msg != "Login success!":
            frame_main_menu.pack()
        else : #Login success
            Get_option()
        frame_login.pack_forget()
    

    frame_main_menu.pack_forget()
    frame_login=tkinter.Frame()
    frame_login.pack()
    name = tkinter.StringVar()
    password = tkinter.StringVar()
    label_login_name=tkinter.Label(frame_login,text="User's name:")
    label_login_name.grid(row=0,column=0)
    e1=tkinter.Entry(frame_login,textvariable=name,width=100)
    e1.grid(row=0,column=1)

    label_login_password=tkinter.Label(frame_login,text="Password:")
    label_login_password.grid(row=1,column=0)
    e2=tkinter.Entry(frame_login,textvariable=password,width=100)
    e2.grid(row=1,column=1)

    button_login2=tkinter.Button(frame_login,text="Login",command=clicked)
    button_login2.grid(row=2,column=2)   


def Get_option():
    #Get option-list
    msg = client_socket.recv(BUFSIZE).decode("utf8")
    while True:
        option_list = json.loads(msg)
        #User choose option
        option = int(input("Enter your option: ")) # a number 
        if option < len(option_list):
            client_socket.send(bytes(option_list[option],"utf8"))
        else :
            client_socket.send(bytes("quit","utf8"))
        #Go to appropriate function
        if option == 0:
            Show_hotel_list()
        elif option == 1:
            Search()
        elif option == 2:
            Reservation()
        else :
            break
    frame_main_menu.pack()

def Show_hotel_list():
    #Get the list
    fragments = []
    while True:
        chunk = ""
        try:
            client_socket.settimeout(1.0)
            chunk = client_socket.recv(BUFSIZE).decode()
            client_socket.settimeout(None)
        except:
            break
        fragments.append(chunk)

    hotels_list_str = ''.join(fragments)
    hotels_list = json.loads(hotels_list_str)
    #Now Show the list
    print("Printing hotel list\r\n")
    if hotels_list:
        print(hotels_list)
    else :
        print("Fail")


def Search():
    search_info = {}
    search_info["hotel_name"] = input("Enter hotel name: ")
    search_info["check-in"] = input("Enter check-in date: ")
    search_info["check-out"] = input("Enter check-out date: ")
    search_info_str = json.dumps(search_info)
    client_socket.send(bytes(search_info_str,"utf8"))
    available_rooms_str = client_socket.recv(BUFSIZE).decode("utf8")
    available_rooms = json.loads(available_rooms_str)
    print(available_rooms)

def Reservation():
    print("foo")





"""Inter-face"""
window = tkinter.Tk()
window.title("E-booking")
#Intro frame
frame_start = tkinter.Frame()
label_greeting = tkinter.Label(master=frame_start, text = "Please connect to server...")
label_greeting.pack()
frame_start.pack()

#Main menu frame
frame_main_menu = tkinter.Frame()
button_login = tkinter.Button(master=frame_main_menu, text = "Login", command=Login)
button_login.pack()
button_register = tkinter.Button(master=frame_main_menu, text = "Register", command=Register)
button_register.pack()


"""Socket"""
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