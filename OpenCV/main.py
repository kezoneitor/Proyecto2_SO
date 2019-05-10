from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from assets.colors import *

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Panel disrruptivo")
        self.master.geometry("800x100")
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
        #Buttons ======================================================================================
        self.btnLoad = Button(self.master,
                              text="Browse",
                              font=self.normalFont,
                              background="light gray",
                              command=self.load_file)
        self.inputAnddress = Entry(self.master, font=self.normalFont, background="light gray")
        self.btnConnect1 = Button(self.master,
                                 text="Connect",
                                 font=self.normalFont,
                                 background="cyan3")
        self.btnConnect2 = Button(self.master, text="Disconnect", font=self.normalFont, background="firebrick3")
        self.btnCreateImages = Button(self.master, text="Eject", font=self.normalFont, background="light gray")
        self.btnQuality = Button(self.master, text="Increment Quality", font=self.normalFont, background="light gray")
        #Positions ====================================================================================
        #   >> Row 1
        self.lblAddress.grid(row=1, column=0)
        self.inputAnddress.grid(row=1, column=1)
        self.btnConnect1.grid(row=1, column=2)
        self.btnConnect2.grid(row=1, column=3)
        #   >> Row 2
        self.lblbtnLoad.grid(row=2, column=0)
        self.btnLoad.grid(row=2, column=1)
        self.lblTextLoad.place(x=200, y=30)
        self.btnCreateImages.place(x=100, y=65)
        self.btnQuality.place(x=150, y=65)

    def load_file(self):
        fname = askopenfilename(filetypes=(("MP4 files", "*.mp4"),
                                           ("JPG files", "*.jpg; *.jpeg"),
                                           ("PNG files", "*.png"),
                                           ("All files", "*.*")))
        if fname:
            try:
                self.lblTextLoad = Label(self.master,
                                         text=fname,
                                         font=self.normalFont,
                                         background=coPrincipal).place(x=200, y=30)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return


if __name__ == "__main__":
    MyFrame().mainloop()