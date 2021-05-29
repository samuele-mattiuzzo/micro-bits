from microbit import Image, display, sleep, button_a, button_b
import speech, random

# CONSTANTS
GAME_NAME = "micro:tunnel"
MS = 1000  # 1000 milliseconds = 1 second
TICK_TIME = 100  # 100 milliseconds
TICKS_TO_SECOND = 10  # 100ms * 10 = 1 second

OBSTACLE_START = "88088:"
PLAYER_START = "00500:"
BLANK = "00000:"


# GAME FUNCTIONS
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

def game_loop():
    # new game
    lives = 3  # hit the wall => decrease
    player_pos = 2  # initial position, horizontal
    obstacle_pos = 0  # initial position, vertical
    
    player = PLAYER_START
    obstacle = OBSTACLE_START
    game_area = setup()

    ticks = score = 0

    while lives > 0:
        # check for player input
        if button_a.is_pressed():  # left
            if player_pos > 0: player_pos -= 1
        elif button_b.is_pressed():  # right
            if player_pos < 4: player_pos += 1
        
        # update the player
        player = move_player(player_pos)

        # update the obstacle
        if ticks == TICKS_TO_SECOND:
            # 1 second elapsed, move down
            obstacle_pos = obstacle_pos + 1 if obstacle_pos < 4 else obstacle_pos
            
            # collision check
            if obstacle_pos == 4:
                if obstacle[player_pos] == "0":  # hole!
                    score += 1
                    speech.say("Nice")
                else:
                    lives -= 1
                    speech.say("Ouch")
                
                obstacle_pos = 0  # reset the obstacle
                obstacle = new_obstacle()
            ticks = 0
        else:
            # regular tick, don't change the obstacle, increase the ticks count
            ticks += 1

        # update the game area
        game_area = next_step(obstacle, player, obstacle_pos)
        display.show(Image(game_area))
        sleep(TICK_TIME)

    display.show(Image.SKULL)
    sleep(3 * MS)
    display.scroll("Score: " + str(score))
    sleep(5 * MS)
    display.clear()

# MAIN
logo()
game_loop()
