import pymysql
from ErrorHandler import ErrorHandler


class DB:
    """
    This class is used to connect to database and perform operations: read, insert, delete, alter.
    """

    # Fill this part
    HOST = ""
    USER = ""
    PASSWORD = ""
    DB = ""

    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host=self.HOST,
                user=self.USER,
                password=self.PASSWORD,
                db=self.DB,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as inst:
            ErrorHandler(inst).manageError("connection_error").showError()

    def read(self, query):
        """
        Execute the query to read some information from db.
        :param query: query to execute.
        :return answer from the DB. [[row1], [row2], ...]
        """
        try:
            with self.conn.cursor() as cursor:
                # Read data from database
                cursor.execute(query)
        except Exception as inst:
            ErrorHandler(inst).manageError("operational_error").showError()

        return self.parse_answer(cursor)

    def insert(self, query):
        """
        Execute the query to insert some data into a table.
        :param query: query to execute.
        """
        try:
            with self.conn.cursor() as cursor:
                # Insert data into database
                cursor.execute(query)
            self.conn.commit()

        except Exception as inst:
            ErrorHandler(inst).manageError("operational_error").showError()

    def alter(self, query):
        """
        Execute the query to update some data from a table.
        :param query: query to execute.
        """
        try:
            with self.conn.cursor() as cursor:
                # Alter data from database
                cursor.execute(query)
            self.conn.commit()

        except Exception as inst:
            ErrorHandler(inst).manageError("operational_error").showError()

    def delete(self, query):
        """
        Execute the query to delete some data from a table.
        :param query: query to execute.
        """
        try:
            with self.conn.cursor() as cursor:
                # Delete data from database
                cursor.execute(query)
            self.conn.commit()

        except Exception as inst:
            ErrorHandler(inst).manageError("operational_error").showError()

    def closeConnection(self):
        """
        Close the connection with the DB.
        """
        try:
            self.conn.close()
        except Exception as inst:
            ErrorHandler(inst).manageError("connection_error").showError()

    @staticmethod
    def parse_answer(cursor):
        """
        This method transforms the answer from DB from a list of dictionaries to a list of lists.
        :param cursor: DB answer to transform.
        """
        parsed_answer = []
        for row in cursor:
            parsed_answer.append(row)
        return parsed_answer
