import easygui
from tkinter import *
from tkinter import font
from Filters import *
from  threading import Thread
import Sockets
from tkinter.messagebox import showerror, showinfo
from Connection import *
import os


class Server(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.proceso = None
        self.coPrincipal = "bisque"
        self.master.title("Server Controller")
        self.master.geometry("800x160")
        self.master.configure(background=self.coPrincipal)
        self.master.rowconfigure(10, weight=1)
        self.master.columnconfigure(10, weight=1)
        #Fonts ========================================================================================
        self.subtitleFont = font.Font(family="Console", size=12, weight="bold")
        self.normalFont = font.Font(family="Console", size=10)
        #Labels =======================================================================================
        self.lblbtnLoad = Label(self.master, text="Load video", font=self.subtitleFont, background=self.coPrincipal)
        self.lblbtnSave = Label(self.master, text="Select Folder", font=self.subtitleFont, background=self.coPrincipal)
        self.lblTextSave = Label(self.master, text="Folder name", font=self.normalFont, background=self.coPrincipal)
        self.lblTextLoad = Label(self.master, text="File name", font=self.normalFont, background=self.coPrincipal)
        self.lblAddress = Label(self.master, text="Address", font=self.subtitleFont, background=self.coPrincipal)
        self.lblFps = Label(self.master, text="Tomar \t fps", font=self.subtitleFont, background=self.coPrincipal)
        self.lblNotification = Label(self.master, text="", fg="red", font=self.subtitleFont, background=self.coPrincipal)
        self.lblTotalImages = Label(self.master, text="Total de imagenes: " + str(sizeRegisters()), font=self.subtitleFont, background=self.coPrincipal)
        #Buttons ======================================================================================
        self.btnLoad = Button(self.master,
                              text="Browse",
                              font=self.normalFont,
                              background="light gray",
                              command=self.load_file)
        self.btnSave = Button(self.master,
                              text="Browse",
                              font=self.normalFont,
                              background="light gray",
                              command=self.save_folder)
        self.inputFps = Entry(self.master, font=self.normalFont, background="light gray", width=3)
        self.InputAddress= Entry(self.master, font=self.normalFont, background="light gray")
        #cyan3
        self.btnConnect = Button(self.master,
                                 text="Connect",
                                 font=self.normalFont,
                                 background="cyan3",
                                 command=self.connect)
        self.btnCreateImages = Button(self.master,
                                      text="RUN",
                                      font=self.normalFont,
                                      background="light gray",
                                      command=self.eject)
        self.btnQuality = Button(self.master,
                                 text="Increment Quality",
                                 font=self.normalFont,
                                 background="light gray",
                                 command=self.quality)

        self.btnExtract = Button(self.master,
                                 text="Extract definity images",
                                 font=self.normalFont,
                                 background="light gray",
                                 command=self.extract)
        #Positions ====================================================================================
        #   >> Row 1
        self.lblAddress.grid(row=1, column=0)
        self.InputAddress.grid(row=1, column=1)
        self.btnConnect.grid(row=1, column=2)
        #   >> Row 2
        self.lblbtnLoad.grid(row=2, column=0)
        self.btnLoad.grid(row=2, column=1)
        self.lblTextLoad.place(x=210, y=30)
        #   >> Row 3
        self.lblbtnSave.grid(row=3, column=0)
        self.btnSave.grid(row=3, column=1)
        self.lblTextSave.place(x=210, y=60)
        # >> Final
        self.lblTotalImages.place(x=10, y=85)
        self.lblFps.place(x=10, y=115)
        self.inputFps.place(x=65, y= 120)
        self.btnCreateImages.place(x=120, y=115)
        self.btnQuality.place(x=170, y=115)
        self.btnExtract.place(x=295, y=115)

    def load_file(self):
        path = easygui.fileopenbox(filetypes = ["*.mp4"])
        if path:
            try:
                self.lblTextLoad.config(text=path)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % path)
            return

    def save_folder(self):
        path = easygui.diropenbox()
        if path:
            try:
                self.lblTextSave.config(text=path)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % path)
            return

    def eject(self):
        process = Thread(target=ejecutarCrearImagenesV2,args=(self.lblTextLoad.cget("text"), self.lblTextSave.cget("text"), self.inputFps.get(),))
        process.start()
        process.join()
        self.lblTotalImages.config(text="Total de imagenes: " + str(sizeRegisters()))

    def quality(self):
        if len(Sockets.ports) != 0:
            Sockets.repartir(sizeRegisters())
        else:
            showerror("Clientes", "No existen conexiones cliente")

    def ipValide(self, ip):
        if 7 <= len(ip) <= 15 and "." in ip:
            return True
        return False

    def extract(self):
        if(self.lblTextSave.cget("text") != "Folder name"):
            nombre_carpeta = self.lblTextSave.cget("text").replace("\\", "/") + "/found_images/"
            try:
                os.stat(nombre_carpeta)
            except:
                os.mkdir(nombre_carpeta)
            list = readImage(nombre_carpeta, 0, 0)
            if len(list) != 0:
                showinfo("Proceso ejecutado", "Terminado correctamente")
            else:
                showinfo("Proceso ejecutado", "Lista vacia")
        else:
            showerror("Falta informacion", "Eliga carpeta donde procesar la ejecucion")

    def connect(self):
            if self.btnConnect.cget("text") == "Connect":
                if self.ipValide(self.InputAddress.get()):
                    self.proceso = Thread(target=Sockets.socketServer, args=(self.InputAddress.get(),))
                    self.proceso.start()
                    self.btnConnect.config(background="firebrick3", text="Disconnect")
                    self.lblNotification.config(text="")
                else:
                    self.lblNotification.config(text="Introduzca una ip valida")

            elif self.btnConnect.cget("text") == "Disconnect":
                self.btnConnect.config(background="cyan3", text="Connect")
                Sockets.mySocket.close()
                self.proceso.join()
                self.lblNotification.config(text="")


if __name__ == "__main__":
    Server().mainloop()
