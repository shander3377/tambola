import socket
from threading import Thread
import time
import random
SERVER = None
IP_ADDRESS = "127.0.0.1"
PORT = 6000
CLIENTS = {}
flashNumberList =[ i  for i in range(1, 91)]

gameOver = False
playersJoined = False

def setup():
    print("\n\t\t\t\t\t**** Welcome to Tambola Game ****\n")
    global SERVER
    global PORT
    global IP_ADDRESS
    
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    
    SERVER.listen(10)
    
    print("\t\t\t\t\t SERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")
    thread = Thread(target = handleClient, args=())
    thread.start()

    acceptConnection()
def acceptConnection():
    global SERVER
    global CLIENTS
    while(True):
        player_socket, addr= SERVER.accept()
        player_name = player_socket.recv(1024).decode().strip()
        print(player_name)
        if(len(CLIENTS.keys()) == 0):
            CLIENTS[player_name] = {'player_type': 'player1'}
        else:
            CLIENTS[player_name] = {'player_type': 'player2'}
        CLIENTS[player_name]["player_socket"] = player_socket
        CLIENTS[player_name]["address"] = addr
        CLIENTS[player_name]["player_name"] = player_name
        CLIENTS[player_name]["turn"] = False;
        
        print(f"Connection established with {player_name}: {addr}")
        thread1 = Thread(target = recvMessage, args=(player_socket,))
        thread1.start()
def handleClient():
    global CLIENTS
    global flashNumberList
    global gameOver
    global playersJoined

    while True:
        if(gameOver):
            break
        try:
            # Atleast two player required to play this game
            print(gameOver)
            if(len(list(CLIENTS.keys())) >=2 and not gameOver):
                if(not playersJoined):
                    playersJoined = True
                    time.sleep(1)


                print(playersJoined)
                print(len(flashNumberList))
                if(len(flashNumberList) > 0):
                    print(len(list(CLIENTS.keys())))
                    print("meow")
                    randomNumber = random.choice(flashNumberList)
                    currentName = None
                    try:
                        for cName in CLIENTS:
                            currentName = cName
                            cSocket = CLIENTS[cName]["player_socket"]
                            print("hehehehhe")
                            cSocket.send(str(randomNumber).encode())

                        flashNumberList.remove(int(randomNumber))
                    except:
                        # Removing Player cleint when they close / terminate the session
                        del CLIENTS[currentName]

                    # After Every 3 Seconds we are sending one number to each CLIENT
                    time.sleep(3)
                else:
                    gameOver = True
        except:
            gameOver = True


def recvMessage(player_socket):
    global CLIENTS
    global gameOver

    while True:
        try:
            message = player_socket.recv(2048).decode()
            if(message):
                for cName in CLIENTS:
                    cSocket = CLIENTS[cName]["player_socket"]
                    if('wins the game.' in message):
                        gameOver = True
                    cSocket.send(message.encode())
        except:
            pass       
setup()