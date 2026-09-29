# GraphTheoryW4_Group6
---
## Group Members

| Name                     | NRP        |
| ------------------------ | ---------- |
| Lina Fatima Azzahra Badr | 5025251168 |
| Naila Sa'ada Cahyani     | 5025251258 |

---

## A. Backbite Procedural Dungeon Generator

This algorithm generates a randomized, solvable dungeon layout that guarantees a single continuous path visiting every room exactly once without reusing tunnels (a Hamiltonian path). 

**This algorithm combines two specific Graph Theory concepts:**
1. **The Boustrophedon Walk (Snake Walk)**: Used to systematically fill the initial grid and construct a mathematically guaranteed Hamiltonian path.
2. **The Backbite Algorithm**: A randomized edge-swapping technique used to heavily shuffle the Hamiltonian path without breaking it.

By applying these algorithms alongside geometric transformations and decoy paths, it makes each generation unique while maintaining solvability.

### Code Explanation

```python
def get_grid_dimensions(num_rooms):
    # Mathematically factors the user's requested number of rooms 
    # into a 2D grid format by finding the closest integer square root divisors.
    ...

def generate_snake_path(width, height):
    # Generates a guaranteed solvable boustrophedon (snake) backbone
    path = []
    for y in range(height):
        if y % 2 == 0:
            for x in range(width): path.append((x, y))
        else:
            for x in range(width - 1, -1, -1): path.append((x, y))
    return path

def backbite(path, width, height):
    # Shuffles the Hamiltonian path while maintaining validity
    # 1. Pick an endpoint.
    # 2. Connect it to a valid random neighbor, forming a cycle.
    # 3. Break one edge from the cycle to form a new valid path.
    ...

```

1. **`get_grid_dimensions`**: Takes the raw number of rooms and converts it into a grid (Width $\times$ Height) suitable for procedural generation.
2. **`generate_snake_path`**: Creates the **Guaranteed Core Backbone**. Instead of random generation that might be unsolvable, this starts with a guaranteed mathematically valid Hamiltonian path (boustrophedon/snake walk) that covers the entire grid.
3. **`backbite`**: Applies the **Backbite Algorithm** to shuffle the core backbone. It randomly picks an endpoint, connects it to a nearby node to form a loop, and deletes an edge inside the loop to create a new valid path endpoint. This heavily randomizes the shape of the guaranteed path.
4. **`apply_geometric_transformations`**: Applies randomized rotations and mirroring so the starting point isn't always in the same corner.
5. **Decoy Tunnels**: Dynamically calculates how many extra edges to add to reach the user's requested tunnel count. These add visual complexity and dead-ends for the player, but do not disrupt the actual core path.

### Output Format
The algorithm prints out the total count and the exact coordinate lists for:
- Generated Rooms: `[(x, y), (x, y), ...]`
- Generated Tunnels: `[((x1, y1), (x2, y2)), ...]`

If you request an impossible configuration (like fewer tunnels than rooms - 1), it will instantly halt and print an error message prompting the user for valid dimensions.

### Result of Sample Runs

The program takes user input for the number of rooms and tunnels, then automatically calculates the optimal grid layout before generating the dungeon. You can run the program using:
```bash
python3 dungeon_generator.py
```

#### 1. Valid Input
Enter a valid number of rooms and tunnels (example: 25 rooms, 30 tunnels).

![Valid Input Sample Run](Assets/Pasted%20image%2020260929134622.png)

#### 2. Invalid Input
![Invalid Input Sample Run](Assets/Pasted%20image%2020260929134751.png)

## B. Depth-First Search Dungeon Validator
This algorithm validates whether a procedurally generated dungeon can be cleared by searching for valid paths that visit every room exactly once without revisiting any room (a Hamiltonian path).

**This algorithm combines two specific Graph Theory and Search concepts:**

1. **Adjacency List Graph Representation: Converts raw room coordinates and tunnel pairs into a fast-lookup graph structure.**
2. **Depth-First Search (DFS) with Backtracking: A recursive search technique that systematically explores every possible branching route from room to room, undoing steps (backtracking) when hitting a dead end.**

By attempting a path search starting from every room and capping the maximum results found, it efficiently checks dungeon solvability without causing a system freeze on complex layouts.

### Code Explanation

```python
def validate_dungeon(dungeon, max_paths_to_find=100):
    # Converts rooms and tunnels into an adjacency list graph,
    # then runs a DFS search starting from every available room.
    ...

def dfs(current_room, current_path, visited):
    # Explores connected rooms recursively:
    # 1. Stops early if max_paths_to_find limit is reached.
    # 2. Saves path if all rooms are visited (Hamiltonian Path found).
    # 3. Recursively visits neighbors, then backtracks when stuck.
    ...
```

1. Adjacency List Construction: Converts **`dungeon['rooms']`** and **`dungeon['tunnels']`** into a graph dictionary (**`adj`**) mapping each room to its adjacent neighbors for $O(1)$ lookup time during search iterations.
2. **`dfs`** (Depth-First Search): Recursively explores adjacent rooms by appending unvisited nodes to **`current_path`** and tracking them in a **`visited`** set to enforce the rule of visiting each room exactly once.
3. Backtracking Mechanism: When the DFS reaches a node with no unvisited neighbors, it removes (**`pop`** / **`remove`**) the current room from **`current_path`** and **`visited`**, unwinding the recursion stack to explore alternate branching routes.
4. Path Validation & Capping: Checks if **`len(current_path) == total_rooms`**. When true, a complete Hamiltonian Path is identified and recorded. Search execution halts early once **`valid_paths`** reaches **`max_paths_to_find`** (default 100) to keep execution times bounded.
5. Multi-Start Room Iteration: Loops through every room in **`dungeon['rooms']`** as a candidate starting node, ensuring valid routes are identified regardless of where the player begins in the dungeon.

### Output Format
The algorithm validates the layout and outputs the following directly to the terminal:
- Dungeon Status: Confirms whether the layout is **`VALID`** or **`Invalid`**.
- Route Counter: Reports the total count of valid clearing routes found (capped at **`100+`**).
- Sample Solution Routes: Displays up to the first 3 viable pathways in sequence format (e.g., **`(0, 0) -> (1, 0) -> (1, 1)`**).
- Error Handling: Catches non-integer inputs and rejects invalid parameters (e.g., fewer than $R - 1$ tunnels or fewer than 2 rooms).

### Result of Sample Runs
1. Using the same valid sample inputs as used in section A (25 rooms & 30 tunnels)
![Valid Input Sample Run: Validation]()

2. Invalid sample input
![Invalid Input Sample Run: Validation]()


### AI Involved:
 https://share.gemini.google/2FDc3OzTBYQb
