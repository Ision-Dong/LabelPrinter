import datetime
import logging
import os
import sqlite3

from utils.date import adjust_time
from utils.log import output


class DBConnector:

    """
    #   通过原生sql语句，来操作数据库。
    #   提供了 增删改查 的功能
    """

    PREFIX = "CMD"   # 已弃用

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
            "create table if not exists labels(_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, IS_UPLOAD BOOLEAN DEFAULT 0, MODEL_CODE varchar, MSN varchar unique)"
        )
        for column in self.args.keys():
            if column not in self.get_columns():
                self.add_column(column=column)

    def rename(self, prefix=None):
        """
        由于app 需求变化，该功能以弃用，该功能能重新命名字段名
        操作步骤：
          1.备份表
          2.新建新表，用新的字段名
          3.从旧表中拿到数据
          4.把数据写到新表中
          5.删除旧表
        :param prefix:
        :return:
        """
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
        """
        app中涉及到字段长度变化， 通过该方法来完成
        :param column:
        :return:
        """
        if column:
            self.con.execute("ALTER TABLE labels ADD COLUMN {} varchar;".format(column))
            self.con.commit()

    def get_columns(self, skip=None):
        """
        #   获取数据库中所有字段名
        :param skip: 如果这个不为空， 查询的数据中跳过对应的字段，目前仅涉及到的字段为: IS_UPLOAD
        :return:
        """
        columns = self.con.execute("PRAGMA table_info([labels]);").fetchall()
        all_columns = [c[1] for c in columns]
        if skip is not None:
            all_columns.pop(all_columns.index(skip))
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
        :param args: device SN or more
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
        columns = self.get_columns()
        columns.pop(columns.index(expr.get("skip", "IS_UPLOAD")))  # IS_UPLOAD 这个字段不需要在页面中展示出来，所以在这里从字段列表中删除
        select_sql = "select {} from {}".format(",".join(columns), expr.get("table_name", "labels"))
        if expr.get("MSN", None):
            select_sql += " where MSN = '{}'".format(expr.get("MSN"))

        self.cursor.execute(select_sql)

    def delete(self, sn=None, all_=False):
        delete_sql = "delete from labels where MSN='{}'".format(sn)
        if all_:
            delete_sql = "delete from labels;"
        self.cursor.execute(delete_sql)
        self.con.commit()

    def update(self, sn=None, column=None, column_value=None):
        update_sql = "update labels set %s='%s' WHERE MSN='%s';"

        if column is not None:
            command = update_sql % (column, column_value, sn)
            self.cursor.execute(command)
            self.con.commit()
            return

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

    def is_upload(self, sn=None):
        """
        #   从main windows中用户的选择对应的行中，拿到sn，来查数据库。并返回true 或者false
        #   IS_UPLOAD 这个字段标记对应行的数据是否传送到服务器中。
        :param sn:
        :return:
        """
        is_upload_sql = "select IS_UPLOAD from labels where MSN='%s'" % sn
        upload = self.cursor.execute(is_upload_sql).fetchone()
        self.con.commit()
        if upload[0] == 1:
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