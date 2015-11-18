from tkinter import *
from queue import Empty
from PIL import Image, ImageTk
import numpy as np


def create(scale, q):
    root = Tk()
    label = Label(root)
    label.pack()
    root.after(0, update_data, root, label, q)
    root.mainloop()


def update_data(root, label, q):
    newodds = None
    while True:
        try:
            newodds = q.get_nowait()
        except Empty:
            break
    if not newodds is None:
        darknesses = (1 - newodds / (newodds + 1)) * 255
        darknesses = darknesses.astype(np.int8, copy=False)
        darknesses = np.flipud(darknesses)
        img = Image.fromarray(darknesses, 'L')
        imgTk = ImageTk.PhotoImage(img)
        label.configure(image=imgTk)
        label.image = imgTk

    root.after(100, update_data, root, label, q)
