import json
import tkinter as tk
import tkinter.ttk as ttk
import os
from tkinter import *
from boolean import *
from as_dialog import *
from mines_data import *
import random
from tkinter import messagebox as mb

from class_miner import Miner,Pixel, make_grid,pixel_mines_null
import datetime
import json

LEVEL_DICT={
   'new': {'geometry':'200x350+300+50',
      'width':10,
      'height':10,
      'mines': 10
      },
   'user': {'geometry':'300x500+300+50',
      'width':16,
      'height':16,
      'mines': 40
      },
   'profi': {'geometry':'900x500+300+5',
      'width':16,
      'height':45,
      'mines': 99
      }
   }

RECORD_DICT={
   'new': 999,
   'user': 999,
   'profi': 999
   }
class Main:
   def __init__(self, master):
      self.master = master
      self.master.title('Miner')
      self.master.geometry('200x240+300+50')
      self.width=0
      self.height=0
      self.mines=0
      self.level='new'
      self.after_id=''
      self.temp_sec=0
      self.result_second=999
      self.frame_desk = Frame(self.master, height=150, relief=SOLID)
      self.frame_desk.pack()
      self.frame_game = Frame(self.master, relief=SOLID)
      self.frame_game.pack()
      self.frame_result = Frame(self.master, height=100, relief=SOLID)
      self.frame_result.pack()
      self.master.protocol('WM_DELETE_WINDOW',self.exitMethod)
      self.menu_panel()
      self.master.mainloop()

   def check_btn(self,event):
      grid_info = event.widget.grid_info()
      if pixel_mines_null(self.MINER._grid[grid_info['row']][grid_info['column']],self.MINER.open,self.MINER.boom,self.MINER.around_pixels):
         print('BOOM!!!')
         self.lbl_result.config(text='LOSE')
         self.stop_tick()
         self.btn_begin.config(text='BEGIN', command=self.new_game)
         return f"BOOM!!!"
      self.MINER._grid[grid_info['row']][grid_info['column']].button['relief'] = tk.SUNKEN
      self.MINER._grid[grid_info['row']][grid_info['column']].button.config(text=self.MINER._grid[grid_info['row']][grid_info['column']].mines)

   def mark_btn(self,event):
      grid_info = event.widget.grid_info()
      if self.MINER._grid[grid_info['row']][grid_info['column']].button['text']=='M':
         self.MINER._grid[grid_info['row']][grid_info['column']].button['text']=' '
      else:
         self.MINER._grid[grid_info['row']][grid_info['column']].button['text'] ='M'
      self.lbl_mines.config(text=str(self.mines - len(self.MINER.mark_pixels_list())))

   def level_new(self):
      self.level='new'
      self.new_game()
   def level_user(self):
      self.level = 'user'
      self.new_game()
   def level_profi(self):
      self.level = 'profi'
      self.new_game()

   def new_game(self):

      self.clean_table()
      self.master.geometry(LEVEL_DICT[self.level]['geometry'])
      self.width = LEVEL_DICT[self.level]['width']
      self.height = LEVEL_DICT[self.level]['height']
      if self.mines==0:
         self.mines = LEVEL_DICT[self.level]['mines']
      self.frame_mines = Frame(self.frame_desk, height=100, relief=SOLID)
      self.frame_mines.grid(column=0, row=0)
      self.lbl_mines = Label(self.frame_mines, text=str(self.mines))
      self.lbl_watches = Label(self.frame_mines, text='')
      self.btn_begin = Button(self.frame_mines, text='BEGIN', command=self.new_game)
      self.lbl_watches.grid(column=0, row=0)
      self.lbl_mines.grid(column=2, row=0)
      self.btn_begin.grid(column=1, row=0)

      self.lbl_result = Label(self.frame_result, text=' ')
      self.lbl_result.grid(row=1, column=1)
      self.MINER = Miner(make_grid(self.width, self.height),self.mines)
      self.btn_begin.config(text='CHECK', command=self.check)
      #print(self.MINER.print_help())
      for i in range(self.width):
         for j in range(self.height):
            self.btn = Button(self.frame_game, width=1, height=1)
            self.btn.grid(column=j, row=i)
            self.btn.bind("<Button-1>", self.check_btn)
            self.btn.bind("<Button-3>", self.mark_btn)
            self.MINER._grid[i][j].button = self.btn
      for row in range(self.MINER._rows):
         for column in range(self.MINER._columns):
            mines = self.MINER.count_mines_for_pixel(self.MINER._grid[row][column].state)
            self.MINER._grid[row][column].mines = mines

      self.tick()
   def check(self):
      if self.MINER.check_solve():
         self.stop_tick()
         self.lbl_result.config(text="WIN")
         if self.mines==LEVEL_DICT[self.level]['mines']:
            self.records_update('records.json')
      else:
         self.stop_tick()
         self.lbl_result.config(text='LOSE')
      self.btn_begin.config(text='BEGIN', command=self.new_game)

   def menu_panel(self):
      main_menu = Menu()
      level_menu = Menu(main_menu,tearoff=0)
      level_menu.add_command(label="Новичек", command=self.level_new)
      level_menu.add_command(label="Любитель", command=self.level_user)
      level_menu.add_command(label="Профи", command=self.level_profi)
      main_menu.add_cascade(label='Новая игра',menu=level_menu)
      main_menu.add_command(label='Мины',command=self.count_mines)
      main_menu.add_command(label='Сброс рекордов', command=lambda file='records.json': self.records_reset(file))

      self.master.config(menu=main_menu)

   def count_mines(self):

      mines_data(self.master)
      self.mines = mines_data.new_count_mines(self)


   def clean_table(self):
      for widget in self.frame_desk.winfo_children():
            widget.destroy()
      for widget in self.frame_game.winfo_children():
            widget.destroy()
      for widget in self.frame_result.winfo_children():
            widget.destroy()

   def tick(self):
      self.after_id=root.after(1000,self.tick)
      f_temp=datetime.datetime.fromtimestamp(self.temp_sec).strftime("%S")
      self.lbl_watches.config(text=str(f_temp))
      self.temp_sec+=1

   def stop_tick(self):
      root.after_cancel(self.after_id)
      self.result_second=self.temp_sec
      self.temp_sec=0

   def exitMethod(self):
       self.dialog = yesno(self.master)
       self.returnValue = self.dialog.go('question',
                                         'Вы хотите выйти?')
       if self.returnValue:
         self.master.destroy()

   def records_update(self,file):
      with open(file) as f:

         templates=json.load(f)
      print(templates[self.level])
      print(self.result_second)
      if templates[self.level]>self.result_second:
         RECORD_DICT[self.level]=self.result_second
      with open(file,'w') as f:
         json.dump(RECORD_DICT,f)

   def records_reset(self,file):
      self.dialog = yesno(self.master)
      self.returnValue = self.dialog.go('question',
                                        'Сбросить рекорды?')
      if self.returnValue:
         with open(file, 'w') as f:
            json.dump(RECORD_DICT, f)


root = Tk()

Main(root)
      
