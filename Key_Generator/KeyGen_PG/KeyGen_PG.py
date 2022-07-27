#!/usr/bin/python3
import pathlib
import pygubu
import string
import random

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "KeyGen_PG.ui"


class GenkeyPgApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)

        self.newKey = None
        self.scoreLo = None
        self.scoreHi = None
        self.checkDigit = None
        self.scoreGenerated = None
        self.keyValue = None
        self.veerifyScore = None
        self.digitCheck = None
        self.isValid = None
        builder.import_variables(
            self,
            [
                "newKey",
                "scoreLo",
                "scoreHi",
                "checkDigit",
                "scoreGenerated",
                "keyValue",
                "veerifyScore",
                "digitCheck",
                "isValid",
            ],
        )

        builder.connect_callbacks(self)
        # Main widget
        self.first_init = True
        self.mainwindow.bind('<Map>', self.center_window)

    def run(self):
        self.mainwindow.mainloop()

    # Event Handler
    def onGenerate_Click(self):
        try:
            self.newKey.set('')
            self.generate()
        except:
            pass
        
    # Event Handler

    def onVerify_Click(self):
        key = self.keyValue.get()
        if self.verify(key,True):
            self.isValid.set('Valid')
        else:
            self.isValid.set('Invalid')
    
    # Center window on screen
    def center_window(self, event=None):
        if self.first_init:
            toplevel = self.mainwindow
            height = toplevel.winfo_height()
            width = toplevel.winfo_width()
            x_coord = int(toplevel.winfo_screenwidth() / 2 - width / 2)
            y_coord = int(toplevel.winfo_screenheight() / 2 - height / 2)
            geom = f'{width}x{height}+{x_coord}+{y_coord}'
            toplevel.geometry(geom)
            self._first_init = False

    # Generate New Key
    def generate(self):

        key = ''
        section = ''
        alphabet = string.ascii_letters + string.digits

        while len(key) < 25:
            char = random.choice(alphabet)
            key += char
            section += char

            if len(section) == 4:
                key += '-'
                section = ''

        key = key[:-1]

        if self.verify(key):
            self.newKey.set(key)
            print(key)
            self.scoreGenerated.set(f'Score: {score}')
        else:
            self.generate()

    # Verify Key
    def verify(self, key, verifying = False):
        global score            
        score = 0
        if not(verifying):
            check_digit = key[int(self.checkDigit.get())-1]
            score_low = int(self.scoreLo.get())
            score_high = int(self.scoreHi.get())
        else:
            check_digit = key[int(self.digitCheck.get())-1]
            score_low = int(self.veerifyScore.get())
            #score_high = int(self.tbScoreHi.get())

        check_digit_count = 0

        chunks = key.split('-')
        for chunk in chunks:
            if len(chunk) != 4:         
                return False
            
            for char in chunk:
                if char == check_digit:
                    check_digit_count += 1
                score += ord(char)
        if not(verifying):
            if score > score_low and score < score_high and check_digit_count ==4:
                return True
            else:
                return False
        else:
            if score == score_low and check_digit_count ==4:
                return True
            else:
                return False


if __name__ == "__main__":
    app = GenkeyPgApp()
    app.run()
