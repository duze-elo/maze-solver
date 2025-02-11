from os import system
from time import sleep
from random import randint

# ! TODOS !
# TODO: randomize maze
# TODO: add option to read from file or generate random maze
# TODO: add fog of war
# TODO: zrobić dedykowane okienko programu

COLORS = {
    "mouse": "\033[92m",
    "cheese": "\033[33m",
    "visited": "\033[35m",
    "wall": "\033[34m",
    "reset": "\033[0m"
}

OBJECTS = {
    "empty": " ",
    "mouse": f"{COLORS['mouse']}{chr(9679)}{COLORS['reset']}",
    "cheese": f"{COLORS['cheese']}{chr(9664)}{COLORS['reset']}",
    "visited": f"{COLORS['visited']}~{COLORS['reset']}",
    "wall": f"{COLORS['wall']}{chr(9608)}{COLORS['reset']}",
}

def read_maze(OBJECTS) -> list:
    with open("maze.txt", "r") as MAZE_FILE:
        lines = MAZE_FILE.readlines()
        if lines:
            HEIGHT = len(lines)
            WIDTH = len(lines[0].strip())
        else:
            print("Main: Maze file is empty")
            exit(1)

    matrix = [[OBJECTS['wall'] for _ in range(WIDTH)] for _ in range(HEIGHT)]

    with open("maze.txt", "r") as MAZE_FILE:
        for i, line in enumerate(MAZE_FILE):
            for j, char in enumerate(line.strip()):
                if char == "r":
                    matrix[i][j] = OBJECTS['empty']
                elif char == "w":
                    matrix[i][j] = OBJECTS['wall']
                elif char == "M":
                    mouse_pos = (i, j)
                    matrix[i][j] = OBJECTS['mouse']
                elif char == "C":
                    cheese_pos = (i, j)
                    matrix[i][j] = OBJECTS['cheese']

    return matrix, WIDTH, HEIGHT, mouse_pos, cheese_pos

def print_matrix(matrix, WIDTH, ) -> None:
    system("cls")
    print(f"{COLORS['wall']}-{COLORS['reset']}" * (WIDTH * 4 + 1))
    for row in matrix:
        print(f"{COLORS['wall']}| {COLORS['reset']}", end="")
        print(f"{COLORS['wall']} | {COLORS['reset']}".join(row) + "", end="")
        print(f"{COLORS['wall']} |{COLORS['reset']}")
        print(f"{COLORS['wall']}-{COLORS['reset']}" * (WIDTH * 4 + 1))

def check_available_routes(matrix, mouse_pos, WIDTH, HEIGHT, OBJECTS) -> list:
    available_directions = []
    try:
        if(mouse_pos[1] < WIDTH - 1):
            checked_space = matrix[mouse_pos[0]][mouse_pos[1] + 1]
            if(checked_space == OBJECTS['empty'] or checked_space == OBJECTS['cheese']):
                available_directions.append('e')

        if(mouse_pos[1] > 0):
            checked_space = matrix[mouse_pos[0]][mouse_pos[1] - 1]
            if(checked_space == OBJECTS['empty'] or checked_space == OBJECTS['cheese']):
                available_directions.append('w')

        if(mouse_pos[0] < HEIGHT - 1):
            checked_space = matrix[mouse_pos[0] + 1][mouse_pos[1]]
            if(checked_space == OBJECTS['empty'] or checked_space == OBJECTS['cheese']):
                available_directions.append('s')

        if(mouse_pos[0] > 0):
            checked_space = matrix[mouse_pos[0] - 1][mouse_pos[1]]
            if(checked_space == OBJECTS['empty'] or checked_space == OBJECTS['cheese']):
                available_directions.append('n')
    except IndexError:
        print("check_available_routes: IndexError")
        pass
    return available_directions

def move_mouse(matrix, direction, mouse_pos):
    new_mouse_pos = mouse_pos
    if direction == 'n':
        new_mouse_pos = (mouse_pos[0] - 1, mouse_pos[1])
        if new_mouse_pos[0] >= 0:
            matrix[new_mouse_pos[0]][new_mouse_pos[1]] = OBJECTS['mouse']
            matrix[mouse_pos[0]][mouse_pos[1]] = OBJECTS['visited']
    elif direction == 's':
        new_mouse_pos = (mouse_pos[0] + 1, mouse_pos[1])
        if new_mouse_pos[0] < len(matrix):
            matrix[new_mouse_pos[0]][new_mouse_pos[1]] = OBJECTS['mouse']
            matrix[mouse_pos[0]][mouse_pos[1]] = OBJECTS['visited']
    elif direction == 'e':
        new_mouse_pos = (mouse_pos[0], mouse_pos[1] + 1)
        if new_mouse_pos[1] < len(matrix[0]):
            matrix[new_mouse_pos[0]][new_mouse_pos[1]] = OBJECTS['mouse']
            matrix[mouse_pos[0]][mouse_pos[1]] = OBJECTS['visited']
    elif direction == 'w':
        new_mouse_pos = (mouse_pos[0], mouse_pos[1] - 1)
        if new_mouse_pos[1] >= 0:
            matrix[new_mouse_pos[0]][new_mouse_pos[1]] = OBJECTS['mouse']
            matrix[mouse_pos[0]][mouse_pos[1]] = OBJECTS['visited']
    else:
        print("move_mouse: ERROR")
        new_mouse_pos = mouse_pos
    return new_mouse_pos

def debug(mouse_pos, available_directions, last_fork, cheese_pos, available_forks, moves):
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

def main(OBJECTS) -> None:
    try:
        DELAY = 0.3 # ~1 second / moves per second

        cheese_pos = (0, 0)
        mouse_pos = (0, 0)
        last_fork = (0, 0)
        available_forks = []
        available_directions = []
        moves = -1

        matrix, WIDTH, HEIGHT, mouse_pos, cheese_pos = read_maze(OBJECTS)

        while True:
            moves += 1
            available_directions = check_available_routes(matrix, mouse_pos, WIDTH, HEIGHT, OBJECTS)
            print_matrix(matrix, WIDTH)
            debug(mouse_pos, available_directions, last_fork, cheese_pos, available_forks, moves)
            check_win_condition(mouse_pos, cheese_pos, moves)

            if len(available_directions) == 1:
                direction = available_directions[0]
                mouse_pos = move_mouse(matrix, direction, mouse_pos)

            elif len(available_directions) > 1:
                last_fork = mouse_pos
                available_forks.append(last_fork)
                direction = available_directions[randint(0, len(available_directions) - 1)]
                mouse_pos = move_mouse(matrix, direction, mouse_pos)

            else: # len(available_directions) == 0
                matrix[mouse_pos[0]][mouse_pos[1]] = OBJECTS['visited']
                if available_forks:
                    mouse_pos = available_forks[len(available_forks) - 1]
                    available_forks.pop()
                    matrix[mouse_pos[0]][mouse_pos[1]] = OBJECTS['mouse']
                else:
                    print("No available forks to backtrack to.")
                    break

            sleep(DELAY)

    except KeyboardInterrupt:
        print("Main: KeyboardInterrupt")
        pass

if __name__ == "__main__":
    main(OBJECTS)