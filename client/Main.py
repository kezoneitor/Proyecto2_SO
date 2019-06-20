import easygui
from tkinter import *
from tkinter import font
import Sockets
from Connection import *
from threading import Thread
from tkinter.messagebox import showerror

class Client(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.proceso = None
        self.coPrincipal = "bisque"
        self.master.title("Client Controller")
        self.master.geometry("800x160")
        self.master.configure(background=self.coPrincipal)
        self.master.rowconfigure(10, weight=1)
        self.master.columnconfigure(10, weight=1)
        #Fonts ========================================================================================
        self.subtitleFont = font.Font(family="Console", size=12, weight="bold")
        self.normalFont = font.Font(family="Console", size=10)
        #Labels =======================================================================================
        self.lblbtnSave = Label(self.master, text="Select Folder", font=self.subtitleFont, background=self.coPrincipal)
        self.lblTextSave = Label(self.master, text="Folder name", font=self.normalFont, background=self.coPrincipal)
        self.lblAddress = Label(self.master, text="Address", font=self.subtitleFont, background=self.coPrincipal)
        self.lblNotification = Label(self.master, text="", fg="red", font=self.subtitleFont, background=self.coPrincipal)
        self.lblTotalImages = Label(self.master, text="Total de imagenes: " + str(sizeRegisters()), font=self.subtitleFont, background=self.coPrincipal)
        #Buttons ======================================================================================
        self.inputAnddress = Entry(self.master, font=self.normalFont, background="light gray")
        self.btnSave = Button(self.master,
                              text="Browse",
                              font=self.normalFont,
                              background="light gray",
                              command=self.save_folder)
        self.btnConnect = Button(self.master,
                                 text="Connect",
                                 font=self.normalFont,
                                 background="light gray",
                                 command=self.connect)
        #Positions ====================================================================================
        #   >> Row 1
        self.lblAddress.grid(row=1, column=0)
        self.inputAnddress.grid(row=1, column=1)
        self.btnConnect.grid(row=1, column=2)
        #   >> Row 3
        self.lblbtnSave.grid(row=3, column=0)
        self.btnSave.grid(row=3, column=1)
        self.lblTextSave.place(x=210, y=30)
        # >> Final
        self.lblTotalImages.place(x=10, y=85)
        self.lblNotification.place(x=290, y=120)

    def save_folder(self):
        path = easygui.diropenbox()
        if path:
            try:
                self.lblTextSave.config(text=path)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % path)
            return

    def ipValide(self, ip):
        if 7 <= len(ip) <= 15 and "." in ip:
            return True
        return False

    def connect(self):
            if self.btnConnect.cget("text") == "Connect" and self.lblTextSave.cget("text") != "Folder name":
                if self.ipValide(self.inputAnddress.get()):
                    dir = self.lblTextSave.cget("text").replace("\\","/") + "/"
                    self.proceso = Thread(target=Sockets.Main, args=(self.inputAnddress.get(), dir,))
                    self.proceso.start()
                    self.btnConnect.config(background="firebrick3", text="Disconnect")
                    self.lblNotification.config(text="Conectado correctamente")
                else:
                    self.lblNotification.config(text="Introduzca una ip valida")

            elif self.btnConnect.cget("text") == "Disconnect":
                self.btnConnect.config(background="cyan3", text="Connect")
                Sockets.mySocket.close()
                self.proceso.join()
                self.lblNotification.config(text="")

if __name__ == "__main__":
    Client().mainloop()