from socket import *
from threading import Thread
from tkinter import *
from tkinter import ttk
import tkinter
import json
import sys
import PIL



def Main_menu():
    """Login or Register"""
    msg = client_socket.recv(BUFSIZE).decode("utf8")
    frame_start.pack_forget() 
    label_greeting_from_server = tkinter.Label(master=frame_main_menu, text = msg)
    label_greeting_from_server.pack()
    frame_main_menu.pack()

def Register():
    """Register"""
    def clicked():
        name=e_register_name.get()
        password=e_register_pass.get()
        bank_ID=e_register_bank_ID.get()
        #require Register modul
        client_socket.send(bytes("Register","utf8"))
        #Get confirm
        msg = (client_socket.recv(BUFSIZE)).decode("utf8")
        print(msg)
        #Generate login information from user
        reg_info = {}
        sys.stdout.flush()
        reg_info["name"] = name
        reg_info["password"] = password
        reg_info["ID"] = bank_ID
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
        frame_register.pack_forget()   


    frame_main_menu.pack_forget()
    frame_register=tkinter.Frame() 
    frame_register.pack()

    name = tkinter.StringVar()
    password = tkinter.StringVar()
    bank_ID = tkinter.StringVar()

    label_program_name=tkinter.Label(frame_register,text="E-Booking")
    label_program_name.grid(row=0,column=1)

    label_register_name=tkinter.Label(frame_register,text="User's name:")
    label_register_name.grid(row=1,column=0)
    e_register_name=tkinter.Entry(frame_register,textvariable=name,width=100)
    e_register_name.grid(row=1,column=1)

    label_register_password=tkinter.Label(frame_register,text="Password:")
    label_register_password.grid(row=2,column=0)
    e_register_pass=tkinter.Entry(frame_register,textvariable=password,width=100)
    e_register_pass.grid(row=2,column=1)

    label_register_bank_ID=tkinter.Label(frame_register,text="Bank ID:")
    label_register_bank_ID.grid(row=3,column=0)
    e_register_bank_ID=tkinter.Entry(frame_register,textvariable=bank_ID,width=100)
    e_register_bank_ID.grid(row=3,column=1)

    button_register2=tkinter.Button(frame_register,text="Register",command=clicked)
    button_register2.grid(row=4,column=1)   
        
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
        log_info["name"] = name
        log_info["password"] = password
        #dump log_info into string and send it to server 
        msg = json.dumps(log_info)
        client_socket.send(bytes(msg,"utf8"))
        #Wait for server acception
        msg = client_socket.recv(BUFSIZE).decode("utf8")
        #handle msg
        # print(msg)
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
    button_login2.grid(row=2,column=1)   


def Get_option():
    #Get option-list

    msg = client_socket.recv(BUFSIZE).decode("utf8")
    while True:

        def option_get_list():
            option=0
            if option < len(option_list):
                client_socket.send(bytes(option_list[option],"utf8"))
            else :
                client_socket.send(bytes("","utf8"))
            Show_hotel_list()

        def option_get_search():
            option=1
            if option < len(option_list):
                client_socket.send(bytes(option_list[option],"utf8"))
            else :
                client_socket.send(bytes("","utf8"))
            Search()

        def option_get_reservation():
            option=2
            if option < len(option_list):
                client_socket.send(bytes(option_list[option],"utf8"))
            else :
                client_socket.send(bytes("","utf8"))
            Reservation()


        option_list = json.loads(msg)    
        label_program_name=tkinter.Label(frame_get_option,text="E-Booking")
        label_program_name.grid(row=0,column=1)

        button_get_list=tkinter.Button(frame_get_option,text="Show hotel list",command=option_get_list)
        button_get_list.grid(row=2,column=1)

        button_get_search=tkinter.Button(frame_get_option,text="Search",command=option_get_search)
        button_get_search.grid(row=3,column=1)

        button_get_resrvation=tkinter.Button(frame_get_option,text="Reservation",command=option_get_reservation)
        button_get_resrvation.grid(row=4,column=1)

        break
    #frame_main_menu.pack()


