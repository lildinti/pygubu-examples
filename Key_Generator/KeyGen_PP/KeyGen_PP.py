#!/usr/bin/python3
import random
import string
import tkinter as tk
import tkinter.ttk as ttk

class KeygenApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.notebook1 = ttk.Notebook(self.toplevel1)
        self.frame1 = ttk.Frame(self.notebook1)
        self.labelframe3 = ttk.Labelframe(self.frame1)
        self.lbNewKey = ttk.Label(self.labelframe3)
        self.lbNewKey.configure(
            font="{Helvetica} 20 {bold}",
            takefocus=False,
            text="1111-22222-3333-4444-5555",
        )
        self.lbNewKey.grid(column=0, columnspan=5, pady="10 20", row=0)
        self.label2 = ttk.Label(self.labelframe3)
        self.label2.configure(text="Scores:")
        self.label2.grid(column=0, row=1)
        self.tbLoScore = ttk.Entry(self.labelframe3)
        self.tbLoScore.configure(width=4)
        self.tbLoScore.grid(column=1, padx=5, row=1)
        self.tbHiScore = ttk.Entry(self.labelframe3)
        self.tbHiScore.configure(width=4)
        self.tbHiScore.grid(column=2, row=1)
        self.label3 = ttk.Label(self.labelframe3)
        self.label3.configure(text="Check Digit:")
        self.label3.grid(column=3, padx="70 5", row=1)
        self.tbCheckDigit = ttk.Entry(self.labelframe3)
        self.tbCheckDigit.configure(width=1)
        self.tbCheckDigit.grid(column=4, padx="0 5", row=1)
        self.btGenerate = ttk.Button(self.labelframe3)
        self.btGenerate.configure(text="Generate")
        self.btGenerate.grid(
            column=3, columnspan=2, padx="20 0", pady=15, row=2, sticky="e"
        )
        self.btGenerate.configure(command=self.onGenerate_Click)
        self.labelframe3.configure(height=200, text="New Key", width=200)
        self.labelframe3.pack(expand="true", fill="x", padx=5, side="top")
        self.labelframe3.columnconfigure(0, pad=10)
        self.labelframe4 = ttk.Labelframe(self.frame1)
        self.lbScoreGenerated = ttk.Label(self.labelframe4)
        self.lbScoreGenerated.configure(font="{Helvetica} 20 {bold}", text="Score:")
        self.lbScoreGenerated.pack(
            expand="true", fill="x", padx=10, pady=10, side="top"
        )
        self.labelframe4.configure(height=200, text="Validation", width=200)
        self.labelframe4.pack(expand="true", fill="x", padx=5, pady="0 10", side="top")
        self.frame1.configure(height=200, width=200)
        self.frame1.pack(expand="true", fill="both", side="top")
        self.notebook1.add(self.frame1, text="Generate Key")
        self.frame3 = ttk.Frame(self.notebook1)
        self.labelframe5 = ttk.Labelframe(self.frame3)
        self.tbKeyValue = ttk.Entry(self.labelframe5)
        self.tbKeyValue.configure(
            font="{Helvetica} 20 {bold}", justify="center", width=24
        )
        self.tbKeyValue.grid(
            column=0, columnspan=4, padx=30, pady=10, row=0, sticky="e"
        )
        self.label6 = ttk.Label(self.labelframe5)
        self.label6.configure(text="Scores:")
        self.label6.grid(column=0, row=1, sticky="e")
        self.tbVeryfyScore = ttk.Entry(self.labelframe5)
        self.tbVeryfyScore.configure(width=4)
        self.tbVeryfyScore.grid(column=1, padx=0, row=1)
        self.label7 = ttk.Label(self.labelframe5)
        self.label7.configure(anchor="e", text="Check Digit:")
        self.label7.grid(column=2, padx="75 5", row=1, sticky="e")
        self.tbDigitCheck = ttk.Entry(self.labelframe5)
        self.tbDigitCheck.configure(width=1)
        self.tbDigitCheck.grid(column=3, padx="0 5", row=1)
        self.button2 = ttk.Button(self.labelframe5)
        self.button2.configure(text="Verify")
        self.button2.grid(
            column=2, columnspan=2, padx="20 0", pady=15, row=2, sticky="e"
        )
        self.button2.configure(command=self.onVerify_Click)
        self.labelframe5.configure(height=200, text="Key Values", width=200)
        self.labelframe5.pack(expand="true", fill="x", padx=5, side="top")
        self.labelframe5.columnconfigure(0, pad=10)
        self.labelframe6 = ttk.Labelframe(self.frame3)
        self.lbIsValid = ttk.Label(self.labelframe6)
        self.lbIsValid.configure(font="{Helvetica} 20 {bold}", text="Invalid")
        self.lbIsValid.pack(pady=5, side="top")
        self.labelframe6.configure(height=200, text="Validation", width=200)
        self.labelframe6.pack(expand="true", fill="x", padx=5, pady="0 10", side="top")
        self.frame3.configure(height=200, width=200)
        self.frame3.pack(side="top")
        self.notebook1.add(self.frame3, text="Verify Key")
        self.notebook1.configure(height=250, width=380)
        self.notebook1.pack(side="top")
        self.toplevel1.configure(height=250, width=380)
        self.toplevel1.resizable(False, False)
        self.toplevel1.title("Registration Key Generator")


        # Main widget
        self.mainwindow = self.toplevel1
        self.first_init = True
        self.mainwindow.bind('<Map>', self.center_window)

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

    # Verify Key
    def verify(self, key, verifying = False):
        global score            
        score = 0
        if not(verifying):
            check_digit = key[int(self.tbCheckDigit.get())-1]
            score_low = int(self.tbLoScore.get())
            score_high = int(self.tbHiScore.get())
        else:
            check_digit = key[int(self.tbDigitCheck.get())-1]
            score_low = int(self.tbVeryfyScore.get())
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
            self.lbNewKey.configure(text = key)
            print(key)
            self.lbScoreGenerated.config(text=f'Score: {score}')
        else:
            self.generate()

    def run(self):
        self.mainwindow.mainloop()

    def onGenerate_Click(self):
        try:
            self.lbNewKey.configure(text ='')
            self.generate()
        except:
            pass

    def onVerify_Click(self):
        key = self.tbKeyValue.get()
        if self.verify(key,True):
            #self.lbVerifiedScore.config(text=f'Score: {score}')
            self.lbIsValid.config(text = 'Valid')
        else:
            #self.lbVerifiedScore.config(text=f'Score: {score}')
            self.lbIsValid.config(text = 'Invalid')


if __name__ == "__main__":
    app = KeygenApp()
    app.run()
