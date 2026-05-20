# Little-Monster-s-Way-Home

A Reverse Tower Defence Puzzle Game. 
A Python game for the COMP9001 final project.

## Project Concept

Little Monster’s Way Home is a text-based adventure puzzle game made with Python that reverses the idea of “tower defence.” Instead of stopping monsters from moving forward, this game presents the monster as a character who needs help. The player’s goal is to guide a lost little monster safely back home. Players observe a randomly generated map, use limited resources to remove obstacles, build bridges over water, and place directional arrows to influence the monster’s movement. The game includes different themes such as forests, rivers, caves, and mazes, so each playthrough creates a different map. Hidden bombs, traps, energy limits, and path-checking mechanics add strategy and exploration. This game is suitable for players who enjoy light puzzle-solving, cute characters, and simple strategy challenges.

---

## Game Goal

Help the monster move from:

```
S = Start
to:
H = Home
```

The player wins if the monster reaches `H`.

The player loses if:

- the monster steps on a trap `T`
- the monster gets stuck
- the monster walks in a loop
- the player runs out of energy

## How to Run

Run the Python file in the terminal:

```
python monsters_way_home.py
```

## Map Symbols

```
S = Start
H = Home
. = Road
X = Obstacle
A = Tree
~ = Water
B = Bridge
T = Trap
? = Hidden cell
* = Hidden bomb
M = Monster
```

Arrow symbols:

```
> = Move right
< = Move left
^ = Move up
v = Move down
```

When placing an arrow, the player types:

```
right
left
up
down
```

The program will turn the word into an arrow symbol.

## Resources

The player has limited resources:

- Remove obstacle = clears trees or removable obstacles
- Bridge = turns water `~` into bridge `B`
- Arrow = guides the monster's direction
- Energy = how many actions the player can still take

Different map themes give different resources.

## Map Themes

The game randomly chooses one theme each time.

### Lost Forest

- There are many trees `A`.
- **Main strategy:** Use remove to clear trees and open a path.

### River

- There is more water `~`.
- **Main strategy:** Use bridges to cross water.

### Trap Cave

- Some cells are hidden as `?`.
- **Main strategy:** Explore carefully and use resources to find a safe route.

### Dark Maze

- There are many obstacles `X`.
- **Main strategy:** Use arrows to guide the monster through the maze.
- In Dark Maze, maze walls are hard to remove directly. Hidden bombs are especially useful.

## Hidden Bomb Mechanic

Hidden bombs are stored as: `*`

But they are usually hidden from the player.

In most themes, bombs look like normal road: `.`

In Trap Cave, bombs may appear as: `?`

When the monster steps on a hidden bomb:

- nearby obstacles `X` are cleared
- nearby trees `A` are cleared
- water `~` is not cleared

This makes the map change during the game and creates surprise paths.

## How to Play

### Step 1: Start the game

After running the file, the program creates a random world.

Example:

```
Generating a new random world...
Theme: Lost Forest
Theme Effect: This map has more trees.
Map size: 9 x 10
```

### Step 2: Look at the map

Example:

```
CURRENT MAP
-----------------------------------
A . . S . A .
. A X . . . H
. . . T . A .
-----------------------------------
```

Find:

`S` = Start
`H` = Home

Then decide how to help the monster.

### Step 3: Type info if you need help

The main screen only shows the map and energy.

Type: `info` to see:

- symbols
- theme tips
- resources
- actions

### Step 4: Choose an action

Available actions:

```
1 = Remove obstacle
2 = Place bridge
3 = Place arrow
4 = Check path
5 = Start monster
6 = Quit
info = Show help menu
```

## Action Guide

### 1. Remove obstacle

Removes a tree or removable obstacle.

Example:

```
>>> Enter your action: 1
Enter row: 2
Enter col: 3
```

### 2. Place bridge

Places a bridge on water `~`.

Example:

```
>>> Enter your action: 2
Enter row: 4
Enter col: 2
```

If successful, water becomes: `B`

### 3. Place arrow

Places an arrow on a road `.` or bridge `B`.

Example:

```
>>> Enter your action: 3
Enter row: 3
Enter col: 4
Enter arrow direction (right, left, up, down): right
```

This places: `>` on the map.

### 4. Check path

Checks whether a possible path exists from `S` to `H`.

Important:

- Check path only checks whether a possible route exists.
- It does not mean the monster will automatically choose the correct route.

The monster may still need arrows.

### 5. Start monster

Starts the monster movement.

The monster follows this rule:

- If there is an arrow, follow the arrow.
- If there is no arrow, try right, down, left, up.

The game ends when the monster:

- reaches home
- steps on a trap
- gets stuck
- walks in a loop

### 6. Quit

Ends the game.

## Output Labels

The game uses labels to make the output clearer.

```
[Event]   = something is happening
[Result]  = result of an action
[Note]    = rule reminder
[Warning] = danger or error
[Effect]  = special effect
```

Example:

```
[Event] Hidden bomb activated!
[Effect] The bomb breaks nearby maze walls.
[Note] Water '~' cannot be cleared by bombs.
[Result] 3 nearby obstacle/tree cell(s) were cleared.
```



