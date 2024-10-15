import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from boolean import *



class mines_data:
    
    def __init__(self, master):
        
        
        self.slave = Toplevel(master)
        self.slave.title('Введите кол-во мин')
        self.slave.geometry('220x120+150+50')

        global Count_mines
        Count_mines=tk.IntVar()
        Count_mines.set(0)
       
        self.lbl_name=Label(self.slave,text="Введите кол-во мин")
        self.ent_name=Entry(self.slave, textvariable=Count_mines)
        self.btn_begin=Button(self.slave, text="Начать", command=self.slave.destroy)
        self.lbl_name.pack()
        self.ent_name.pack()
        self.btn_begin.pack()
        self.slave.grab_set()
        self.slave.focus_set()
        self.slave.wait_window()
        self.new_count_mines()
                     
    def new_count_mines(self):
        count_mines=Count_mines.get()
        return count_mines
            
            
            

