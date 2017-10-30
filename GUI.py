from Tkinter import *

root = Tk()

messages = Text(root)
messages.pack()

input_user = StringVar()
input_field = Entry(root, text=input_user)
input_field.pack(side=BOTTOM, fill=X)

def send(event):
	input_get = input_field.get()
	if input_get:
		messages.insert(INSERT, 'Me: %s\n' % input_get)
		input_user.set('')
		return "break"

def sendButton():
	input_get = input_field.get()
	if input_get:
		messages.insert(INSERT, 'Me: %s\n' % input_get)
		input_user.set('')

Label(root, text= "Message: ").pack(padx = 10, pady = 20, side = LEFT)
enter = Text(root, height = 1, width = 50, wrap = WORD)
enter.pack(padx = 20, pady = 20, side = LEFT)

input_field.bind("<Return>", send)
but = Button(root, text = "Send", command=sendButton)
but.pack(padx = 20, pady = 20, side = LEFT)
#but.place(width = 120, height = 40)
root.mainloop()
