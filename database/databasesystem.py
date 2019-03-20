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

    @classmethod
    def game_exists(cls, name: str):
        cls.cursor.execute("SELECT ID FROM Games WHERE Game = ?;", [name])
        if len(cls.cursor.fetchall()) <= 0:
            return False
        else:
            return True

    @classmethod
    def game_page_exists(cls, page: str):
        from os import chdir
        chdir("../Games/Pages")
        try:
            n = open(page)
            del n
        except FileNotFoundError:
            chdir("..")
            chdir("../database")
            return False
        chdir("..")
        chdir("../database")
        return True

    @classmethod
    def game_media_exists(cls, media):
        if media is str and "/" in media:
            n = "/".split(media)
        elif media is list or tuple or iter:
            n = media
        else:
            raise TypeError
        from os import chdir
        chdir("../Games/Media")
        for i in n:
            try:
                s = open(i)
                del s
            except FileNotFoundError:
                chdir("..")
                chdir("../database")
                return False
        chdir("..")
        chdir("../database")
        return True

    @classmethod
    def game_id_exists(cls, id: int):
        cls.cursor.execute("SELECT * FROM Games WHERE ID = ?;", [id])
        return len(cls.cursor.fetchall()) > 0

    @classmethod
    def other_id_exists(cls, id: int):
        cls.cursor.execute("SELECT ID FROM Others WHERE ID = ?;", [id])
        if len(cls.cursor.fetchone()) <= 0:
            return False
        return True

    @classmethod
    def other_page_exists(cls, page: str):
        from os import chdir
        chdir("../../others/pages")
        try:
            n = open(page, "r")
            del n
        except FileNotFoundError:
            chdir("../../database")
            return False
        chdir("../../database")
        return True

    @classmethod
    def other_media_exists(cls, media):
        from os import chdir
        chdir("../../others/media")
        if media is any([list, tuple, iter]):
            for i in media:
                try:
                    n = open(i)
                    del n
                except FileNotFoundError:
                    chdir("../../database")
                    return False
        else:
            try:
                n = open(media, "r")
                del n
            except FileNotFoundError:
                return False
        return True

    @classmethod
    def other_exists(cls, name: str):
        cls.cursor.execute("SELECT Name FROM Others WHERE Name = ?;", [name])
        if len(cls.cursor.fetchall()[0]) <= 0:
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
        value = "SELECT {} FROM Animatronics WHERE {} = {};"
        if pre_value or param is None:
            value = "SELECT {} FROM Games;"
            if camp == "*" or camp is None:
                value = "SELECT * FROM Animatronics;"
                self.cursor.execute(value)
                return self.cursor.fetchall()
            else:
                self.cursor.execute(value.format(camp))
                return self.cursor.fetchall()
        if camp == "*" or camp is None:
            value = "SELECT * FROM Animatronics WHERE {} = {}"
            if pre_value is None or param is None:
                value = "SELECT * FROM Animatronics;"
                self.cursor.execute(value)
                return self.cursor.fetchall()
            else:
                self.cursor.execute(value.format(param, pre_value))
                return self.cursor.fetchall()
        self.cursor.execute(value.format(camp, param, pre_value))
        return self.cursor.fetchall()


class Games(SystemDatabase):

    class GameNotFound(Exception):
        args = "This game does not exists in the database"
        pass

    class GameExists(Exception):
        args = "This game's already in the database"
        pass

    class GamePageNotExists(Exception):
        args = "This html page does not exist"
        pass

    class GameMediaNotExists(Exception):
        args = "This media does not exists"
        pass

    def __add__(self, other: list):
        """

        :param other: [Name, Page, Media]
        :return:
        """
        if self.game_exists(other[0]):
            return [self.GameExists.args, self.GameExists]
        if not self.game_page_exists(other[1]):
            return [self.GamePageNotExists.args, self.GamePageNotExists]
        if not self.game_media_exists(other[2]):
            return [self.GameMediaNotExists.args, self.GameMediaNotExists]
        try:
            self.cursor.execute("INSERT INTO Games (Name, Page, Media) VALUES (?,?,?);", other)
        except Exception as error:
            return [error.args, error]
        self.con.commit()
        return ["Done"]

    def __delete_info__(self, id: int):
        if not self.game_id_exists(id):
            return [self.GameNotFound.args, self.GameNotFound]
        else:
            try:
                self.cursor.execute("DELETE FROM Games WHERE ID = ?;", [id])
            except Exception as error:
                return [error.args, error]
            self.con.commit()
            return ["Done!"]

    def __alt_data__(self, camp, new_value, id: int):
        if not self.game_id_exists(id):
            return [self.GameNotFound.args, self.GameNotFound]
        try:
            self.cursor.execute("UPDATE FROM Games SET {} = {} WHERE ID = {};".format(camp, new_value, id))
        except Exception as error:
            return [error.args, error]
        return ["Done!"]


class GetGamesInfo(Games):

    class SyntaxSystemError(Exception):
        args = "This way to type the camp param is wrong"
        pass

    def __search_all__(self, camp, pre_value, param):
        value = "SELECT {} FROM Games WHERE {} = {};"
        if pre_value or param is None :
            value = "SELECT {} FROM Games;"
            if camp == "*" or camp is None:
                value = "SELECT * FROM Games;"
                self.cursor.execute(value)
                return self.cursor.fetchall()
            else:
                self.cursor.execute(value.format(camp))
                return self.cursor.fetchall()
        if camp == "*" or camp is None:
            value = "SELECT * FROM Games WHERE {} = {}"
            if pre_value is None or param is None:
                value = "SELECT * FROM Games;"
                self.cursor.execute(value)
                return self.cursor.fetchall()
            else:
                self.cursor.execute(value.format(param, pre_value))
                return self.cursor.fetchall()
        self.cursor.execute(value.format(camp, param, pre_value))
        return self.cursor.fetchall()


class Others(SystemDatabase):

    class OtherExists(Exception):
        args = "This value always exists"

    class OtherNotFound(Exception):
        args = "This reference does not exists"




    def __add_info__(self, data: list):
        """

        :param data: [Name, GamesAppear,
        :return:
        """
        if not self.other_exists(data[0]):
            return [self.OtherNotFound.args, self.OtherNotFound]
























