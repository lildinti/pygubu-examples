#!/usr/bin/python3
import pathlib
import tkinter
from tkinter import messagebox
import tkinter.ttk as ttk
import pygubu
from tkinter import ACTIVE, filedialog as fd
import os
import pygame

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "player.ui"


class PlayerApp:

    def __init__(self, master=None):
        pygame.mixer.init()
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        # Main menu
        _main_menu = builder.get_object("menu1", self.mainwindow)
        self.mainwindow.configure(menu=_main_menu)

        # song list with just name and extension used for Listbox
        self.song_list = [] 

        # song list with full name (including path) to play
        self.songs = []

        # Reference to Listbox
        self.lb=self.builder.get_object("song_box")

        # Playlist varaiable populated with song_list
        self.playlist = None
        builder.import_variables(self, ["playlist"])

        builder.connect_callbacks(self)

    def add_song(self):
        # Ask file to add
        filename = fd.askopenfile(
            title='Select song file', initialdir='/', filetypes=(('MP3 Files', '*.mp3'),))
        self.songs.append(filename.name)
        # Get just name and extension to display in listbox
        self.song_list.append(os.path.basename(filename.name))
        self.playlist.set(self.song_list)

    def add_multiple_songs(self):
        print("adding many songs")

    def delete_song(self):
        # Delete selected song if deletion confirmed
        if messagebox.askyesno("Delete Song","really deleete song?"):
             index = self.get_song_index()
             self.lb.delete(index)
             self.song_list.pop(index)

    def delete_all_songs(self):
        # Delete all songs if deletion confirmed
        if messagebox.askyesno("Delete all songs","Delete playlist?"):
            pygame.mixer.music.stop()
            self.song_list.clear()
            self.lb.delete(0,tkinter.END)


    def run(self):
        self.mainwindow.mainloop()

    # Select and play previous song
    def previous_song(self):
        # Get Selected song index
        index = self.get_song_index()
        # Verify can move to previous song
        if index > 0:
            index -= 1
            # Change selection on listbox
            self.lb.select_clear(0,'end')
            self.lb.selection_set(index)
            self.lb.activate(index)
            # Get full name of song to play (previous song)
            song_name = self.songs[index]
            # Play it!
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0)               

    def play_song(self):
        # Get full name of song to play (selected song)
        song_name = self.songs[self.get_song_index()]
        # Play it!
        pygame.mixer.music.load(song_name)
        pygame.mixer.music.play(loops=0)

    def stop_song(self):
        pygame.mixer.music.stop()   

    def pause_song(self):
        # check if player is currently playing song
        if pygame.mixer.music.get_busy() == True:
            # Pause it!
            pygame.mixer.music.pause()
        else:
            # Unpause it
            pygame.mixer.music.unpause()

    # Select and play next song
    def next_song(self):
        # Get Selected song index
        index = self.get_song_index()
        # Verifyy and move to next song
        if index < len(self.songs)-1:
            index +=1
            # Change selection on listbox
            self.lb.select_clear(0,'end')
            self.lb.selection_set(index)
            self.lb.activate(index)
            # Get full name of song to play (next song)
            song_name = self.songs[index]
            # Play it!
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0)

    # Get index of selected son in listbox
    def get_song_index(self):
        song_index = self.lb.curselection()[0]
        return song_index


if __name__ == "__main__":
    app = PlayerApp()
    app.run()
