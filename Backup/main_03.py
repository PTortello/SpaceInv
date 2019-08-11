# TODO enemy fire
# TODO turtle.mainloop() and turtle.done() in another file as function?
# TODO change enemies continuous movement to step movement
#   Try:
#       turtle.delay(t); t = milliseconds
#       multithread

import time
import turtle
import winsound

# Fire weapon
def fire_weapon():
    # Declare weaponstate as a global if it needs changes
    global weaponstate
    if weaponstate == 0:
        winsound.PlaySound(".\Sounds\s_laser.wav", winsound.SND_ASYNC)
        weaponstate = 1
        # Move the missile to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        weapon.goto(x, y)

# Check hit
def is_hit(t1, t2):
    distance = (
        (t1.xcor() - t2.xcor()) ** 2 + (t1.ycor() - t2.ycor()) ** 2
    ) ** 0.5
    return True if distance < 15 else False

# Move player
def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 235:
        x = 235
    player.setx(x)

def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -235:
        x = -235
    player.setx(x)

# Screen set up
screen = turtle.Screen()
screen.title("Space Invaders")
screen.setup(width = 700, height = 800)

# Register shapes
screen.register_shape(".\Images\_player.gif")
screen.register_shape(".\Images\_enemy_1.gif")
screen.register_shape(".\Images\_enemy_2.gif")
screen.register_shape(".\Images\_enemy_3.gif")

