import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "dlg.ui"


class CalendarDlgApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow', master)

        self.lbl_date = builder.get_object('lbl_date') # lbl_Date refence
        self.mydlg = None  # Dialog reference

        builder.connect_callbacks(self)
    
    def run(self):
        self.mainwindow.mainloop()

    def toggle_calendar(self):
        if self.mydlg is None:
            self.mydlg = self.builder.get_object('dialog1', self.mainwindow)
            self.builder.connect_callbacks(self)
        # Run the dialog
        self.mydlg.run()


    def on_dialog_close_event(self, event=None):
        print('User clicked on window manager close button.')
        self.mydlg.close()
    
    def on_date_selected(self, event=None):
        # Get picked date
        date = self.builder.get_object('fcalendar').selection

        print("user picked: ", date.strftime('%d-%m-%Y'))
        # Set lbl_date's text
        self.lbl_date.configure(text=date.strftime('%d-%m-%Y'))
        # Close diallog
        self.mydlg.close()
        

if __name__ == '__main__':
    app = CalendarDlgApp()
    app.run()