from http.client import NON_AUTHORITATIVE_INFORMATION
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from io import BytesIO
from tkinter import NONE, messagebox

import pygubu
import requests
from idlelib.tooltip import Hovertip
from PIL import Image, ImageTk

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "apod.ui"


class ApodApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('toplevel1', master)

        # Import tkVariables
        self.strTitle = None
        self.strDate = None
        self.strCopyright = None
        builder.import_variables(self, ['strTitle', 'strDate', 'strCopyright'])

        # Add tooltips to butttons
        entryTip = Hovertip(self.builder.get_object('entr1'),
            'Enter date as YYYY-mm-dd')
        submitTip = Hovertip(self.builder.get_object(
            'button1'), "Get date's picture")
        fullimgTip = Hovertip(self.builder.get_object(
            'button2'), "Show full picture")
        aboutTip = Hovertip(self.builder.get_object(
            'button3'), "About thsi app")

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def submit_clicked(self):
        """Get request data from NASA APOD API"""
        global response

        # Set the parameters for the request
        url = 'https://api.nasa.gov/planetary/apod'
        api_key = 'DEMO_KEY'  # USE YOUR OWN API KEY!!!!
        date = self.builder.get_object('entry1').get()
        querystring = {'api_key': api_key, 'date': date}

        # Call the request and turn it into a python usable format
        response = requests.request("GET", url, params=querystring)
        response = response.json()

        # Set labels to response values
        self.strTitle.set(response['title'])
        self.strDate.set(response['date'])
        if 'copyright' in response:
            self.strCopyright.set(response['copyright'])
        else:
            self.strCopyright.set('')

        # Set textarea text to response value
        self.builder.get_object('text1').insert(0.0, response['explanation'])

        self.get_images()

    def get_images(self):
        # We need to use 3 images in other functions; an img, a thumb, and a full_img
        global img
        global thumb
        global full_img

        url = response['url']

        if response['media_type'] == 'image':
            # Grab the photo that is stored in our response.
            img_response = requests.get(url, stream=True)

            # Get the content of the response and use BytesIO to open it as an an image
            # Kepp a reference to this img as this is what we can use to save the image (Image not PhotoImage)
            # Create the full screen image for a second window
            img_data = img_response.content
            img = Image.open(BytesIO(img_data))

            full_img = ImageTk.PhotoImage(img)

            # Create the thumbnail for the main screen
            thumb_data = img_response.content
            thumb = Image.open(BytesIO(thumb_data))
            thumb.thumbnail((340, 280))
            thumb = ImageTk.PhotoImage(thumb)

            # Set the thumbnail image
            self.builder.get_object('label4').config(image=thumb)
        elif response['media_type'] == 'video':
            self.builder.get_object('label4').config(text=url, image='')
            webbrowser.open(url)

    def fullscreen_clicked(self):
        # Open the full size photo in a new window
        if 'response' in globals():
            top = tk.Toplevel()
            top.title('Full APOD Photo')
            top.iconbitmap('rocket.ico')

            # Load the full image to the new window
            img_label = tk.Label(top, image=full_img)
            img_label.pack()

    def about_clicked(self):
        # Display messgae box with info about app
        messagebox.showinfo(
            'NASA - APOD', "Written in Python, using PYGUBU. \n by C. Olivera")


if __name__ == '__main__':
    app = ApodApp()
    app.run()
