import geopy.distance

class Node:
    def __init__(self, scats, parent=None, cost=0):
        self.scats = scats
        self.parent = parent
        self.cost = cost
        self.heuristic_value = 0
    
    def set_heuristic_value(self, value):
        self.heuristic_value = value

    def explore_available_children(self):
        for other_scats in self.scats.connections:
            child_node = Node(other_scats,self)
            
            
    def calculate_cost(self):
        parent_coords = (float(self.parent.scats.latitude),float(self.parent.scats.longitude))
        this_coords = (float(self.scats.latitude),float(self.scats.longitude))
        #calculate distance in km using geopy
        distance_from_parent = geopy.distance.geodesic(parent_coords,this_coords).km
        cost = self.parent.cost + distance_from_parent
        
        return cost
    
    def set_cost(self, value):
        self.cost = value
        
    def get_path_to_node(self):
        if(self.parent==None):
            return [self]
        return [self] + self.parent.get_path_to_node()
        
class Graph:
    def __init__(self, nodes):
        self.nodes = nodes