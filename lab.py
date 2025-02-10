from os import system
from time import sleep
from random import randint

# ! TODOS !
# TODO: change maze to 2D array in separate file
# TODO: check for renduntant code and organize it better
# TODO: randomize maze
# TODO: add fog of war

# ANSII colors
MOUSE_COLOR = "\033[92m"
CHEESE_COLOR = "\033[33m"
VISITET_COLOR = "\033[35m"
WALL_COLOR = "\033[34m"
RESET = "\033[0m"

# maze objects
EMPTY = " "
MOUSE = f"{MOUSE_COLOR}{chr(9679)}{RESET}"
CHEESE = f"{CHEESE_COLOR}{chr(9664)}{RESET}"
VISITET = f"{VISITET_COLOR}~{RESET}"
WALL = f"{WALL_COLOR}{chr(9608)}{RESET}"

# directions
NORTH, SOUTH, EAST, WEST = "north", "south", "east", "west"

# playground settings
DELAY = 0.1 # ~1 second / moves per second
WIDTH = 12
HEIGHT = 7

cheese_pos = (0, 11)
mouse_pos = (6, 0)
last_fork = (0, 0)
available_forks = []
available_directions = []
moves = -1

# playground
MATRIX = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]
MATRIX[0][0] = MATRIX[0][2] = MATRIX[0][4] = MATRIX[0][8] = MATRIX[0][9] = MATRIX[0][11] = EMPTY
MATRIX[1][0] = MATRIX[1][2] = MATRIX[1][4] = MATRIX[1][5] = MATRIX[1][6] = MATRIX[1][8] = MATRIX[1][11] = EMPTY
MATRIX[2][0] = MATRIX[2][1] = MATRIX[2][2] = MATRIX[2][4] = MATRIX[2][6] = MATRIX[2][7] = MATRIX[2][8] = MATRIX[2][11] = EMPTY
MATRIX[3][1] = MATRIX[3][4] = MATRIX[3][6] = MATRIX[3][8] = MATRIX[3][11] = EMPTY
MATRIX[4][1] = MATRIX[4][2] = MATRIX[4][3] = MATRIX[4][4] = MATRIX[4][6] = MATRIX[4][8] = MATRIX[4][9] = MATRIX[4][10] = MATRIX[4][11] = EMPTY
MATRIX[5][3] = MATRIX[5][6] = EMPTY
MATRIX[6][0] = MATRIX[6][1] = MATRIX[6][2] = MATRIX[6][3] = MATRIX[6][6] = MATRIX[6][7] = MATRIX[6][8] = MATRIX[6][9] = MATRIX[6][10] = MATRIX[6][11] = EMPTY

# toys
MATRIX[cheese_pos[0]][cheese_pos[1]] = CHEESE
MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE

def print_matrix(matrix):
    system("cls")
    print(f"{WALL_COLOR}-{RESET}" * (WIDTH * 4 + 1))
    for row in matrix:
        print(f"{WALL_COLOR}| {RESET}", end="")
        print(f"{WALL_COLOR} | {RESET}".join(row) + "", end="")
        print(f"{WALL_COLOR} |{RESET}")
        print(f"{WALL_COLOR}-{RESET}" * (WIDTH * 4 + 1))

def check_available_routes(matrix, mouse_pos) -> list:
    available_directions = []
    try:
        if(mouse_pos[1] != 11):
            if(MATRIX[mouse_pos[0]][mouse_pos[1] + 1] == EMPTY or MATRIX[mouse_pos[0]][mouse_pos[1] + 1] == CHEESE):
                available_directions.append(EAST)
        if(mouse_pos[1] != 0):
            if(MATRIX[mouse_pos[0]][mouse_pos[1] - 1] == EMPTY or MATRIX[mouse_pos[0]][mouse_pos[1] - 1] == CHEESE):
                available_directions.append(WEST)
        if(mouse_pos[0] != 6):
            if(MATRIX[mouse_pos[0] + 1][mouse_pos[1]] == EMPTY or MATRIX[mouse_pos[0] + 1][mouse_pos[1]] == CHEESE):
                available_directions.append(SOUTH)
        if(mouse_pos[0] != 0):
            if(MATRIX[mouse_pos[0] - 1][mouse_pos[1]] == EMPTY or MATRIX[mouse_pos[0] - 1][mouse_pos[1]] == CHEESE):
                available_directions.append(NORTH)
    except IndexError:
        print("check_available_routes: IndexError")
        pass
    return available_directions

