from tkinter import *

class yesno:
  def __init__(self, master):
    self.slave = Toplevel(master)
    self.slave.title('Выход')
    self.slave.geometry('200x100+300+250')
    self.frame = Frame(self.slave)
    self.frame.pack(side = BOTTOM)
    self.yes_button = Button(self.frame,
                             text = 'yes',
                             command = self.yes)
    self.yes_button.pack(side = LEFT)
    self.no_button = Button(self.frame,
                            text = 'no',
                            command = self.no)
    self.no_button.pack(side = RIGHT)
    self.label = Label(self.slave)
    self.label.pack(side = TOP, fill = BOTH, expand = YES)
    self.slave.protocol('WM_DELETE_WINDOW', self.no)

  def go(self, title = '', message = ''):
    self.slave.title(title)
    self.label.configure(text = message)
    self.booleanValue = TRUE
    self.slave.grab_set()
    self.slave.focus_set()
    self.slave.wait_window()
    return self.booleanValue

  def yes(self):
    self.booleanValue = TRUE
    self.slave.destroy()

  def no(self):
    self.booleanValue = FALSE
    self.slave.destroy()      
