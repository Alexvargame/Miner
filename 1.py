from tkinter import *
 
root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")
 
canvas = Canvas(width=85, height=105)
canvas.pack(anchor=CENTER, expand=1)
 
python_image = PhotoImage(file="cards\oborot.png")
 
canvas.create_image(0, 0, anchor=NW, image=python_image)
 
root.mainloop()
