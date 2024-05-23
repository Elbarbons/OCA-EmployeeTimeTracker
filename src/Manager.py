import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from DBOperations import DB
from Util import clear_window, MyTreeview
from datetime import date, datetime, timedelta
from tkcalendar import DateEntry


class ManagerGUI:
    """
    This class manages and renders the application page related to Managers.
    """
    def __init__(self, window, user):
        """
        Sets manager window's properties and calls the manager_menu method to render the page.
        :param window:  a ttk window instance
        :param user: instance of user class.
        """
        self.window = window
        self.USER = user
        self.window.title(f"{self.USER.getName()}")
        self.today_date = date.today()

    def managerMenu(self):
        """
        Renders manager menu, in which there are 3 buttons: one that redirects on editJobsPage, one that redirects on
        jobsStatsPage, and the third one that redirects to workersStatsPage.
        :return: None
        """
        clear_window(self.window)
        ttk.Button(self.window, text="MODIFICA COMMESSE", style="Bold.TButton", command=self.editJobsPage).pack(
            side=tk.TOP, fill=tk.BOTH, padx=20, pady=10)
        ttk.Button(self.window, text="RIEPILOGO COMMESSE", style="Bold.TButton", command=self.jobsStatsPage).pack(
            side=tk.TOP, fill=tk.BOTH, padx=20, pady=10)
        ttk.Button(self.window, text="RIEPILOGO PROGETTISTI", style="Bold.TButton", command=self.workersStatsPage).pack(
            side=tk.TOP, fill=tk.BOTH, padx=20, pady=10)

    def editJobsPage(self):
        """
        Renders the page in which managers can edit the job's registry.
        :return: None
        """
        clear_window(self.window)
        # get data to display in the page
        columns = ['Cliente', 'Nome', 'Tipo', 'Descrizione', 'Budget']
        self.jobs, _ = self.USER.getData()

        self.jobs = [[row['Cliente'], row['Nome'], row['Tipo'], row['Descrizione'], row['Budget']] for row in self.jobs]

        # creating needed frames
        insert_frame = ttk.Frame(self.window)
        insert_frame.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, padx=10, pady=20, expand=True)
        container = ttk.Frame(self.window)
        container.pack(side=tk.TOP, anchor="n", expand=True, fill=tk.BOTH, padx=40)
        button_container = ttk.Frame(self.window)
        button_container.pack(side=tk.TOP, anchor="n", expand=True, fill=tk.BOTH, padx=40)

        # creating widgets needed to insert rows in table
        insert_fields = {'cliente_label': ttk.Label(insert_frame, text="Cliente:", font=('aerial', 14)),
                         'cliente': ttk.Entry(insert_frame, font=('aerial', 14)),
                         'commessa_label': ttk.Label(insert_frame, text="Commessa:", font=('aerial', 14)),
                         'commessa': ttk.Entry(insert_frame, font=('aerial', 14)),
                         'tipo_label': ttk.Label(insert_frame, text="Tipo:", font=('aerial', 14)),
                         'tipo': ttk.Entry(insert_frame, font=('aerial', 14)),
                         'descrizione_label': ttk.Label(insert_frame, text="Descrizione:", font=('aerial', 14)),
                         'descrizione': ttk.Entry(insert_frame, font=('aerial', 14)),
                         'budget_label': ttk.Label(insert_frame, text="Budget:", font=('aerial', 14)),
                         'budget': ttk.Entry(insert_frame, font=('aerial', 14), width=7),
                         'insert_button': ttk.Button(insert_frame, text="INSERISCI", style="Bold.TButton",
                                                     command=lambda: self.insertJob(insert_fields['commessa'].get(),
                                                                                     insert_fields['tipo'].get(),
                                                                                     insert_fields['cliente'].get(),
                                                                                     insert_fields['descrizione'].get(),
                                                                                     insert_fields['budget'].get()))}
        # render widgets in insert_fields
        for field in insert_fields.values():
            field.pack(side=tk.LEFT, anchor=tk.E, padx=5, fill=tk.X, expand=True)

        # create the table to display jobs data
        self.table = MyTreeview(container, columns=columns, show='headings', height=20)
        self.table.heading('Cliente', text='Cliente', sort_by='str')
        self.table.column("Cliente", minwidth=0, width=250, stretch=True)
        self.table.heading('Nome', text='Commessa', sort_by='str')
        self.table.column("Nome", minwidth=0, width=250, stretch=False)
        self.table.heading('Tipo', text='Tipo Commessa', sort_by='str')
        self.table.column("Tipo", minwidth=0, width=300, stretch=False)
        self.table.heading('Descrizione', text='Descrizione', sort_by='str')
        self.table.column("Descrizione", minwidth=0, width=600, stretch=True)
        self.table.heading('Budget', text='Budget', sort_by='num')
        self.table.column("Budget", minwidth=0, width=150, stretch=False)

        self.table.tag_configure('gray', background='#f5f5f5')
        alternate = True
        for item in self.jobs:
            if alternate:
                self.table.insert('', tk.END, values=item)
                alternate = False
            else:
                alternate = True
                self.table.insert('', tk.END, values=item, tag='gray')

        # render table and scrollbar
        self.table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # render button to delete and button to go back to initial manager menu
        back_to_home_button = ttk.Button(button_container, text="HOME", style="Bold.TButton", command=self.managerMenu)
        back_to_home_button.pack(side=tk.LEFT, padx=40, pady=10)
        delete_button = ttk.Button(button_container, text="CANCELLA", style="Bold.TButton", command=self.deleteJob)
        delete_button.pack(side=tk.RIGHT, padx=40, pady=10)
        edit_item_button = ttk.Button(button_container, text="MODIFICA", style="Bold.TButton", command=self.testProgramThread)
        edit_item_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def testProgramThread(self):
        thread = threading.Thread(None, self.editItem(), None, (), {})
        thread.start()

    def editItem(self):
        """
        This method allows to edit an item inside the treeview instance.
        """
        focused = self.table.focus()
        values = self.table.item(focused)['values']
        USER_INP = simpledialog.askinteger(title="MODIFICA", prompt="Inserire nuovo budget:")

        self.table.item(focused, values=(values[0], values[1], values[2], values[3], USER_INP))
        for index in range(len(self.USER.jobs_to_display)):
            if self.USER.jobs_to_display[index]['Cliente'] == values[0] and str(self.USER.jobs_to_display[index]['Nome']) == str(
                    values[1]) and self.USER.jobs_to_display[index]['Tipo'] == \
                    values[2] and self.USER.jobs_to_display[index]['Descrizione'] == values[3] and int(self.USER.jobs_to_display[index]['Budget']) == int(values[4]):
                self.USER.jobs_to_display[index]['Budget'] = int(USER_INP)

        query = f"UPDATE oca.commesse SET Budget = {USER_INP} WHERE Cliente = '{values[0]}' AND " \
                f"Nome = '{values[1]}' AND Tipo LIKE '%{values[2]}' AND Descrizione = '{values[3]}'"

        db_connection = DB()
        db_connection.alter(query)
        db_connection.closeConnection()

    def insertJob(self, job, job_type, client, description, budget):
        """
        Insert the new user in the database table.
        :param job: job to insert
        :param job_type: job type to insert
        :param client: client to insert
        :param description: description to insert
        :param budget: budget to insert
        :return: None
        """
        # check if all camps are compiled
        if not job or not job_type or not description:
            tk.messagebox.showerror("Errore", "Compilare tutti i campi")

        else:
            db_connection = DB()
            query = f"INSERT commesse(Nome, Tipo, Cliente, Descrizione, Budget) VALUES ('{job}', '{job_type}', '{client}', '{description}', {budget})"
            db_connection.insert(query)

            tk.messagebox.showinfo("Riga inserita", "Riga inserita correttamente")
            # insert the new row also in the table
            self.table.insert("", tk.END, values=(client, job, job_type, description,budget))

            db_connection.closeConnection()

    def deleteJob(self):
        """
        Deletes the selected rows in the treeview from the database.
        :return: None
        """
        # ask for confirm
        answer = tk.messagebox.askyesno("Confermare", "Sei sicuro di voler eliminare le righe selezionate ?")

        if answer:
            db_connection = DB()
            for selected_item in self.table.selection():
                item = self.table.item(selected_item)
                record = item['values']
                job = record[1]
                tipo = record[2]
                client = record[0]
                description = record[3]
                budget = record[4]

                query = f"DELETE FROM commesse WHERE Nome = '{job}' AND Tipo LIKE '%{tipo}' AND Cliente = '{client}' AND Descrizione = '{description}' AND Budget = {budget}"
                db_connection.delete(query)

                self.table.delete(selected_item)

                tk.messagebox.showinfo("Riga eliminata", "Riga eliminata correttamente")

            db_connection.closeConnection()

    def jobsStatsPage(self):
        """
        Render the page in which managers can see data inserted by workers grouped first by client, job and type of job.
        :return: None
        """
        clear_window(self.window)

        #get data to display in this page
        jobs_list, self.users = self.USER.getData()

        columns = ['Cliente', 'Commessa', 'TipoCommessa', 'CognomeLavoratore', 'Data', 'Ore', 'Budget', 'BudgetSpeso']
        self.jobs_statistics = {}
        # {Commessa1:
        #               {budgetCommessa: y, budgetSpeso:z, oreCommessa: x, Cliente: y, tipoCommesse:
        #                        {
        #                         tipoCommessa1: {budgetCommessa: y, budgetSpeso:z, oreTipoCommessa, history: []},
        #                         tipoCommessa2: {budgetCommessa: y, budgetSpeso:z, oreTipoCommessa, history: []}
        #               }},...}

        for job in jobs_list:
            if job['Nome'] not in self.jobs_statistics.keys():
                self.jobs_statistics[job['Nome']] = {'budgetCommessa': 0, 'budgetSpeso': 0, 'oreCommessa': 0, 'Cliente': job['Cliente'],
                                                     'tipoCommesse': {}}

            self.jobs_statistics[job['Nome']]['tipoCommesse'][job['Tipo']] = {'budgetTipoCommessa': job['Budget'],
                                                                              'budgetTipoSpeso': 0,
                                                                              'oreTipoCommessa': 0,
                                                                              'history': []}
            self.jobs_statistics[job['Nome']]['budgetCommessa'] += job['Budget']

        for row in self.users:
            self.jobs_statistics[row['Commessa']]['tipoCommesse'][row['TipoCommessa']]['history'].append(
                                                                    (row['CognomeLavoratore'], row['Data'], row['Ore'],
                                                                     row['Ore'] * row['CostoOrario'], row['CostoOrario']))
            self.jobs_statistics[row['Commessa']]['oreCommessa'] += row['Ore']
            self.jobs_statistics[row['Commessa']]['tipoCommesse'][row['TipoCommessa']]['oreTipoCommessa'] += row['Ore']
            self.jobs_statistics[row['Commessa']]['budgetSpeso'] += row['Ore']*row['CostoOrario']
            self.jobs_statistics[row['Commessa']]['tipoCommesse'][row['TipoCommessa']]['budgetTipoSpeso'] += row['Ore'] * row['CostoOrario']


        # create frames
        filters_frame = ttk.Frame(self.window)
        filters_frame.pack(side=tk.TOP, anchor="n", padx=40, pady=20)
        tree_frame = ttk.Frame(self.window)
        tree_frame.pack(side=tk.TOP, anchor="n", expand=True, fill=tk.BOTH, padx=40, pady=20)
        button_container = ttk.Frame(self.window)
        button_container.pack(side=tk.TOP, anchor="n", expand=True, fill=tk.BOTH, padx=40)

        year = self.today_date.year
        month = self.today_date.month
        first_day_of_month = self.today_date.replace(day=1)

        # Calculate the last day of the month
        last_day_of_month = self.today_date.replace(month=first_day_of_month.month % 12 + 1, day=1) - timedelta(days=1)

        # create widgets to filter table
        self.filters = {'starting_date_label': ttk.Label(filters_frame, text="Data inizio:", font=('aerial', 14)),
                        'starting_date': DateEntry(filters_frame, selectmode='day', date_pattern="yyyy-mm-dd", font=('aerial', 14),
                                                   year=year, month=month, day=first_day_of_month.day),
                        'ending_date_label': ttk.Label(filters_frame, text="Data fine:", font=('aerial', 14)),
                        'ending_date': DateEntry(filters_frame, selectmode='day', date_pattern="yyyy-mm-dd", font=('aerial', 14),
                                                   year=year, month=month, day=last_day_of_month.day),
                        'filter_button': ttk.Button(filters_frame, text='FILTRA', style="Bold.TButton", command=self.displayClientsData)}

        # render widgets to filter table
        for widget in self.filters.values():
            widget.pack(side=tk.LEFT, anchor='w', padx=5)


        # creating treeview element
        self.table = MyTreeview(tree_frame, columns=columns, height=20)
        self.table.column("#0", minwidth=0, width=15, stretch=False)
        self.table.heading('Cliente', text='Cliente', sort_by='srt')
        self.table.column("Cliente", minwidth=0, width=150, stretch=True)
        self.table.heading('Commessa', text='Commessa', sort_by='srt')
        self.table.column("Commessa", minwidth=0, width=250, stretch=True)
        self.table.heading('TipoCommessa', text='Tipo Commessa', sort_by='srt')
        self.table.column("TipoCommessa", minwidth=0, width=220, stretch=False)
        self.table.heading('CognomeLavoratore', text='Progettista', sort_by='srt')
        self.table.column("CognomeLavoratore", minwidth=0, width=200, stretch=False)
        self.table.heading('Data', text='Data', sort_by='srt')
        self.table.column("Data", minwidth=0, width=120, stretch=False)
        self.table.heading('Ore', text='Ore', sort_by='srt')
        self.table.column("Ore", minwidth=0, width=80, stretch=False)
        self.table.heading('Budget', text='Budget')
        self.table.column("Budget", minwidth=0, width=100, stretch=False)
        self.table.heading('BudgetSpeso', text='Costo')
        self.table.column("BudgetSpeso", minwidth=0, width=100, stretch=True)

        self.table.tag_configure('gray', background='#f5f5f5')

        self.displayClientsData()

        # rendering treeview and scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # creating and rendering a button to go back to manager home page
        back_to_home_button = ttk.Button(button_container, text="HOME", style="Bold.TButton", command=self.managerMenu)
        back_to_home_button.pack(side=tk.LEFT, padx=40, pady=10)

    def displayClientsData(self):
        """
        Method to filter data on a treeview given some date filters.
        :return: None
        """
        self.table.delete(*self.table.get_children())

        # insert only rows with values equal to the selected values of the filters. If a filter is empty then it is not
        # checked if the value of the row to insert is equal to the filter's value
        # {Commessa1:
        #               {budgetCommessa: y, budgetSpeso:z, oreCommessa: x, Cliente: y, tipoCommesse:
        #                        {
        #                         tipoCommessa1: {budgetCommessa: y, budgetSpeso:z, oreTipoCommessa, history: []},
        #                         tipoCommessa2: {budgetCommessa: y, budgetSpeso:z, oreTipoCommessa, history: []}
        #               }},...}
        starting_date = self.filters['starting_date'].get_date()
        ending_date = self.filters['ending_date'].get_date()
        filtered = {}
        client_table_rows_id = {}

        for key, value in self.jobs_statistics.items():
            filtered[key] = {'budgetCommessa': value['budgetCommessa'], 'budgetSpeso': 0, 'oreCommessa': 0, 'Cliente': value['Cliente'],
                             'tipoCommesse': {}}
            for subkey, subvalue in value['tipoCommesse'].items():
                filtered[key]['tipoCommesse'][subkey] = {'budgetTipoCommessa': subvalue['budgetTipoCommessa'],
                                                         'budgetTipoSpeso': 0, 'oreTipoCommessa': 0, 'history': []}

                for row in subvalue['history']:
                    if starting_date <= datetime.strptime(row[1], "%Y-%m-%d").date() <= ending_date:
                        filtered[key]['tipoCommesse'][subkey]['history'].append(row)
                        filtered[key]['oreCommessa'] += row[2]
                        filtered[key]['tipoCommesse'][subkey]['oreTipoCommessa'] += row[2]

                        filtered[key]['tipoCommesse'][subkey]['budgetTipoSpeso'] += row[3]
                        filtered[key]['budgetSpeso'] += row[3]

        for key, value in filtered.items():
            if value['oreCommessa'] > 0:
                new_client_inserted = False

                if value['Cliente'] not in client_table_rows_id:
                    client = self.table.insert('', tk.END, values=(value['Cliente'], '', '', '', '', '', ''))
                    client_table_rows_id[value['Cliente']] = client
                    new_client_inserted = True

                job = self.table.insert(client_table_rows_id[value['Cliente']], tk.END, values=('', key, '', '', '', value['oreCommessa'],
                                                                value['budgetCommessa'], value['budgetSpeso']))

                for subkey, subvalue in value['tipoCommesse'].items():
                    subjob = self.table.insert(job, tk.END, values=('', '', subkey, '', '', subvalue['oreTipoCommessa'],
                                                                    subvalue['budgetTipoCommessa'],
                                                                    subvalue['budgetTipoSpeso']))
                    inserted = []
                    for row in subvalue['history']:
                        if row[0] not in inserted:
                            worker = self.table.insert(subjob, tk.END, values=('', '', '') + (row[0], '', '', '', ''))
                            inserted.append(row[0])
                        self.table.insert(worker, tk.END, values=('', '', '') + ('', row[1], row[2], '', row[3]))

                if new_client_inserted:
                    self.table.insert('', tk.END, values=('', '', '', '', '', '', '', ''), tag='gray')

    def workersStatsPage(self):
        """
        Renders the page in which managers can see data inserted by workers grouped first by worker, job and type of job.
        :return: None
        """
        clear_window(self.window)

        #get data to display in this page
        #CognomeLavoratore, Data, Anno, Mese, Ore, Commessa, TipoCommessa, CostoOrario
        jobs_list, self.users = self.USER.getData()
        self.workerCosts = self.USER.getWorkerCosts()

        columns = ['CognomeLavoratore', 'Commessa', 'Ore Complessive', 'Costo', 'TipoCommessa',  'Data', 'Ore Giornata']
        self.worker_statistics = {}
        # {CognomeLavoratore:
        #                   {Commessa:
        #                       {Ore: x, Costo: y: history:{
        #                          Tipocommessa:{
        #                            [Data: x, Ore: y],[...],[...]}
        #  }}}}}

        for row in self.users:
            if row['CognomeLavoratore'] not in self.worker_statistics.keys():
                self.worker_statistics[row['CognomeLavoratore']] = {}
            if row['Commessa'] not in self.worker_statistics[row["CognomeLavoratore"]].keys():
                self.worker_statistics[row['CognomeLavoratore']][row['Commessa']] = {"Costo": 0,
                                                                  "Ore": 0, 'history': {}}
            if row['TipoCommessa'] not in self.worker_statistics[row["CognomeLavoratore"]][row["Commessa"]]['history'].keys():
                self.worker_statistics[row['CognomeLavoratore']][row['Commessa']]['history'][row["TipoCommessa"]] = []

            self.worker_statistics[row['CognomeLavoratore']][row['Commessa']]["Ore"] += row["Ore"]
            self.worker_statistics[row['CognomeLavoratore']][row['Commessa']]["Costo"] += row["Ore"]*row["CostoOrario"]
            self.worker_statistics[row['CognomeLavoratore']][row['Commessa']]['history'][row["TipoCommessa"]].append([row["Data"], row["Ore"]])


        # create frames
        filters_frame = ttk.Frame(self.window)
        filters_frame.pack(side=tk.TOP, anchor="n", padx=40, pady=20)
        tree_frame = ttk.Frame(self.window)
        tree_frame.pack(side=tk.TOP, anchor="n", expand=True, fill=tk.BOTH, padx=40, pady=20)
        button_container = ttk.Frame(self.window)
        button_container.pack(side=tk.TOP, anchor="n", expand=True, fill=tk.BOTH, padx=40)

        year = self.today_date.year
        month = self.today_date.month
        first_day_of_month = self.today_date.replace(day=1)

        # Calculate the last day of the month
        last_day_of_month = self.today_date.replace(month=first_day_of_month.month % 12 + 1, day=1) - timedelta(days=1)

        # create widgets to filter table
        self.worker_filters = {'starting_date_label': ttk.Label(filters_frame, text="Data inizio:", font=('aerial', 14)),
                        'starting_date': DateEntry(filters_frame, selectmode='day', date_pattern="yyyy-mm-dd", font=('aerial', 14),
                                                   year=year, month=month, day=first_day_of_month.day),
                        'ending_date_label': ttk.Label(filters_frame, text="Data fine:", font=('aerial', 14)),
                        'ending_date': DateEntry(filters_frame, selectmode='day', date_pattern="yyyy-mm-dd", font=('aerial', 14),
                                                   year=year, month=month, day=last_day_of_month.day),
                        'filter_button': ttk.Button(filters_frame, text='FILTRA', style="Bold.TButton", command=self.displayWorkerData)}

        # render widgets to filter table
        for widget in self.worker_filters.values():
            widget.pack(side=tk.LEFT, anchor='w', padx=5)

        # creating treeview element
        self.worker_table = MyTreeview(tree_frame, columns=columns, height=20)
        self.worker_table.column("#0", minwidth=0, width=15, stretch=False)
        self.worker_table.heading('CognomeLavoratore', text='Progettista', sort_by='srt')
        self.worker_table.column("CognomeLavoratore", minwidth=0, width=150, stretch=True)
        self.worker_table.heading('Commessa', text='Commessa', sort_by='srt')
        self.worker_table.column("Commessa", minwidth=0, width=220, stretch=True)
        self.worker_table.heading('Ore Complessive', text='Ore Complessive', sort_by='srt')
        self.worker_table.column("Ore Complessive", minwidth=0, width=180, stretch=False)
        self.worker_table.heading('Costo', text='Costo', sort_by='srt')
        self.worker_table.column("Costo", minwidth=0, width=150, stretch=False)
        self.worker_table.heading('TipoCommessa', text='TipoCommessa', sort_by='srt')
        self.worker_table.column("TipoCommessa", minwidth=0, width=200, stretch=False)
        self.worker_table.heading('Data', text='Data', sort_by='srt')
        self.worker_table.column("Data", minwidth=0, width=150, stretch=False)
        self.worker_table.heading('Ore Giornata', text='Ore Giornata', sort_by='srt')
        self.worker_table.column("Ore Giornata", minwidth=0, width=150, stretch=False)

        self.worker_table.tag_configure('gray', background='#f5f5f5')

        self.displayWorkerData()

        # rendering treeview and scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.worker_table.yview)
        self.worker_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.worker_table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # creating and rendering a button to go back to manager home page
        back_to_home_button = ttk.Button(button_container, text="HOME", style="Bold.TButton", command=self.managerMenu)
        back_to_home_button.pack(side=tk.LEFT, padx=40, pady=10)

    def displayWorkerData(self):
        """
        Method to filter data on a treeview given some date filters.
        :return: None
        """
        self.worker_table.delete(*self.worker_table.get_children())

        # insert only rows with values equal to the selected values of the filters. If a filter is empty then it is not
        # checked if the value of the row to insert is equal to the filter's value
        # {CognomeLavoratore:
        #                   {Ore: x, Costo: y, Commessa:
        #                       {Ore: x, Costo: y: history:{
        #                          Tipocommessa:[
        #                            [Data: x, Ore: y],[...],[...]]
        #  }}}}}

        starting_date = self.worker_filters['starting_date'].get_date()
        ending_date = self.worker_filters['ending_date'].get_date()
        filtered = {}

        for key, value in self.worker_statistics.items():
            if key not in filtered.keys():
                filtered[key] = {"Costo": 0, "Ore": 0, 'history': {}}

            for subkey, subvalue in value.items():
                if subkey not in filtered[key]['history'].keys():
                    filtered[key]['history'][subkey] = {"Costo": 0, "Ore": 0, 'history': {}}

                for subsubkey, subsubvalue in subvalue['history'].items():
                    if subsubkey not in filtered[key]['history'][subkey]['history'].keys():
                        filtered[key]['history'][subkey]['history'] = {subsubkey: []}

                    for item in subsubvalue:
                        if starting_date <= datetime.strptime(item[0], "%Y-%m-%d").date() <= ending_date:

                            filtered[key]['history'][subkey]['history'][subsubkey].append(item)
                            filtered[key]['Costo'] += item[1] * self.workerCosts[key]
                            filtered[key]['Ore'] += item[1]
                            filtered[key]['history'][subkey]['Costo'] += item[1] * self.workerCosts[key]
                            filtered[key]['history'][subkey]['Ore'] += item[1]

        for key, value in filtered.items():
            if value['Ore'] > 0:
                worker = self.worker_table.insert('', tk.END, values=(key, '', value['Ore'], value['Costo'], '', '', ''))

                for subkey, subvalue in value['history'].items():
                    if subvalue['Ore'] > 0:
                        job = self.worker_table.insert(worker, tk.END, values=('', subkey, subvalue['Ore'], subvalue['Costo'], '', '', ''))

                    for subsubkey, subsubvalue in subvalue['history'].items():
                        subjob = self.worker_table.insert(job, tk.END, values=('', '', '', '') + (subsubkey, '', ''))

                        for row in subsubvalue:
                            self.worker_table.insert(subjob, tk.END, values=('', '', '', '', '') + (row[0], row[1]))

            self.worker_table.insert('', tk.END, values=('', '', '', '', '', '', '', ''), tag='gray')
