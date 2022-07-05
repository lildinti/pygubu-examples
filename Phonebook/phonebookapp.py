#!/usr/bin/python3
import json
import pathlib
from tkinter import END
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "phonebook.ui"
PROJECT_DATA = PROJECT_PATH / "phonebook.json"

class PhonebookApp:
    #init UI
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        self.mainwindow.protocol("WM_DELETE_WINDOW",self.on_close_window)

        self.counter = 1
        self.varName = None
        self.varPhone = None
        self.tv = self.builder.get_object("treeview1")

        builder.import_variables(self, ["varName", "varPhone"])
        builder.connect_callbacks(self)

        self.first_init = True
        self.mainwindow.bind('<Map>', self.center_window)
        
        # read data 
        self.read_data_file()   

    def on_close_window(self, event=None):
        
        datalist = []
        for line in self.tv.get_children():
            datalist.append(self.tv.item(line)['values'])
        with open(PROJECT_DATA,'w') as outfile:
            json.dump(datalist,outfile)
        self.mainwindow.destroy()

    def center_window(self, event=None):
        if self.    first_init:
            toplevel = self.mainwindow
            height = toplevel.winfo_height()
            width = toplevel.winfo_width()
            x_coord = int(toplevel.winfo_screenwidth() / 2 - width / 2)
            y_coord = int(toplevel.winfo_screenheight() / 2 - height / 2)
            geom = f'{width}x{height}+{x_coord}+{y_coord}'
            toplevel.geometry(geom)
            self._first_init = False

    def run(self):
        self.mainwindow.mainloop()

    def read_data_file(self):
        # check if data file exists
        datafile = pathlib.Path(PROJECT_DATA)
        if datafile.is_file():
            # read data file
            with open(PROJECT_DATA) as json_file:
                data = json.load(json_file)
                # incresse row counter for correct insertion of new record
                self.counter=len(data)+1 
        self.populate_tree(data)


    def add_record(self):
        action = self.builder.get_object('btnAdd')['text']
        if action == "Add Record":
            # Add new record
            name = self.varName.get()
            phone = self.varPhone.get()
            #insert record and increase ID (Counter)
            self.tv.insert("",'end',iid=self.counter,values=(name,str(phone)))
            self.counter+=1
            # Clear Entry Fields
            self.varName.set('')
            self.varPhone.set('')
        else:
            # refresh tree with ne record data
            sel = self.tv.focus()
            self.tv.item(sel,values=(self.varName.get(),str(self.varPhone.get())))
            # Clear edit boxes
            self.varName.set('')
            self.varPhone.set('')
            # Restore "Add Record' button
            self.builder.get_object("btnAdd").configure(text='Add Record')

    def delete_item(self):
        # get selected record
        sel = self.tv.focus()   
        # delete and decrease counter
        self.tv.delete(sel)
        self.counter -= 1
        
    def populate_tree(self,data):
        row_counter = 1
        for item in data:
            v = [tuple(item)]
            name = item[0]
            phone = item[1]
            self.tv.insert("",'end',iid=row_counter,values=(name,phone))
            row_counter +=1
        

    def modify_item(self):
        # Get selected record , populate edit boxes and change update button
        sel = self.tv.focus()
        item = self.tv.item(sel)['values']
        self.varName.set(item[0])
        self.varPhone.set(item[1])
        self.builder.get_object("btnAdd").configure(text='Update Record')


if __name__ == "__main__":
    app = PhonebookApp()
    app.run()
