from socket import *
import threading
from threading import Thread
import re
import json

lock = threading.Lock()

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        client.send(bytes("Welcome! Please Enter your choice...","utf8"))
        addresses[client] = client_address
        Thread(target=handle_client,args=(client,)).start()
  
def handle_client(client):
    while True:
        option = client.recv(BUFSIZE).decode("utf8")
        print("%sing" % option)
        if option == "quit":
            client.close()
            del clients[client]
            break
        elif option == "Logg": 
            Login(client)
        elif option == "Register":
            Register(client)


def Register(client):    
    print("Registering...")
    #Tell client to send a dictionary containing name, password and ID 
    client.send(bytes("REGISTER","utf8"))
    #Get the dictionary as bytes, decode it and loads the dictionary
    reg_info = json.loads(client.recv(BUFSIZE).decode("utf8"))
    #Load the database to check
    lock.acquire()
    with open('users.json','r') as inputFile:
        users = json.load(inputFile)
    lock.release()
    """Check if information is valid"""
    #Check username
    if (len(reg_info["name"]) >= 5) and bool(re.match('^[a-z0-9]*$',reg_info["name"])):
        #Check password
        if len(reg_info["password"]) >= 3:
            #Check ID
            if len(reg_info["ID"]) == 10 and bool(re.match('^[0-9]*$',reg_info["ID"])):
                #Add new user's informations
                users[reg_info["name"]] = {"password":reg_info["password"],
                                           "ID" : reg_info["ID"]} 
                #Rewrite all data
                lock.acquire()
                with open('users.json','w') as inputFile:
                    json.dump(users,inputFile)
                lock.release()
                client.send(bytes("Register Success!","utf8"))

            else :
                client.send(bytes("Register Denied! - Invalid ID","utf8"))
        else :
            client.send(bytes("Register Denied! - Invalid password","utf8"))
    else:
        client.send(bytes("Register Denied! - Invalid username" ,"utf8"))


def Login(client):
    print("Logging in...")
    #Tell client to send a dictionary containing name and password
    client.send(bytes("LOGIN","utf8"))
    #Get the dictionary as bytes, decode it and loads the dictionary
    msg = client.recv(BUFSIZE).decode("utf8")
    log_info = json.loads(msg)
    #Load the database to check
    lock.acquire()
    with open('users.json','r') as inputFile:
        users = json.load(inputFile)
    lock.release()
    #Check if user exist and password is correct
    if str(log_info['name']) in users.keys():
        print("Hi %s\r\n" % log_info["name"])
    
        if str(log_info['password']) == str(users[log_info["name"]]["password"]):
            #Login success
            print("%s joined!"%str(addresses[client]))
            client.send(bytes("Login success!","utf8"))
            Option_list(client)
        else :
            print("%s's accesssion denied!"%str(addresses[client]))
            client.send(bytes("Wrong password!","utf8")) 
    else :
        print("%s's accesssion denied!"%str(addresses[client]))
        client.send(bytes("User name does not exist!","utf8"))
    return

def Option_list(client):
    """Send option and receive choice form client"""
    option_list = ["Hotel_list","Search", "Reservation"]
    msg = json.dumps(option_list)
    client.send(bytes(msg,"utf8"))

    while True:
        option = client.recv(BUFSIZE).decode("utf8")
        print("%sing" % option)
    
        if option == option_list[0]:
            Send_hotel_list(client)
        elif option == option_list[1]:
            #Call Search modul
            Search()
        elif option == option_list[2]:
            Reservation()

def Send_hotel_list(client):
    print("readFile")
    with open("hotels.json","rb") as inputFile:
        msg = inputFile.read()
        client.sendall(msg)
        # client.send(bytes("FNished"))
    
    

def Search():
    print("foo")

def Reservation():
    print("foo")



    

clients = {}
addresses = {}
users = {}

HOST = ''
PORT = 33000
BUFSIZE = 1024
ADDR = (HOST,PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)

    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()