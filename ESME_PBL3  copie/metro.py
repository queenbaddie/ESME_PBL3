import json

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
  #without join, we would have a listé



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
