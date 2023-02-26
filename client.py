import socket
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
import random

CLIENT = None
IP_ADDRESS = "127.0.0.1"
PORT = 6000
ticketGrid = []
currentNumberList = []
def setup():
    global CLIENT
    global IP_ADDRESS
    global PORT
    
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT.connect((IP_ADDRESS, PORT))
    askPlayerName()
    # thread = Thread(target=recieveMsg)
    # thread.start()
def saveName():
    global CLIENT
    global playerName
    global nameWindow
    global nameEntry
    
    playerName= nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()
    
    CLIENT.send(playerName.encode())
    gameWindow()
    
def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1
    
    nameWindow = Tk()
    nameWindow.title("Tambola Family FUn")
    nameWindow.geometry("800x600")

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()
    bg = ImageTk.PhotoImage(file="./assets/background.png")
    
    canvas1 = Canvas(nameWindow, width=500, height=500)
    canvas1.pack(fill="both", expand=True) #pack is a geometrical method, fill both means it will fill both in width and height, expand means that it will take all the available space
    canvas1.create_image(0,0, image=bg, anchor="nw") #anchor nw is for northwest direction of image
    canvas1.create_text(screen_width/3.5, screen_height/8, text="Enter Name", font=("ChalkBoard SE", 60), fill="black")
    
    nameEntry = Entry(nameWindow, width=8, justify="center", bd=5, bg="white", font=("ChalkBoard SE", 60))
    nameEntry.place(x=screen_width/8, y=screen_height/5.5)
    
    button = Button(nameWindow, text="Save", font=("ChalkBoard SE", 60), width=6, height=2, command=saveName, bg="#80deea", bd=3)
    button.place(x=screen_width/6.3, y=screen_height/2.5) #bd is for border width
    
    nameWindow.resizable(True, True) #allow the user to change size
    nameWindow.mainloop()

def createTicket():
    global gameWindow
    global ticketGrid
    
    mainLabel = Label(gameWindow, width=73,height=13, relief="ridge", borderwidth=5, bg='white')
    mainLabel.place(x=screen_width/17.5, y=screen_height/5.5)
    xpos =screen_width/15.5
    ypos = screen_height/4.8
    for row in range(0,3):
        rowList = []
        for col in range(0,9):
            boxButton = Button(gameWindow, font=("ChalkBoard SE", 30), width=1, height=1, borderwidth=5, relief="flat", bg="#fff176")
            boxButton.place(x=xpos, y=ypos)
            # print(boxButton.config())
            rowList.append(boxButton)
            xpos += 64
            # print(boxButton)
        ticketGrid.append(rowList)
        xpos = screen_width/15.5
        ypos += 64
def placeNumbers():
    global ticketGrid
    global currentNumberList
    
    for row in range(0,3):
        randomColList = []
        counter = 0
        while counter <= 4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1
        numberContainer = {
        "0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "2": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        "3": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        "4": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "5": [50 , 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "6": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        "7": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
        "8": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
        }
        counter=0
        while(counter < len(randomColList)):
            colNum = randomColList[counter]
            numbersListByIndex = numberContainer[str(colNum)]
            randomNumber = random.choice(numbersListByIndex)
            if randomNumber not in currentNumberList:
                numberBox = ticketGrid[row][colNum]
                numberBox.configure(text=randomNumber, fg="black", bg="#f5693b")
                currentNumberList.append(randomNumber)
                counter+=1

def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global winingMessage
    global resetButton
    global flashNumberLabel


    gameWindow = Tk()
    gameWindow.title("Tambola Family Fun")
    gameWindow.geometry('800x600')

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background2.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/3.5,screen_height/9, text = "Tambola Family Fun", font=("Chalkboard SE",50), fill="#3e2723")

    createTicket()
    placeNumbers()


    # Flash Number Label
    flashNumberLabel = canvas2.create_text(screen_width/3.5,screen_height/1.6, text = "Waiting for others to join...", font=("Chalkboard SE",30), fill="#3e2723")

    gameWindow.resizable(True, True)
    gameWindow.mainloop()
setup()