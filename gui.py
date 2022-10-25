from doctest import master
from enum import unique
from re import sub
import tkinter as tk
import tkintermapview
import pandas as pd

def main():
    
    # Set up root window
    root = tk.Tk()
    
    # Set up map
    frame_map = tk.Frame()
    map_widget = tkintermapview.TkinterMapView(frame_map, width=1600, height=1200, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    map_widget.set_position(-37.8236299, 145.0699878)  # Paris, France
    map_widget.set_zoom(14)
    
    # Mark SCATS
    data_df = pd.read_csv("data/boroondara.csv")
    unique_sites_df = data_df.drop_duplicates(subset=['SCATS Number', 'Location'])
    markers = {}
    for _, row in unique_sites_df.iterrows():
        new_marker = map_widget.set_marker(row['NB_LATITUDE'], row['NB_LONGITUDE'])
        #new_marker.set_text("SCATS: "+str(row['SCATS Number'])+"\nLocation: "+row['Location'])
        markers[row['SCATS Number']] = {row['Location'] : new_marker}
        
    # Set up menu
    frame_menu = tk.Frame()
    menu = tk.Label(master=frame_menu, text="MENU HERE")
    menu.pack()
    

    map_widget.pack()
    frame_map.pack()
    frame_menu.pack()

    root.mainloop()
    

if __name__ == '__main__':
    main()