# Main game loop
level = 1
gameover = False
while not gameover:

    # Screen
    screen.bgcolor("black")
    screen.tracer(0)

    # Border
    border_pen = turtle.Turtle()
    border_pen.speed(0)
    border_pen.hideturtle()
    border_pen.color("white")
    border_pen.pensize(3)
    border_pen.penup()
    border_pen.goto(-250, -350)
    border_pen.pendown()
    v = -100
    for side in range(4):
        border_pen.fd(600 + v)
        border_pen.lt(90)
        v *= -1

    # Disclaimer
    disc_pen = turtle.Turtle()
    disc_pen.speed(0)
    disc_pen.hideturtle()
    disc_pen.color("white")
    disc_pen.penup()
    disc_pen.goto(0, 0)

    # Score
    score_pen = turtle.Turtle()
    score_pen.speed(0)
    score_pen.hideturtle()
    score_pen.color("white")
    score_pen.penup()
    score_pen.goto(0, 350)
    scorecor = []
    with open ('score.ttl', "r") as f:
        for line in f:
            scorecor.append(int(line.strip()))
    if level == 1:
        scorecor[0] = 0
        with open ('score.ttl', "w") as f:
            f.write(str(scorecor[0]) + "\n" + str(scorecor[1]))
    score_str = f"Score: {scorecor[0]}\t\t\tRecord: {scorecor[1]}"
    score_pen.write(score_str, False, align="center", font=("Courier", 12, "normal"))

    # Player
    player = turtle.Turtle()
    player.speed(0)
    player.shape(".\Images\_player.gif")
    player.penup()
    player.goto(0, -300)
    playerspeed = 15

    # Player weapon
    weapon = turtle.Turtle()
    weapon.speed(0)
    weapon.hideturtle()
    weapon.shape("arrow")
    weapon.shapesize(0.1, 0.5)
    weapon.color("white")
    weapon.penup()
    weapon.goto(0, -450)
    weapon.setheading(90)
    weaponspeed = 2
    weaponstate = 0

    # Keyboard binding
    screen.listen()
    screen.onkeypress(move_right, "Right")
    screen.onkeypress(move_left, "Left")
    screen.onkeypress(fire_weapon, "space")

    screen.update()

    # Enemies
    enemies_rows = 5
    enemies_in_row = 11
    enemies = [[], [], [], [], []]
    x_origin = -220
    y_origin = 340 - 40 * level
    y_space = 0
    for i in range(enemies_rows):
        for j in range(enemies_in_row):
            enemies[i].append(turtle.Turtle())
        x_space = 0
        for enemy in enemies[i]:
            if y_space == 0:
                enemy.shape(".\Images\_enemy_3.gif")
            elif y_space < -80:
                enemy.shape(".\Images\_enemy_1.gif")
            else:
                enemy.shape(".\Images\_enemy_2.gif")
            enemy.speed(0)
            enemy.penup()
            enemy.goto(x_origin + x_space, y_origin + y_space)
            x_space += 40
        y_space -= 40
    speed_in = 0
    x_speed = 0.1
    y_speed = 40
    e_alive = enemies_rows * enemies_in_row
    
    # Level loop
    disc_pen.write(f"Level {level}", False, align="center", font=("Courier", 28, "normal"))
    time.sleep(3)
    disc_pen.clear()
    next_lvl = False
    while not next_lvl:
        screen.update()
        
        # Move enemies
        for i in range(enemies_rows):
            temp_lis = enemies[0].copy()
            for enemy in enemies[i]:
                enemy.setx(enemy.xcor() + x_speed)

                # Check for a hit
                if is_hit(weapon, enemy):
                    winsound.PlaySound(".\Sounds\s_explod.wav", winsound.SND_ASYNC)
                    weapon.hideturtle()
                    weaponstate = 0
                    weapon.goto(0, -450)
                    e_alive -= 1
                    speed_in += 1
                    if i == 0:
                        temp_lis = [k for k in enemies[0] if k != enemy]
                    enemy.goto(0, 1500)
                    # Update score
                    if i < 1:
                        scorecor[0] += 30
                    elif i < 3:
                        scorecor[0] += 20
                    else:
                        scorecor[0] += 10
                    score_str = score_str = f"Score: {scorecor[0]}\t\t\tRecord: {scorecor[1]}"
                    score_pen.clear()
                    score_pen.write(score_str, False, align="center", font=("Courier", 12, "normal"))

                # Check for enemy reaching player
                if is_hit(player, enemy) or enemy.ycor() <= player.ycor():
                    winsound.PlaySound(".\Sounds\s_gm_ovr.wav", winsound.SND_ASYNC)
                    screen.update()
                    disc_pen.write(
                        f"GAME OVER", False, align="center", font=("Courier", 28, "normal")
                        )
                    print('Game Over')
                    if scorecor[0] > scorecor[1]:
                        time.sleep(3)
                        disc_pen.clear()
                        disc_pen.write(
                            f"New Record: {scorecor[0]}", False, align="center", font=("Courier", 28, "normal")
                            )
                        with open ('score.ttl', "w") as f:
                            f.write(str(0) + "\n" + str(scorecor[0]))
                    else:
                        with open ('score.ttl', "w") as f:
                            f.write(str(0) + "\n" + str(scorecor[1]))
                    gameover = True
                    next_lvl = True
                    break
            enemies[0] = temp_lis.copy()
        
        # Speed increase
        if speed_in == 7:
            speed_in = 0
            if x_speed > 0:
                x_speed += 0.01
            else:
                x_speed -= 0.01

        # Level & Wall bump
        if e_alive == 0:
            # Next level
            print('Next Level')
            level += 1
            next_lvl = True
            with open ('score.ttl', "w") as f:
                f.write(str(scorecor[0]) + "\n" + str(scorecor[1]))
            turtle.clearscreen()
            for i in range(enemies_rows):
                for enemy in enemies[i]:
                    del enemy
        else:
            # Check wall bump
            if enemies[0][0].xcor() > 235 or enemies[0][len(enemies[0])-1].xcor() > 235:
                x_speed *= -1
                for i in range(enemies_rows):
                    for enemy in enemies[i]:
                        enemy.sety(enemy.ycor() - y_speed)
            elif enemies[0][0].xcor() < -235 or enemies[0][len(enemies[0])-1].xcor() < -235:
                x_speed *= -1
                for i in range(enemies_rows):
                    for enemy in enemies[i]:
                        enemy.sety(enemy.ycor() - y_speed)

        # Move missile
        if weaponstate == 1:
            weapon.showturtle()
            y_w = weapon.ycor()
            y_w += weaponspeed
            weapon.sety(y_w)
        if weapon.ycor() > 340:
            weapon.hideturtle()
            weaponstate = 0
            weapon.goto(0, -450)

time.sleep(3)
