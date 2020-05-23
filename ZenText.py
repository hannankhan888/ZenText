#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a simple text editor."""

__author__ = "Hannan Khan"
__copyright__ = "Copyright 2020, ZenText"
__credits__ = ["Hannan Khan"]
__license__ = "MIT"
__version__ = "2.0"
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
from ctypes import windll


# function needed to use pyinstaller properly:
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")

    def place(self, **kw):
        raise TclError("cannot use place with this widget")


class newTextEditor():
    def __init__(self):
        # to set the screen DPI correct, and fix any blur.
        windll.shcore.SetProcessDpiAwareness(1)
        self.HEIGHT = 720
        self.WIDTH = 1274
        self.root = Tk()
        self.X = int((self.root.winfo_screenwidth() / 2) - (self.WIDTH / 2))
        self.Y = int(self.root.winfo_screenheight() / 20)

        self.root.geometry(str(self.WIDTH) + "x" + str(self.HEIGHT) + "+" + str(self.X) + "+" + str(self.Y))
        self.root.title("ZenText")
        self.root.iconbitmap(resource_path('icon.ico'))
        self._initVars()

        # add the text editor to a frame with scrollbars
        self.textCanvas = tkinter.Canvas(self.root)
        self.textCanvas.grid(row=0, column=0, sticky=N + S + E + W)
        self.textBox = Text(self.root, undo=True, bg="white")
        self.textBox.config(font=("Yu Gothic UI Semilight", "12"))
        self.root.wm_attributes("-alpha", self.alpha.get())

        #adds auto scroll bars to the grid configuration.
        self.vscroll = AutoScrollbar(self.root)
        self.vscroll.grid(row=0, column=1, sticky=N + S)
        self.hscroll = AutoScrollbar(self.root, orient=HORIZONTAL)
        self.hscroll.grid(row=1, column=0, sticky=E + W)
        self.textBox.config(yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set, wrap='char')
        self.textBox.grid(row=0, column=0, sticky=N + S + E + W)
        self.vscroll.config(command=self.textBox.yview)
        self.hscroll.config(command=self.textBox.xview)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self._initMenuBar()

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
        self._initShortcuts()

        self.textCanvas.config(scrollregion=self.textCanvas.bbox(ALL))
        self.root.mainloop()

    def _initVars(self):
        self.filename = ''
        self.theme = StringVar()
        self.theme.set("Default")
        # adds value for word/char wrap option
        self.wordVal = IntVar()
        self.wordVal.set(0)
        self.charVal = IntVar()
        self.charVal.set(1)
        self.signature = StringVar()
        self.endSignature = StringVar()
        self.alpha = DoubleVar()
        self.alpha.set(1.0)

    def _initMenuBar(self):
        """Initializes the topMenuBar"""
        self.topMenuBar = Menu(self.root)
        self.topMenuBar.config(relief='groove')
        self.root.config(menu=self.topMenuBar)

        # adds the cascade and option of File menu
        self.fileMenu = Menu(self.topMenuBar, tearoff=0)
        self.fileMenu.add_command(label="Save As", command=self.saveAs)
        self.fileMenu.add_command(label='Save', command=self.save, accelerator="Ctrl+S")
        self.fileMenu.add_command(label="Open", command=self.openFile, accelerator="Ctrl+O")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.exitRootWindow, accelerator="Ctrl+Q")
        self.topMenuBar.add_cascade(label="File", menu=self.fileMenu)

        # creates the viewmenu, and adds cascade of change view
        self.viewMenu = Menu(self.topMenuBar, tearoff=0)
        self.viewMenu.add_checkbutton(label="Word Wrap", onvalue=1, offvalue=0, variable=self.wordVal,command=self.wordWrap)
        self.viewMenu.add_checkbutton(label='Character Wrap', onvalue=1, offvalue=0, variable=self.charVal,command=self.charWrap)

        # add a changefont option to the viewmenu
        self.viewMenu.add_command(label="Change Font", command=self.setFont)
        # change colors menu -- choose color for window, or for caret
        self.changeColorsMenu = Menu(self.viewMenu, tearoff=0)
        self.themeMenu = Menu(self.changeColorsMenu, tearoff=0)
        self.themeMenu.add_radiobutton(label="Default", value="Default", variable=self.theme, command=self.setTheme)
        self.themeMenu.add_separator()
        for i in ["Beige", "Aquamarine", "Space Blue", "Very Pink", "Super Green"]:
            self.themeMenu.add_radiobutton(label=i, value=i, variable=self.theme, command=self.setTheme)

        self.viewMenu.add_cascade(label="Theme", menu=self.themeMenu)
        self.changeColorsMenu.add_command(label="Background Color", command=self.setBackgroundColor,accelerator="Ctrl+B")
        self.changeColorsMenu.add_command(label="Caret Color", command=self.setCaretColor, accelerator="Ctrl+R")
        self.changeColorsMenu.add_command(label="Change Text Color", command=self.setTextColor, accelerator="Ctrl+T")
        self.viewMenu.add_cascade(label="Adjust colors", menu=self.changeColorsMenu)
        self.viewMenu.add_command(label="Adjust Opacity", command=self.opacityWindow, accelerator="Ctrl+P")

        # adds more options to the view menu
        self.topMenuBar.add_cascade(label="View", menu=self.viewMenu)

        # adds helpmenu to topmenu with cascade
        self.helpMenu = Menu(self.topMenuBar, tearoff=0)
        self.helpMenu.add_command(label="About", command=self.about)
        self.topMenuBar.add_cascade(label="Help", menu=self.helpMenu)

    def _initShortcuts(self):
        self.root.bind("<Control-s>", self.save)
        self.root.bind("<Control-o>", self.openFile)
        self.root.bind("<Control-q>", self.saveAndExit)
        self.root.bind("<Control-b>", self.setBackgroundColor)
        self.root.bind("<Control-r>", self.setCaretColor)
        self.root.bind("<Control-t>", self.setTextColor)
        self.root.bind("<Control-p>", self.opacityWindow)

    def exitRootWindow(self):
        self.root.destroy()

    def saveAs(self):
        """Saves file either as .txt or as ALL FILES via save dialogue."""
        self.filename = asksaveasfilename(title="Select File",
                                          filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if self.filename:
            file = open(self.filename + ".txt", "w")
            self.root.title("ZenText" + " - " + os.path.basename(self.filename))
            file.write(self.textBox.get(1.0, END))
            file.close()
            self.signature.set(self.textBox.get(1.0, END))

    def save(self, event=None):
        """Saves files if it exists already, also updates the signature of the file."""
        if self.filename:
            if '.txt' in self.filename:
                file = open(self.filename, "w")
            else:
                file = open(self.filename + ".txt", "w")
            self.root.title("ZenText" + " - " + os.path.basename(self.filename))
            file.write(self.textBox.get(1.0, END))
            file.close()
            self.signature.set(self.textBox.get(1.0, END))
        else:
            self.saveAs()

    def saveAndExit(self, event=None):
        """Checks to see if endsignature matches signature, takes appropriate action."""
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

    def openFile(self, event=None):
        """Simple file-open dialogue."""
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
        """:returns the color value in hex with the # included"""
        self.color = tkinter.colorchooser.askcolor()
        return self.color[1]

    def setTheme(self):
        self.themesDict = {"Default": {"Background": '#FFFFFF', "Text": '#000000', "Caret": "#000000", "Opacity": 1.0},
                           "Beige": {"Background": '#EAF4D3', "Text": '#994636', "Caret": "#895B1E"},
                           "Aquamarine": {"Background": '#60D394', "Text": '#EE2555', "Caret": "#AAF683"},
                           "Space Blue": {"Background": '#222E50', "Text": '#427369', "Caret": "#8B9A74"},
                           "Very Pink": {"Background": '#EF27A6', "Text": '#DBDBDB', "Caret": "#B0B5B3"},
                           "Super Green": {"Background": '#2A7F62', "Text": '#003108', "Caret": "#03B5AA"}}
        colorPallette = self.themesDict[self.theme.get()]
        self.adjustOpacity(alpha=0.94)
        for place, hexcolor in colorPallette.items():
            if place == "Background":
                self.textBox.config(bg=hexcolor)
            elif place == "Text":
                self.textBox.config(fg=hexcolor)
            elif place == "Caret":
                self.textBox.config(insertbackground=hexcolor, highlightcolor='blue')
            elif place == "Opacity":
                self.adjustOpacity(alpha=hexcolor)

    # color needs to be a char or string value '  '
    def setBackgroundColor(self, event=None):
        c = self.getColor()
        self.textBox.config(bg=c)

    def setTextColor(self, event=None):
        c = self.getColor()
        self.textBox.config(fg=c)

    def setCaretColor(self, event=None):
        c = self.getColor()
        self.textBox.config(insertbackground=c, highlightcolor='blue')

    def charWrap(self):
        """Sets the character wrap, and updates corresponding variables appropriately."""
        if self.charVal.get() == 1:
            self.wordVal.set(0)
            self.textBox.config(wrap='char')
        elif (self.charVal.get() == 0) and (self.wordVal.get() == 0):
            self.textBox.config(wrap='none')

    def wordWrap(self):
        """Sets word wrap to ON. Updates corresponding vars appropriately."""
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

    def adjustOpacity(self, alpha):
        self.alpha.set(alpha)
        self.root.wm_attributes("-alpha", self.alpha.get())

    def opacityWindow(self, event=None):
        """Smaller window from root to set the opacity."""
        self.leaf1 = Toplevel(self.root)
        self.leaf1.title("Opacity")
        width = 285
        height = 50
        x = int(self.root.winfo_x() + self.root.winfo_width() / 2 - width / 2)
        y = int(self.root.winfo_y() + self.root.winfo_height() / 2)
        self.leaf1.geometry('285x50' + "+" + str(x) + "+" + str(y))
        self.leaf1.iconbitmap(resource_path('icon.ico'))
        self.opacitySlider = Scale(self.leaf1, orient=HORIZONTAL, from_=0, to=1,command=self.adjustOpacity)
        self.opacitySlider.set(self.alpha.get())
        self.opacitySlider.pack_configure(fill=BOTH, expand=1)

    def about(self):
        """Small leaf window with the about section and license."""
        self.leaf = Toplevel(self.root)
        self.leaf.title('About')
        self.leaf.geometry('285x95')
        self.leaf.iconbitmap(resource_path('icon.ico'))
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
        self.leaflet.iconbitmap(resource_path('icon.ico'))
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

