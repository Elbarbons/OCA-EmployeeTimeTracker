from datetime import date
from tkinter import ttk
from ttkthemes import ThemedTk
from LoginPage import Login


class OCA:
    """
    This class creates a tkinter window that will hold all the widgets for the OCA application and when initialized
    calls the login method to render the login page.
    This class also sets the window's properties.
    """
    WINDOW_DIMENSION = "600x600"
    # User information that will be update later
    USER = None

    def __init__(self):
        """
        Initialize the OCA class by creating tkinter base window and setting some basic properties of the window
        """
        self.window = ThemedTk(theme='breeze')
        # Setting properties of the window
        self.window.option_add("*Font", "aerial")
        self.window.maxsize(1700, 950)
        self.today_date = date.today()

        # Setting application icon
        self.window.iconbitmap('./Images/Goose.ico')

        # Setting buttons' style
        style = ttk.Style(self.window)
        style.configure("Bold.TButton", font=('aerial', 15, 'bold'))
        style.configure("Treeview", highlightthickness=0, bd=0, font=(None, 14))
        style.configure("Treeview.Heading", font=(None, 15, 'bold'))
        style.configure('Treeview', rowheight=28)

    def start(self):
        """
        Call the method that renders login page
        """
        login = Login(self.window)
        login.loginPage()

    def mainloop(self):
        """
        Starts mainloop()
        :return: None
        """
        self.window.mainloop()

    # This method is used to debug the application and bypass the login phase
    # def fakeLogin(self):
    #     login = Login(self.window)
    #     login.fakeLogin('manager')


if __name__ == '__main__':
    app = OCA()
    app.start()
    app.mainloop()