#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a simple text editor."""

__author__ = "Hannan Khan"
__copyright__ = "Copyright 2020, ZenText"
__credits__ = ["Hannan Khan"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Hannan Khan"
__email__ = "hannankhan888@gmail.com"

import sys, os
import webbrowser
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesnocancel
import tkinter.colorchooser
from tkfontchooser import askfont


# function needed to use pyinstaller properly:
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


class newTextEditor():
    def __init__(self):
        self.HEIGHT = 600
        self.WIDTH = 800
        self.root = Tk()
        self.root.tk.call('tk', 'scaling', 1.6)
        self.root.geometry(str(self.WIDTH) + "x" + str(self.HEIGHT))
        self.root.title("ZenText")
        self.root.iconbitmap(resource_path('icon.ico'))
        self.filename = ''
        # adds value for word/char wrap option
        self.wordVal = IntVar()
        self.wordVal.set(0)
        self.charVal = IntVar()
        self.charVal.set(1)
        self.signature = StringVar()
        self.endSignature = StringVar()

        # add the text editor to a frame with scrollbars
        self.textFrame = tkinter.Frame(self.root)
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
        self.viewMenu.add_checkbutton(label="Word Wrap", onvalue=1, offvalue=0, variable=self.wordVal,
                                      command=self.wordWrap)
        self.viewMenu.add_checkbutton(label='Character Wrap', onvalue=1, offvalue=0, variable=self.charVal,
                                      command=self.charWrap)

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

        # if argument exists, open the specified file (also takes care of spaces in path)
        if (len(sys.argv) > 1):
            self.fullpath = r""""""
            for i, word in enumerate(sys.argv):
                if (i == 1):
                    self.fullpath = self.fullpath + word
                elif (i > 1):
                    self.fullpath = self.fullpath + ' ' + word
            self.fullpath.strip()
            self.filename = os.path.basename(self.fullpath)
            file = open(self.fullpath, "r")
            self.root.title('ZenText' + ' - ' + os.path.basename(self.fullpath))
            self.textBox.delete(1.0, END)
            text = file.read()
            self.textBox.insert(END, text)
            file.close()

        self.signature.set(self.textBox.get(1.0, END))
        self.root.protocol("WM_DELETE_WINDOW", self.saveAndExit)
        self.root.mainloop()

    def exitRootWindow(self):
        self.root.destroy()

    def saveAs(self):
        self.filename = asksaveasfilename(title="Select File",
                                          filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if self.filename:
            file = open(self.filename + ".txt", "w")
            self.root.title("ZenText" + " - " + os.path.basename(self.filename))
            file.write(self.textBox.get(1.0, END))
            file.close()

    def save(self):
        if self.filename:
            if '.txt' in self.filename:
                file = open(self.filename, "w")
            else:
                file = open(self.filename + ".txt", "w")
            self.root.title("ZenText" + " - " + os.path.basename(self.filename))
            file.write(self.textBox.get(1.0, END))
            file.close()
        else:
            self.saveAs()

    def saveAndExit(self):
        self.endSignature.set(self.textBox.get(1.0, END))
        if self.signature.get() == self.endSignature.get():
            self.exitRootWindow()
        elif self.signature.get() != self.endSignature.get():
            result = askyesnocancel("Exit", "Save changes before exiting?")
            if result == NO:
                self.exitRootWindow()
            elif result == YES:
                self.save()
                self.exitRootWindow()
            elif result is NONE:
                pass


    def openFile(self):
        self.filename = askopenfilename(title="Select file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        if self.filename:
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
        self.leaf.geometry('285x95')
        self.leaf.iconbitmap('icon.ico')
        self.a = Label(self.leaf, text='Created by Hannan Khan (2020)')
        self.githublink = tkinter.Label(self.leaf, text='https://github.com/hannankhan888', foreground='blue',
                                        cursor='hand2')
        self.githublink.bind('<Button-1>', lambda e: webbrowser.open_new('https://github.com/hannankhan888'))
        self.linkedinlink = tkinter.Label(self.leaf, text='https://www.linkedin.com/in/hannankhan888/', fg='blue',
                                          cursor='hand2')
        self.linkedinlink.bind("<Button-1>",
                               lambda e: webbrowser.open_new('https://www.linkedin.com/in/hannankhan888/'))
        self.licenseLink = tkinter.Label(self.leaf, text='License', fg='blue', cursor='hand2')
        self.licenseLink.bind('<Button-1>', lambda e: self.licenseBox())
        self.a.pack()
        self.githublink.pack()
        self.linkedinlink.pack()
        self.licenseLink.pack()

    def licenseBox(self):
        self.leaflet = Toplevel(self.leaf)
        self.leaflet.title('License')
        self.leaflet.geometry('500x510')
        self.leaflet.iconbitmap('icon.ico')
        self.licenseText = Text(self.leaflet, bg='lightgray')
        self.licenseText.insert(END, 'MIT License\n\nCopyright (c) 2020 Hannan Khan\n\nPermission is hereby granted, '
                                     'free of charge, to any person obtaining a copy of this software and associated '
                                     'documentation files (the \"Software\"), to deal in the Software without '
                                     'restriction, including without limitation the rights to use, copy, modify, '
                                     'merge, publish, distribute, sublicense, and/or sell copies of the Software, '
                                     'and to permit persons to whom the Software is furnished to do so, subject to the '
                                     'following conditions:\nThe above copyright notice and this permission notice '
                                     'shall be included in all copies or substantial portions of the Software.\n\nTHE '
                                     'SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR '
                                     'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, '
                                     'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE '
                                     'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER '
                                     'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, '
                                     'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE '
                                     'SOFTWARE.')
        self.licenseText.configure(state=DISABLED, wrap=WORD)
        self.licenseText.pack(fill=BOTH, expand=1)


def main():
    txt = newTextEditor()


if __name__ == '__main__': main()

