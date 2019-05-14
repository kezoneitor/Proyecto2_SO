import easygui
from tkinter import *
from tkinter import font
from assets.colors import *
from funcs.filtros import *
from tkinter.messagebox import showerror


class Server(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Server Controller")
        self.master.geometry("800x160")
        self.master.configure(background=coPrincipal)
        self.master.rowconfigure(10, weight=1)
        self.master.columnconfigure(10, weight=1)
        #Fonts ========================================================================================
        self.subtitleFont = font.Font(family="Console", size=12, weight="bold")
        self.normalFont = font.Font(family="Console", size=10)
        #Labels =======================================================================================
        self.lblbtnLoad = Label(self.master, text="Load video", font=self.subtitleFont, background=coPrincipal)
        self.lblTextLoad = Label(self.master, text="File name", font=self.normalFont, background=coPrincipal)
        self.lblAddress = Label(self.master, text="Address", font=self.subtitleFont, background=coPrincipal)
        self.lblFps = Label(self.master, text="Tomar \t fps", font=self.subtitleFont, background=coPrincipal)
        self.lblNotification = Label(self.master, text="", fg="red", font=self.subtitleFont, background=coPrincipal)
        self.lblTotalImages = Label(self.master, text="Total de imagenes: " + str(sizeRegisters()), font=self.subtitleFont, background=coPrincipal)
        #Buttons ======================================================================================
        self.btnLoad = Button(self.master,
                              text="Browse",
                              font=self.normalFont,
                              background="light gray",
                              command=self.load_file)
        self.inputAnddress = Entry(self.master, font=self.normalFont, background="light gray")
        self.inputFps = Entry(self.master, font=self.normalFont, background="light gray", width=3)
        self.btnConnect = Button(self.master,
                                 text="Connect",
                                 font=self.normalFont,
                                 background="cyan3")
        self.btnDisconnect = Button(self.master, text="Disconnect", font=self.normalFont, background="firebrick3")
        self.btnCreateImages = Button(self.master,
                                      text="Eject",
                                      font=self.normalFont,
                                      background="light gray",
                                      command=self.eject)
        self.btnQuality = Button(self.master,
                                 text="Increment Quality",
                                 font=self.normalFont,
                                 background="light gray",
                                 command=self.test)
        #Positions ====================================================================================
        #   >> Row 1
        self.lblAddress.grid(row=1, column=0)
        self.inputAnddress.grid(row=1, column=1)
        self.btnConnect.grid(row=1, column=2)
        self.btnDisconnect.grid(row=1, column=3)
        #   >> Row 2
        self.lblbtnLoad.grid(row=2, column=0)
        self.btnLoad.grid(row=2, column=1)
        self.lblTextLoad.place(x=200, y=30)
        # >> Final
        self.lblTotalImages.place(x=10, y=85)
        self.lblFps.place(x=10, y=115)
        self.inputFps.place(x=65, y= 120)
        self.btnCreateImages.place(x=120, y=115)
        self.btnQuality.place(x=170, y=115)
        self.lblNotification.place(x=290, y=120)

    def load_file(self):
        path = easygui.fileopenbox(filetypes = ["*.mp4"])
        if path:
            try:
                self.lblTextLoad.config(text=path)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % path)
            return

    def combine_funcs(self,*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    def eject(self):
        self.lblNotification.config(text=ejecutarCrearImagenes(self.lblTextLoad.cget("text"), self.inputFps.get()))
        self.lblTotalImages.config(text="Total de imagenes: " + str(sizeRegisters()))

    def test(self):
        print("Adress",self.inputAnddress.get())
        print("fps",self.inputFps.get())


if __name__ == "__main__":
    Server().mainloop()