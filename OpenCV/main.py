from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Panel disrruptivo")
        self.master.geometry("900x200")
        self.master.configure(background="SpringGreen3")
        self.master.rowconfigure(10, weight=1)
        self.master.columnconfigure(10, weight=1)
        #Fonts ========================================================================================
        self.titleFont = font.Font(family="Console", size=12, weight="bold")
        self.normalFont = font.Font(family="Console", size=10)
        #Labels =======================================================================================
        self.lblbtnLoad = Label(self.master, text="Load video", font=self.titleFont, background="SpringGreen3")
        self.lblTextLoad = Label(self.master, text="File name", font=self.normalFont, background="SpringGreen3")
        self.lblAddress = Label(self.master, text="Address", font=self.titleFont, background="SpringGreen3")
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
        #   >> Row 0
        self.lblbtnLoad.grid(row=0, column=0)
        self.btnLoad.grid(row=0, column=1)
        self.lblTextLoad.place(x=200, y=5)
        self.btnCreateImages.place(x=200, y=40)
        self.btnQuality.place(x=250, y=40)
        Label(self.master, text="", font=self.titleFont, background="SpringGreen3").grid(row=1,column=0)
        Label(self.master, text="", font=self.titleFont, background="SpringGreen3").grid(row=2,column=0)
        #   >> Row 2
        self.lblAddress.grid(row=3, column=0)
        self.inputAnddress.grid(row=3, column=1)
        self.btnConnect1.grid(row=3, column=2)
        self.btnConnect2.grid(row=3, column=3)
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
                                         background="SpringGreen3").place(x=200, y=5)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return


if __name__ == "__main__":
    MyFrame().mainloop()