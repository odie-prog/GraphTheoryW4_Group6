import random
import math

def get_grid_dimensions(num_rooms):
    """Factors the number of rooms into a 2D grid width and height."""
    for i in range(int(math.sqrt(num_rooms)), 0, -1):
        if num_rooms % i == 0:
            return i, num_rooms // i
    return 1, num_rooms

def generate_snake_path(width, height):
    """
    Generates a basic snake/boustrophedon path visiting all nodes.
    This constructs the guaranteed core backbone in linear time.
    """
    path = []
    for y in range(height):
        if y % 2 == 0:
            # Move right on even rows
            for x in range(width):
                path.append((x, y))
        else:
            # Move left on odd rows
            for x in range(width - 1, -1, -1):
                path.append((x, y))
    return path

def get_neighbors(node, width, height):
    """Returns valid adjacent grid coordinates for a given node."""
    x, y = node
    neighbors = []
    if x > 0: neighbors.append((x - 1, y))
    if x < width - 1: neighbors.append((x + 1, y))
    if y > 0: neighbors.append((x, y - 1))
    if y < height - 1: neighbors.append((x, y + 1))
    return neighbors

def apply_geometric_transformations(path, width, height):
    """
    Randomly applies rotation or mirroring to the path.
    Prevents the dungeon from always having the same orientation.
    """
    transformation = random.choice(['none', 'rotate90', 'rotate180', 'rotate270', 'mirror_x', 'mirror_y'])
    new_path = []
    
    for (x, y) in path:
        if transformation == 'rotate90':
            new_path.append((height - 1 - y, x))
        elif transformation == 'rotate180':
            new_path.append((width - 1 - x, height - 1 - y))
        elif transformation == 'rotate270':
            new_path.append((y, width - 1 - x))
        elif transformation == 'mirror_x':
            new_path.append((width - 1 - x, y))
        elif transformation == 'mirror_y':
            new_path.append((x, height - 1 - y))
        else:
            new_path.append((x, y))
            
    # Swap width and height if rotated by 90 or 270 degrees
    if transformation in ['rotate90', 'rotate270']:
        return new_path, height, width
    return new_path, width, height

def backbite(path, width, height):
    """
    Applies the backbite algorithm to shuffle the Hamiltonian path.
    It picks an endpoint, connects it to a random neighbor to form a loop,
    and removes one edge from the loop to create a new valid path.
    """
    # Randomly pick either the start or end of the path
    endpoint = path[0] if random.random() < 0.5 else path[-1]
    is_start = (endpoint == path[0])
    
    # Find valid grid neighbors
    neighbors = get_neighbors(endpoint, width, height)
    
    # Identify the node already connected to this endpoint in the path
    if is_start:
        connected = path[1]
    else:
        connected = path[-2]
        
    # Exclude the currently connected node to find new valid edges
    valid_neighbors = [n for n in neighbors if n != connected]
    
    if not valid_neighbors:
        return path # No valid moves, return original path
        
    # Pick a random neighbor to connect to, forming a cycle
    neighbor = random.choice(valid_neighbors)
    idx = path.index(neighbor)
    
    # Break the cycle by removing an adjacent edge, forming the new path
    if is_start:
        new_path = path[1:idx][::-1] + [path[0]] + path[idx:]
        return new_path
    else:
        new_path = path[:idx+1] + path[idx+1:][::-1]
        return new_path

def generate_dungeon(num_rooms, num_tunnels, shuffle_iterations=200):
    """
    Generates a dungeon with a guaranteed Hamiltonian path.
    Adds decoy tunnels to reach the requested tunnel count.
    """
    width, height = get_grid_dimensions(num_rooms)

    # 1. Construct Guaranteed Core Backbone (Solvable path)
    path = generate_snake_path(width, height)
    
    # 2. Apply Random Variations (Backbite algorithm)
    for _ in range(shuffle_iterations):
        path = backbite(path, width, height)
        
    # Apply Geometric Transformations (Rotate/Mirror)
    path, final_width, final_height = apply_geometric_transformations(path, width, height)
        
    # Extract the core backbone edges (essential tunnels)
    edges = set()
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        edges.add(frozenset([u, v]))
        
    # Identify all possible edges on the grid
    all_possible_edges = set()
    for y in range(final_height):
        for x in range(final_width):
            if x < final_width - 1:
                all_possible_edges.add(frozenset([(x, y), (x + 1, y)]))
            if y < final_height - 1:
                all_possible_edges.add(frozenset([(x, y), (x, y + 1)]))
                
    remaining_edges = list(all_possible_edges - edges)
    
    # Calculate how many decoy tunnels to add
    extra_tunnels_needed = num_tunnels - (num_rooms - 1)
    
    if extra_tunnels_needed > len(remaining_edges):
        print(f"Warning: A {width}x{height} grid cannot fit {num_tunnels} tunnels. Generating maximum possible.")
        extra_tunnels_needed = len(remaining_edges)
    
    # Add random decoy tunnels (These will act as dead-ends)
    if extra_tunnels_needed > 0:
        decoys = random.sample(remaining_edges, extra_tunnels_needed)
        for decoy in decoys:
            edges.add(decoy)
        
    # Generate list of all rooms
    rooms = [(x, y) for y in range(final_height) for x in range(final_width)]
    
    return {
        "rooms": rooms,
        "tunnels": [tuple(edge) for edge in edges]
    }



if __name__ == "__main__":
    print("--- Procedural Dungeon Generator ---")
    try:
        r = int(input("Enter number of rooms: "))
        t = int(input("Enter number of tunnels: "))
        
        if r < 2:
            print("Error: A dungeon must have at least 2 rooms.")
        elif t < r - 1:
            print("Error: You must request at least R-1 tunnels to generate a connected dungeon.")
        else:
            dungeon = generate_dungeon(r, t, shuffle_iterations=200)
            
            print(f"\nGenerated Dungeon successfully!")
            
            print(f"Total Rooms: {len(dungeon['rooms'])}")
            print("Rooms List:")
            for i in range(0, len(dungeon['rooms']), 5):
                print("  " + ", ".join(map(str, dungeon['rooms'][i:i+5])))
            print()
            
            print(f"Total Tunnels (including decoys): {len(dungeon['tunnels'])}")
            print("Tunnels List:")
            for i in range(0, len(dungeon['tunnels']), 3):
                print("  " + ", ".join(map(str, dungeon['tunnels'][i:i+3])))
            print()
            
    except ValueError:
        print("Error: Please enter valid integer numbers. (Invalid input)")
