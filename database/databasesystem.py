# coding = utf-8
# using namespace std
import sqlite3
from typing import Type


class SystemDatabase:
    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    def __init__(self, file="database.db"):
        self.con = sqlite3.connect(file)
        self.cursor = self.con.cursor()

    def __delete__(self):
        del self.cursor
        del self.con

    @classmethod
    def __new__(cls, class_using):
        class_using = cls
        return class_using

    @classmethod
    def page_exists(cls, page):
        try:
            n = open(page)
            del n
        except FileNotFoundError:
            return False
        return True

    @classmethod
    def media_exists(cls, media_list: list):
        from os import chdir
        chdir("../Animatronics/media")
        for i in media_list:
            try:
                n = open(i)
                del n
            except FileNotFoundError:
                return False
        return True

    @classmethod
    def animatronic_exists(cls, name: str):
        cls.cursor.execute("SELECT Name FROM Animatronics WHERE Name = ?;", [name])
        if len(cls.cursor.fetchall()) == 0:
            return False
        else:
            return True

    @classmethod
    def page_animatronic_exists(cls, page: str):
        from os import chdir
        chdir("../Animatronics/Pages")
        try:
            n = open(page)
            del n
        except FileNotFoundError:
            return False
        return True

    @classmethod
    def id_exists(cls, id: int, table: str):
        cls.cursor.execute("SELECT * FROM {} WHERE ID = {};".format(table, str(id)))
        if len(cls.cursor.fetchall()) <= 0:
            return False
        else:
            return True


class AnimatronicsData(SystemDatabase):

    class AnimatronicExists(Exception):
        args = "This animatronic already exists"
        pass

    class AnimatronicNotExists(Exception):
        args = "This animatronic not exists"
        pass

    def addinfos(self, info_list):
        """
        Add information about the animatronics
        :param info_list: [name, games, page, gender, media]
        :return: None
        """
        if info_list[3] is bool:
            n = info_list[3]
            info_list[3] = int(n)
            del n
        elif not self.page_exists(info_list[2]) or not self.page_animatronic_exists(info_list[2]):
            return ["This page '"+info_list[2]+"' not exists", FileNotFoundError]
        elif info_list[4] is list or tuple or iter:
            if not self.media_exists(info_list):
                return ["Those medias does not exists!", FileNotFoundError]
        elif info_list[4] is str:
            if not self.media_exists([i for i in "/".split(info_list)]):
                return ["Those medias does not exists!", FileNotFoundError]
        elif not self.animatronic_exists(info_list[0]):
            return ["This animatronic already exists!", self.AnimatronicExists]
        else:
            if info_list[4] is list or iter or tuple:
                n = info_list[4]
                info_list[4] = "/".join(n)
                del n
            if info_list[1] is list or tuple or iter:
                n = info_list[1]
                info_list[1] = "/".join(n)
                del n
            self.cursor.execute("INSERT INTO Animatronics (Name, Games, Page, Gender, Media) VALUES(?,?,?,?,?);",
                                info_list)
            self.con.commit()
            return ["Done"]

    def __delete_info__(self, id: int):
        if not self.id_exists(id, "Animatronics"):
            return [self.AnimatronicNotExists.args, self.AnimatronicNotExists]
        else:
            self.cursor.execute("DELETE FROM Animatronics WHERE ID = ?;", [id])
            self.con.commit()

    def __alt_info__(self, id: int, camp, new_value):
        if not self.id_exists(id, "Animatronics"):
            return [self.AnimatronicNotExists.args, self.AnimatronicNotExists]
        else:
            self.cursor.execute("UPDATE FROM Animatronics SET {} = {} WHERE ID = {};".format(camp, new_value, id))
            self.con.commit()

    @classmethod
    def get_animatronic_reference(cls, camp: str, value, nedd):
        cls.cursor.execute("SELECT {} FROM Animatronics WHERE {} = {};".format(nedd, camp, value))
        return cls.cursor.fetchall()


class GetAnimatronicInfo(AnimatronicsData):

    def _search_at_all(self, camp, pre_value, param):
        val = "SELECT {} FROM Animatronics WHERE {} = {};"
        if pre_value is None and param is None:
            val = "SELECT {} FROM Animatronics;"
        if camp == "*":
            val = "SELECT * FROM Animatronics"
        self.cursor.execute(val.format(camp, param, pre_value))
        return self.cursor.fetchall()














