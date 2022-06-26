#!/usr/bin/python3
import pathlib
import tkinter.ttk as ttk
import pygubu
from ttkthemes import ThemedStyle

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "Calculator.ui"


class CalculatorApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)

        self.equation = None
        builder.import_variables(self, ["equation"])

        builder.connect_callbacks(self)
        self.style = ThemedStyle() # Enable ttk theme
        self.style.set_theme("radiance")# Set tthem to radiance (Unix-style)
        self.equation.set('0')

    def run(self):
        self.mainwindow.mainloop()

    def press_key(self, widget_id):
         # trim pressed key (widget_id) to number or operator
        widget_id = widget_id.replace('button','')
        # replcae widget_id if porator or deciaml dot.
        match widget_id:
            case'mult':
                widget_id = '*'
            case'div':
                widget_id = '/'
            case'min':
                widget_id = '-'
            case'plus':
                widget_id = '+'
            case'dec':
                widget_id = '.'
        # Get equation from display
        current_value = self.equation.get()
    
        if current_value == '0': # if equation is "0"
            self.equation.set(widget_id)
        else:
            self.equation.set(current_value + widget_id)
            

    def clear(self):
        self.equation.set('0') # Clear display to 0

    def clear_all(self):
        self.equation.set('0') # Clear display to 0

    def resolve(self):
        current_value = str(eval(self.equation.get())) # calculate result

        if '.0' in current_value: # remove for 0 decimal to the right
            current_value = str(int(eval(self.equation.get())))

        if len(current_value) > 13: # truncet to 13 digits
            current_value=current_value[0:13]

        self.equation.set(current_value)# display result


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
