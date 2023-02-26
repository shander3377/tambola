import socket
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
import random

CLIENT = None
IP_ADDRESS = "127.0.0.1"
PORT = 6000

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
    
setup()