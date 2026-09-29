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

![[Pasted image 20260929134622.png]]

#### 2. Invalid Input
![[Pasted image 20260929134751.png]]

### AI Involved:
 https://share.gemini.google/2FDc3OzTBYQb
