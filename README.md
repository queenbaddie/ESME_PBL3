[README.md](https://github.com/user-attachments/files/27948176/README.md)
# **📦 [A short ride on the metro and tramway]**

**MVP Status:** v1.0-Production

**Group Members:** Sarah AVENAS, Chloé ALLAIRE, Nour JABER, Clara BISIAUX, Camy MERDJI


## **🎯 Project Overview**

Provide a concise (2-3 sentence) description of what your application does and the specific problem it solves. Why did you build this?

This application is a offline route planner for the public transport networks of four French cities: Paris, Lyon, Lille, and Bordeaux. It solves the problem of finding the fastest or least-stop route between two stations, taking into account line transfers, by implementing graph traversal algorithms (BFS, DFS) and Dijkstra's shortest path algorithm.

## **🚀 Quick Start (Architect Level: < 60s Setup)**

Upload the main code metro.py in the same folder as the data folder (with the json files)

1. **Clone the repo:**  
   git clone [https://github.com/queenbaddie/ESME_PBL3]
   cd [ESME_PBL3]

2. **Setup Virtual Environment:**  
   python -m venv .venv  
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Dependencies:**  
   heapq
   collections

5. **Run Application:**  
   python metro.py


## **🛠️ Technical Architecture**

**metro.py**: 
  - Entry point of the application. It loads the dataset, builds the metro graph, and implements all the algorithms used in the project:
  - BFS (Breadth-First Search) to find the route with the fewest stops
  - DFS (Depth-First Search) to explore reachable stations in the network
  - Dijkstra’s algorithm to compute the fastest path while taking into account travel times and line transfers


## **🧪 Testing & Validation**

How can a user verify the code works?

- Verify that the data folder is in the same folder as metro.py
- Run the application using `python metro.py`.
- Choose a city (paris, lille, bordeaux, lyon).
- Enter a departure and arrival station
- Verify the different outputs: BFS pth, DFS path, Djikstra path, navigation instructions and travel time

Happy Path demonstration:

- Load the selected metro network without errors
- Accept valid station names (with input error handling)
- Display a valid path between stations if one exists
- Show coherent travel instructions with correct line transfers
- Output a total estimated travel time in minutes and seconds


## **📦 Dependencies**


- **heapq**: Built-in Python module used to implement the priority queue required for Dijkstra’s algorithm. It allows efficient retrieval of the node with the smallest distance.
- **collections**: Used in the BFS (Breadth-First Search) algorithm to efficiently manage a queue with fast append and pop operations from both ends.


## **🔮 Future Roadmap (v2.0)**

What features would you add if you had more time or a larger budget?

- Add a graphical interface to have a better interaction
- Add a graph visualization
- Add every kind of public transportation for Paris (train, bus, RER...)
- Option to find another way if there are disruptions on a line
