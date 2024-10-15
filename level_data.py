import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from boolean import *
from player import *
from blackjack import *
import random
from tkinter import messagebox as mb



class level_data:
    
    def __init__(self, master):
        
        
        self.slave = Toplevel(master)
        self.slave.title('Выберите параметры игры')
        self.slave.geometry('220x120+150+50')

        global Name
        Name=tk.StringVar()     
        Name.set("Alex") 
       
        self.lbl_name=Label(self.slave,text="Введите имя")
        self.ent_name=Entry(self.slave, textvariable=Name)
        self.btn_begin=Button(self.slave, text="Начать", command=self.slave.destroy)
        self.lbl_name.pack()
        self.ent_name.pack()
        self.btn_begin.pack()
        self.slave.grab_set()
        self.slave.focus_set()
        self.slave.wait_window()
        self.new_player_name()
                     
    def new_player_name(self):
        name=Name.get()
        return name
            
            
            

