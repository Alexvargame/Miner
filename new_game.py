import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from boolean import *
from player import *
from blackjack import *
import random




class Main:
   def __init__(self, master):
      self.slave = Toplevel(master)
      self.master.title('Выберите параметры игры')
      self.master.geometry('220x120+150+50')
      
      

      main_menu = Menu()
      main_menu.add_command(label="Новая игра", command=self.game_table)
      main_menu.add_command(label="Новая игра")#, command=)
      main_menu.add_command(label="Выход",command=self.master.destroy)
      self.frame_croupier=Frame(self.master, relief=SOLID)
      self.frame_desk=Frame(self.master, relief=SOLID)
      self.frame_player=Frame(self.master, relief=SOLID)


      self.master.config(menu=main_menu)
      self.master.protocol('WM_DELETE_WINDOW',self.exitMethod)
      
      
      self.master.mainloop()
