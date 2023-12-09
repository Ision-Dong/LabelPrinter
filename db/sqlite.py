import datetime
import logging
import os
import sqlite3

from utils.date import adjust_time
from utils.log import output


class DBConnector:

    PREFIX = "CMD"

    def __init__(self, **kwargs):
        self.args = kwargs
        try:
            self.con = sqlite3.connect(os.getcwd() + "\db\label.sqlite3" or "label.sqlite3")
        except sqlite3.OperationalError:
            self.con = sqlite3.connect("label.sqlite3")
        self.cursor = self.con.cursor()
        # self.__delete_db()
        self.__init_db()

    def __delete_db(self, table_name=None):
        delete_sql = "drop table {};".format(table_name or "labels")
        self.cursor.execute(delete_sql)
        self.con.commit()

    def __init_db(self):
        self.con.execute(
            "create table if not exists labels(_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, MSN varchar unique)"
        )
        for column in self.args.keys():
            if column not in self.get_columns():
                self.add_column(column=column)

    def rename(self, prefix=None):
        table_bak = "bak"
        re_name = "ALTER TABLE labels RENAME TO {};".format(table_bak)
        self.con.execute(re_name)

        self.PREFIX = prefix  # Rename column
        self.__init_db()

        sql = "INSERT INTO labels SELECT * FROM bak;"
        self.con.execute(sql)

        self.__delete_db(table_name=table_bak)

        self.con.commit()

    def add_column(self, column=None):

        if column:
            self.con.execute("ALTER TABLE labels ADD COLUMN {} varchar;".format(column))
            self.con.commit()

    def get_columns(self):
        columns = self.con.execute("PRAGMA table_info([labels]);").fetchall()
        all_columns = [c[1] for c in columns]
        return all_columns

    def delete_column(self, column=None):
        if column:
            self.con.execute("ALTER TABLE labels DROP COLUMN {};".format(column))
            self.con.commit()

    def insert(self, *args):
        """
        If len(args) > 1:
            Only pass the device SN
        otherwise:
            Pass device SN & commands.
        :param args:
        :return:
        """
        current_time = str(datetime.datetime.now()).split(".")[0]
        right_time = adjust_time(current_time, 0)
        insert_sql = "insert into labels(_date, MSN) values('{}', '{}')".format(right_time, args[0]) # Build the sql command.
        if self.is_exist(args[0]):
            return
        try:
            self.cursor.execute(insert_sql)
            self.con.commit()
        except sqlite3.IntegrityError as ex:
            output(message="{} not unique, Raise error: {}".format(args[0], ex), level=logging.ERROR)
            self.con.rollback()
            return

    def select(self, **expr):
        select_sql = "select * from {}".format(expr.get("table_name", "labels"))
        if expr.get("MSN", None):
            select_sql += " where MSN = '{}'".format(expr.get("MSN"))

        self.cursor.execute(select_sql)

    def delete(self, sn=None, all_=False):
        delete_sql = "delete from labels where MSN='{}'".format(sn)
        if all_:
            delete_sql = "delete from labels;"
        self.cursor.execute(delete_sql)
        self.con.commit()

    def update(self, sn=None):
        update_sql = "update labels set %s='%s' WHERE MSN='%s';"
        for key, value in self.args.items():
            command = update_sql % (key, value, sn)
            self.cursor.execute(command)

        self.con.commit()

    @property
    def datas(self):
        return self.cursor

    def is_exist(self, sn):
        for data in self.datas:
            if sn == data[1]:
                return True
        return False

    def close(self):
        self.cursor.close()
        self.con.close()


if __name__ == '__main__':
    cur = DBConnector()
    # cur.insert("80AD012036131BDC31")
    # cur.insert("80AD012036131BDC33")
    # cur.insert("80AD012036131BDC34")
    # cur.insert("80AD012036131BDC35")
    # cur.insert("80AD012036131BDC36")
    # cur.insert("666")
    # cur.insert("222")
    # cur.insert("333")
    # cur.insert("444")
    # cur.insert("555")
    # cur.insert("111")
    # cur.select()
    # for d in cur.datas:
    #     print(d)
    cur.rename(prefix="SN")