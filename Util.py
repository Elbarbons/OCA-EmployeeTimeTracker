from tkinter import ttk
from datetime import date
from functools import partial


def clear_window(window):
    """
    Given a window created with tkinter, the function clears all widgets inside the window
    :param window: tkinter window create with the statement tk.Tk()
    """
    for widget in window.winfo_children():
        widget.destroy()


class MyTreeview(ttk.Treeview):
    """
    Extension of the ttk.Treeview class. Added a way of sorting treeviews by clicking on the column header.
    Credits to Rami Hassan, post https://stackoverflow.com/questions/1966929/tk-treeview-column-sort/78145744#78145744.
    """
    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs['command'] = partial(func, column, True)
        return super().heading(column, **kwargs)

    def _sort(self, column, reverse, data_type, callback):
        row = [(self.set(k, column).lower(), k) for k in self.get_children('')]
        row.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(row):
            self.move(k, '', index)
        self.heading(column, command=partial(callback, column, not reverse))

    def _sort_by_num(self, column, reverse):
        self._sort(column, reverse, int, self._sort_by_num)

    def _sort_by_str(self, column, reverse):
        self._sort(column, reverse, str, self._sort_by_str)

    def _sort_by_date(self, column, reverse):
        def _str_to_datetime(string):
            return date.strftime(string, "%Y-%m-%d")
        self._sort(column, reverse, _str_to_datetime, self._sort_by_date)