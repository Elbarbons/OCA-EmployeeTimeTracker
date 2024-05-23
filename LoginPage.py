import tkinter as tk
from tkinter import ttk, messagebox
from DBOperations import DB
from Util import clear_window
from Users import Worker, Manager, Admin
from Worker import WorkerGUI
from Admin import AdminGUI
from Manager import ManagerGUI


class Login:
    """
    This class renders the login page and manage the login phase by confronting username and password inserted and
    usernames and password saved in the database. After the login is correctly performed redirects to the right
    application's window based on the user's role.
    """

    USER = None

    def __init__(self, window):
        """
        Set login window's properties and call the login_page method to render the page.
        :param window: a ttk window instance
        """
        self.window = window
        # Setting properties of the window
        self.window.option_add("*Font", "aerial")

        # Setting application icon
        self.window.iconbitmap('./Images/Goose.ico')

        # setting window's properties
        self.window.resizable(False, False)



    def loginPage(self):
        """
        Renders all the element needed for the login page.
        """
        self.window.title("Login")

        # defining frame needed
        username_frame = ttk.Frame(self.window)
        password_frame = ttk.Frame(self.window)
        username_frame.pack(side=tk.TOP, anchor=tk.N, padx=5, pady=5)
        password_frame.pack(side=tk.TOP, anchor=tk.N, padx=5, pady=5)

        # defining all the widged needed: username and password label and entry widgets
        fields = {'username_label': ttk.Label(username_frame, text='Username:', width=10, font=('aerial', 14)),
                  'password_label': ttk.Label(password_frame, text='Password:', width=10, font=('aerial', 14)),
                  'username': ttk.Entry(username_frame, font=('aerial', 14)),
                  'password': ttk.Entry(password_frame, font=('aerial', 14), show="*")}

        # programming the username and password entry widgets to call the manage_login method also when user press enter
        fields['username'].bind('<Return>',
                                lambda event: self.manageLogin(fields['username'].get(), fields['password'].get()),
                                add='+')
        fields['password'].bind('<Return>',
                                lambda event: self.manageLogin(fields['username'].get(), fields['password'].get()),
                                add='+')

        # renders all the elements in the login window
        for field in fields.values():
            field.pack(side=tk.LEFT, anchor=tk.E, padx=10, pady=5, fill=tk.X)

        # insert login button
        login_button = ttk.Button(self.window, text='LOGIN', style="Bold.TButton",
                                  command=lambda: self.manageLogin(fields['username'].get(), fields['password'].get()))

        login_button.pack(side=tk.TOP, anchor=tk.N, padx=10, pady=5)

    def manageLogin(self, username: str, password: str):
        """
        Get as inputs the password and username inserted by the user and checks, first if they are both fill out,
        and then if they match with an existing account stored in the database.
        If the data inserted match with an existing account the method saves some personal information about the user
        and redirects him on the correct page based on his role.
        :param username: username inserted by the user
        :param password: password inserted by the user
        """
        # checks if both username and password are empty, if so displays an error
        if not username or not password:
            tk.messagebox.showerror("Errore", "Compilare tutti i campi")

        else:
            # establish connection to the DB and submit the query to extract data about the username inserted
            db_connection = DB()
            query = f"SELECT Username, Password, Ruolo, Nome, Cognome, firstLogin FROM users WHERE Username = '{username}'"
            answer = db_connection.read(query)
            db_connection.closeConnection()

            # checks if account with that username exists and if the password held in DB matches the password inserted
            if len(answer) != 0 and password == answer[0]['Password']:

                if answer[0]['firstLogin'] == 1:
                    self.setPasswordFirstLogin()

                # saves user's information
                match answer[0]['Ruolo']:
                    case 'Progettista':
                        self.USER = Worker(answer[0]['Nome'], answer[0]['Cognome'], answer[0]['Username'])
                        WorkerGUI(self.window, self.USER).workerPage()
                    case 'Admin':
                        self.USER = Admin()
                        AdminGUI(self.window, self.USER).adminPage()
                    case 'Responsabile':
                        self.USER = Manager(answer[0]['Nome'], answer[0]['Cognome'], answer[0]['Username'])
                        ManagerGUI(self.window, self.USER).managerMenu()
                    case _:
                        tk.messagebox.showerror("Error", "Utente non correttamente censito")

            # if username and/or password are wrong, throws an error
            else:
                tk.messagebox.showerror("Error", "Username e/o password sbagliata !")

    def setPasswordFirstLogin(self):
        """
        Render the page to change the password on first login.
        """
        clear_window(self.window)
        self.window.title("Impostare password")

        # defining frame needed
        label_frame = ttk.Frame(self.window)
        label_frame.pack(side=tk.TOP, anchor=tk.N, padx=5, pady=5)
        description_frame = ttk.Frame(self.window)
        description_frame.pack(side=tk.TOP, anchor=tk.N, padx=5, pady=5)
        password_frame = ttk.Frame(self.window)
        password_frame.pack(side=tk.TOP, anchor=tk.N, padx=5, pady=5)

        # defining all the widgets needed
        fields = {'label': ttk.Label(label_frame, text='Imposta una nuova password', font=('aerial', 18)),
                  'description': ttk.Label(description_frame, text='Inserisci una password di almeno 6 caratteri che non contenga i seguenti caratteri (\'   "   \\   ;   %   #   &)', font=('aerial', 14)),
                  'password_label': ttk.Label(password_frame, text='Password:', width=10, font=('aerial', 14)),
                  'password': ttk.Entry(password_frame, font=('aerial', 14))}

        # programming the password entry widgets to call the change_password method also when user press enter
        fields['password'].bind('<Return>',
                                lambda event: self.changePassword(fields['password'].get()),
                                add='+')

        # renders all the elements in the window
        for field in fields.values():
            field.pack(side=tk.LEFT, anchor=tk.E, padx=10, pady=5, fill=tk.X)

        # insert enter button
        login_button = ttk.Button(self.window, text='CAMBIA', style="Bold.TButton",
                                  command=lambda: self.changePassword(fields['password'].get()))
        login_button.pack(side=tk.TOP, anchor=tk.N, padx=10, pady=5)

    def changePassword(self, new_password):
        """
        Get as inputs the new password and change the old password in the DB with the new one. Then redirects
        to the correct page based on user's role.
        :param new_password: new password to insert into the DB
        """
        # checks the new_password has the right format
        if not new_password:
            tk.messagebox.showerror("Errore", "Compilare il campo password !")

        elif len(new_password) < 6:
            tk.messagebox.showerror("Errore", "Password troppo corta !")

        elif any((c in ["'", '"', "\\", ';', '%', '#', '&']) for c in new_password):
            tk.messagebox.showerror("Errore", "Caratteri inseriti nella password non ammessi !")

        else:
            # establish connection to the DB and submit the query
            db_connection = DB()
            query = f"UPDATE oca.users SET Password = '{new_password}', firstLogin = 0 WHERE Username = '{self.USER['USERNAME']}'"
            db_connection.alter(query)
            db_connection.closeConnection()

    # Used to bypass the login phase to debug following parts of the application faster
    # def fakeLogin(self, who):
    #     match who:
    #         case "worker":
    #             self.manageLogin('', '') # <- Insert Username and password of a worker
    #         case "admin":
    #             self.manageLogin('', '') # <- Insert Username and password of a admin
    #         case "manager":
    #             self.manageLogin('', '') # <- Insert Username and password of a manager
