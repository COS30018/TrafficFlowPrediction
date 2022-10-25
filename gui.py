from enum import unique
from re import sub
import tkinter
import tkintermapview
import pandas as pd

def main():
    
    # Create and start map at Boroondora
    window_w = 1600
    window_h = 1200

    root = tkinter.Tk()
    root.geometry(f"{window_w}x{window_h}")
    
    map_widget = tkintermapview.TkinterMapView(root, width=window_w, height=window_h, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    
    map_widget.set_position(-37.81157, 145.00978)  # Paris, France
    map_widget.set_zoom(15)
    
    # Mark SCATS
    data_df = pd.read_csv("data/boroondara.csv")
    unique_sites_df = data_df.drop_duplicates(subset=['SCATS Number', 'Location'])
    markers = {}
    for _, row in unique_sites_df.iterrows():
        new_marker = map_widget.set_marker(row['NB_LATITUDE'], row['NB_LONGITUDE'])
        markers[row['SCATS Number']] = {row['Location'] : new_marker}
    
    root.mainloop()
    

if __name__ == '__main__':
    main()