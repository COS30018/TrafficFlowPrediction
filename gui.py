from doctest import master
from enum import unique
from re import sub
import tkinter as tk
import tkintermapview
import pandas as pd


class MapGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        # Get Dataframe of boroondara data
        data_df = pd.read_csv("data/boroondara.csv")
    
        # Set up root window
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Set up map
        self.frame_map = tk.Frame()
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=1600, height=1200, corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.map_widget.set_position(-37.8236299, 145.0699878)  # Paris, France
        self.map_widget.set_zoom(14)
        
        # Mark SCATS
        unique_sites_df = data_df.drop_duplicates(subset=['SCATS Number', 'Location'])
        self.markers = {}
        for _, row in unique_sites_df.iterrows():
            new_marker = self.map_widget.set_marker(row['NB_LATITUDE'], row['NB_LONGITUDE'])
            #new_marker.set_text("SCATS: "+str(row['SCATS Number'])+"\nLocation: "+row['Location'])
            self.markers[row['SCATS Number']] = {row['Location'] : new_marker}
            
        # Pack map widget
        self.map_widget.pack()
    
        # Set up menu
        self.frame_menu = tk.Frame()
        self.menu = tk.Label(master=self.frame_menu, text="MENU HERE")
        self.menu.pack()
        
    
        self.frame_map.pack()
        self.frame_menu.pack()
    
    def start(self):
        self.mainloop()
        

if __name__ == '__main__':
    gui = MapGUI()
    gui.start()