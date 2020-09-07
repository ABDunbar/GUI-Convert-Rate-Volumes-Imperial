from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from conversion_class_objects import ScrolledList
import pandas as pd


class SimpleEditor(ScrolledList):
    """
    Class to attach functionality to "ScrolledList"
    ======================================================================
    Open: Open .xlsx file and read/print the sheets to Listbox
    Load: Load selected sheet and read/print columns to Listbox
    Rename: Rename selected column name to selected Radiobutton name
    Well: Read/print all wells to Listbox
    Convert: Run hardcoded conversion factors to RATE(M3) and PRESSURE(KPA)
    Graph: Graph RATE(M3) and PRESSURE(KPA) against DATE-TIME
    Save: Save converted file to .xlsx
    Quit: Quit
    """
    def __init__(self, parent=None):
        """
        Initialise functionality buttons
        :param parent:
        """
        frm = Frame(parent)
        frm.grid(row=0, column=0, columnspan=24)
        ttk.Button(frm, text='Open', command=self.onOpen).grid(row=0, column=0)
        ttk.Button(frm, text='Load', command=self.onLoad).grid(row=0, column=3)
        ttk.Button(frm, text='Rename', command=self.onRename).grid(row=0, column=6)
        ttk.Button(frm, text='Well', command=self.onWell).grid(row=0, column=9)
        ttk.Button(frm, text='Convert', command=self.onConvert).grid(row=0, column=12)
        ttk.Button(frm, text='Graph', command=self.onGraph).grid(row=0, column=15)
        ttk.Button(frm, text='Save', command=self.onSave).grid(row=0, column=18)
        ttk.Button(frm, text='Quit', command=self.onQuit).grid(row=0, column=21)
        ScrolledList.__init__(self, parent)

    def onOpen(self):
        file_path = askopenfilename()
        self.xl = pd.ExcelFile(file_path)
        self.list_left.delete(0, END)
        for sheet in self.xl.sheet_names:
            self.list_left.insert(END, sheet)

    def onLoad(self):
        self.df = pd.DataFrame(self.xl.parse(self.label_left))
        self.textbox.delete('1.0', END)
        self.textbox.insert(END, self.df.head())

        self.list_mid.delete(0, END)
        for column in self.df.columns:
            self.list_mid.insert(END, column)

    def onRename(self):
        rename = {self.label_mid: self.radSel}
        self.df.rename(columns=rename, inplace=True)
        self.textbox.delete('1.0', END)
        self.textbox.insert(END, rename)

    def onWell(self):
        self.list_right.delete(0, END)
        for well in self.df.WELL_NAME.unique():
            self.list_right.insert(END, well)

    def onConvert(self):
        """
        m3 -> mmcfd = 35.3147 / 1,000,000
        """
        self.well = self.label_right
        self.df = self.df[self.df['WELL_NAME'] == self.well]
        self.df = self.df[["WELL_NAME", "DATE-TIME", "RATE(M3)", "PRESSURE(KPA)"]]

        CUBIC_METRES_TO_MILLIONS_OF_CUBIC_FEET_PER_DAY = 35.3147 / 1000000
        KILOPASCALS_TO_POUNDS_PER_SQUARE_INCH = 0.000145038 * 1000

        self.df['RATE(M3)_MMCFD'] = self.df['RATE(M3)'] * CUBIC_METRES_TO_MILLIONS_OF_CUBIC_FEET_PER_DAY
        self.df['PRESSURE(KPA)_PSI'] = self.df['PRESSURE(KPA)'] * KILOPASCALS_TO_POUNDS_PER_SQUARE_INCH

        self.df = self.df[["WELL_NAME", "DATE-TIME", "RATE(M3)_MMCFD", "PRESSURE(KPA)_PSI"]]
        self.df.set_index('DATE-TIME', inplace=True)
        self.df.sort_index(inplace=True)

        self.textbox.delete('1.0', END)
        self.textbox.insert(END, self.df.head())

    def onGraph(self):
        pass

    def onSave(self):
        save_file = asksaveasfilename()
        self.df.to_excel(save_file)

    def onQuit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans:
            Frame.quit(self)


if __name__ == '__main__':
    SimpleEditor().mainloop()
