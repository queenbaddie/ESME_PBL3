[README.md](https://github.com/user-attachments/files/27948176/README.md)
# **📦 [A short ride on the metro and tramway]**

**MVP Status:** v1.0-Production

**Group Members:** Sarah AVENAS, Chloé ALLAIRE, Nour JABER, Clara BISIAUX


## **🎯 Project Overview**

Provide a concise (2-3 sentence) description of what your application does and the specific problem it solves. Why did you build this?

This application is a offline route planner for the public transport networks of four French cities: Paris, Lyon, Lille, and Bordeaux. It solves the problem of finding the fastest or least-stop route between two stations, taking into account line transfers, by implementing graph traversal algorithms (BFS, DFS) and Dijkstra's shortest path algorithm

## **🚀 Quick Start (Architect Level: < 60s Setup)**

Instructions on how to get this project running on a fresh machine.

1. **Clone the repo:**  
   git clone [your-repo-link]  
   cd [project-folder]

2. **Setup Virtual Environment:**  
   python -m venv .venv  
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Dependencies:**  
   pip install -r requirements.txt

4. **Run Application:**  
   python main.py


## **🛠️ Technical Architecture**

Explain how your code is organized. An "Architect-level" README should describe the separation of concerns.

- **main.py**: Entry point of the application. It initializes the Tkinter window, displays the menus, manages the game flow and connects the interface with the game logic.


## **🧪 Testing & Validation**

How can a user verify the code works?

- Run the application using `python main.py`.
- Choose a game mode (Player vs Player or Player vs AI or AI vs AI).
- Play by clicking on the grid.

Happy Path demonstration:

- The game starts with player **X**.
- Players alternate turns after each move.
- The game detects a win when three symbols are aligned.
- If the board is full with no winner, the game declares a draw.
- The user can return to the main menu after the game ends.


## **📦 Dependencies**

List the main third-party libraries used and why they were chosen:

- **tkinter**: Used to create the graphical user interface and manage user interactions such as buttons, menus, and the game grid.


## **🔮 Future Roadmap (v2.0)**

What features would you add if you had more time or a larger budget?

- Add a score tracking system between games
- Improve the graphical interface and design
- Add animations and sound effects
