from pyexpat import model
import math 
import geopy.distance
from map_parser import parse_csv
from predict import precict,process_data, load_model_file
from datetime import datetime, timedelta

MAX_SPEED = 60

def round_dt(dt, delta=timedelta(minutes=15)):
    return datetime.min + round((dt - datetime.min) / delta) * delta

def flow_to_speed(flow):
    flow = int(flow)
    speed = (62.5 + math.sqrt(3906.25 + 3.908*int(flow)))/2.153125
    print(speed)
    if(speed>MAX_SPEED):
        speed = MAX_SPEED
    elif(speed<5):
        speed = 5
    
    
    return speed
class Model:
    def __init__(self,model_number,model):
        self.model_number = model_number
        self.model = model
    def is_model(self,model_number):
        if(str(self.model_number) == str(model_number)):
            return True
        
        return False
    

class Node:
    def __init__(self, scats, parent=None,):
        self.scats = scats
        self.parent = parent
        self.heuristic_value = 0
        self.cost = 0
        self.traversed_scats = self.initiate_traversed_scats_list()
        
    def initiate_traversed_scats_list(self):
        if(self.parent is None):
            return []
        return self.parent.traversed_scats
        
    def add_traversed_scats(self,scats):
        self.traversed_scats.append(scats)
        
    def set_heuristic_value(self, value):
        self.heuristic_value = value
    
    def went_through_scats(self,scats):
        for traversed_s in self.traversed_scats:
            if(scats.number == traversed_s.number):
                return True
            
        return False  
      
    def explore_available_children(self):
        child_nodes = []
        for other_scats in self.scats.connections:
            if(not self.went_through_scats(other_scats)):
                child_node = Node(other_scats,parent=self)
                child_node.add_traversed_scats(self.scats)
                child_nodes.append(child_node)
                
        return child_nodes
    
    def calculate_cost(self, data_df, scaler, model, default_cost=30):
        cost = default_cost
        if(self.parent is None):
            return cost
        #calculate distance in km using geopy
        distance_from_parent = self.distance_from(self.parent.scats)
        
        #predict the traffic flow
        traffic_flow = precict(self.scats.number,round_dt(datetime.now()),data_df=data_df,scaler=scaler,model=model)
        speed = flow_to_speed(traffic_flow)
        
        cost += (float)(distance_from_parent/speed)*3600
        
        cost += self.parent.cost
        
        
        return cost
    def distance_from(self,end_point):
        this_coords = (float(self.scats.latitude),float(self.scats.longitude))
        
        end_point_coords = (float(end_point.latitude),float(end_point.longitude))
        
         #calculate distance in km using geopy
        distance = geopy.distance.geodesic(end_point_coords,this_coords).km
        
        return distance
    
    def set_cost(self, value):
        self.cost = value
        
    def get_path_to_node(self):
        if(self.parent==None):
            return [self]
        return [self] + self.parent.get_path_to_node()
    def is_scats(self,destination_scats):
        return self.scats == destination_scats
    
    
        
class SearchAStar:
    def __init__(self, data_df, scaler,solution_size=5):
        self.frontier = []
        self.solution_size = solution_size
        self.data_df = data_df
        self.scaler = scaler
        self.models = []
        
    def add_to_frontier(self,node):
        self.frontier.append(node)
    
    
    def pop_frontier(self):
        return self.frontier.pop()
    
    def search(self,start_scats, end_scats):
        solutions = []
        #first add the start node to frontier
        self.add_to_frontier(Node(scats=start_scats))
        
        #loop over the frontier
        while(len(self.frontier)>0):
           
            
            current_node = self.pop_frontier()
            
            if(current_node.is_scats(end_scats)):
                solutions.append(current_node.get_path_to_node())
            
            #if number of solutions reached
            if(len(solutions)==self.solution_size):
                return solutions
            
            #if not the goal, explore this node
            child_nodes = current_node.explore_available_children()
            for child_node in child_nodes:
                #calculate cost
                
                cost = child_node.calculate_cost(data_df=self.data_df, scaler=self.scaler,model=self.get_model(child_node.scats.number).model)
                child_node.set_cost(cost)
                
                #calculate heuristic function
                heuristic_value = self.calculate_heuristic(child_node,end_scats)
                child_node.set_heuristic_value(heuristic_value)
                
                #add to frontier
                self.add_to_frontier(child_node)
            #finally sort the frontier
            self.frontier.sort(key=lambda x: x.heuristic_value,reverse=True)
            
        return solutions
    def get_model(self,scats_number):

        for model in self.models:
            if(model.is_model(scats_number)):
                return model
        
        new_model = Model(scats_number,load_model_file('lstm',scats_number))
        self.models.append(new_model)
        return new_model
    def calculate_heuristic(self, node, end_scats):
        #f = g + h
        g = node.cost
        
        h = node.distance_from(end_scats)/MAX_SPEED*3600
        
        f = g + h
        
        return f
    
def search_scats(scats_list, scats_number):
    for scats in scats_list:
        if(scats.number == scats_number):
            return scats
        
    return None

def print_solution(solution):
    solution.reverse()
    path = ""
    first_node = solution.pop(0)
    
    path += str(first_node.scats.number)
    
    for node in solution:
        path += " -> "
        path += str(node.scats.number)
    print(path)
    
    last_node = solution.pop(-1)
    
    total_second = int(last_node.cost)
    print("Total seconds: " +  str(total_second))
    

def main():
    scats_list = parse_csv()
    
    data_df, scaler = process_data()
    
    
    A_star_search = SearchAStar(data_df=data_df,scaler=scaler)
    
    start_num = int(input('Enter start point: '))
    
    end_num = int(input('Enter end point: '))
    
    start_point = search_scats(scats_list,start_num)
    end_point = search_scats(scats_list,end_num)
    
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
        for solution in solutions:
            print_solution(solution)
    
    
    

main()    