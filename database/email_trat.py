# coding = utf-8
# using namespace std
import email
import smtplib


class JsonFileTrat:
    import json

    class EmptyFileError(Exception):
        args = "Um arquivo vazio nao e aceito para o sistema"

    archive = open("emails_database.json")
    docs: list = json.loads(archive)

    def __add__(self, other: dict):
        if len(other.items()) <= 0:
            return [self.EmptyFileError.args, self.EmptyFileError]
        for i, l in other.items():
            if i not in ("Email", "Tratament", "ID", "Date", "Hour", "Error"):
                return ["Esse campo nao esta disponivel", IndexError]
            if l is not str:
                raise TypeError()
        self.docs.append(other)

    def errors_checking(self ,other: dict):
        if len(other.items()) <= 0:
            return True
        for i, l in other.items():
            if i not in ("Email", "Tratament", "ID", "Date", "Hour", "Error"):
                return True
            if l is not str:
                return True
        return False

    def __delete__(self, index: int):
        if index > len(self.docs):
            return [IndexError.args, IndexError]
        del self.docs[index]




















