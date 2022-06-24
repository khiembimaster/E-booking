from socket import *
from threading import Thread
import re
import json

clients = {}
addresses = {}
users = {}

HOST = ''
PORT = 33000
BUFSIZE = 1024
ADDR = (HOST,BUFSIZE)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)



def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        client.send(bytes("Welcome! Please Enter your choice...","utf8"))
        addresses[client] = client_address
        Thread(target=handle_client,args=(client,)).start()

def handle_client(client):
    options = {
        "Logg" : Login(client), 
        "Resgiter" : Register(client),
        }
    while True:
        option = client.recv(BUFSIZE).decode("utf8")
        print("%sing" % option)
        if option == "quit":
            client.close()
            del clients[client]
            break
        else: 
            options[option]

def Login(client):
    print("Logging in...")
    #Tell client to send a dictionary containing name and password
    client.send(bytes("LOGIN","utf8"))
    #Get the dictionary as bytes, decode it and loads the dictionary
    log_info = json.loads(client.recv(BUFSIZE).decode("utf8"))
    #Load the database to check
    with open('users.json','r') as inputFile:
        users = json.load(inputFile)
    #Check if user exist and password is correct
    if log_info["name"] in users.key():
        print("Hi %s\r\n" % log_info["name"])
        if log_info["password"] == users[log_info["name"]]:
            #Login success
            print("%s joined!"%addresses[client])
            client.send(bytes("Login success!","utf8"))
        else :
            print("%s's accesssion denied!"%addresses[client])
            client.send(bytes("Wrong password!","utf8")) 
    else :
        print("%s's accesssion denied!"%addresses[client])
        client.send(bytes("User name does not exist!","utf8"))


def Register(client):    
    print("Registering...")
    #Tell client to send a dictionary containing name, password and ID 
    client.send(bytes("REGISTER","utf8"))
    #Get the dictionary as bytes, decode it and loads the dictionary
    reg_info = json.loads(client.recv(BUFSIZE).decode("utf8"))
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
                with open('users.json','w') as inputFile:
                    json.dump(users,inputFile)
                client.send(bytes("Register Success!","utf8"))

            else :
                client.send(bytes("Register Denied! - Invalid ID","utf8"))
        else :
            client.send(bytes("Register Denied! - Invalid password","utf8"))
    else:
        client.send(bytes("Register Denied! - Invalid username" ,"utf8"))



if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)

    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()