from operator import index
from tokenize import String
import pandas as pd
import numpy as np

class SCATS:
    def __init__(self,number,longitude,latitude):
        self.number = number
        self.roads = []
        self.connections = []
        self.longitude = longitude
        self.latitude = latitude
    
    def add_connection(self, other_scats):
        if(other_scats in self.connections):
            return
        self.connections.append(other_scats)
    def connected_to_road(self,road):
        if(road in self.roads):
            return True
        return False
    def add_road(self,road_name):
        if(road_name in self.roads):
            return
        
        self.roads.append(road_name)
    def print_debug(self):
        debug_msg = ""
        debug_msg += "SCATS Number: " + str(self.number) +"\n"
        debug_msg += "Longitude: " + str(self.longitude) + "\n"
        debug_msg += "Latitude: " + str(self.latitude) + "\n"
        debug_msg += "Connections to other SCATS: \n"
        
        for connection in self.connections:
            debug_msg += "\t"
            debug_msg += "-" + str(connection.number)
            debug_msg += "\n"
        debug_msg += "Roads: \n"
        for road in self.roads:
            debug_msg += "\t"
            debug_msg += "-" + road
            debug_msg += "\n"
        print(debug_msg)
    
    def share_road_with(self,road_name, other_scats):
        if(road_name in other_scats.roads):
            return True
        
        return False
        
def parse_csv(filename="boroondara.csv"):
    #read df
    scats_df = pd.read_csv(filename, encoding='utf-8').fillna(0)
    #delete the time columns
    df_subset = ['SCATS Number','Location','NB_LATITUDE','NB_LONGITUDE']
    scats_df = scats_df.drop_duplicates(subset=df_subset)
    #take only the necessary columns
    scats_df = scats_df[df_subset]
    #calculate mean coordinates of each scats site with Location
    scats_df = scats_df.groupby(by=['SCATS Number','Location'],).mean().reset_index()
    
    #make 2 subsets: 1 with longlat and 1 with road name
    scats_sites_with_long_lat = scats_df.groupby(by=['SCATS Number']).mean().reset_index()
    
    scats_sites_with_road_names = scats_df[['SCATS Number','Location']]
    
    #create a scats list
    scats_list = []
    
    #create scats objects
    for index in scats_sites_with_long_lat.index:
        scats = SCATS(scats_sites_with_long_lat['SCATS Number'][index], scats_sites_with_long_lat['NB_LONGITUDE'][index], scats_sites_with_long_lat['NB_LATITUDE'][index])
        scats_list.append(scats)
    
    #Add roads to scats
    for scats in scats_list:
        road_connections = scats_sites_with_road_names.loc[scats_sites_with_road_names['SCATS Number']==scats.number]['Location']
        for index in road_connections.index:
            roads = parse_string_to_roads(road_connections[index])
            for road in roads:
                scats.add_road(road)
    
    #Add connection to scats
    scats_vertically_sorted = sorted(scats_list, key=lambda x : float(x.longitude))
    
    scats_horizontally_sorted = sorted(scats_list, key=lambda x : float(x.latitude))
    
    # for scats in scats_horizontally_sorted:
    #     scats.print_debug()
    
    
    for scats in scats_list:
        for road in scats.roads:
            scats_with_same_road = []
            
            for other_scats in scats_vertically_sorted:
                if(scats.share_road_with(road,other_scats)):
                    scats_with_same_road.append(other_scats)
            
            this_scats_index = scats_with_same_road.index(scats)
            if(this_scats_index!=0):
                scats.add_connection(scats_with_same_road[this_scats_index-1])
            if(this_scats_index!=len(scats_with_same_road)-1):
                scats.add_connection(scats_with_same_road[this_scats_index+1])
            
            scats_with_same_road = []
            
            for other_scats in scats_horizontally_sorted:
                if(scats.share_road_with(road,other_scats)):
                    scats_with_same_road.append(other_scats)
            
            this_scats_index = scats_with_same_road.index(scats)
            if(this_scats_index!=0):
                scats.add_connection(scats_with_same_road[this_scats_index-1])
            if(this_scats_index!=len(scats_with_same_road)-1):
                scats.add_connection(scats_with_same_road[this_scats_index+1])
            
                

        
    
    # print(scats_sites_with_road_names)
    for scats in scats_list:
        scats.print_debug()
    return scats_list

def parse_string_to_roads(roads_string):
    splitted_data = split((str(roads_string)),[" of ", " OF "])
    
    #Get the first string to delete the direction
    splitted_data[0] = splitted_data[0].rsplit(" ",1)[0]
    
    return splitted_data
    
def split(txt, seps):
    default_sep = seps[0]

    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]
parse_csv()

