from os import system
from time import sleep
from random import randint
import pygame
from pygame.locals import *

# ! TODOS !
# TODO: randomize maze
# TODO: add option to read from file or generate random maze
# TODO: add fog of war

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

def print_matrix(matrix, WIDTH, COLORS) -> None:
    system("cls")
    print(f"{COLORS['wall']}-{COLORS['reset']}" * (WIDTH * 4 + 1))
    for row in matrix:
        print(f"{COLORS['wall']}| {COLORS['reset']}", end="")
        print(f"{COLORS['wall']} | {COLORS['reset']}".join(row) + "", end="")
        print(f"{COLORS['wall']} |{COLORS['reset']}")
        print(f"{COLORS['wall']}-{COLORS['reset']}" * (WIDTH * 4 + 1))

def draw_maze(screen, matrix, WIDTH, HEIGHT, OBJECTS, cell_size, mouse_pos, available_directions, last_fork, cheese_pos, available_forks, moves):
    pygame.font.init()
    font_size = int(cell_size * 3 / 5)
    font = pygame.font.SysFont("Sonoran Sans Serif", font_size)
    screen.fill((0, 0, 0))

    for y in range(HEIGHT):
        for x in range(WIDTH):
            cell = matrix[y][x]
            color = (0, 0, 0)

            if cell == OBJECTS['wall']:
                color = (0, 0, 255)
            elif cell == OBJECTS['mouse']:
                color = (88, 57, 39)
            elif cell == OBJECTS['cheese']:
                color = (255, 255, 0)
            elif cell == OBJECTS['visited']:
                color = (0, 100, 0)

            pygame.draw.rect(screen, color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
    
    debug_text = debug_get(mouse_pos, available_directions, last_fork, cheese_pos, available_forks, moves)

    for i, line in enumerate(debug_text.splitlines()):
        text_surface = font.render(line, False, (255, 255, 255))
        screen.blit(text_surface, (0, HEIGHT * cell_size + i * (font_size - 5)))
    
    if mouse_pos == cheese_pos:
        win_condition_text = f"Mouse found cheese in {moves} moves!"
        to_exit_test = f"To exit press space"
        text_surface = font.render(win_condition_text, False, (255, 255, 255))
        screen.blit(text_surface, ((WIDTH / 2) * cell_size, HEIGHT * cell_size))
        text_surface = font.render(to_exit_test, False, (255, 255, 255))
        screen.blit(text_surface, ((WIDTH / 2) * cell_size, HEIGHT * cell_size + font_size))
    pygame.display.update()

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

def debug_print(mouse_pos, available_directions, last_fork, cheese_pos, available_forks, moves):
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

def debug_get(mouse_pos, available_directions, last_fork, cheese_pos, available_forks, moves):
    return (f"mouse_pos = {mouse_pos}\n"
           f"available_directions = {available_directions}\n"
           f"last_fork = {last_fork}\n"
           f"cheese_pos = {cheese_pos}\n"
           f"available_forks = {available_forks}\n"
           f"moves = {moves}\n"
    )

def check_win_condition(mouse_pos, cheese_pos, moves) -> bool:
    if mouse_pos == cheese_pos:
        print(f"Mouse found cheese in {moves} moves!")
        return True  # Keep the game loop running
    return False

def main(OBJECTS) -> None:
    try:
        pygame.init()
        pygame.event.clear()
        DELAY = 0.05 # ~1 second / moves per second

        cheese_pos = (0, 0)
        mouse_pos = (0, 0)
        last_fork = (0, 0)
        available_forks = []
        available_directions = []
        moves = -1
        game_loop = True
        cell_size = 50

        matrix, WIDTH, HEIGHT, mouse_pos, cheese_pos = read_maze(OBJECTS)

        screen = pygame.display.set_mode((WIDTH * cell_size, HEIGHT * cell_size + (cell_size * 3)))
        pygame.display.set_caption("Maze Solver")

        while game_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                

            moves += 1
            available_directions = check_available_routes(matrix, mouse_pos, WIDTH, HEIGHT, OBJECTS)
            draw_maze(screen, matrix, WIDTH, HEIGHT, OBJECTS, cell_size, mouse_pos, available_directions, last_fork, cheese_pos, available_forks, moves)
            game_loop = not check_win_condition(mouse_pos, cheese_pos, moves)

            if game_loop:
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

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                        if game_loop != True:
                            if event.key == K_SPACE:
                                pygame.quit()
                                exit()
            sleep(DELAY) 

    except KeyboardInterrupt:
        print("Main: KeyboardInterrupt")
        pass

if __name__ == "__main__":
    main(OBJECTS)