def Show_hotel_list():
    #Get the list
    fragments = []
    frame_get_option.pack_forget()
    while True:
        chunk = ""
        try:
            client_socket.settimeout(2.0)
            chunk = client_socket.recv(BUFSIZE).decode()
            client_socket.settimeout(None)
        except:
            break
        fragments.append(chunk)

    hotels_list_str = ''.join(fragments)
    hotels_list = json.loads(hotels_list_str)
    #Now Show the list
    frame_show_list=tkinter.Frame(window)
    mycanvas=Canvas(frame_show_list)
    mycanvas.pack(side=LEFT, fill= BOTH, expand=1)

    my_scrollbar=ttk.Scrollbar(frame_show_list,orient=VERTICAL,command=mycanvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    mycanvas.configure(yscrollcommand=my_scrollbar.set)
    mycanvas.bind('<Configure>',  lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))

    sup_frame=tkinter.Frame(mycanvas)

    mycanvas.create_window((0,0), window=sup_frame, anchor="nw")
    frame_show_list.pack(fill=BOTH, expand=1)
    if hotels_list:
        x=[0] 
        hotel_name=[]
        for i in hotels_list.keys():
            hotel_name.append(i)
        for i in range(len(hotel_name)):
            label_hotel_name=tkinter.Label(sup_frame,text=hotel_name[i])
            label_hotel_name.grid(row=x)
            j=0
            x[0]+=1
            while True:
                label_hotel_name=tkinter.Label(sup_frame,text=hotels_list[hotel_name[i]][j]["name"])
                label_hotel_name.grid(row=x, column=0,sticky=tkinter.W)
                x[0]+=1
                if len(hotels_list[hotel_name[i]][j]["reservation-date"])==0:
                    label_reservation_date=tkinter.Label(sup_frame,text="Reservation-date: ")
                    label_reservation_date.grid(row=x,column=0,sticky=tkinter.W)
                else:
                    z=hotels_list[hotel_name[i]][j]["reservation-date"]
                    label_reservation_date=tkinter.Label(sup_frame,text="Reservation-date: "+str(z[0]))
                    label_reservation_date.grid(row=x,column=0,sticky=tkinter.W)
                x[0]+=1
                
                if len(hotels_list[hotel_name[i]][j]["check-in"])==0:
                    label_check_in=tkinter.Label(sup_frame,text="Check-in: ")
                    label_check_in.grid(row=x,column=0,sticky=tkinter.W)
                else:  
                    z=hotels_list[hotel_name[i]][j]["check-in"]
                    label_check_in=tkinter.Label(sup_frame,text="Check-in: "+str(z[0])+", "+str(z[1])+", "+str(z[2]))
                    label_check_in.grid(row=x,column=0,sticky=tkinter.W)
                x[0]+=1

                label_type=tkinter.Label(sup_frame,text="Type: "+hotels_list[hotel_name[i]][j]["type"])
                label_type.grid(row=x, column=0,sticky=tkinter.W)
                x[0]+=1

                label_description=tkinter.Label(sup_frame,text="Description: "+hotels_list[hotel_name[i]][j]["description"])
                label_description.grid(row=x,column=0,sticky=tkinter.W)
                x[0]+=1

                label_price=tkinter.Label(sup_frame,text="Price: "+str(hotels_list[hotel_name[i]][j]["price"]))
                label_price.grid(row=x,column=0,sticky=tkinter.W)
                x[0]+=1

                label_note=tkinter.Label(sup_frame,text="Note: "+hotels_list[hotel_name[i]][j]["Note"])
                label_note.grid(row=x,column=0,sticky=tkinter.W)
                x[0]+=1
                # image=ImageTk.PhotoImage(file=hotels_list[hotel_name[i]][j]["image"])
                # label_image=tkinter.Label(sup_frame,text="Image: ",image=image)
                # label_image.grid(row=x,column=0,sticky=tkinter.W)
                # x[0]+=1

                label_blank=tkinter.Label(sup_frame,text=" ")
                label_blank.grid(row=x)
                x[0]+=1
                j+=1

                if j==len(hotels_list[hotel_name[i]]):
                    break
    else :
        print("Fail")
    
    def return_get_option():
        sup_frame.destroy()
        frame_show_list.pack_forget()
        frame_get_option.pack()
    button_test=Button(sup_frame,text="Return",command=return_get_option)
    button_test.grid(row=x[0],column=0,sticky=W)
    return

