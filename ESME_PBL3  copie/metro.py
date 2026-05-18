import json
import heapq
from collections import deque 

#Nomalize to have no accent
def normalize(text):
  text=text.strip().lower() #remove space at biginnig and end + minuscule 
  accents={
    'à':'a','â':'a','á':'a',
    'é':'e','è':'e','ê':'e','ë':'e',
    'î':'i','ï':'i','ì':'i','í':'i',
    'ô': 'o', 'ö': 'o', 'ó': 'o',
    'ù': 'u', 'û': 'u', 'ú': 'u', 'ü': 'u',
    'ç': 'c', 'ñ': 'n'
  }
  return "".join(accents.get(c,c) for c in text #parcours the text and replace it with the version without accent
  #without join, we would have a list

# LOAD DATA
def load_data(city_name): 
    
    # Construct the file path based on the chosen city name
    file_path = f"data/{city_name}.json" 
 
    try: 
        # Attempt to open the JSON file in read mode with UTF-8 encoding
        with open(file_path, "r", encoding="utf-8") as file: 
            # Parse the JSON file and store its contents in the 'data' variable
            data = json.load(file) 
 
    except FileNotFoundError: 
        # If the specific city JSON file does not exist, print an error and stop
        print("File not found") 
        return None 
 
    # Return the extracted information as a tuple to be used later in the script
    return ( 
        data["lignes"], 
        data["connexions"], 
        data["correspondances"], 
        data["temps_moyen"] 
    )


#BUILD GRAPH 

def build_graph(lignes, connexions, correspondances, temps_moyen): 
    graph = {} 
    if connexions:
        for conn in connexions: 
            #take values from the dictonnary 
            s1 = conn["de"] 
            s2 = conn["vers"] 
            temps = conn["temps"] 
            ligne = conn["ligne"]
          
	          #each station store a list of neighbors 
            if s1 not in graph: 
                graph[s1] = [] 
            if s2 not in graph: 
                graph[s2] = [] 

            graph[s1].append((s2, temps, ligne)) 
            graph[s2].append((s1, temps, ligne)) 
          
    else: 
        #go through every stations for each line 
        for ligne_id, ligne_data in lignes.items(): 
            stations = ligne_data["stations"]
            for i in range(len(stations) - 1): 
                s1 = stations[i] 
                s2 = stations[i + 1] 
              
                if s1 not in graph: 
                    graph[s1] = [] 
                if s2 not in graph: 
                    graph[s2] = [] 
                  
	              #add connexions 
                graph[s1].append((s2, temps_moyen, ligne_id)) 
                graph[s2].append((s1, temps_moyen, ligne_id)) 
    
    #add transfer stations 
    for corr in correspondances: 
        station = corr["station"] 
        if station not in graph: 
            graph[station] = [] 
    return graph
#BFS
def bfs_shortest_path(graph, start, end):
    visited = set()  # Tracks stations already fully explored
    queue = deque([(start, [(start, None)])])  # Each entry: (current station, path taken so far)

    while queue:  # Keep exploring until no stations remain
        current, path = queue.popleft()  # Process the station that was added first (FIFO)

        if current == end:  # Destination reached: BFS guarantees this is the shortest path
            return path

        if current not in visited:  # Skip if already explored from a shorter path
            visited.add(current)  # Mark as explored before queuing neighbors

            for neighbor, weight, line in graph[current]:  # Iterate over adjacent stations
                if neighbor not in visited:  # Avoid re-queuing already explored stations
                    queue.append((neighbor, path + [(neighbor, line)]))  # Extend path with the metro line used

    return []
#DFS
def dfs(graph, start, visited=None):
    if visited is None:  # Avoid mutable default argument bug: create a fresh set on first call
        visited = set()

    visited.add(start)  # Mark current station as visited before exploring neighbors

    for neighbor, weight, line in graph[start]:  # Check all stations directly connected to current
        if neighbor not in visited:  # Only recurse into unvisited stations
            dfs(graph, neighbor, visited)  # Recursive call: go deeper into the graph

    return visited  # Return the full set of stations reachable from start


# DIJKSTRA


def dijkstra(graph, start, end): 
 
    # Initialize a priority queue with the starting node and a distance of 0
    queue = [(0, start)] 
 
    # Set the initial distance to all nodes to infinity
    distances = {node: float("inf") for node in graph} 
    distances[start] = 0 
 
    # Track the previous node to reconstruct the path later
    previous = {node: None for node in graph} 
    # Track the line used to reach the node to calculate transfer penalties
    previous_line = {node: None for node in graph} 
 
    # Continue until there are no more nodes to evaluate in the queue
    while queue: 
 
        # Pop the node with the shortest known distance from the priority queue
        current_distance, current_node = heapq.heappop(queue) 
 
        # If we have reached the destination, we can stop searching to save time
        if current_node == end: 
            break 
 
        # Iterate through all adjacent stations (neighbors)
        for neighbor, weight, line in graph[current_node]: 
 
            transfer_cost = 0 
 
            # Apply a time penalty (120 seconds) if the passenger needs to change lines
            if previous_line[current_node] is not None and line != previous_line[current_node]: 
                transfer_cost = 120 
 
            # Calculate the total time to reach the neighbor through the current node
            new_dist = current_distance + weight + transfer_cost 
 
            # If this new path is faster than any previously found path to this neighbor
            if new_dist < distances[neighbor]: 
 
                # Update the shortest distance and how we got there
                distances[neighbor] = new_dist 
                previous[neighbor] = current_node 
                previous_line[neighbor] = line 
 
                # Add the neighbor and its new distance to the priority queue
                heapq.heappush(queue, (new_dist, neighbor)) 
 
    # Return the dictionaries needed to trace the fastest route back to the start
    return distances, previous, previous_line

#REBUILD PATH 

def get_path(previous, previous_line, start, end): 
    path = [] 
    current = end	#start with the end 

    while current is not None: 
        path.append((current, previous_line[current]))	#add current station 
        current = previous[current] 
      
    path.reverse()	#put the path in the right order 
  
    #Fix start line 
    if len(path) > 1: 
        path[0] = (path[0][0], path[1][1]) 

    return path 
#MAIN

if __name__ == "__main__":

    while True: #loop that continues until the user quit

        print("\n===== METRO ROUTE PLANNER =====")

        city = input("Choose city (paris, lyon, lille, bordeaux): ").lower()

        data = load_data(city)

        if data is None:
            continue #if the file is not found, skip to the next iteration

        lignes, connexions, correspondances, temps_moyen = data #unpack the data into 4 variables

        graph = build_graph(lignes, connexions, correspondances, temps_moyen) #build the graph from the loaded data

        print("\nTransfer stations:")
        for c in correspondances: #Loop through all transfer stations and display them
            print("-", c["station"])

		#dictionary mapping normalized station names to their real names
        #allows the user to type without accents or majuscule
        station_map = {normalize(s): s for s in graph}

        start_input = normalize(input("\nDeparture station: ")) #ask departure station and normalize the input
        end_input = normalize(input("Arrival station: ")) #same for the arrival

        start = station_map.get(start_input) #find the real station name from the normalized input
        end = station_map.get(end_input) #same for the arrival

        if start is None or end is None: #if one of the station is not find in the graph 
            print("Invalid station")
            continue #ask again

 # BFS 

        bfs_path = bfs_shortest_path(graph, start, end)  #finds the path with the fewest stations

        print("\nFEWEST STOPS (BFS)") 

        for station, line in bfs_path: #display the station and metro line
            print(f"-> {station}" + (f" (line {line})" if line else "")) 

        print(f"\nStops: {len(bfs_path) - 1}") #dis^lay number of stops

 

        # DFS 

        visited = dfs(graph, start) #explores reachabl stations

        print("\nDFS") 
        print("Reachable stations:", len(visited)) #display number of reachable stations

        # DIJKSTRA  

        distances, previous, previous_line = dijkstra(graph, start, end) #finds fastest route
        path = get_path(previous, previous_line, start, end)#rebuilt path

        print("\nFASTEST PATH\n") 
		
        if not path: #checks if there is a path
            print("No path found") 
            continue 

#Build Segments
segments = []  # All journey segments, one per metro line
current_line = path[1][1] if len(path) > 1 else path[0][1]  # First line used
segment = [path[0][0]]  # Start segment with departure station

for i in range(1, len(path)):  # Loop through each station in the path
    station, line = path[i]  # Unpack station and its line

    if line == current_line or line is None:  # Still on the same line
        segment.append(station)  # Add to current segment
    else:  # Line change detected
        segments.append((current_line, segment))  # Save completed segment
        current_line = line  # Switch to new line
        segment = [path[i - 1][0], station]  # New segment starts from last station

segments.append((current_line, segment))

#Display
first_line, first_segment = segments[0] #gets first segment

print(f"Board at {first_segment[0]} station, line {first_line}") #displays where to board 

for i, (line, stations) in enumerate(segments): #loops through each segment

    for s in stations[1:-1]: 
        print(f"Continue through {s} station") #displays intermediate stations

    if i < len(segments) - 1: #checks if tranfer is needed
        transfer_station = stations[-1] 
        next_line = segments[i + 1][0] 

        print( 
            f"Transfer at {transfer_station} station, " 
            f"take line {next_line}" 
        ) #displays transfer instructions

    last_line, last_segment = segments[-1] #gets last segment

    print( 
        f"Alight at {last_segment[-1]} station, " 
        f"line {last_line}" 
        ) #displays arrival station

    minutes = distances[end] // 60 #converts time to minutes
    seconds = distances[end] % 60 #keeps the remaining time in seconds

    print(f"\nEstimated total time: {minutes} minutes {seconds} seconds") #print total time

 

    again = input("\nDo you want to do another reaserch ? (yes/no) : ").strip().lower() #asks the user if he wants another research 

    if again not in ("yes"): #if not yes stops the program
        print("Good bye!") 
        break 
