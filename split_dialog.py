from tkinter import *

class split_dialog:
  def __init__(self, master):
    self.slave = Toplevel(master)
    self.slave.title('Сплит')
    self.slave.geometry('200x100+300+250')
    self.frame = Frame(self.slave)
    self.frame.pack(side = BOTTOM)
    self.yes_button = Button(self.frame,
                             text = 'Да',command = self.yes)
    self.yes_button.pack(side = LEFT)
    self.no_button = Button(self.frame,
                            text = 'Нет', command = self.no)
    self.no_button.pack(side = RIGHT)
    self.label = Label(self.slave, text="Хотите разделить раздачу?")
    self.label.pack(side = TOP, fill = BOTH, expand = YES)
    self.slave.protocol('WM_DELETE_WINDOW', self.no)
    
    

  def go(self):
    
    
    self.val=True

    self.slave.grab_set()
    self.slave.focus_set()
    self.slave.wait_window()
    return self.val
 
  def yes(self):
    self.val=True
    self.slave.destroy()
    
    
    

  def no(self):
    self.val=False 
    self.slave.destroy()
    
