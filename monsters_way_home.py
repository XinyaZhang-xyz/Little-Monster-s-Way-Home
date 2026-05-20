# Reverse Tower Defence Help the Monster Go Home
# This is a text-based puzzle game.
# The player helps a lost monster go back home.

import copy
import random


# Display map
# If the theme is Trap Cave, some cells will be hidden as "?"
def display_grid(grid, theme):
    print("\nCURRENT MAP")
    print("-----------------------------------")

    for row in range(len(grid)):
        line = ""

        for col in range(len(grid[row])):
            cell = grid[row][col]

            # In Trap Cave, some important cells are hidden
            if theme == "Trap Cave":
                if cell in ["X", "A", "*"]:
                    line = line + "?" + " "
                else:
                    line = line + cell + " "

            # In other themes, the hidden bomb is shown as road
            else:
                if cell == "*":
                    line = line + "." + " "
                else:
                    line = line + cell + " "

        print(line)

    print("-----------------------------------")

# Display the map while the monster is moving
# M shows the monster's current position
def display_grid_with_monster(grid, monster_row, monster_col, theme):
    print("\nMonster Moving:")
    for row in range(len(grid)):
        line = ""

        for col in range(len(grid[row])):
            # Show monster at its current position
            if row == monster_row and col == monster_col:
                line = line + "M" + " "
            else:
                cell = grid[row][col]

                # Hide some cells in Trap Cave
                if theme == "Trap Cave":
                    if cell in ["X", "A", "*"]:
                        line = line + "?" + " "
                    else:
                        line = line + cell + " "

                # Hide bombs in other themes
                else:
                    if cell == "*":
                        line = line + "." + " "
                    else:
                        line = line + cell + " "
        print(line)
    print()


# Find a symbol in the map
# For example, find "S" or "H"
def find_symbol(grid, symbol):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == symbol:
                return row, col
    # If the symbol is not found, return None
    return None


# Check whether a row and column are inside the map
def is_inside_grid(grid, row, col):
    if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]):
        return True
    else:
        return False


# Check whether the monster can walk on a cell
def can_step_on(grid, row, col):
    if not is_inside_grid(grid, row, col):
        return False

    # The monster cannot walk on obstacle, tree, water, or trap
    # Bridge B, arrows, road, and hidden bomb are walkable
    if grid[row][col] in ["X", "A", "~", "T"]:
        return False

    return True


# Player action 1:
# Remove a tree or removable obstacle depending on the theme
def remove_obstacle(grid, resources, theme):
    if resources["remove"] <= 0:
        print("[Warning] You have no remove obstacle resource left.")
        return

    row = int(input("Enter row: "))
    col = int(input("Enter col: "))

    if not is_inside_grid(grid, row, col):
        print("[Warning] This position is outside the map.")
        return

    cell = grid[row][col]

    # In Lost Forest, trees are the main removable obstacle
    if theme == "Lost Forest":
        if cell == "A":
            grid[row][col] = "."
            resources["remove"] -= 1
            print("[Result] Tree removed. A new road has been opened.")
        else:
            print("[Note] In Lost Forest, you can mainly remove trees A.")

    # In Dark Maze, walls are too strong to remove directly
    elif theme == "Dark Maze":
        if cell == "X":
            print("[Warning] The maze wall is too strong to remove directly.")
            print("[Note] Try using arrows or finding a hidden bomb.")
        elif cell == "A":
            grid[row][col] = "."
            resources["remove"] -= 1
            print("[Result] Small tree removed!")
        else:
            print("[Note] You can only remove small trees A in Dark Maze.")

    # In other themes, both X and A can be removed
    else:
        if cell in ["X", "A"]:
            grid[row][col] = "."
            resources["remove"] -= 1
            print("[Result] Obstacle removed. The path is more open now.")
        else:
            print("[Note] You can only remove X obstacle or A tree.")


