from get_response import *
from tkinter import *
import tkinter


root = tkinter.Tk()
frame = Frame(root)
frame.pack()

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

# Create the text field where user will enter his query
v = StringVar()

E1 = Entry(frame, bd =5, textvariable= v)
E1.pack(side = LEFT)


def buttonAction(user_query):

    reply = getResponse(user_query)
    var = StringVar()
    label = Message( root, textvariable=var, relief=RAISED, width = 1000)

    var.set(reply)
    label.pack()

B = tkinter.Button(frame, text ="Send", command = lambda:buttonAction(v.get()))
B.pack(side = RIGHT)

root.mainloop()

