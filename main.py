import random
import curses
import time

BOARD_WIDTH  = 20
BOARD_HEIGHT = 10
SCORE = 0

def exit_game(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "You lose! Final score: {}. Press 'q' to exit.".format(SCORE))
    # Wait for quit input
    stdscr.nodelay(False)
    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
    
def eat_fruit(snake):
    # Add a new block to the back of the snake
    snake.append((snake[-1][0], snake[-1][1]))
    # Spawn a new fruit
    fruit = [(random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1))]
    # Increment the score
    global SCORE
    SCORE += 1
    return snake, fruit

def move_head(snake, dir):
    # Keep track of old head before moving
    old_head = snake[0]
    # Move up
    if dir == 0:
        snake[0] = (snake[0][0], snake[0][1] - 1)
    # Move left
    elif dir == 1:
        snake[0] = (snake[0][0] - 1, snake[0][1])
    # Move down
    elif dir == 2:
        snake[0] = (snake[0][0], snake[0][1] + 1)
    # Move right
    elif dir == 3:
        snake[0] = (snake[0][0] + 1, snake[0][1])
    # Move the remainder of the snake
    if len(snake) > 1:
        for i in range(1, len(snake)):
            temp = old_head
            old_head = snake[i]
            snake[i] = temp
 
    return snake


def print_board(stdscr, snake, fruit):
    for i in range(BOARD_HEIGHT + 2):
        stdscr.addstr(i, 0, "\n")
        for j in range(BOARD_WIDTH + 2):
            # Print corners and edges
            if not i or not j:
                stdscr.addstr(i, j, "\u25A0")
            elif i == BOARD_HEIGHT + 2 - 1 or j == BOARD_WIDTH + 2 - 1:
                stdscr.addstr(i, j, "\u25A0")
            # Print middle
            else:
                # Print snake
                if (j - 1, i - 1) in snake:
                    stdscr.addstr(i, j, "\u25A3")
                # Print fruit
                elif (j - 1, i - 1) in fruit:
                    stdscr.addstr(i, j, "\u25C8")
                # Print empty space
                else:
                    stdscr.addstr(i, j, "\u25A1")
    stdscr.addstr(i, j + 1, "\n")
     

def main(stdscr):
    # Clear screen
    stdscr.clear()
    random.seed()
    
    # Randomly generate snake head and fruit
    snake = [(random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1))]
    fruit = snake

    # Make sure the fruit is not on top of the snake head by chance
    while (fruit == snake):
        fruit = [(random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1))]
    
    # Print initial screen
    print_board(stdscr, snake, fruit)
    
    # Get the first move
    stdscr.nodelay(False)
    c = stdscr.getch()
    if c == ord('w'):
        heading = 0
        snake = move_head(snake, heading)
        print_board(stdscr, snake, fruit)
    elif c == ord('a'):
        heading = 1
        snake = move_head(snake, heading)
        print_board(stdscr, snake, fruit)
    elif c == ord('s'):
        heading = 2
        snake = move_head(snake, heading)
        print_board(stdscr, snake, fruit)
    else:
        heading = 3
        snake = move_head(snake, heading)
        print_board(stdscr, snake, fruit)

    # Game loop
    stdscr.nodelay(True)
    while True:
        # Check for out of bounds
        if snake[0][0] == -1 or snake[0][0] == BOARD_WIDTH or snake[0][1] == -1 or snake[0][1] == BOARD_HEIGHT:
            exit_game(stdscr)
            break
        # Check if hit itself
        if len(snake) > 1:
            if snake[0] in snake[1:]:
                exit_game(stdscr)
                break
        # Check if fruit eaten
        if snake[0] == fruit[0]:
            snake, fruit = eat_fruit(snake)

        # Field input constantly
        c = stdscr.getch()
        # Move the snake on input
        if c == ord('w'):
            heading = 0
            snake = move_head(snake, heading)
            print_board(stdscr, snake, fruit)
        elif c == ord('a'):
            heading = 1
            snake = move_head(snake, heading)
            print_board(stdscr, snake, fruit)
        elif c == ord('s'):
            heading = 2
            snake = move_head(snake, heading)
            print_board(stdscr, snake, fruit)
        elif c == ord('d'):
            heading = 3
            snake = move_head(snake, heading)
            print_board(stdscr, snake, fruit)
        elif c == ord('q'):
            exit_game(stdscr)
            break
        # Move the snake on no input
        elif c == -1:
            snake = move_head(snake, heading)
            print_board(stdscr, snake, fruit)
        

        # Sleep a bit
        time.sleep(0.25)

if __name__ == '__main__':
    curses.wrapper(main)