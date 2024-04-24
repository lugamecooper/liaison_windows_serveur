import tkinter
from tkinter import filedialog
class main:
    def __init__(self) -> None:
        self.path = None
        self.fen = tkinter.Tk()
        self.fen.geometry("500x500")
        self.select_folder = tkinter.Button(self.fen,text="choisissez un dossier",command=self.test)

        self.select_folder.pack()
        self.fen.mainloop()

    def test(self):
        test = filedialog.askopenfile(title="séléctionner le dossier cible", initialdir=self.path)
        if test:
            self.path = test.name
            self.select_folder.config(text=f"changer de dossier\nactuelle : '{self.path}'")
            self.select_folder.update()
            print(test)

main()