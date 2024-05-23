import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from DBOperations import DB
from Util import clear_window, MyTreeview
from ErrorHandler import ErrorHandler


class WorkerGUI:
    """
    This class manages and renders the application page related to workers.
    """

    def __init__(self, window, user):
        """
        Sets worker window's properties and calls the worker_frame method to render the page.
        :param window:  a ttk window instance
        :param user: instance of user class.
        """
        self.window = window
        self.USER = user
        self.user_inserted_jobs, self.jobs_available = self.USER.getData()
        self.window.title(f"{self.USER.getName()}")

        # clears all the widget from previous page
        clear_window(self.window)

    def workerPage(self):
        """
        This method creates and renders all the widgets needed in the worker's page, in particular: a row to insert new data,
        a row to filter the table, a tree view to render a table and a delete button to delete selected rows.
        """

        # get and format the data to display
        client_available = list(set([item['Cliente'] for item in self.jobs_available] + [""]))
        name_jobs_available = []
        type_jobs_available = []
        dates_choice = list(set([item[0][0:7] for item in self.user_inserted_jobs] + [""]))
        client_choice = list(set([item[1] for item in self.user_inserted_jobs] + [""]))
        jobs_choice = list(set([item[2] for item in self.user_inserted_jobs] + [""]))
        jobs_type_choice = list(set([item[3] for item in self.user_inserted_jobs] + [""]))
        client_available.sort(), jobs_type_choice.sort(), client_choice.sort(), dates_choice.sort(), jobs_choice.sort()

        columns = ['Data', 'Cliente', 'Commessa', 'TipoCommessa', 'Ore']

        # define frames for the insert-rows part
        insert_frame = ttk.Frame(self.window)
        insert_frame.pack(side=tk.TOP, anchor=tk.N, padx=40, pady=30, expand=True)

        # create all the widgets necessary to insert rows in the table
        insert_fields = {'date_label': ttk.Label(insert_frame, text="Data:", font=('aerial', 14)),
                         'calendar': DateEntry(insert_frame, selectmode='day', date_pattern="yyyy-mm-dd",
                                               font=('aerial', 14)),
                         'client_label': ttk.Label(insert_frame, text="Cliente:", font=('aerial', 14)),
                         'client_combobox': ttk.Combobox(insert_frame, values=client_available, state="readonly",
                                                         font=('aerial', 14)),
                         'job_label': ttk.Label(insert_frame, text="Commessa:", font=('aerial', 14)),
                         'job_combobox': ttk.Combobox(insert_frame, values=name_jobs_available, state="readonly",
                                                      font=('aerial', 14)),
                         'job_type_label': ttk.Label(insert_frame, text="Tipo:", font=('aerial', 14)),
                         'job_type_combobox': ttk.Combobox(insert_frame, values=type_jobs_available, state="readonly",
                                                           font=('aerial', 14)),
                         'hours_label': ttk.Label(insert_frame, text="Ore:", font=('aerial', 14)),
                         'hours': ttk.Entry(insert_frame, width=3, font=('aerial', 14)),
                         'insert_button': ttk.Button(insert_frame, text="INSERISCI", style="Bold.TButton",
                                                     command=lambda: self.insertJobs(
                                                         insert_fields['client_combobox'].get(),
                                                         insert_fields['calendar'].get(),
                                                         insert_fields[
                                                             'job_combobox'].get(),
                                                         insert_fields[
                                                             'job_type_combobox'].get(),
                                                         insert_fields['hours'].get()))}

        insert_fields['client_combobox'].bind('<<ComboboxSelected>>', lambda event: self.comboFill(
            insert_fields['client_combobox'].get(), insert_fields['job_combobox'], 'client'))
        insert_fields['job_combobox'].bind('<<ComboboxSelected>>', lambda event: self.comboFill(
            insert_fields['job_combobox'].get(), insert_fields['job_type_combobox'], 'job'))

        # render all elements
        for widget in insert_fields.values():
            widget.pack(side=tk.LEFT, anchor=tk.E, padx=5)

        # define frames for the table and filters part
        container = ttk.Frame(self.window)
        container.pack(side=tk.TOP, anchor="n", fill=tk.BOTH, expand=True, padx=40, pady=20)
        filters_frame = ttk.Frame(container)
        filters_frame.pack(side=tk.TOP, anchor="n", padx=40, pady=10)
        tree_view_frame = ttk.Frame(container)
        tree_view_frame.pack(side=tk.TOP, anchor="n", expand=True, fill=tk.BOTH, padx=40, pady=0)

        # create all the widgets necessary for the table and to filter the table
        self.filters = {'client_label': ttk.Label(filters_frame, text="Cliente:", font=('aerial', 14)),
                        'client': ttk.Combobox(filters_frame, values=client_choice, state="readonly",
                                               font=('aerial', 14)),
                        'anno_mese_label': ttk.Label(filters_frame, text="Data:", font=('aerial', 14)),
                        'anno_mese': ttk.Combobox(filters_frame, values=dates_choice, state="readonly", width=12,
                                                  font=('aerial', 14)),
                        'commessa_label': ttk.Label(filters_frame, text="Commessa:", font=('aerial', 14)),
                        'commessa': ttk.Combobox(filters_frame, values=jobs_choice, state="readonly",
                                                 font=('aerial', 14)),
                        'tipocommessa_label': ttk.Label(filters_frame, text="Tipo:", font=('aerial', 14)),
                        'tipocommessa': ttk.Combobox(filters_frame, values=jobs_type_choice, state="readonly",
                                                     font=('aerial', 14))}

        self.table = MyTreeview(tree_view_frame, columns=columns, show='headings', height=20)
        self.table.heading('Data', text='Data', sort_by='str')
        self.table.column("Data", minwidth=0, width=150, stretch=False)
        self.table.heading('Cliente', text='Cliente', sort_by='str')
        self.table.column("Cliente", minwidth=0, width=350, stretch=False)
        self.table.heading('Commessa', text='Commessa', sort_by='str')
        self.table.column("Commessa", minwidth=0, width=350, stretch=False)
        self.table.heading('TipoCommessa', text='Tipo Commessa', sort_by='str')
        self.table.column("TipoCommessa", minwidth=0, width=350, stretch=False)
        self.table.heading('Ore', text='Ore', sort_by='str')
        self.table.column("Ore", minwidth=0, width=80, stretch=True)

        # render all elements
        for widget in self.filters.values():
            widget.pack(side=tk.LEFT, anchor=tk.E, padx=5)

        # bind the filter event to the comboboxes
        self.filters['anno_mese'].bind("<<ComboboxSelected>>", lambda event: self.filterData(event))
        self.filters['commessa'].bind("<<ComboboxSelected>>", lambda event: self.filterData(event))
        self.filters['tipocommessa'].bind("<<ComboboxSelected>>",
                                          lambda event: self.filterData(event))

        self.table.tag_configure('gray', background='#f5f5f5')

        alternate = True
        # insert data in the treeview
        for item in self.user_inserted_jobs:
            if alternate:
                self.table.insert('', tk.END, values=item)
                alternate = False
            else:
                self.table.insert('', tk.END, values=item, tag='gray')
                alternate = True

        # render last elements needed
        self.table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(tree_view_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        ttk.Button(self.window, text="CANCELLA", style="Bold.TButton",
                   command=lambda: self.deleteJob(self.table)).pack(side=tk.TOP, anchor=tk.E, padx=120, pady=10)

    def comboFill(self, selected, combo_box_to_fill, type_filled):
        """
        Fill the combo-box based on the previous selection, so the choices from different combo-boxes are compatible.
        :param selected: selection in the first combo-box
        :param combo_box_to_fill: combo-box to fill with compaible choices
        :param type_filled: type of combo-box to be filled
        """
        match type_filled:
            case 'client':
                if selected == '':
                    combo_box_to_fill["values"] = [""]

                else:
                    jobs_choice = list(
                        set([item['Nome'] for item in self.jobs_available if item['Cliente'] == selected] + [""]))
                    jobs_choice.sort()
                    combo_box_to_fill["values"] = jobs_choice
                    combo_box_to_fill.set('')

        match type_filled:
            case 'job':
                if selected == '':
                    combo_box_to_fill["values"] = [""]

                else:
                    jobs_type_choice = list(
                        set([item['Tipo'] for item in self.jobs_available if item['Nome'] == selected] + [""]))
                    jobs_type_choice.sort()
                    combo_box_to_fill["values"] = jobs_type_choice
                    combo_box_to_fill.set('')

    def insertJobs(self, client, date_given, job, type_job, hours):
        """
        First checks if the passed inputs are all not empty, if so try to insert the passed data into the table on DB.
        :param client: client to insert
        :param date_given: data to insert
        :param job: job name to insert
        :param hours: hours to insert
        :param type_job: job type to insert
        """
        # checks if one or more inputs are empty
        if not date_given or not job or not hours or not type_job:
            tk.messagebox.showerror("Errore", "Compilare tutti i campi !")

        else:
            db_connection = DB()
            try:
                query = f"INSERT storico_commesse(Cliente, CognomeLavoratore, Data, Anno, Mese, Ore, Commessa, TipoCommessa) VALUES ('{client}','{self.USER.getName()}', '{date_given}','{date_given[0:4]}','{date_given[5:7]}', {hours}, '{job}', '{type_job}' )"
                db_connection.insert(query)
                db_connection.closeConnection()

                tk.messagebox.showinfo("Riga inserita", "Riga inserita correttamente !")

                # call the method that updates the table by adding the new row and to updates filters choices
                row = {'Data': date_given, 'Cliente': client, 'Commessa': job, 'Ore': hours, 'TipoCommessa': type_job}
                self.user_inserted_jobs.append([date_given, client, job, type_job, str(hours)])
                self.updateTree(row, 'insert')

            except Exception as error:
                ErrorHandler(error)
                db_connection.closeConnection()

    def deleteJob(self, tree):
        """
        Deletes the selected rows in the treeview from the database.
        :param tree: a treeview instance containing the data to delete
        """
        # ask for confirm
        answer = tk.messagebox.askyesno("Confermare", "Sei sicuro di voler eliminare le righe selezionate ?")

        if answer:
            db_connection = DB()
            for selected_item in tree.selection():
                # prepare query
                item = tree.item(selected_item)
                record = item['values']
                data = record[0]
                cliente = record[1]
                commessa = record[2]
                tipo_commessa = record[3]
                ore = record[4]

                query = f"DELETE FROM storico_commesse WHERE CognomeLavoratore = '{self.USER.getName()}' AND Data = '{data}' AND Ore = {ore} AND Commessa = '{commessa}' AND Cliente = '{cliente}' AND TipoCommessa LIKE '%{tipo_commessa}'"
                db_connection.delete(query)
                # call the method that update the tree and filters
                self.updateTree(selected_item, 'delete')
                # remove row from data to display
                self.user_inserted_jobs.remove([record[0], record[1], str(record[2]), record[3], str(record[4])])

            db_connection.closeConnection()
            tk.messagebox.showinfo("Riga eliminata", "Riga eliminata correttamente")

    def filterData(self, event):
        """
        Based on the filters' selection, filters the treeview
        :param event: event item
        """
        self.table.delete(*self.table.get_children())
        for row in self.user_inserted_jobs:
            # insert only rows that match the filter values for filers that are filled out
            if (row[0][0:7] == self.filters['anno_mese'].get() or not self.filters['anno_mese'].get()) and \
                    (row[1] == self.filters['client'].get() or not self.filters['client'].get()) and \
                    (row[2] == self.filters['commessa'].get() or not self.filters['commessa'].get()) and \
                    (row[3] == self.filters['tipocommessa'].get() or not self.filters['tipocommessa'].get()):
                self.table.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4]))

    def updateTree(self, row, mode):
        """
        Inserts or deletes rows from the treeview. In the insert case also ads new values to lists for the treeview
        filters.
        :param row: row to insert or delete
        :param mode: 'insert' or 'delete'
        """
        match mode:
            case 'insert':

                self.table.insert("", tk.END,
                                  values=(str(row['Data']), row['Cliente'], row['Commessa'], row['TipoCommessa'],
                                          str(row['Ore'])))
                # if the inserted row contains a new value that was previously not listed in the filters list,
                # adds it to the list
                if row['Cliente'][0:7] not in self.filters['client']['values']:
                    self.filters['client']['values'] += (row['Cliente'],)
                if row['Data'][0:7] not in self.filters['anno_mese']['values']:
                    self.filters['anno_mese']['values'] += (row['Data'][0:7],)
                if row['Commessa'] not in self.filters['commessa']['values']:
                    self.filters['commessa']['values'] += (row['Commessa'],)
                if row['TipoCommessa'] not in self.filters['tipocommessa']['values']:
                    self.filters['tipocommessa']['values'] += (row['TipoCommessa'],)

            case 'delete':
                self.table.delete(row)
