import tkinter as tk
from tkinter import ttk
import tkintermapview
import pandas as pd
import graph_search as gs
from geopy.geocoders import Nominatim
import requests


class MapGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        # Get Dataframe of boroondara data
        data_df = pd.read_csv("data/boroondara.csv")
        self.unique_scats = list(data_df.groupby(['SCATS Number']).groups)
        
        # Set up root window
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Set up map
        self.frame_map = tk.Frame()
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=1600, height=1200, corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.map_widget.set_position(-37.8236299, 145.0699878)  # Paris, France
        self.map_widget.set_zoom(14)
        
        ## Mark SCATS
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
        ## Starting SCATS input
        self.dropdown_start_selected = tk.IntVar()
        self.dropdown_start = ttk.Combobox(master=self.frame_menu, textvariable=self.dropdown_start_selected, values=self.unique_scats, state='readonly')
        self.dropdown_start.pack(side=tk.LEFT, padx=20, pady=20)
        ## Destination SCATS input
        self.dropdown_dest_selected = tk.IntVar()
        self.dropdown_dest = ttk.Combobox(master=self.frame_menu, textvariable=self.dropdown_dest_selected, values=self.unique_scats, state='readonly')
        self.dropdown_dest.pack(side=tk.LEFT, padx=20, pady=20)
        ## Navigate button
        self.nav_button = tk.Button(master=self.frame_menu, text="Navigate", command=self.generate_route)
        self.nav_button.pack(padx=20, pady=20)
    
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



    def generate_route(self):
        scats_list = gs.parse_csv()
        
        A_star_search = gs.SearchAStar(7)
        
        start_num = self.dropdown_start_selected.get()

        #970 - 2827
        #4821 - 2000
        #3180 - 4812
        #4812 - 3180
        #start_num = 4812
        
        end_num = self.dropdown_dest_selected.get()
        #end_num = 3180

        start_point = gs.search_scats(scats_list,start_num)
        end_point = gs.search_scats(scats_list,end_num)
        
        if(start_point is None):
            print('Start point not found')
            exit()
        
        if(end_point is None):
            print('End point not found')
            exit()
            
        solutions = A_star_search.search(start_point,end_point)
        if(len(solutions)==0):
            print("No possible paths found")
        else:
            print("amt of solutions: " + str(len(solutions)))
            for solution in solutions:
                
                path_coords = [] 
                for point in solution: 
                    path_coords.append((point.scats.latitude, point.scats.longitude))

                #path = self.map_widget.set_path(path_coords)

                
                lat_lons = [self.get_lat_long_from_address(addr) for addr in path_coords]

                responses = []
                for n in range(len(lat_lons)-1):
                    lat1, lon1, lat2, lon2 = lat_lons[n][0], lat_lons[n][1], lat_lons[n+1][0], lat_lons[n+1][1]
                    response = self.get_directions_response(lat1, lon1, lat2, lon2, mode='walk')
                    responses.append(response)

                df = pd.DataFrame()
                # add markers for the places we visit
                for point in lat_lons:
                    #this for loop can add markers to every 'visit' location 
                    #folium.Marker(point, popup="[" + str(point[0]) + ", " + str(point[1]) + "]").add_to(m)
                    break
                # loop over the responses and plot the lines of the route
                for response in responses:
                  mls = response.json()['features'][0]['geometry']['coordinates']
                  points = [(i[1], i[0]) for i in mls[0]]
  
                  # add the lines
                  self.map_widget.set_path(points)
                  #folium.PolyLine(points, weight=5, opacity=1).add_to(m)
                  temp = pd.DataFrame(mls[0]).rename(columns={0:'Lon', 1:'Lat'})[['Lat', 'Lon']]
                  df = pd.concat([df, temp])

                print("")
                #gs.print_solution(solution)
    
    def start(self):
        self.generate_route()
        self.mainloop()
        

if __name__ == '__main__':
    gui = MapGUI()
    gui.start()