import pandas as pd


class Conversion:
    """
    Take and return Excel file
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.xl_object = pd.ExcelFile(self.filepath)
        self.sheet_names = dict()
        self.which_sheet = 0
        self.df = pd.DataFrame
        self.current_column_names = dict()
        self.new_column_names = dict()
        self.convert_column_names = []
        self.well_names = dict()
        self.well = ""

    def load_sheet(self):
        self.sheet_names = {i: name for (i, name) in enumerate(self.xl_object.sheet_names, start=1)}
        print(self.sheet_names)
        self.which_sheet = int(input("Which sheet to load: "))
        if self.which_sheet == 0:
            print("No sheet selected")
        else:
            self.df = pd.DataFrame(self.xl_object.parse(self.sheet_names[self.which_sheet]))

    def rename_columns(self):
        self.current_column_names = {i: name for (i, name) in enumerate(self.df.columns, start=1)}
        list_new_column_names = ["WELL_NAME", "DATE-TIME", "RATE(M3)", "PRESSURE(KPA)"]
        self.convert_column_names = ["WELL_NAME", "DATE-TIME", "RATE(M3)_MMCFD", "PRESSURE(KPA)_PSI"]
        print(self.current_column_names)

        for name in list_new_column_names:
            print()
            index = int(input("Which column goes with " + name + ":"))
            self.new_column_names[self.current_column_names[index]] = name
            print(self.new_column_names)

        self.df.rename(columns=self.new_column_names, inplace=True)
        self.df = self.df[list_new_column_names]

    def select_well(self):
        self.well_names = {i: name for (i, name) in enumerate(self.df.WELL_NAME.unique(), start=1)}
        print(self.well_names)
        well_index = int(input("Which well: "))
        self.well = self.well_names[well_index]
        self.df = self.df[self.df['WELL_NAME'] == self.well]

    def run_conversions(self):
        """
        m3 -> mmcfd = 35.3147 / 1,000,000
        """
        CUBIC_METRES_TO_MILLIONS_OF_CUBIC_FEET_PER_DAY = 35.3147 / 1000000
        KILOPASCALS_TO_POUNDS_PER_SQUARE_INCH = 0.000145038 * 1000

        self.df['RATE(M3)_MMCFD'] = self.df['RATE(M3)'] * CUBIC_METRES_TO_MILLIONS_OF_CUBIC_FEET_PER_DAY
        self.df['PRESSURE(KPA)_PSI'] = self.df['PRESSURE(KPA)'] * KILOPASCALS_TO_POUNDS_PER_SQUARE_INCH

        # self.df = self.df[(output_col_names)]
        # self.df.set_index('DATE-TIME', inplace=True)
        self.df.sort_index(inplace=True)
        self.df.to_excel(self.well+"_output.xlsx")


def load_and_convert(well, file):
    well = Conversion(file)
    well.load_sheet()
    well.rename_columns()
    well.select_well()
    well.run_conversions()


if __name__ == '__main__':
    file = "file.xlsx"
    load_and_convert("Well-18", file)