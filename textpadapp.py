from fileinput import filename
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as fd
import pygubu



PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "textpad.ui"


class TextpadApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('toplevel1', master)
        self.textEdit = self.builder.get_object("text1")
        self.myFile = None
        self.fileName = "untitled"

        builder.connect_callbacks(self)
    
    def run(self):
        self.mainwindow.mainloop()

    def new_clicked(self):
        #self.my_text = self.builder.get_object('text1').delete('0.0',tk.END)
        message = "Do you want to save %s before closing?" % (self.fileName)
        confirm = tkMessageBox.askyesnocancel(
                  title="Save On Close",
                  message=message,
                  default=tkMessageBox.YES,
                  parent=self.mainwindow)
        if confirm:
            reply = "yes"
            """self.save(None)
            if not self.get_saved():
                reply = "cancel"""
            print('Save file here')
        elif confirm is None:
            reply = "cancel"
        else:
            reply = "no"
        self.textEdit.focus_set()
    
    def open_clicked(self):
        # Select file to open
        self.fileName = fd.askopenfilename()
        if self.fileName:
            base = pathlib.Path(self.fileName + "").name
            self.mainwindow.title("pygubu notepad - " + base)
            self.textEdit.delete("0.0",tk.END)
            with open(self.fileName) as f:
                contents = f.read()
                self.textEdit.insert("0.0",contents)
            self.textEdit.focus_set()
        

    def save_clicked(self):
        self.fileName = fd.asksaveasfilename()
        if self.fileName:
            with open(self.fileName,'w')as f:
                f.write(self.textEdit.get("0.0",tk.END))
            base = pathlib.Path(self.fileName + "").name
            self.mainwindow.title("pygubu notepad - " + base)
            self.textEdit.focus_set()

    def copy_clicked(self):
        self.mainwindow.clipboard_clear()
        if self.textEdit.tag_ranges(tk.SEL):
            self.mainwindow.clipboard_append(self.textEdit.get(tk.SEL_FIRST,tk.SEL_LAST))
        self.textEdit.focus_set()

    def cut_clicked(self):
        if self.textEdit.tag_ranges(tk.SEL):
            self.mainwindow.clipboard_clear()
            self.mainwindow.clipboard_append(self.textEdit.get(tk.SEL_FIRST,tk.SEL_LAST))
            self.textEdit.delete(tk.SEL_FIRST,tk.SEL_LAST)
        else:
            self.textEdit.delete("0.0",tk.END)
        self.textEdit.focus_set()
        
    def paste_clicked(self):
        self.textEdit.insert(tk.END, self.mainwindow.clipboard_get())
        self.textEdit.focus_set()

    def undo_clicked(self):
        self.textEdit.edit_undo()
        self.textEdit.focus_set()


if __name__ == '__main__':
    app = TextpadApp()
    app.run()