# Player action 2:
# Place a bridge on water
def place_bridge(grid, resources):
    if resources["bridge"] <= 0:
        print("[Warning] You have no bridge resource left.")
        return

    row = int(input("Enter row: "))
    col = int(input("Enter col: "))

    # Bridge can only be placed on water
    if is_inside_grid(grid, row, col) and grid[row][col] == "~":
        grid[row][col] = "B"
        resources["bridge"] -= 1
        print("[Result] Bridge placed. The monster can now cross this water cell.")
    else:
        print("[Note] You can only place a bridge on water '~'.")

# Player action 3:
# Place an arrow on the road
def place_arrow(grid, resources):
    if resources["arrow"] <= 0:
        print("[Warning] You have no arrow resource left.")
        return

    row = int(input("Enter row: "))
    col = int(input("Enter col: "))
    direction = input("Enter arrow direction (right, left, up, down): ")

    # Change word input into arrow symbol
    if direction == "right":
        arrow = ">"
    elif direction == "left":
        arrow = "<"
    elif direction == "up":
        arrow = "^"
    elif direction == "down":
        arrow = "v"
    else:
        print("[Warning] Invalid direction. Please type right, left, up, or down.")
        return

    # Arrow can only be placed on road
    if is_inside_grid(grid, row, col) and (grid[row][col] == "." or grid[row][col] == "B"):
        grid[row][col] = arrow
        resources["arrow"] -= 1
        print("[Result] Arrow placed. The monster will follow this direction.")
    else:
        print("[Note] You can only place an arrow on a road '.' or bridge 'B'.")


# Use recursion to check whether a path exists
# The function searches up, down, left, and right
def path_exists(grid, row, col):
    # Stop if the position is outside the map
    if not is_inside_grid(grid, row, col):
        return False

    # Stop if the cell is blocked or dangerous
    if grid[row][col] in ["X", "A", "~", "T"]:
        return False

    # If the function reaches Home, path exists
    if grid[row][col] == "H":
        return True

    # Save the original cell
    original = grid[row][col]

    # Mark this cell as visited
    # This prevents the function from checking the same cell again
    grid[row][col] = "X"

    # Try four directions
    found = (
        path_exists(grid, row + 1, col) or
        path_exists(grid, row - 1, col) or
        path_exists(grid, row, col + 1) or
        path_exists(grid, row, col - 1)
    )

    # Change the cell back after checking
    grid[row][col] = original

    return found


# Check whether the current map has a safe path
def check_path(grid):
    start = find_symbol(grid, "S")
    if start == None:
        print("[Warning] No start position found.")
        return

    row, col = start

    # Use a copied map so the real map will not be changed
    test_grid = copy.deepcopy(grid)

    if path_exists(test_grid, row, col):
        print("[Result] A possible path exists.")
        print("[Note] The monster may be able to go home, but it may still need arrows to follow the correct route.")
    else:
        print("[Result] No possible path yet.")
        print("[Note] Try removing obstacles, placing bridges, or using arrows.")


# Hidden bomb effect
# The bomb clears nearby obstacles and trees
# It does not clear water
def explode_bomb(grid, bomb_row, bomb_col, theme):
    print("\n[Event] Hidden bomb activated!")

    # Different themes have different explanation messages
    if theme == "Lost Forest":
        print("[Effect] The bomb clears nearby trees and opens the forest path.")
    elif theme == "Dark Maze":
        print("[Effect] The bomb breaks nearby maze walls.")
    elif theme == "Trap Cave":
        print("[Effect] The bomb reveals and clears nearby hidden obstacles.")
    elif theme == "River":
        print("[Effect] The bomb clears nearby obstacles, but water remains.")
    else:
        print("[Effect] Nearby obstacles and trees have been cleared.")

    print("[Note] Water '~' cannot be cleared by bombs.")

    cleared_count = 0

    # Check the 8 cells around the bomb and the bomb cell itself
    for row_change in [-1, 0, 1]:
        for col_change in [-1, 0, 1]:
            new_row = bomb_row + row_change
            new_col = bomb_col + col_change

            if is_inside_grid(grid, new_row, new_col):

                # Bomb only clears obstacle X and tree A
                if grid[new_row][new_col] == "X" or grid[new_row][new_col] == "A":
                    grid[new_row][new_col] = "."
                    cleared_count += 1

    # The bomb cell becomes road after exploding
    grid[bomb_row][bomb_col] = "."

    print("[Result]", cleared_count, "nearby obstacle/tree cell(s) were cleared.")


