from tkinter import *

root = Tk()

msgBox = Message(root, text = "Text Here")
msgBox.config(font = ('times', 24))
msgBox.pack(padx = 30, pady = 50, side = TOP)

Label(root, text = "Message: ").pack(padx = 10, pady = 20, side = LEFT)
enter = Text(root, height = 1, width = 50, wrap = WORD)
enter.pack(padx = 20, pady = 20, side = LEFT)


but = Button(root, text = "Send")
but.pack(padx = 20, pady = 20, side = LEFT)
#but.place(width = 120, height = 40)
root.mainloop()
