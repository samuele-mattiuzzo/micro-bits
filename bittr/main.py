from microbit import *
import random
pin2.set_touch_mode(pin2.CAPACITIVE)


MS = 1000
CHECK_TIME = 10 * MS  # speed, in seconds
SPACING = 4  # how many lines to wait before the next obstacle

OBSTACLE = "88088:"
PLAYER = "00500:"
BLANK = "00000:"

current_pos = 2  # initial position, horizontal
obstacle_pos = 0  # initial position, vertical
lives = 3  # hit the wall => decrease

start_time = 0
total_game_time = 0
playing = False
score = 0  # 1 obstacle = 1 point
game_area = OBSTACLE + BLANK * 3 + PLAYER
steps = 0

while lives > 0:
    if not playing:
        display.show(Image(game_area))
        if pin2.is_touched():
            playing = True
            start_time = running_time()
    else:
        # game loop:
        # - check for player input
        # - every SPEED seconds, update the game area (scroll down) + append PLAYER
        # - if obstacle_pos = current_pos -> check for death
        # - if alive, score + 1, reset spacing
        # - if time elapsed is multiple of 60, increase speed by 10%
        # - when lives = 0, show scores

        if button_a.is_pressed():  # left
            if current_pos > 0:
                current_pos -= 1
        elif button_b.is_pressed():  # right
            if current_pos < 4:
                current_pos += 1
        PLAYER = "00000:"
        PLAYER = PLAYER[:current_pos] + "5" + PLAYER[current_pos + 1:]

        if (running_time() - start_time) / MS >= CHECK_TIME:
            # reset the timer
            start_time = running_time()
            steps += 1

            # move the obstacle down
            if steps < SPACING:
                obstacle_pos = obstacle_pos + 1 if obstacle_pos < 4 else obstacle_pos
            else:
                steps = 0
                obstacle_pos = 0  # reset the obstacle
                # randomizes the next obstacle
                OBSTACLE = "88888:"
                new_hole = random.randrange(5)
                OBSTACLE = OBSTACLE[:new_hole] + "0" + OBSTACLE[new_hole + 1:]

        # update the game area
        game_area = (
            (BLANK * 0 + obstacle_pos)
            + OBSTACLE
            + (BLANK * 3 - obstacle_pos)
            + PLAYER
        )

        if obstacle_pos == current_pos:
            if OBSTACLE[current_pos] == "0":
                score += 1
            else:
                lives -= 1
        display.show(Image(game_area + PLAYER))
        if lives == 0:
            break

display.show(Image.SKULL)

display.scroll("Score: " + score)
display.clear()
