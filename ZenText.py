from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter.colorchooser
from tkfontchooser import askfont
import webbrowser
import os


class newTextEditor():
    def __init__(self):
        self.HEIGHT = 600
        self.WIDTH = 800
        self.root = Tk()
        self.root.tk.call('tk', 'scaling', 1.45)
        self.root.geometry(str(self.WIDTH) + "x" + str(self.HEIGHT))
        self.root.title("ZenText")
        self.root.iconbitmap('icon.ico')
        self.filename = ''
        # adds value for word/char wrap option
        self.wordVal = IntVar()
        self.wordVal.set(0)
        self.charVal = IntVar()
        self.charVal.set(1)

        # add the text editor to a frame with scrollbars
        self.textFrame = Frame(self.root)
        self.textFrame.pack()
        self.textBox = Text(self.root, undo=True)
        # adds scrollbars to text box
        self.scroll = Scrollbar(self.root)
        self.scrollx = Scrollbar(self.root)
        self.scrollx.config(orient=HORIZONTAL)
        self.scrollx.pack(side=BOTTOM, fill=X)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.textBox.pack(fill=BOTH, expand=1)
        self.textBox.config(yscrollcommand=self.scroll.set, xscrollcommand=self.scrollx.set, wrap='char')
        self.scroll.config(command=self.textBox.yview)
        self.scrollx.config(command=self.textBox.xview)

        # creates the topMenuBar
        self.topMenuBar = Menu(self.root)
        self.root.config(menu=self.topMenuBar)

        # adds the cascade and option of File menu
        self.fileMenu = Menu(self.topMenuBar, tearoff=0)
        self.fileMenu.add_command(label="Save As", command=self.saveAs)
        self.fileMenu.add_command(label='Save', command=self.save)
        self.fileMenu.add_command(label="Open", command=self.openFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.exitRootWindow)
        self.topMenuBar.add_cascade(label="File", menu=self.fileMenu)

        # creates the viewmenu, and adds cascade of change view
        self.viewMenu = Menu(self.topMenuBar, tearoff=0)
        self.viewMenu.add_checkbutton(label="Word Wrap", onvalue=1, offvalue=0, variable=self.wordVal, command=self.wordWrap)
        self.viewMenu.add_checkbutton(label='Character Wrap', onvalue=1, offvalue=0, variable=self.charVal, command=self.charWrap)

        # add a changefont option to the viewmenu
        self.viewMenu.add_command(label="Change Font", command=self.setFont)
        # change colors menu -- choose color for window, or for caret
        self.changeColorsMenu = Menu(self.viewMenu, tearoff=0)
        self.changeColorsMenu.add_command(label="Background Color", command=self.setBackgroundColor)
        self.changeColorsMenu.add_command(label="Caret Color", command=self.setCaretColor)
        self.changeColorsMenu.add_command(label="Change Text Color", command=self.setTextColor)
        self.viewMenu.add_cascade(label="Adjust colors", menu=self.changeColorsMenu)

        # adds more options to the view menu
        self.topMenuBar.add_cascade(label="View", menu=self.viewMenu)

        # adds helpmenu to topmenu with cascade
        self.helpMenu = Menu(self.topMenuBar, tearoff=0)
        self.helpMenu.add_command(label="About", command=self.about)
        self.topMenuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.root.mainloop()

    def exitRootWindow(self):
        self.root.quit()

    def saveAs(self):
        self.filename = asksaveasfilename(title="Select File",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        file = open(self.filename + ".txt", "w")
        self.root.title("ZenText" + " - " + os.path.basename(self.filename))
        file.write(self.textBox.get(1.0, END))
        file.close()

    def save(self):
        if self.filename:
            file = open(self.filename + ".txt", "w")
            self.root.title("ZenText" + " - " + os.path.basename(self.filename))
            file.write(self.textBox.get(1.0, END))
            file.close()
        else:
            self.saveAs()

    def openFile(self):
        self.filename = askopenfilename(title="Select file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        file = open(self.filename)
        self.root.title('ZenText' + ' - ' + os.path.basename(self.filename))
        self.textBox.delete(1.0, END)
        text = file.read()
        self.textBox.insert(END, text)
        file.close()

    # returns the color value in hex with the # included
    def getColor(self):
        self.color = tkinter.colorchooser.askcolor()
        return self.color[1]

    # color needs to be a char or string value '  '
    def setBackgroundColor(self):
        self.c = self.getColor()
        self.textBox.config(bg=self.c)

    def setTextColor(self):
        self.c = self.getColor()
        self.textBox.config(fg=self.c)

    def setCaretColor(self):
        self.c = self.getColor()
        self.textBox.config(insertbackground=self.c, highlightcolor='blue')

    def charWrap(self):
        if self.charVal.get() == 1:
            self.wordVal.set(0)
            self.textBox.config(wrap='char')
        elif (self.charVal.get() == 0) and (self.wordVal.get() == 0):
            self.textBox.config(wrap='none')

    def wordWrap(self):
        if self.wordVal.get() == 1:
            self.charVal.set(0)
            self.textBox.config(wrap="word")
        elif (self.charVal.get() == 0) and (self.wordVal.get() == 0):
            self.textBox.config(wrap="none")

    def setFont(self):
        # open the font chooser and get the font selected by the user
        self.font = askfont(self.root)
        # font is "" if the user has cancelled
        if self.font:
            # spaces in the family name need to be escaped
            self.font['family'] = self.font['family'].replace(' ', '\ ')
            self.font_str = "%(family)s %(size)i %(weight)s %(slant)s" % self.font
            if self.font['underline']:
                self.font_str += ' underline'
            if self.font['overstrike']:
                self.font_str += ' overstrike'
            self.textBox.configure(font=self.font_str)

    def about(self):
        self.leaf = Toplevel(self.root)
        self.leaf.title('About')
        self.leaf.geometry('285x85')
        self.leaf.iconbitmap('icon.ico')
        self.a = Label(self.leaf, text='Created by Hannan Khan (2020)')
        self.githublink = tkinter.Label(self.leaf, text='https://github.com/hannankhan888', foreground='blue', cursor='hand2')
        self.githublink.bind('<Button-1>', lambda e: webbrowser.open_new('https://github.com/hannankhan888'))
        self.linkedinlink = tkinter.Label(self.leaf, text='https://www.linkedin.com/in/hannankhan888/', fg='blue', cursor='hand2')
        self.linkedinlink.bind("<Button-1>", lambda e: webbrowser.open_new('https://www.linkedin.com/in/hannankhan888/'))
        self.a.pack()
        self.githublink.pack()
        self.linkedinlink.pack()


def main():
    txt = newTextEditor()


if __name__ == '__main__': main()
