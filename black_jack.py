import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image, ImageTk
from tkinter import *
from boolean import *
from player import *
from blackjack import *
from player_data import *
from game_data import *
from deck import *
from split_dialog import *
from as_dialog import *
import random
from tkinter import messagebox as mb





class Main:
   def __init__(self, master):
      self.master = master
      self.master.title('BlackJack')
      self.master.geometry('800x620+300+50')
      self.player=Player("")
      self.n=4
      self.bet=10
      self.numtable=0
      self.card_deck=[]
      self.card_deck_dict={}
      
      self.frame_desk=Frame(self.master,height=150, relief=SOLID)
      self.frame_croupier=Frame(self.master,height=150,relief=SOLID)
      self.frame_player=Frame(self.master,height=150, relief=SOLID)

      
      self.frame_menu=Frame(self.master, relief=SOLID)
      self.frame_croupier.pack(pady=3)
      self.frame_desk.pack(pady=3)
      self.frame_player.pack(pady=3)
      self.frame_menu.pack(pady=3)

      

     
      self.master.protocol('WM_DELETE_WINDOW',self.exitMethod)
      self.menu_panel(self.player)
      self.master.mainloop()

   def menu_panel(self, player):

      main_menu = Menu()
      main_menu.add_command(label="Новая игра", command=self.new_player)
      if player.name!='':
         for widget in self.frame_croupier.winfo_children():
            widget.destroy()
         for widget in self.frame_desk.winfo_children():
            widget.destroy()
         for widget in self.frame_player.winfo_children():
            widget.destroy()
         for widget in self.frame_menu.winfo_children():
            widget.destroy()
         self.begin_btn=ttk.Button(self.frame_menu, width=15, text="Начать раздачу", command=self.clean_table)
         self.begin_btn.pack(side=LEFT, ipady=10, padx=20, pady=20)
         self.choice_btn_2=ttk.Button(self.frame_menu, text='Стоп', command=self.no_card)
         #self.choice_btn_2.pack()
         main_menu.add_command(label="Параметры игры",command=self.new_param)
      main_menu.add_command(label="Правила игры")#,command=self.master.destroy)
      main_menu.add_command(label="Выход",command=self.master.destroy)
      self.master.config(menu=main_menu)
      
   def new_player(self):
      
      player_data(self.master)
      self.player.name=player_data.new_player_name(self)
      if self.player.name!='':
         self.menu_panel(self.player)
      else:
         player_data(self.master)

   def new_param(self):
      
      game_data(self.master)
      self.n, self.bet=game_data.new_game_param(self)
      if all(game_data.new_game_param(self)):
         self.card_deck, self.card_deck_dict=get_deck(self.n)
         self.clean_table()
      else:
         game_data(self.master)
    
      
   def clean_table(self):
      if self.choice_btn_2:
         self.choice_btn_2.destroy()
      for widget in self.frame_croupier.winfo_children():
            widget.destroy()
      for widget in self.frame_desk.winfo_children():
            widget.destroy()
      for widget in self.frame_player.winfo_children():
            widget.destroy()
      self.choice_btn_2=ttk.Button(self.frame_menu, text='Стоп',width=15, command=self.no_card)
      self.choice_btn_2.pack(side=RIGHT, ipady=10, padx=20, pady=20)
      


      self.game_table(self.player,self.n, self.bet)
  
##      
   def game_table(self,name, n=4, bet=10):
      self.frame_player_1=Frame(self.frame_player, relief=SOLID)
      self.frame_player_2=Frame(self.frame_player, relief=SOLID)
      self.frame_player_1.grid(column=0, row=0)
      self.frame_player_2.grid(column=0, row=1)
      self.player.game_list=[[]]
      #self.player.balance=self.player.balance-self.bet
      if len(self.card_deck)<50:  #########Смена колоды
        self.card_deck, self.card_deck_dict=get_deck(self.n)
      self.Croupier=Player("Croupier")
      
      self.player.game_list=begin_game(self.card_deck, self.player)
      self.Croupier.game_list=player_game(self.card_deck, self.Croupier,0)
      
      self.croupier_label=ttk.Label(self.frame_croupier, font=('Arial',14),text=self.Croupier.name.upper())
      self.croupier_label_res=ttk.Label(self.frame_croupier, text=f"Сумма {sum(self.card_deck_dict[i] for i in self.Croupier.game_list[0])}")
      #self.croupier_cards=ttk.Label(self.frame_croupier, text=f"Комбинация на руках {self.Croupier.game_list[0]}")
      self.add_card_img(self.Croupier,1)
      self.add_card_img(self.player,len(self.player.game_list))
      self.croupier_label.grid(column=0, row=0, columnspan=2)
      self.croupier_label_res.grid(column=0, row=1, columnspan=2)
      #self.croupier_cards.grid(column=0, row=2, columnspan=2)
      
      
      
      self.desk_bet=ttk.Label(self.frame_desk, text=f"Ставка {bet}")
     
      self.desk_image = tk.Canvas(self.frame_desk, height=105, width=85)
      self.deck_img = tk.PhotoImage(file="cards\oborot.png") 
      image = self.desk_image.create_image(0, 0, anchor='nw',image=self.deck_img)
       
      self.player_label=ttk.Label(self.frame_player_1, font=('Arial',14),text=f" {self.player.name.upper()}")
      self.player_balance=ttk.Label(self.frame_player_1, text=f"Баланс {self.player.balance}")  
      self.player_label.grid(column=0, row=0, columnspan=2)
      self.player_balance.grid(column=0, row=2, columnspan=2)
      
  
      #self.desk_label.grid(column=0, row=1, sticky=EW)
      self.desk_bet.grid(column=0, row=0, sticky=W)
      self.desk_image.grid(column=3,row=0)

     

      self.player_table()
      self.if_BJ(sum(self.card_deck_dict[i]  for i in self.player.game_list[len(self.player.game_list)-1]))
      self.is_stop(sum(self.card_deck_dict[i]  for i in self.player.game_list[len(self.player.game_list)-1]))
      self.is_split(self.player)


   

   def player_table(self):
      for i in range(len(self.player.game_list)):
         self.frame_player_table=Frame(self.frame_player_2, relief=SOLID)
         #self.frame_player_table.grid(column=i, row=0)
         self.numtable=i
         self.player_label_res=ttk.Label(self.frame_player_2,
                                         text=f"Сумма {sum(self.card_deck_dict[i]  for i in self.player.game_list[i])}")
