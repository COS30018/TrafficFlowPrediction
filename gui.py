from importlib.resources import path
import tkinter as tk
from tkinter import Label, ttk
from matplotlib.pyplot import sca
import tkintermapview
import pandas as pd
import requests 
from geopy.geocoders import Nominatim

import graph_search as gs


class MapGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        # Get Dataframe of boroondara data
        data_df = pd.read_csv("data/boroondara.csv")
        self.unique_scats = list(data_df.groupby(['SCATS Number']).groups)
        
        # Set up root window
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Set up map
        self.frame_map = tk.Frame()
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=1000, height=500, corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.map_widget.set_position(-37.8236299, 145.0699878)  # Paris, France
        self.map_widget.set_zoom(14)
        
        ## Mark SCATS
        unique_sites_df = data_df.drop_duplicates(subset=['SCATS Number', 'Location'])
        self.markers = {}
        for _, row in unique_sites_df.iterrows():
            new_marker = self.map_widget.set_marker(row['NB_LATITUDE'], row['NB_LONGITUDE'])
            new_marker.set_text(str(row['SCATS Number']))
            self.markers[row['SCATS Number']] = {row['Location'] : new_marker}
            
        # Pack map widget
        self.map_widget.pack()
    
        # Set up menu
        self.frame_menu = tk.Frame()
        ## Starting SCATS label
        self.start_label = Label(master=self.frame_menu, text="Start:")
        self.start_label.pack(side=tk.LEFT)
        ## Starting SCATS input
        self.dropdown_start_selected = tk.IntVar()
        self.dropdown_start = ttk.Combobox(master=self.frame_menu, textvariable=self.dropdown_start_selected, values=self.unique_scats, state='readonly')
        self.dropdown_start.pack(side=tk.LEFT, padx=20, pady=20)
        ## Destination SCATS label
        self.dest_label = Label(master=self.frame_menu, text="Destination:")
        self.dest_label.pack(side=tk.LEFT)
        ## Destination SCATS input
        self.dropdown_dest_selected = tk.IntVar()
        self.dropdown_dest = ttk.Combobox(master=self.frame_menu, textvariable=self.dropdown_dest_selected, values=self.unique_scats, state='readonly')
        self.dropdown_dest.pack(side=tk.LEFT, padx=20, pady=20)
        ## Navigate button
        self.routes = [] # Found routes
        self.path = None # Currently shown path
        self.nav_button = tk.Button(master=self.frame_menu, text="Navigate", command=self.generate_routes)
        self.nav_button.pack(side=tk.LEFT, padx=20, pady=20)
        ## Route selection label
        self.route_label = Label(master=self.frame_menu, text="Route:")
        self.route_label.pack(side=tk.LEFT)
        ## Route selection dropdown
        self.dropdown_route_selected = tk.IntVar()
        self.dropdown_route_values = []
        self.dropdown_route = ttk.Combobox(master=self.frame_menu, textvariable=self.dropdown_route_selected, values=self.dropdown_route_values, state='readonly' )
        self.dropdown_route.bind('<<ComboboxSelected>>', self.draw_path)
        self.dropdown_route.pack(side=tk.LEFT, padx=20, pady=20)
        ## Route time label
        self.time_label = Label(master=self.frame_menu, text="Time:")
        self.time_label.pack(side=tk.LEFT)
        ## Route time estimation
        self.total_seconds = [] # Time for found routes
        self.time_est_value = tk.IntVar()
        self.time_est = Label(master=self.frame_menu, textvariable=self.time_est_value)
        self.time_est.pack(side=tk.LEFT)
    
        # Pack frames
        self.frame_map.pack()
        self.frame_menu.pack(side=tk.BOTTOM)
    
    def get_lat_long_from_address(self, address):
        if type(address) == str :
            locator = Nominatim(user_agent='myGeocoder')
            location = locator.geocode(address)
            return location.latitude, location.longitude
        else :
            return address 

    def get_directions_response(self, lat1, long1, lat2, long2, mode='Drive'):
        url = "https://route-and-directions.p.rapidapi.com/v1/routing"
        key = "ab885194e0mshfeb1f467af853bcp19b10bjsn5a46125b5464"
        host = "route-and-directions.p.rapidapi.com"
        headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": host}
        querystring = {"waypoints":f"{str(lat1)},{str(long1)}|{str(lat2)},{str(long2)}","mode":mode}
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response

    def generate_routes(self):
        self.routes.clear()
        self.total_seconds.clear()
        scats_list = gs.parse_csv()
        
        data_df, scaler = gs.process_data()

        A_star_search = gs.SearchAStar(data_df=data_df, scaler=scaler)
        
        start_num = self.dropdown_start_selected.get()
        
        end_num = self.dropdown_dest_selected.get()
        
        start_point = gs.search_scats(scats_list,start_num)
        end_point   = gs.search_scats(scats_list,end_num)
        
        solutions = A_star_search.search(start_point,end_point)
        if(len(solutions)==0):
            print("No possible paths found")
        else:
            for solution in solutions:
                
                self.total_seconds.append(int(solution[0].cost))

                gs.print_solution(solution) 
                path_coords = [(start_point.latitude, start_point.longitude)]
                for point in solution:
                    path_coords.append((point.scats.latitude, point.scats.longitude))

                path_coords.append((end_point.latitude, end_point.longitude))

                responses = []
                for n in range(len(path_coords)-1):
                    lat1, lon1, lat2, lon2 = path_coords[n][0], path_coords[n][1], path_coords[n+1][0], path_coords[n+1][1]
                    response = self.get_directions_response(lat1, lon1, lat2, lon2, mode='drive')
                    responses.append(response)

                #for point in lat_lons
                # loop over the responses and plot the lines of the route
                points = []
                thisRoute = []
                for response in responses:
                  mls = response.json()['features'][0]['geometry']['coordinates']
                  points = [(i[1], i[0]) for i in mls[0]]
                  thisRoute = thisRoute + points
                
                self.routes.append(thisRoute)
                self.dropdown_route['values'] = list(range(1, len(self.routes)+1))

            print("Found routes")

    def draw_path(self, _):

        if (self.path != None):
            self.path.delete()

        self.path = self.map_widget.set_path(self.routes[self.dropdown_route_selected.get()-1])
        time = self.to_mins(self.total_seconds[self.dropdown_route_selected.get()-1])
        self.time_est_value.set(time)
        
        
    def to_mins(self, seconds):
        seconds = seconds % (24 * 3600)
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
         
        return "%02d mins, %02d secs" % (minutes, seconds)
        

    
    
    def start(self): 
        self.mainloop()
        

if __name__ == '__main__':
    gui = MapGUI()
    gui.start()