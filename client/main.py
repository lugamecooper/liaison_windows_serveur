import socket
import os
import _thread
import json
import tkinter

class main:
    def __init__(self) -> None:
        self.fen = tkinter.Tk("client liaison windows serveur",className="client liaison windows serveur")
        self.fen.geometry(f"{self.fen.winfo_screenwidth()}x{self.fen.winfo_screenheight()}")

        self.menu_bar = tkinter.Menu(self.fen)
        self.menu_connection = tkinter.Menu(self.menu_bar,tearoff=1)
        self.menu_connection.add_command(label="test",command=self.test)
        
        self.fen.config(menu=self.menu_bar)


        self.fen.mainloop()

    def test(self):
        print("test")

main()