# Generate a random map based on theme
def generate_random_map(rows, cols, theme):
    grid = []

    # Create an empty map
    for row in range(rows):
        new_row = []
        for col in range(cols):
            new_row.append(".")
        grid.append(new_row)

    # Random start and home positions
    start_row = random.randint(0, rows - 1)
    start_col = random.randint(0, cols - 1)
    home_row = random.randint(0, rows - 1)
    home_col = random.randint(0, cols - 1)

    # Make sure Start and Home are not in the same position
    while home_row == start_row and home_col == start_col:
        home_row = random.randint(0, rows - 1)
        home_col = random.randint(0, cols - 1)

    grid[start_row][start_col] = "S"
    grid[home_row][home_col] = "H"

    # Fill the map with different cells based on the theme
    for row in range(rows):
        for col in range(cols):

            # Do not change Start and Home
            if grid[row][col] == "S" or grid[row][col] == "H":
                continue

            random_number = random.randint(1, 100)

            # Lost Forest has more trees
            if theme == "Lost Forest":
                if random_number <= 45:
                    grid[row][col] = "A" 
                elif random_number <= 50:
                    grid[row][col] = "X"
                elif random_number <= 57:
                    grid[row][col] = "~"
                elif random_number <= 62:
                    grid[row][col] = "T"
                elif random_number <= 68:
                    grid[row][col] = "*"
                else:
                    grid[row][col] = "."

            # River has more water
            elif theme == "River":
                if random_number <= 35:
                    grid[row][col] = "~" 
                elif random_number <= 48:
                    grid[row][col] = "X"
                elif random_number <= 55:
                    grid[row][col] = "A"
                elif random_number <= 60:
                    grid[row][col] = "T"
                elif random_number <= 65:
                    grid[row][col] = "*"
                else:
                    grid[row][col] = "."

            # Trap Cave has more traps and hidden cells
            elif theme == "Trap Cave":
                if random_number <= 10:
                    grid[row][col] = "T" 
                elif random_number <= 22:
                    grid[row][col] = "X"
                elif random_number <= 30:
                    grid[row][col] = "~"
                elif random_number <= 38:
                    grid[row][col] = "A"
                elif random_number <= 50:
                    grid[row][col] = "*"
                else:
                    grid[row][col] = "."

            # Dark Maze has more obstacles
            elif theme == "Dark Maze":
                if random_number <= 45:
                    grid[row][col] = "X" 
                elif random_number <= 50:
                    grid[row][col] = "A"
                elif random_number <= 55:
                    grid[row][col] = "~"
                elif random_number <= 60:
                    grid[row][col] = "T"
                elif random_number <= 68:
                    grid[row][col] = "*"
                else:
                    grid[row][col] = "."

    return grid


# Generate maps until the map has at least one safe path
def generate_valid_random_map(rows, cols, theme):
    while True:
        grid = generate_random_map(rows, cols, theme)

        start = find_symbol(grid, "S")

        if start != None:
            row, col = start

            # Use copy because path_exists will temporarily change the map
            test_grid = copy.deepcopy(grid)

            if path_exists(test_grid, row, col):
                return grid


