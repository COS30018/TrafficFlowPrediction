from unicodedata import numeric
import pandas as pd

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
        
def parse_csv(filename="data/boroondara.csv"):

    scats_df = pd.read_csv(filename, encoding='utf-8').fillna(0)  
    scats_list = [] 
    index = 0
    while index < scats_df.shape[0] :
        scats = SCATS(scats_df['SCATS Number'][index], scats_df['NB_LONGITUDE'][index], scats_df['NB_LATITUDE'][index]) 
        scats_list.append(scats) 
        currentSCATS = scats_df.iloc[index, 0] #site 970
        while scats_df.iloc[index, 0] == currentSCATS : 
          index+=1
          if index >= scats_df.shape[0] - 1:
              index = scats_df.shape[0]
              break;
 
    #hard code the connections instead.
    for scats in scats_list :
      #for the love of god, don't look at this function
      add_connections(scats, scats_list)
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
 

def check_against(current, aList, connections) :
    for site in aList:
      if site.number in connections :
        current.add_connection(site) 
def add_connections(current, aList) :
    #HARD CODING BAYBEEE
    num = current.number 
    if num == 970:
      check_against(current, aList, [2846, 3685])
    elif num == 2000:
      check_against(current, aList, [3685, 3682, 4043, 3812])
    elif num == 2200:
      check_against(current, aList, [3126, 4063])
    elif num == 2820:
      check_against(current, aList, [4321, 3662, 2825, ])
    elif num == 2825:
      check_against(current, aList, [2827, 4030, 2820])
    elif num == 2827:
      check_against(current, aList, [2825, 4051])
    elif num == 2846:
      check_against(current, aList, [970, 4273, 4043])
    elif num == 3001:
      check_against(current, aList, [3662, 3002, 4262, 4821])
    elif num == 3002:
      check_against(current, aList, [3662, 3001, 4263, 4324, 4035, 3120])
    elif num == 3120:
      check_against(current, aList, [4035, 3122, 4040, 3002])
    elif num == 3122:
      check_against(current, aList, [3120, 3804, 3127])
    elif num == 3126:
      check_against(current, aList, [3682, 2200, 3127])
    elif num == 3127:
      check_against(current, aList, [4063, 3126, 3122])
    elif num == 3180:
      check_against(current, aList, [4057, 4051])
    elif num == 3662:
      check_against(current, aList, [4335, 4324, 3002, 3001, 2820])
    elif num == 3682:
      check_against(current, aList, [3126, 3804, 2000])
    elif num == 3685:
      check_against(current, aList, [2000, 970])
    elif num == 3804:
      check_against(current, aList, [4040, 3812, 3122, 3682])
    elif num == 3812:
      check_against(current, aList, [3804, 4040, 2000, 4043])
    elif num == 4030:
      check_against(current, aList, [2825, 4051, 4032, 4321])
    elif num == 4032:
      check_against(current, aList, [4030, 4057, 4034, 4321])
    elif num == 4034:
      check_against(current, aList, [4032, 4063, 4324, 4035])
    elif num == 4035:
      check_against(current, aList, [4034, 3120, 3002])
    elif num == 4040:
      check_against(current, aList, [3120, 3804, 3812, 4272, 4043])
    elif num == 4043:
      check_against(current, aList, [4273, 4040, 2000, 2846])
    elif num == 4051:
      check_against(current, aList, [2827, 3180, 4030, ])
    elif num == 4057:
      check_against(current, aList, [3180, 4032, 4063, 2200])
    elif num == 4063:
      check_against(current, aList, [4057, 4034, 2200, 3127])
    elif num == 4262:
      check_against(current, aList, [3001, 4263, 4821, 4812])
    elif num == 4263:
      check_against(current, aList, [3002, 4264, 4262])
    elif num == 4264:
      check_against(current, aList, [4270, 4266, 4263, 4035, 4324])
    elif num == 4266:
      check_against(current, aList, [4264, 4272, 4040, 3120])
    elif num == 4270:
      check_against(current, aList, [4264, 4266, 4272, 4263, 4812])
    elif num == 4272:
      check_against(current, aList, [4266, 4040, 4270, 4273])
    elif num == 4273:
      check_against(current, aList, [4043, 4272])
    elif num == 4321:
      check_against(current, aList, [4030, 4032, 4335, 2820])
    elif num == 4324:
      check_against(current, aList, [4264, 3002, 4335, 3662, 4034])
    elif num == 4335:
      check_against(current, aList, [3662, 4321, 4324])
    elif num == 4812:
      check_against(current, aList, [4270, 4262, 4263])
    elif num == 4821:
      check_against(current, aList, [3001, 4262])
	  
	  

parse_csv()

