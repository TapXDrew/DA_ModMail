import os
import sqlite3

DATABASE = os.getcwd()+'/databases/commandInfo.db'
TABLE = 'Commands'


def index_replace(text, index=0, replacement=''):
    return '%s%s%s' % (text[:index], replacement, text[index + 1:])


class Command:
    def __init__(self, bot):
        self.bot = bot

        self.conn = None

        try:
            self.conn = sqlite3.connect(DATABASE)
        except sqlite3.Error as e:
            print(e)
        self.cursor = self.conn.cursor()

        self._create_table()
        self._create_commandTable()
        self._get_custom_info()

    def close(self):
        self.conn.close()
        del self

    def _create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE} (commands TEXT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def _create_commandTable(self):
        try:
            query = f"""INSERT INTO {TABLE} VALUES (?)"""
            self.cursor.execute(query, ("",))
            self.conn.commit()
        except sqlite3.Error:
            pass

    def _get_custom_info(self):
        query = f"SELECT * FROM {TABLE}"
        self.cursor.execute(query)
        info = self.cursor.fetchall()
        if info:
            self.raw_commands = info[0][0]
            self.commands = {}

            for command in self.raw_commands.split("|"):
                try:
                    name, response = command.split(":")
                    self.commands[name] = response
                except ValueError:
                    continue

        else:
            self._create_commandTable()
            self._get_custom_info()

    def add_command(self, command, response):
        query = f"UPDATE {TABLE} SET commands = ?"
        total_comms = ""
        self.commands[command] = response
        for index, list_items in enumerate(list(self.commands.items())):
            command, response = list_items
            if index == 0:
                total_comms += f"{command}:{response}"
            else:
                total_comms += f"|{command}:{response}"

        self.cursor.execute(query, (total_comms,))
        self.conn.commit()
        self._get_custom_info()
        return True

    def remove_command(self, removing):
        query = f"UPDATE {TABLE} SET commands = ?"
        total_comms = ""
        del self.commands[removing]
        for index, list_items in enumerate(list(self.commands.items())):
            command, response = list_items
            if index == 0:
                total_comms += f"{command}:{response}"
            else:
                total_comms += f"|{command}:{response}"

        self.cursor.execute(query, (total_comms,))
        self.conn.commit()
        self._get_custom_info()
        return True
