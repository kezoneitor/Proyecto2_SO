from tkinter import *
from tkinter import font
from assets.colors import *
from funcs.filtros import *

class Client(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Client Controller")
        self.master.geometry("800x160")
        self.master.configure(background=coPrincipal)
        self.master.rowconfigure(10, weight=1)
        self.master.columnconfigure(10, weight=1)
        #Fonts ========================================================================================
        self.subtitleFont = font.Font(family="Console", size=12, weight="bold")
        self.normalFont = font.Font(family="Console", size=10)
        #Labels =======================================================================================
        self.lblAddress = Label(self.master, text="Address", font=self.subtitleFont, background=coPrincipal)
        self.lblNotification = Label(self.master, text="", fg="red", font=self.subtitleFont, background=coPrincipal)
        self.lblTotalImages = Label(self.master, text="Total de imagenes: " + str(sizeRegisters()), font=self.subtitleFont, background=coPrincipal)
        #Buttons ======================================================================================
        self.inputAnddress = Entry(self.master, font=self.normalFont, background="light gray")
        self.btnConnect = Button(self.master,
                                 text="Connect",
                                 font=self.normalFont,
                                 background="cyan3")
        self.btnDisconnect = Button(self.master,
                                    text="Disconnect",
                                    font=self.normalFont,
                                    background="firebrick3")
        #Positions ====================================================================================
        #   >> Row 1
        self.lblAddress.grid(row=1, column=0)
        self.inputAnddress.grid(row=1, column=1)
        self.btnConnect.grid(row=1, column=2)
        self.btnDisconnect.grid(row=1, column=3)
        # >> Final
        self.lblTotalImages.place(x=10, y=85)
        self.lblNotification.place(x=290, y=120)


if __name__ == "__main__":
    Client().mainloop()