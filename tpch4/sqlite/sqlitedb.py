import sqlite3

class SQLITEDB:
    """Class for connections to Sqlite database
    """
    __connection__ = None
    __cursor__ = None

    def __init__(self, db_name):
        # Exception handling is done by the method using this.
        self.__connection__ = sqlite3.connect(db_name)
        self.__cursor__ = self.__connection__.cursor()

    def close(self):
        if self.__cursor__ is not None:
            self.__cursor__.close()
            self.__cursor__ = None
        if self.__connection__ is not None:
            self.__connection__.close()
            self.__connection__ = None

    def executeQueryFromFile(self, filepath, function=None):
        if function is None:
            function = lambda x: x
        with open(filepath) as query_file:
            query = query_file.read()
            query = function(query)
            return self.executeQuery(query)

    def executeQuery(self, query):
        if self.__cursor__ is not None:
            self.__cursor__.executescript(query)
            return 0
        else:
            print("database has been closed")
            return 1

    def copyFrom(self, filepath, separator, table):
        if self.__cursor__ is not None:
            with open(filepath, 'r') as in_file:
                self.__cursor__.copy_from(in_file, table=table, sep=separator)
            return 0
        else:
            print("database has been closed")
            return 1

    def commit(self):
        if self.__connection__ is not None:
            self.__connection__.commit()
            return 0
        else:
            print("cursor not initialized")
            return 1
