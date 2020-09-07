from tkinter import *


class ScrolledList(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.left = Frame()
        self.right = Frame()
        self.rbuttons = Frame()
        self.mid = Frame()
        self.text = Frame()

        # FRAMES - GRID
        self.left.grid(row=1, column=0, rowspan=10, columnspan=6)
        self.mid.grid(row=1, column=6, rowspan=10, columnspan=6)
        self.rbuttons.grid(row=1, column=12, rowspan=10, columnspan=6)
        self.right.grid(row=1, column=18, rowspan=10, columnspan=6)
        self.text.grid(row=11, column=0, rowspan=10, columnspan=24)

        self.makewidgets()

    def makewidgets(self):
        # LEFT LISTBOX
        self.sbar_left = Scrollbar(self.left)
        self.list_left = Listbox(self.left, relief=SUNKEN)
        self.sbar_left.config(command=self.list_left.yview)
        self.list_left.config(yscrollcommand=self.sbar_left.set)
        self.list_left.bind('<<ListboxSelect>>', self.selection_left)
        # MIDDLE LISTBOX
        self.sbar_mid = Scrollbar(self.mid)
        self.list_mid = Listbox(self.mid, relief=SUNKEN)
        self.sbar_mid.config(command=self.list_mid.yview)
        self.list_mid.config(yscrollcommand=self.sbar_mid.set)
        self.list_mid.bind('<<ListboxSelect>>', self.selection_mid)
        # RIGHT LISTBOX
        self.sbar_right = Scrollbar(self.right)
        self.list_right = Listbox(self.right, relief=SUNKEN)
        self.sbar_right.config(command=self.list_right.yview)
        self.list_right.config(yscrollcommand=self.sbar_right.set)
        self.list_right.bind('<<ListboxSelect>>', self.selection_right)
        # RIGHT RADIOBUTTONS
        self.radVar = IntVar()
        self.rad1 = Radiobutton(self.rbuttons, text="WELL_NAME", variable=self.radVar, value=1, command=self.radCall)
        self.rad2 = Radiobutton(self.rbuttons, text="DATE-TIME", variable=self.radVar, value=2, command=self.radCall)
        self.rad3 = Radiobutton(self.rbuttons, text="RATE(M3)", variable=self.radVar, value=3, command=self.radCall)
        self.rad4 = Radiobutton(self.rbuttons, text="PRESSURE(KPA)", variable=self.radVar, value=4, command=self.radCall)
        # BOTTOM TEXT BOX
        self.textbox = Text(self.text, relief=SUNKEN)


        # GRID PLACEMENTS
        self.list_left.grid (row=1, column=0)
        self.sbar_left.grid (row=1, column=5)
        self.list_mid.grid  (row=1, column=6)
        self.sbar_mid.grid  (row=1, column=11)
        self.rad1.grid      (row=1, column=12, sticky='w')
        self.rad2.grid      (row=2, column=12, sticky='w')
        self.rad3.grid      (row=3, column=12, sticky='w')
        self.rad4.grid      (row=4, column=12, sticky='w')
        self.list_right.grid(row=1, column=18)
        self.sbar_right.grid(row=1, column=23)
        self.textbox.grid(row=11, column=0)

    def radCall(self):
        self.radSel = self.radVar.get()
        if self.radSel == 1:
            self.radSel = "WELL_NAME"
        elif self.radSel == 2:
            self.radSel = "DATE-TIME"
        elif self.radSel == 3:
            self.radSel = "RATE(M3)"
        elif self.radSel == 4:
            self.radSel = "PRESSURE(KPA)"

    def selection_left(self, event):
        # self.list_left.delete(0, END)
        self.label_left = self.list_left.get(ACTIVE)

    def selection_mid(self, event):
        # self.list_left.delete(0, END)
        self.label_mid = self.list_mid.get(ACTIVE)

    def selection_right(self, event):
        # self.list_left.delete(0, END)
        self.label_right = self.list_right.get(ACTIVE)
        print(self.label_right)


if __name__ == '__main__':
    root = Tk()
    st = ScrolledList(root)
    root.mainloop()
