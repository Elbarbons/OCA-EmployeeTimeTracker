from tkinter import messagebox
import logging
import os


class ErrorHandler:
    """
    This class manage errors in a personalized way by rendering error's messages on the application.
    """

    textError = "Errore !"

    def __init__(self, exception):
        self.exception = exception

        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")

        logging.basicConfig(filename='./tmp/LOGS.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logger = logging.getLogger(__name__)
        logger.error(exception)

    def manageError(self, identification):
        """
        Set the error's message based on the input.
        :param identification: string that define the type of error.
                                Possible strings: connection_error, operational_error, generic string for default msg.
        """
        match identification:
            case "connection_error":
                self.textError = "Impossibile connettersi al Database. Controllare connessione VPN !"

            case "operational_error":
                self.textError = "Impossibile eseguire l'operazione !"

            case _:
                self.textError = "Errore !"

        return self

    def showError(self):
        """
        Render the error's message on screen.
        """
        messagebox.showerror("Errore", self.textError)