def Search():
    # #Get information
    search_info = {}
    frame_get_option.pack_forget()
    frame_search=tkinter.Frame()
    frame_search.pack()
    #Handshake
    msg = client_socket.recv(BUFSIZE)
    if(msg): client_socket.send(b"start")
    #Get the list
    fragments = []
    while True:
        chunk = ""
        try:
            client_socket.settimeout(1.0)
            chunk = client_socket.recv(BUFSIZE).decode("utf8")
            client_socket.settimeout(None)
        except:
            break
        fragments.append(chunk)

    hotels_list_str = ''.join(fragments)
    hotels_list = json.loads(hotels_list_str)
    # client_socket.send(bytes("okie","utf8"))

    hotel_name=tkinter.StringVar()


    hotel_option=[]
    for i in hotels_list.keys():
        hotel_option.append(i)

    hotel_name.set(hotel_option[0])

    drop_menu=tkinter.OptionMenu(frame_search, hotel_name, *hotel_option)
    drop_menu.grid(row=0,column=0)

    label_check_in=tkinter.Label(frame_search,text="Enter your check-in date (year/month/date):")
    label_check_in.grid(row=1,column=0)
    
    e_year_in=tkinter.Entry(frame_search,width=10)
    e_year_in.grid(row=1,column=1)
    label_n=tkinter.Label(frame_search,text="/")
    label_n.grid(row=1,column=2,sticky=W)

    e_month_in=tkinter.Entry(frame_search,width=10)
    e_month_in.grid(row=1,column=3,sticky=W)
    label_n=tkinter.Label(frame_search,text="/")
    label_n.grid(row=1,column=4,sticky=W)

    e_date_in=tkinter.Entry(frame_search,width=10)
    e_date_in.grid(row=1,column=5,sticky=W)
    label_n=tkinter.Label(frame_search,text="/")
    label_n.grid(row=1,column=6,sticky=W)

    label_check_out=tkinter.Label(frame_search,text="Enter your check-out date (year/month/date):")
    label_check_out.grid(row=2,column=0)

    e_year_out=tkinter.Entry(frame_search,width=10)
    e_year_out.grid(row=2,column=1)
    label_n=tkinter.Label(frame_search,text="/")
    label_n.grid(row=2,column=2,sticky=W)

    e_month_out=tkinter.Entry(frame_search,width=10)
    e_month_out.grid(row=2,column=3,sticky=W)
    label_n=tkinter.Label(frame_search,text="/")
    label_n.grid(row=2,column=4,sticky=W)

    e_date_out=tkinter.Entry(frame_search,width=10)
    e_date_out.grid(row=2,column=5,sticky=W)
    label_n=tkinter.Label(frame_search,text="/")
    label_n.grid(row=2,column=6,sticky=W)

    def Searching():
        search_info["hotel_name"]=hotel_name.get()
        valid_day=True
        check_in_date=[e_year_in.get(),e_month_in.get(),e_date_in.get()]
        if check_in_date[0].isdecimal and check_in_date[1].isdecimal and check_in_date[2].isdecimal:
            check_in_date=[int(e_year_in.get()),int(e_month_in.get()),int(e_date_in.get())]
            month_30_day=[4,6,9,10]
            if check_in_date[1] in month_30_day:
                if check_in_date[2] > 30:
                    valid_day=False  
            elif check_in_date[1] == 2:
                if check_in_date[2] > 28:
                    if check_in_date[2]>29 or check_in_date[0]%4!=0:
                        valid_day=False 
            elif check_in_date[1]<=12:
                if check_in_date[2] > 31:
                    valid_day=False 
        else:
            valid_day=False

        check_out_date=[e_year_out.get(),e_month_out.get(),e_date_out.get()]
        if check_out_date[0].isdecimal and check_out_date[1].isdecimal and check_out_date[2].isdecimal:
            check_out_date=[int(e_year_out.get()),int(e_month_out.get()),int(e_date_out.get())]
            month_30_day=[4,6,9,10]
            if check_out_date[1] in month_30_day:
                if check_out_date[2] > 30:
                    valid_day=False  
            elif check_out_date[1] == 2:
                if check_out_date[2] > 28:
                    if check_out_date[2]>29 or check_out_date[0]%4!=0:
                        valid_day=False 
            elif check_out_date[1]<=12:
                if check_out_date[2] > 31:
                    valid_day=False
        else:
            valid_day=False

        if valid_day:
            for i in range(6):
                check_in_date.append(0)
                check_out_date.append(0)
            search_info["check-in"] = check_in_date
            search_info["check-out"] = check_out_date

            #Send information
            search_info_str = json.dumps(search_info)
            client_socket.send(bytes(search_info_str,"utf8"))
            #Get the list
            client_socket.send(bytes("start","utf8"))
            fragments = []
            while True:
                chunk = ""
                try:
                    client_socket.settimeout(1.0)
                    chunk = client_socket.recv(BUFSIZE).decode("utf8")
                    client_socket.settimeout(None)
                except:
                    break
                fragments.append(chunk)
            available_rooms_str = ''.join(fragments)
            available_rooms = json.loads(available_rooms_str)
            
            if available_rooms:
                    frame_search.pack_forget()
                    frame_show_list=tkinter.Frame(window)
                    mycanvas=Canvas(frame_show_list)
                    mycanvas.pack(side=LEFT, fill= BOTH, expand=1)

                    my_scrollbar=ttk.Scrollbar(frame_show_list,orient=VERTICAL,command=mycanvas.yview)
                    my_scrollbar.pack(side=RIGHT, fill=Y)

                    mycanvas.configure(yscrollcommand=my_scrollbar.set)
                    mycanvas.bind('<Configure>',  lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))

                    sup_frame=tkinter.Frame(mycanvas)

                    mycanvas.create_window((0,0), window=sup_frame, anchor="nw")
            
                    x=[0]
                    for j in range(len(available_rooms)):
                        label_hotel_name=tkinter.Label(sup_frame,text=available_rooms[j]["name"])
                        label_hotel_name.grid(row=x, column=0,sticky=tkinter.W)
                        x[0]+=1
                        if len(available_rooms[j]["reservation-date"])==0:
                            label_reservation_date=tkinter.Label(sup_frame,text="Reservation-date: ")
                            label_reservation_date.grid(row=x,column=0,sticky=tkinter.W)
                        else:
                            z=available_rooms[j]["reservation-date"]
                            label_reservation_date=tkinter.Label(sup_frame,text="Reservation-date: "+str(z[0]))
                            label_reservation_date.grid(row=x,column=0,sticky=tkinter.W)
                        x[0]+=1
                        
                        if len(available_rooms[j]["check-in"])==0:
                            label_check_in=tkinter.Label(sup_frame,text="Check-in: ")
                            label_check_in.grid(row=x,column=0,sticky=tkinter.W)
                        else:  
                            z=available_rooms[j]["check-in"]
                            label_check_in=tkinter.Label(sup_frame,text="Check-in: "+str(z[0])+", "+str(z[1])+", "+str(z[2]))
                            label_check_in.grid(row=x,column=0,sticky=tkinter.W)
                        x[0]+=1

                        label_type=tkinter.Label(sup_frame,text="Type: "+available_rooms[j]["type"])
                        label_type.grid(row=x, column=0,sticky=tkinter.W)
                        x[0]+=1

                        label_description=tkinter.Label(sup_frame,text="Description: "+available_rooms[j]["description"])
                        label_description.grid(row=x,column=0,sticky=tkinter.W)
                        x[0]+=1

                        label_price=tkinter.Label(sup_frame,text="Price: "+str(available_rooms[j]["price"]))
                        label_price.grid(row=x,column=0,sticky=tkinter.W)
                        x[0]+=1

                        label_note=tkinter.Label(sup_frame,text="Note: "+available_rooms[j]["Note"])
                        label_note.grid(row=x,column=0,sticky=tkinter.W)
                        x[0]+=1

                        label_blank=tkinter.Label(sup_frame,text=" ")
                        label_blank.grid(row=x)
                        x[0]+=1
                     
            # print(available_rooms)
            # available_rooms["image"]
        else:
            frame_search.destroy()
            Search()

    button_search=tkinter.Button(frame_search,text="Search",command=Searching)
    button_search.grid(row=3,column=4)
    
    # print(available_rooms)
    # available_rooms["image"]



def Reservation():
    print("foo")





"""Inter-face"""
window = tkinter.Tk()
window.title("E-booking")
screenW=window.winfo_screenwidth()
screenH=window.winfo_screenheight()
window.geometry('%dx%d' %(screenW/2,screenH/2))
window.resizable(width=False,height=False)
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

frame_get_option=tkinter.Frame()
frame_get_option.pack()

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