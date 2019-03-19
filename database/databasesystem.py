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


class AnimatronicsData(SystemDatabase):

    class AnimatronicExists(Exception):
        args = "This animatronic already exists"
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
        elif not self.page_exists(info_list[2]):
            return ["This page '"+info_list[2]+"' not exists", FileNotFoundError]
        elif info_list[4] is list or tuple or iter:
            if not self.media_exists(info_list):
                return ["Those medias does not exists!", FileNotFoundError]
        elif info_list[4] is str:
            if not self.media_exists([i for i in "/".split(info_list)]):
                return ["Those medias does not exists!", FileNotFoundError]
        elif not self.animatronic_exists(info_list[0]):
            return ["This animatronic already exists!", self.AnimatronicExists]







