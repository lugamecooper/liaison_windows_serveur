
# Import tkinter
from tkinter import *
 
# Create the root window
root = Tk()
root.geometry('180x200')
 
# Create a listbox
listbox = Listbox(root, width=40, height=10, selectmode=MULTIPLE)
 
# Inserting the listbox items
listbox.insert(1, "Data Structure")
listbox.insert(2, "Algorithm")
listbox.insert(3, "Data Science")
listbox.insert(4, "Machine Learning")
listbox.insert(5, "Blockchain")
 
# Function for printing the
# selected listbox value(s)
def selected_item():
     
    # Traverse the tuple returned by
    # curselection method and print
    # corresponding value(s) in the listbox
    for i in listbox.curselection():
        print(listbox.get(i))
 
# Create a button widget and
# map the command parameter to
# selected_item function
btn = Button(root, text='Print Selected', command=selected_item)
 
# Placing the button and listbox
btn.pack(side='bottom')
listbox.pack()
 
root.mainloop()