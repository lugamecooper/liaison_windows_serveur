#!/usr/bin/python3

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


class MyWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.create_menu_bar()

        # TODO: Fill the content of the window

        self.geometry("300x200")
        self.title("My First MenuBar V1.0")

    def create_menu_bar(self):
        menu_bar = Menu(self)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="New", command=self.do_something)
        menu_file.add_command(label="Open", command=self.open_file)
        menu_file.add_command(label="Save", command=self.do_something)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_edit = Menu(menu_bar, tearoff=0)
        menu_edit.add_command(label="Undo", command=self.do_something)
        menu_edit.add_separator()
        menu_edit.add_command(label="Copy", command=self.do_something)
        menu_edit.add_command(label="Cut", command=self.do_something)
        menu_edit.add_command(label="Paste", command=self.do_something)
        menu_bar.add_cascade(label="Edit", menu=menu_edit)

        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About", command=self.do_about)
        menu_bar.add_cascade(label="Help", menu=menu_help)

        self.config(menu=menu_bar)

    def open_file(self):
        file = askopenfilename(title="Choose the file to open",
                               filetypes=[("PNG image", ".png"), ("GIF image", ".gif"), ("All files", ".*")])
        print(file)

    def do_something(self):
        print("Menu clicked")

    def do_about(self):
        messagebox.showinfo("My title", "My message")


window = MyWindow()
window.mainloop()