from DBOperations import DB


class Worker:
    """
    This class holds all the information related to a worker.
    """

    TYPE = "Worker"

    def __init__(self, name, surname, username):
        self.NAME = name
        self.SURNAME = surname
        self.USERNAME = username
        self.jobsInserted = None
        self.jobsAvailable = None

        # download needed data from DB
        self.setData()

    def getName(self):
        """
        Return surname of the worker.
        :return worker's surname
        """
        return self.SURNAME

    def getType(self):
        """
        Return user type.
        :return user type
        """
        return self.TYPE

    def getUsername(self):
        """
        Return username of the worker.
        :return worker's username
        """
        return self.USERNAME

    def setData(self):
        """
        Query the database to get all the jobs done by the current user and all available jobs.
        """
        db_connection = DB()
        query = f"SELECT Data, Cliente, Commessa, TipoCommessa, Ore FROM storico_commesse WHERE CognomeLavoratore = '{self.SURNAME}' ORDER BY Data, Cliente, Commessa, TipoCommessa"
        insertedJobs = db_connection.read(query)
        query = "SELECT Cliente, Nome, Tipo, Descrizione FROM commesse ORDER BY Cliente, Nome, Tipo"
        jobsAvailable = db_connection.read(query)
        db_connection.closeConnection()

        # convert the date column and hour column to string
        for item in insertedJobs:
            item["Data"] = str(item["Data"])
            item["Ore"] = str(item["Ore"])

        # [Data, Commessa, TipoCommessa, Ore, Cliente]
        self.jobsInserted = [[d[key] for key in d] for d in insertedJobs]
        # [Cliente, Nome, Tipo, Descrizione]
        self.jobsAvailable = jobsAvailable

    def getData(self):
        """
        Return all the jobs done by the current user and all available jobs.
        :returns: List of lists = [[Data, Cliente, Commessa, TipoCommessa, Ore], [row2], ...]
                and
                List of lists = [[Cliente, Nome, Tipo, Descrizione], [row2], ...]
        """
        return self.jobsInserted, self.jobsAvailable


class Manager:
    """
    This class holds all the information related to a manager.
    """

    TYPE = "Manager"

    def __init__(self, name, surname, username):
        self.NAME = name
        self.SURNAME = surname
        self.USERNAME = username
        self.setData()
        self.setCostiOrari()

    def getName(self):
        """
        Return surname of the worker.
        :return worker's surname
        """
        return self.SURNAME

    def getType(self):
        """
        Return user type.
        :return user type
        """
        return self.TYPE

    def setData(self):
        """
        Query the database to get all the jobs done by workers and all available jobs.
        """
        query = "SELECT Cliente, Nome, Tipo, Descrizione, Budget FROM commesse ORDER BY LOWER(Cliente), Nome, Tipo"
        db_connection = DB()
        answerJobs = db_connection.read(query)

        query = "SELECT CognomeLavoratore, Data, Anno, Mese, Ore, Commessa, TipoCommessa, CostoOrario FROM storico_commesse, users WHERE Cognome = CognomeLavoratore ORDER BY CognomeLavoratore, Data"
        answerHistory = db_connection.read(query)
        db_connection.closeConnection()

        for item in answerHistory:
            item["Data"] = str(item["Data"])

        self.jobs_to_display = answerJobs
        self.history = answerHistory

    def getData(self):
        """
        Return all the jobs done by workers and all available jobs.
        :returns: list of lists = [[Cliente, Nome, Tipo, Descrizione, Budget], [user2], ...]
                  and
                  list of lists = [[CognomeLavoratore, Data, Anno, Mese, Ore, Commessa, TipoCommessa, CostoOrario], [user2], ...]
        """
        return self.jobs_to_display, self.history

    def setCostiOrari(self):
        """
            Query the database to get the information about workers and their hour pay.
        """

        query = "SELECT Cognome, CostoOrario FROM users WHERE Ruolo = 'Progettista' ORDER BY Cognome"
        db_connection = DB()
        answer = db_connection.read(query)
        db_connection.closeConnection()

        workerCosts = {}

        for row in answer:
            workerCosts[row['Cognome']] = row['CostoOrario']

        self.workerCosts = workerCosts

    def getWorkerCosts(self):
        """
            Return information about workers and their hour pay.
            :return: list of lists = [[Cognome, CostoOrario], [row2], ...]
        """
        return self.workerCosts


class Admin:
    """
    This class holds all the information related to a admin.
    """
    TYPE = "Admin"

    def __init__(self):
        self.NAME = "Admin"
        self.SURNAME = "Admin"
        self.USERNAME = "Admin"
        self.setData()

    def getName(self):
        """
        Return surname of the worker.
        :return worker's surname
        """
        return self.SURNAME

    def getType(self):
        """
        Return user type.
        :return user type
        """
        return self.TYPE

    def setData(self):
        """
        Query the database to get the information related to users.
        """
        db_connection = DB()
        query = "SELECT Cognome, Nome, Username, Password, CostoOrario, Ruolo FROM users ORDER BY Cognome"
        answer = db_connection.read(query)
        db_connection.closeConnection()

        self.user_data = [[d[key] for key in d] for d in answer]

    def getData(self):
        """
        Query the database to get the information related to users.
        :return: list of lists = [[Cognome, Nome, Username, Password, CostoOrario, Ruolo], [user2], ...]
        """
        return self.user_data
