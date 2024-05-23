import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from DBOperations import DB
from Util import clear_window, MyTreeview


class AdminGUI:
    """
    This class manages and renders the application page related to admins.
    """
    def __init__(self, window, user):
        """
        Sets admin window's properties and calls the worker_frame method to render the page.
        :param window:  a ttk window instance
        :param user: instance of user class.
        """
        self.window = window
        self.USER = user
        self.window.title("Admin")

        # clean all widgets from previous page and call method to render the admin page
        clear_window(self.window)

    def adminPage(self):
        """
        This method creates and renders all the widgets needed in the admin's page, in particular: a row to insert new
        users, a tree view to render a table and a delete button to delete selected rows.
        :return: None
        """
        # get data to display
        columns = ['Cognome', 'Nome', 'Username', 'Password', 'Costo Orario', 'Ruolo']
        users_to_display = self.USER.getData()

        # create needed frames
        insert_frame = ttk.Frame(self.window)
        insert_frame.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, padx=10, pady=20, expand=True)
        container = ttk.Frame(self.window)
        container.pack(side=tk.TOP, anchor="n", expand=True, fill=tk.BOTH, padx=40)
        button_container = ttk.Frame(self.window)
        button_container.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, padx=10, pady=20, expand=True)

        # dictionary of needed widgets for the insert-row part
        insert_fields = {'username_label': ttk.Label(insert_frame, text="Username:", font=('aerial', 14)),
                         'username': ttk.Entry(insert_frame, font=('aerial', 14), width=15),
                         'password_label': ttk.Label(insert_frame, text="Password:", font=('aerial', 14)),
                         'password': ttk.Entry(insert_frame, font=('aerial', 14), width=15),
                         'cognome_label': ttk.Label(insert_frame, text="Cognome:", font=('aerial', 14)),
                         'cognome': ttk.Entry(insert_frame, font=('aerial', 14), width=10),
                         'nome_label': ttk.Label(insert_frame, text="Nome:", font=('aerial', 14)),
                         'nome': ttk.Entry(insert_frame, font=('aerial', 14), width=10),
                         'costo_orario_label': ttk.Label(insert_frame, text="Costo Orario:", font=('aerial', 14)),
                         'costo_orario': ttk.Entry(insert_frame, font=('aerial', 14), width=4),
                         'role_label': ttk.Label(insert_frame, text="Ruolo:", font=('aerial', 14)),
                         'role_combobox': ttk.Combobox(insert_frame, values=['Progettista', 'Admin', 'Responsabile'],
                                                       state="readonly", font=('aerial', 14), width=10),
                         'insert_button': ttk.Button(insert_frame, text="INSERISCI", style="Bold.TButton")}

        insert_fields['insert_button']['command'] = lambda: self.insertUser(insert_fields['username'].get(),
                                                                             insert_fields['password'].get(),
                                                                             insert_fields['cognome'].get(),
                                                                             insert_fields['nome'].get(),
                                                                             insert_fields['costo_orario'].get(),
                                                                             insert_fields['role_combobox'].get(),
                                                                             table)

        # render widgets
        for field in insert_fields.values():
            field.pack(side=tk.LEFT, anchor=tk.E, padx=5, fill=tk.X, expand=True)

        # create treeview
        table = MyTreeview(container, columns=columns, show='headings', height=20)
        for column in columns:
            table.heading(column, text=column, sort_by='str')
        table.column("Costo Orario", minwidth=0, width=150, stretch=False)
        table.column("Ruolo", minwidth=0, width=100, stretch=True)

        table.tag_configure('gray', background='#f5f5f5')
        alternate = True
        for item in users_to_display:
            if alternate:
                alternate = False
                table.insert('', tk.END, values=item, tag='gray')
            else:
                alternate = True
                table.insert('', tk.END, values=item)

        # render last elements needed
        table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        table.configure(yscroll=scrollbar.set)

        ttk.Button(button_container, text="CANCELLA", style="Bold.TButton",
                   command=lambda: self.deleteUser(table)).pack(side=tk.RIGHT, anchor=tk.E, padx=80, pady=10)
        ttk.Button(button_container, text="MODIFICA", style="Bold.TButton", command=lambda: self.testProgramThread(table)
                                      ).pack(side=tk.RIGHT, anchor=tk.E, padx=80, pady=10)

    def testProgramThread(self, table):
        thread = threading.Thread(None, self.editItem(table), None, (), {})
        thread.start()

    def editItem(self, table):
        focused = table.focus()
        values = table.item(focused)['values']
        USER_INP = simpledialog.askinteger(title="MODIFICA", prompt="Inserire nuovo costo orario:")
        table.item(focused, values=(values[0], values[1], values[2], values[3], USER_INP, values[5]))

        query = f"UPDATE oca.users SET CostoOrario = {USER_INP} WHERE Cognome = '{values[0]}' AND " \
                f"Nome = '{values[1]}' AND Username = '{values[2]}' AND Password = '{values[3]}' AND Ruolo = '{values[5]}'"

        db_connection = DB()
        db_connection.alter(query)
        db_connection.closeConnection()

    @staticmethod
    def deleteUser(table):
        """
        Deletes the selected rows in the treeview from the database.
        :param table: a ttk.treeview object
        :return: None
        """
        # ask for confirm
        answer = tk.messagebox.askyesno("Confermare", "Sei sicuro di voler eliminare le righe selezionate ?")
        if answer:
            db_connection = DB()
            for selected_item in table.selection():
                item = table.item(selected_item)
                record = item['values']
                cognome = record[0]
                nome = record[1]
                username = record[2]
                password = record[3]
                paycheck = record[4]
                ruolo = record[5]

                query = f"DELETE FROM users WHERE Cognome = '{cognome}' AND Nome = '{nome}' AND Username = '{username}' AND Password = '{password}' AND Ruolo = '{ruolo}'"
                db_connection.delete(query)
                table.delete(selected_item)

            tk.messagebox.showinfo("Riga eliminata", "Riga eliminata correttamente")
            db_connection.closeConnection()

    @staticmethod
    def insertUser( username, password, surname, name, paycheck, role, table):
        """
        Insert the new user in the database table.
        :param username: username to insert
        :param password: password to insert
        :param surname: surname to insert
        :param name: name to insert
        :param paycheck: paycheck to insert
        :param role: role to insert
        :param table: treeview to manipulate
        :return:
        """
        # checks if all the needed data are not empty
        if not username or not password or not surname or not name or not paycheck or not role:
            tk.messagebox.showerror("Errore", "Compilare tutti i campi")

        else:
            db_connection = DB()
            query = f"INSERT users(Username, Password, Ruolo, Nome, Cognome, CostoOrario) VALUES ('{username}', '{password}', '{role}', '{name}', '{surname}', '{paycheck}' )"
            db_connection.insert(query)

            tk.messagebox.showinfo("Riga inserita", "Riga inserita correttamente")

            # insert row in table
            table.insert("", tk.END, values=(surname, name, username, password, paycheck, role))

            db_connection.closeConnection()
