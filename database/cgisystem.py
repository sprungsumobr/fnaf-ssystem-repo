# coding = utf-8
# using namespace std
import cgi
from typing import Type
from database import databasesystem
import cgitb
from database import email_trat


cgitb.enable(display=0)

agent = cgi.FieldStorage()


class EmailAddition:
    values = {}
    var_names = tuple()
    emails_agent = agent

    def __get_all_data__(self):
        for i in self.var_names:
            value = self.emails_agent.getvalue(i)
            self.values[i] = value


