# Decide the monster's next move
def get_next_move(grid, row, col):
    current_cell = grid[row][col]

    # If the monster stands on an arrow, follow the arrow
    if current_cell == ">":
        return row, col + 1

    elif current_cell == "<":
        return row, col - 1

    elif current_cell == "^":
        return row - 1, col

    elif current_cell == "v":
        return row + 1, col

    # If there is no arrow, try right, down, left, up
    directions = [
        [0, 1],    # right
        [1, 0],    # down
        [0, -1],   # left
        [-1, 0]    # up
    ]

    for direction in directions:
        new_row = row + direction[0]
        new_col = col + direction[1]

        if can_step_on(grid, new_row, new_col):
            return new_row, new_col

    # If there is no valid move, return None
    return None


# Start moving the monster
def start_monster(grid, resources_used, theme):
    start = find_symbol(grid, "S")

    if start == None:
        print("[Warning] No start position found.")
        return

    row, col = start
    steps = 0
    visited = []

    print("\n[Event] The monster starts moving!")

    while True:
        display_grid_with_monster(grid, row, col, theme)

        # If the monster steps on a hidden bomb
        if grid[row][col] == "*":
            explode_bomb(grid, row, col, theme)

        # Win condition
        if grid[row][col] == "H":
            print("[Result] The monster arrived home!")
            score = calculate_score(True, steps, resources_used)
            print("[Result] Final Score:", score)
            return

        # Lose condition
        if grid[row][col] == "T":
            print("[Event] The monster stepped on a trap.")
            print("[Result] Game over.")
            score = calculate_score(False, steps, resources_used)
            print("[Result] Final Score:", score)
            return

         # If the monster visits the same place again, it is walking in a loop
        if [row, col] in visited:
            print("[Warning] The monster is walking in a loop.")
            print("[Result] Game over.")
            score = calculate_score(False, steps, resources_used)
            print("[Result] Final Score:", score)
            return

        visited.append([row, col])

        next_position = get_next_move(grid, row, col)

        # If no next move exists, the monster is stuck
        if next_position == None:
            print("[Warning] The monster is stuck.")
            print("[Result] Game over.")
            score = calculate_score(False, steps, resources_used)
            print("[Result] Final Score:", score)
            return

        row = next_position[0]
        col = next_position[1]
        steps += 1

        input("Press Enter to continue...")


# Calculate the final score
def calculate_score(success, steps, resources_used):
    if not success:
        return 0

    score = 100
    score -= steps * 2             # More steps means lower score
    score -= resources_used * 10   # More resources used means lower score

    if score < 0:
        score = 0

    return score


# Choose a random theme and create a random map
def choose_level():
    themes = ["Lost Forest", "River", "Trap Cave", "Dark Maze"]
    theme = random.choice(themes)

    # Random map size, at least 8 x 8
    rows = random.randint(8, 12)
    cols = random.randint(8, 12)

    print("\nGenerating a new random world...")
    print("Theme:", theme)

    # Explain the theme effect
    if theme == "Lost Forest":
        print("Theme Effect: This map has more trees.")
    elif theme == "River":
        print("Theme Effect: This map has more water.")
    elif theme == "Trap Cave":
        print("Theme Effect: Some cells are hidden.")
    elif theme == "Dark Maze":
        print("Theme Effect: This map has more obstacles.")
    print("Map size:", rows, "x", cols)

    grid = generate_valid_random_map(rows, cols, theme)

    # Different themes give different resources
    if theme == "Lost Forest":
        resources = {
            "remove": 5, # Clears blocking X obstacles or A trees.
            "bridge": 2, # Turns water ~ into a walkable bridge B.
            "arrow": 4,  # Places a direction guide to help the monster move along the correct path.
            "energy": 18 # Shows how many actions the player can still take.
        }

    elif theme == "River":
        resources = {
            "remove": 3,
            "bridge": 5,
            "arrow": 5,
            "energy": 18
        }

    elif theme == "Trap Cave":
        resources = {
            "remove": 4,
            "bridge": 4,
            "arrow": 7,
            "energy": 20
        }

    else:
        resources = {
            "remove": 1,
            "bridge": 2,
            "arrow": 8,
            "energy": 17
        }

    return grid, resources, theme