##         self.player_cards=ttk.Label(self.frame_player,
##                                     text=f"Комбинация на руках {self.player.game_list[i]}")
         self.choice_btn_1=ttk.Button(self.frame_player_2,
                                      text='Еще карту?')         
         
         
     #    self.player_cards.grid(column=i*3, row=1, columnspan=2)
         self.player_label_res.grid(column=i*4, row=3, columnspan=2)
         
         self.choice_btn_1.grid(column=i*4, row=5)
         self.choice_btn_1.bind('<Button-1>', self.add_card)
         self.add_card_img(self.player,len(self.player.game_list))
         

      
   def split_game_table(self):
      self.split_btn.destroy()
      
      self.player_balance.config(text=f"Баланс {self.player.balance}")
      crd=self.player.game_list[self.numtable].pop(0)
      self.player.game_list=player_game(self.card_deck, self.player,self.numtable)######################
      #print('list',self.player.game_list)
      self.player.game_list.append([crd])
      self.player.game_list=player_game(self.card_deck, self.player, self.numtable+1)
      self.player_table()
      

   def add_card(self,event):
      if self.split_btn:
         self.split_btn.destroy()
      grid_info = event.widget.grid_info()
      if sum(self.card_deck_dict[i]  for i in self.player.game_list[grid_info['column']//3])>21:
         mb.showwarning(message='Перебор')
      elif sum(self.card_deck_dict[i]  for i in self.player.game_list[grid_info['column']//3])==21:
         mb.showinfo(message='У Вас 21')
      else:
         r=player_game(self.card_deck, self.player,grid_info['column']//3)
         self.add_card_img(self.player,len(self.player.game_list) )
         if r[grid_info['column']//3][-1][-1]=='A':
            if self.if_As(r[grid_info['column']//3][-1]):
               r[grid_info['column']//3][-1]=r[grid_info['column']//3][-1][0]+'1'
         #print(r)
         for widget in self.frame_player_2.winfo_children():
            if widget.widgetName.split('::')[-1]=='label':
               if widget.grid_info()['column']==grid_info['column'] and widget.grid_info()['row']==grid_info['row']-2:
                  
                  widget.config(text=f" Сумма {sum(self.card_deck_dict[i]  for i in r[grid_info['column']//3])}")
                  
##            elif widget.grid_info()['column']==grid_info['column'] and widget.grid_info()['row']==grid_info['row']-4:
##               widget.config(text=f"Комбинация на руках {r[grid_info['column']//3]}")
               
     # self.desk_label.config(text=len(self.card_deck))


   def no_card(self):
      self.choice_btn_1.destroy()
      self.choice_btn_2.destroy()
      self.add_croupier()
      
   def add_croupier(self):
      
      self.Croupier.game_list=player_game(self.card_deck, self.Croupier,0)
      if self.Croupier.sum_res()[0]==21:
         for widget in self.frame_desk.winfo_children():
            widget.destroy()
         self.desk_label=ttk.Label(self.frame_desk)
         self.desk_label.grid(column=0, row=0)
         #self.croupier_cards.config(text=f"Комбинация на руках {self.Croupier.game_list[0]}")
         self.croupier_label_res.config(text=f" Сумма {sum(self.card_deck_dict[i]  for i in self.Croupier.game_list[0])}")
         self.add_card_img(self.Croupier,1)
         
         self.desk_label.config(text=f"Все игроки проиграли раунд")
         self.player.balance=self.player.balance+-self.bet*len(self.player.game_list)
         self.player_balance.config(text=f"Баланс {self.player.balance}")

        
      else:
         r=game_croupier(self.card_deck,self.Croupier)
         
   
         #self.croupier_cards.config(text=f"Комбинация на руках {r[len(self.Croupier.game_list)-1]}")
         self.croupier_label_res.config(text=f" Сумма {sum(self.card_deck_dict[i]  for i in r[len(self.Croupier.game_list)-1])}")
         self.add_card_img(self.Croupier,1)
         #self.desk_label.config(text=len(self.card_deck))
         self.result_game(self.bet)
      
   def result_game(self, bet):
      winners=WhoWin(self.Croupier, self.player)
      wins=''
      for k, v in winners.items():
         if len(v)>0:
            wins+=','.join(v)+' игрока '+k
      w=len(winners[self.player.name])*2-len(self.player.game_list)
      for widget in self.frame_desk.winfo_children():
            widget.destroy()
      self.desk_label=ttk.Label(self.frame_desk)
      self.desk_label.grid(column=0, row=0)
      if len(wins)>0:
         self.desk_label.config(text=f"Победили столы {wins}", font=('Arial', 14))        
      else:
         self.desk_label.config(text=f"Все игроки проиграли раунд",font=('Arial', 14))
         
      self.player.balance=self.player.balance+self.bet*(len(winners[self.player.name])*2-len(self.player.game_list))
      self.player_balance.config(text=f"Баланс {self.player.balance}")

   def is_split(self, pl):
      self.split_btn=ttk.Button(self.frame_player_2, text="Сплит?", command=self.split_game_table)
      if self.card_deck_dict[pl.game_list[len(self.player.game_list)-1][0]]==self.card_deck_dict[pl.game_list[len(self.player.game_list)-1][1]]:
        
         self.split_btn.grid(column=1, row=5)

   def is_stop(self,s):
      if s>21:
         self.choice_btn_1.destroy()
         self.choice_btn_2.destroy()
         self.add_croupier()
   def if_BJ(self,s):
      if s==21:
         self.player.balance=self.player.balance+self.bet
         self.choice_btn_1.destroy()
         self.choice_btn_2.destroy()
         mb.showinfo(message="У Вас БлекДжек! Вы выиграли")
         self.add_croupier()
         
   def if_As(self,card):
      self.as_dialog=as_dialog(self.master)
      self.as_choice=self.as_dialog.go()
      return self.as_choice


   def add_card_img(self, pl,pos):
      if pl.name=='Croupier':
         widget_im=self.frame_croupier
      else:
         widget_im=self.frame_player_2         
      pl.image_list=[[]]

           
      for i in range(len(pl.game_list)):
         pl.image_list.append([])
         for j in range(len(pl.game_list[i])):
            self.cards_images=tk.Canvas(widget_im, height=130, width=90)
##            if str(pl.game_list[i][j])[-1]=='1':
##               path=str(pl.game_list[i][j][0])+'A.png'
##            else:               
            path=str(pl.game_list[i][j])+'.png'
 
            file_name = os.path.join("cards", path)
            #print("i,j,pl,list",i,j,pl.name,pl.game_list[i][j])
            im=tk.PhotoImage(file=file_name)
            pl.image_list[i].append(im)
            
            image = self.cards_images.create_image(0, 0, anchor='nw',image=pl.image_list[i][j])
            self.cards_images.grid(column=j+4*i, row=4,pady=1)
##         else:
##            for widget in self.frame_player_2.winfo_children():
##               print(widget.widgetName, widget.grid_info()['column'])
##               if (widget.widgetName.split('::')[-1]=='frame') and widget.grid_info()['column']==i:
##                  widget_im=widget
##                  pl.image_list.append([])
##                  print(widget_im)
##                  for j in range(len(pl.game_list[i])):
##                     self.cards_images=tk.Canvas(widget_im, height=120, width=90)
##                     if str(pl.game_list[i][j])[-1]==1:
##                        path=str(pl.game_list[i][j][0])+'A.png'
##                        print(path)
##                     else:               
##                        path=str(pl.game_list[i][j])+'.png'
##                     
##                     #print(path)
##                     
##                     file_name = os.path.join("cards", path)
##                     #print("i,j,pl,list",i,j,pl.name,pl.game_list[i][j])
##                     im=tk.PhotoImage(file=file_name)
##                     pl.image_list[i].append(im)
##                     
##                     image = self.cards_images.create_image(0, 0, anchor='nw',image=pl.image_list[i][j])
##                     self.cards_images.grid(column=j, row=4)
            
   
   def exitMethod(self):
       self.dialog = yesno(self.master)
       self.returnValue = self.dialog.go('question',
                                         'Вы хотите выйти?')
       if self.returnValue:
         self.master.destroy()
      
       
root = Tk()

Main(root)
      