def debug(mouse_pos, available_directions, last_fork):
    print("mouse_pos = ", end="")
    print(mouse_pos)
    print("available_directions = ", end="")
    print(available_directions)
    print("last_fork = ", end="")
    print(last_fork)
    print("cheese_pos = ", end="")
    print(cheese_pos)
    print("available_forks = ", end="")
    print(available_forks)
    print("moves = ", end="")
    print(moves)

def check_win_condition(mouse_pos, cheese_pos, moves):
    if mouse_pos == cheese_pos:
        print(f"Mouse found cheese in {moves} moves!")
        exit(0)

try:
    while True:
        moves += 1
        available_directions = check_available_routes(MATRIX, mouse_pos)
        print_matrix(MATRIX)
        debug(mouse_pos, available_directions, last_fork)
        check_win_condition(mouse_pos, cheese_pos, moves)

        # jeśli jest tylko jedna droga to idziemy nią
        if len(available_directions) == 1:
            if available_directions[0] == NORTH:
                mouse_pos = (mouse_pos[0] - 1, mouse_pos[1])
                MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE
                MATRIX[mouse_pos[0] + 1][mouse_pos[1]] = VISITET
            elif available_directions[0] == SOUTH:
                mouse_pos = (mouse_pos[0] + 1, mouse_pos[1])
                MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE
                MATRIX[mouse_pos[0] - 1][mouse_pos[1]] = VISITET
            elif available_directions[0] == EAST:
                mouse_pos = (mouse_pos[0], mouse_pos[1] + 1)
                MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE
                MATRIX[mouse_pos[0]][mouse_pos[1] - 1] = VISITET
            elif available_directions[0] == WEST:
                mouse_pos = (mouse_pos[0], mouse_pos[1] - 1)
                MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE
                MATRIX[mouse_pos[0]][mouse_pos[1] + 1] = VISITET
            else:
                print("Main: droga == 1: ERROR")

        # jeśli jest więcej niż jedna droga to zapisujemy ostatni rozdział
        elif len(available_directions) > 1:
            last_fork = mouse_pos
            available_forks.append(last_fork)
            direction = available_directions[randint(0, len(available_directions) - 1)]

            if direction == NORTH:
                mouse_pos = (mouse_pos[0] - 1, mouse_pos[1])
                MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE
                MATRIX[mouse_pos[0] + 1][mouse_pos[1]] = VISITET
            elif direction == SOUTH:
                mouse_pos = (mouse_pos[0] + 1, mouse_pos[1])
                MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE
                MATRIX[mouse_pos[0] - 1][mouse_pos[1]] = VISITET
            elif direction == EAST:
                mouse_pos = (mouse_pos[0], mouse_pos[1] + 1)
                MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE
                MATRIX[mouse_pos[0]][mouse_pos[1] - 1] = VISITET
            elif direction == WEST:
                mouse_pos = (mouse_pos[0], mouse_pos[1] - 1)
                MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE
                MATRIX[mouse_pos[0]][mouse_pos[1] + 1] = VISITET
            else:
                print("Main: droga > 1: ERROR")
        
        # jeśli nie ma dróg to wracamy do ostatniego rozdziału z wolnymi drogami
        else: # len(available_directions) == 0
            MATRIX[mouse_pos[0]][mouse_pos[1]] = VISITET
            mouse_pos = available_forks[len(available_forks) - 1]
            available_forks.pop()
            MATRIX[mouse_pos[0]][mouse_pos[1]] = MOUSE

        sleep(DELAY)

except KeyboardInterrupt:
    print("Main: KeyboardInterrupt")
    pass