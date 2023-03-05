from tkinter import *

root = Tk()

root.title("Search Engine")

root.configure(bg='#d4fffc')


break_text = Label(root,text="\nInformation Retrieval Search Engine\n",font="verdana",bg='#d4fffc')

break_text.grid(row = 0)


search_bar = Entry(root,width = 50,bd='5px',relief="flat",font='verdana')

search_bar.grid(row = 2)

break_text_2 = Label(root,text="\n",bg='#d4fffc')

break_text_2.grid(row = 3)

search_button = Button(root,text="Search",width = 25,activeforeground = "red",font='verdana',bg='#4efcf1')

search_button.grid(row = 4)

root.mainloop()

srp = Tk()

T = Text(srp,yscrollcommand=True,xscrollcommand=True,font='verdana')

T.grid(row = 0)

T.insert(END,"Hello World")

T.config(state=DISABLED)


srp.mainloop()

