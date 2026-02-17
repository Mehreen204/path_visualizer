Pathfinding Visualizer (Uninformed Search Algorithms)

An interactive Python + Pygame application that visualizes classical uninformed search algorithms on a grid in real time.

This project demonstrates how different search strategies explore a state space and find paths between a start node and a target node — including handling dynamic obstacles.

🚀 Features

Interactive 10×10 grid

Mouse-based start, target, and obstacle placement

Real-time visualization

Dynamic obstacle simulation

Path reconstruction animation

Multiple search algorithms implemented

🧠 Implemented Algorithms
Algorithm	Description
Breadth-First Search (BFS)	Explores level-by-level, guarantees shortest path
Depth-First Search (DFS)	Explores deeply before backtracking
Depth-Limited Search (DLS)	DFS with depth constraint
Iterative Deepening DFS (IDDFS)	Repeated DLS with increasing depth
Uniform-Cost Search (UCS)	Cost-priority based search (uses priority queue)
Bidirectional Search	Simultaneous search from start and goal
🎮 Controls
Action	Key
Run BFS	SPACE
Run DFS	D
Run DLS	L
Run IDDFS	I
Run UCS	U
Run Bidirectional Search	B
Clear Grid	C
Place Start/Target/Obstacles	Mouse Left Click
🎨 Color Legend
Color	Meaning
🟢 Green	Start Node
🔴 Red	Target Node
⚫ Grey	Obstacle
🟡 Yellow	Visited Node (BFS/DFS/UCS)
🔷 Cyan	Visited Node (DLS / Bidirectional backward)
🔵 Blue	Final Path
⚙️ Installation & Running
1️⃣ Clone the Repository
git clone https://github.com/your-username/pathfinding-visualizer.git
cd pathfinding-visualizer

2️⃣ Install Dependencies
pip install pygame

3️⃣ Run the Program
python search_visualizer.py

🏗️ Project Structure
search_visualizer.py   # Main application file
README.md              # Project documentation

📌 Key Learning Outcomes

Understanding differences between uninformed search strategies

Visualizing algorithm behavior instead of just reading theory

Event-driven programming with Pygame

Priority queues using heapq

Managing state and parent tracking for path reconstruction

Handling dynamic environments in search problems

🔍 Why This Project Matters

Search algorithms are foundational in:

Artificial Intelligence

Robotics Navigation

Game AI

GPS Routing Systems

Problem Solving Systems

This visualizer transforms theoretical algorithms into observable behavior.

🛠️ Technologies Used

Python 3

Pygame

heapq (priority queue)

collections (deque)

📈 Future Improvements

Add heuristic algorithms (A* Search)

Add weighted grids

Adjustable grid size

Performance metrics display

Step-by-step execution mode

👨‍💻 Author

Developed as part of an Artificial Intelligence / Search Algorithms project.
