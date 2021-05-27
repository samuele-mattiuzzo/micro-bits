from microbit import *
import random

pin2.set_touch_mode(pin2.CAPACITIVE)  # start button

# CONSTANTS
GAME_NAME = "micro:tunnel"
MS = 1000  # 1 millisecond
CHECK_TIME = 1 * MS  # speed, in seconds
SPACING = 5  # how many steps to wait before the next obstacle

OBSTACLE_START = "88088:"
PLAYER_START = "00500:"
BLANK = "00000:"

def setup():
    # creates the start
    return OBSTACLE_START + BLANK * 3 + PLAYER_START

def new_obstacle():
    # randomizes the next obstacle
    obstacle = "88888:"
    new_hole = random.randrange(5)
    return obstacle[:new_hole] + "0" + obstacle[new_hole + 1:]

def move_player(pos):
    # moves the player
    player = "00000:"
    return player[:pos] + "5" + player[pos + 1:]

def next_step(obstacle, player, obstacle_pos):
    # moves the obstacle one down
    return (BLANK * (0 + obstacle_pos)) \
            + obstacle \
            + (BLANK * (3 - obstacle_pos)) \
            + player

# MAIN GAME LOOPS
def logo():
    # shows the initial logo
    display.scroll(GAME_NAME)
    sleep(3 * MS)

def start_loop():
    while True:
        # waits for start to be pressed
        display.scroll("Press start (pin 3)")
        if pin2.is_touched(): break
        sleep(1 * MS)

def game_loop():
    # SESSION CONF
    lives = 3  # hit the wall => decrease
    player_pos = 2  # initial position, horizontal
    obstacle_pos = 0  # initial position, vertical
    
    player = PLAYER_START
    obstacle = OBSTACLE_START
    game_area = setup()

    start_time = 0
    total_game_time = 0

    score = 0  # 1 obstacle = 1 point
    steps = 0
    start_time = running_time()

    while lives > 0:
        
        # - every SPEED seconds, update the game area (scroll down) + append PLAYER
        # - if obstacle_pos = player_pos -> check for death
        # - if alive, score + 1, reset spacing
        # - if time elapsed is multiple of 60, increase speed by 10%
        # - when lives = 0, show scores

        # check for player input
        if button_a.is_pressed():  # left
            if player_pos > 0: player_pos -= 1
        elif button_b.is_pressed():  # right
            if player_pos < 4: player_pos += 1
        
        # update the player
        player = move_player(player_pos)

        if ((running_time() - start_time) / MS) % CHECK_TIME >= 0:
            # reset the timer
            start_time = running_time()
            steps += 1

            # move the obstacle down
            if steps < SPACING:
                obstacle_pos = obstacle_pos + 1 if obstacle_pos < 5 else obstacle_pos
            else:
                steps = 0
                obstacle_pos = 0  # reset the obstacle
                obstacle = new_obstacle()

        # update the game area
        game_area = next_step(obstacle, player, obstacle_pos)
        display.show(Image(game_area))

        # collision check
        if obstacle_pos == 4:
            if obstacle[player_pos] == "0":  # hole!
                score += 1
            else:
                lives -= 1

    display.show(Image.SKULL)
    display.scroll("Score: " + str(score))
    display.clear()


# MAIN
#logo()
#start_loop()
game_loop()