# Show help information when the player types info
def show_info(resources):
    print("\n" + "=" * 42)
    print("HELP MENU")
    print("=" * 42)

    # Symbols
    print("\n[ Symbols ]")
    print("-" * 42)
    print("S = Start")
    print("H = Home")
    print(". = Road")
    print("X = Obstacle")
    print("A = Tree")
    print("~ = Water")
    print("B = Bridge")
    print("T = Trap")
    print("? = Hidden cell")
    print("* = Hidden bomb")
    print("    Bombs are usually hidden as '.' or '?'.")
    print("> = Move right")
    print("< = Move left")
    print("^ = Move up")
    print("v = Move down")

    # Theme Tips
    print("\n[ Theme Tips ]")
    print("-" * 42)
    print("Lost Forest : Trees are common.")
    print("              Bombs can clear groups of trees.")
    print("Dark Maze   : Maze walls are hard to remove.")
    print("              Bombs can break nearby maze walls.")
    print("River       : Water cells are common.")
    print("              Bombs cannot clear water.")
    print("Trap Cave   : Some cells are hidden.")
    print("              Hidden bombs may create surprise paths.")

    # Resources
    print("\n[ Resources ]")
    print("-" * 42)
    print("Energy:", resources["energy"])
    print("Remove obstacle:", resources["remove"])
    print("Bridge:", resources["bridge"])
    print("Arrow:", resources["arrow"])

    # Actions
    print("\n[ Actions ]")
    print("-" * 42)
    print("1    : Remove obstacle")
    print("2    : Place bridge")
    print("3    : Place arrow")
    print("       Arrows can be placed on road '.' or bridge 'B'.")
    print("4    : Check path")
    print("5    : Start monster")
    print("6    : Quit")
    print("info : Show this help menu")
    
    print("=" * 42)



# Main game loop
def play_game():
    grid, resources, theme = choose_level()
    # Save original resources for score calculation
    original_resources = copy.deepcopy(resources)

    while True:
        display_grid(grid, theme)

        # If energy is 0, the player loses
        if resources["energy"] <= 0:
            print("\n[Warning] Out of energy!")
            print("[Result] The monster is too tired to continue.")
            break

        # Only show energy on the main screen
        print("\nEnergy:", resources["energy"])
        print("\nType 'info' to show symbols, resources, and actions.")
        action = input(">>> Enter your action: ")

        if action == "info":
            show_info(resources)


        elif action == "1":
            print("\n[Event] You are removing an obstacle...")
            resources["energy"] -= 1
            remove_obstacle(grid, resources, theme)

        elif action == "2":
            print("\n[Event] You are placing a bridge...")
            resources["energy"] -= 1
            place_bridge(grid, resources)

        elif action == "3":
            print("\n[Event] You are placing an arrow...")
            resources["energy"] -= 1
            place_arrow(grid, resources)

        elif action == "4":
            print("\n[Event] You are checking the path...")
            resources["energy"] -= 1
            check_path(grid)

        elif action == "5":
            print("\n[Event] You are starting the monster...")
            resources_used = 0
            resources_used += original_resources["remove"] - resources["remove"]
            resources_used += original_resources["bridge"] - resources["bridge"]
            resources_used += original_resources["arrow"] - resources["arrow"]

            start_monster(grid, resources_used, theme)
            break

        elif action == "6":
            print("[Result] Game ended.")
            break

        else:
            print("[Warning] Invalid choice. Please try again.")


# Program start
def main():
    print("===================================")
    print("Reverse Tower Defence")
    print("Help the Monster Go Home")
    print("===================================")

    play_game()


# Run the program
if __name__ == "__main__":
    main()
