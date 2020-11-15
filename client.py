import socket
import threading
from tkinter import *
from tkinter import messagebox
 
HOST = '' #Enter server IP here from server.py
PORT = 5555
NICKNAME = ""
CLIENT = None #Socket object for client 
MAIN = None #MainWindow object
SELF_MESSAGE = '' #Message currently typed

#Recieve request about nick, send nick
#Keep listening for new incomming messages
#Close connection when recieve disconnect message 
def recieve():
    while True:    
        try:
            message = CLIENT.recv(1024).decode('cp852')
            if message == 'NICK':
                CLIENT.send(NICKNAME.encode('cp852'))
            elif message == '!DISCONNECT':
                CLIENT.close()
                break
            else:
                print(message)
                display(message)
        except:
            print("Error occurred!")
            CLIENT.close()
            break       

#Create socket, set it as global
#Connect to server
#Run recieve() as thread
def threads():
    global CLIENT
    CLIENT = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    CLIENT.connect((HOST,PORT))
    print(f'Connected successfully. Type !DISCONNECT to left chat') 
    thread1 = threading.Thread(target=recieve)
    thread1.start()

#GUI - MAIN window
class MainWindow(Frame):            
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()
    def insert_message(self,message):
        self.messages.configure(state=NORMAL)
        message = message + '\n' 
        self.messages.insert(END,message)
        if message == SELF_MESSAGE:
            self.messages.tag_add('current_message', 'insert - 1 lines', 'end - 1 lines')       
            self.messages.tag_config('current_message',background='#4d68ff')       
        self.messages.see('end')
        self.messages.configure(state=DISABLED)
    def create_widgets(self):
        #Label just for more elegant view
            self.separate1 = Label(self)
            self.separate1.grid(column=0,row=0,columnspan=2)         
        #Textbox for incomming and sended messages 
            self.messages = Text(self,width=50,height=20, wrap='word',bg='#e3e8d7')
            self.messages.grid(column=0,row=1,columnspan=2)
            self.messages.insert(END,'Hit connect to enter the chat! \n')
            self.messages.configure(state=DISABLED)
        #Label to separate Listbox from Textbox
            self.separate2 = Label(self)
            self.separate2.grid(column=0,row=2,columnspan=2)
        #Textbox for writing and sending messages
            self.new_message = Text(self,height=4,width=50,padx=5)
            self.new_message.grid(column=0,row=3,columnspan=2)
        #Exit and connect buttons
            self.exit_button = Button(self,text='Exit',command=self.exit)
            self.exit_button.grid(column=0,row=4)
            self.connect_button = Button(self,text='Connect',command=self.connect)   
            self.connect_button.grid(column=1,row=4)
        #Bind 'enter' button to send function
            self.master.bind('<Return>',self.send)
    #Button send,exit and connect function
    def connect(self):
        threads()
        self.connect_button.configure(state=DISABLED)
    #Get message from textbox, send it to global, send message to server, clear textbox
    def send(self,event):
        try:
            global SELF_MESSAGE
            message = f'{NICKNAME}: {self.new_message.get(0.0,END)}'
            message = message.strip()
            SELF_MESSAGE = message + '\n'
            CLIENT.send(message.encode('cp852'))
            self.new_message.delete(0.0,END)
        except:
            display('Connection error! Check your connection with server.')
            self.new_message.delete(0.0,END)
    def exit(self):
        try:
            CLIENT.send('!DISCONNECT'.encode('cp852'))
            self.master.destroy()
        except:
            self.master.destroy()

#GUI - Nickname window
class Nickname(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()
    #Nickname question label
        nickname_question = Label(self,text='Enter your nickname:')
        nickname_question.pack()
    #Nickname entry
        self.nickname_entry = Entry(self)
        self.nickname_entry.pack()
    #Accept button
        self.nickname_accept = Button(self,text='Accept',command=self.accept)
        self.nickname_accept.pack()
    #Accept function - set global NICKNAME,close nickname window, run main window
    def accept(self):
        global NICKNAME
        nick = self.nickname_entry.get()
        if nick:
            NICKNAME = nick
            self.master.destroy()
            root = Tk()
            main_window = MainWindow(root)
            global MAIN
            MAIN = main_window
            root.title('Chat')
            root.geometry('418x520')
            root.resizable(width=False,height=False)
            root.mainloop()
        else:
            messagebox.showerror("Error!", "Nickname cannot be empty.") 
           
#GUI - Nickname window run
def run_nickname_window():
    nickname_window_root = Tk()
    nickname_window = Nickname(nickname_window_root)
    nickname_window_root.title("Nickname")
    nickname_window_root.geometry('261x90')
    nickname_window_root.resizable(width=False, height=False)
    nickname_window_root.mainloop()

#Display incomming messages on GUI listbox
def display(message):
    MAIN.insert_message(message)

#Program starts
run_nickname_window()
