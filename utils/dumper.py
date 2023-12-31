import json

import xlrd
import xlwt


class Dumper:

    def __init__(self, access_count=None, s1_status=None, s2_status=None, save_to="test_result.csv"):
        self.__filename = save_to
        self.__access_count = access_count
        self.__s1_status = s1_status
        self.__s2_status = s2_status

        self.header = []

    def __gen_header(self):
        if self.__access_count is not None:
            self.header.append("access_count")
            for index, column in enumerate(self.__access_count[1:]):
                column = "S2_L%d" % (index + 1)
                self.header.append(column)

        if self.__s1_status is not None:
            self.header.append("s1_count")
            for index, column in enumerate(self.__s1_status[1:]):
                column = "S1_L%d" % (index + 1)
                self.header.append(column)

        if self.__s2_status is not None:
            self.header.append("s2_count")
            for index, column in enumerate(self.__s2_status[1:]):
                column = "S3_L%d" % (index + 1)
                self.header.append(column)

    @property
    def acc_count(self):
        return self.__access_count

    @acc_count.setter
    def acc_count(self, value):
        self.__access_count = value.split(" ") if type(value) == str else value

    @property
    def s1_status(self):
        return self.__s1_status

    @s1_status.setter
    def s1_status(self, value):
        self.__s1_status = value.split(" ") if type(value) == str else value

    @property
    def s2_status(self):
        return self.__s2_status

    @s2_status.setter
    def s2_status(self, value):
        self.__s2_status = value.split(" ") if type(value) == str else value

    def save_to_csv(self):
        self.__gen_header()
        workbook = xlwt.Workbook(encoding="utf-8")
        sheet = workbook.add_sheet("result")
        for i in self.header:
            sheet.write(0, self.header.index(i), i)

        result = self.__access_count + self.s1_status + self.__s2_status

        for index, _ in enumerate(self.header):
            sheet.write(1, index, int(result[index]))

        workbook.save(self.__filename)

    def read_from_csv(self, row=1, is_dict=False, format_=False):
        workbook = xlrd.open_workbook(self.__filename)
        rows = workbook.sheet_by_name("result")
        if is_dict:
            return dict(zip(d.read_from_csv(row=0), d.read_from_csv(row=1))) if not format_ else \
                json.dumps(dict(zip(d.read_from_csv(row=0), d.read_from_csv(row=1))), indent=4)
        return rows.row_values(row)


if __name__ == '__main__':
    d = Dumper()
    d.acc_count = "04 00 01 01 00 00 00 00 01 00 00 00 02"
    d.s1_status = "05 01 01 01 00 00 00 00 01 00 00 00 02"
    d.s2_status = "06 01 01 01 01 00 00 00 01 00 00 00 02"
    d.save_to_csv()

    output = d.read_from_csv(is_dict=True, format_=True)
    print(output)

