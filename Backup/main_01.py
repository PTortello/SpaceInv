import os
import random
import turtle
import winsound

# Screen
screen = turtle.Screen()
screen.title("Space Invaders")
screen.bgcolor("black")
screen.setup(width = 800, height = 700)
screen.tracer(0)

# Register shapes
screen.register_shape("_player.gif")
screen.register_shape("_enemy_1.gif")
screen.register_shape("_enemy_2.gif")
screen.register_shape("_enemy_3.gif")

# Border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.hideturtle()
border_pen.color("white")
border_pen.pensize(3)
border_pen.penup()
border_pen.goto(-300, -300)
border_pen.pendown()
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)

# Score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.hideturtle()
score_pen.color("white")
score_pen.penup()
score_pen.goto(-290, 280)
score = 0
score_str = f"Score: {score}"
score_pen.write(score_str, False, align="left", font=("Courier", 12, "normal"))

# Enemies
num_enemies = 10
enemies = []
for i in range(num_enemies):
    enemies.append(turtle.Turtle())
for enemy in enemies:
    enemy.speed(0)
    enemy.shape("_enemy_1.gif")
    enemy.color("white")
    enemy.penup()
    x = random.randint(-200, 200)
    y = random.randint(120, 240)
    enemy.goto(x, y)
    # enemy.goto(-200, 240)     # original enemy position
x_speed = 0.1
y_speed = 40

# Player
player = turtle.Turtle()
player.speed(0)
player.shape("_player.gif")
player.color("lime")
player.penup()
player.goto(0, -250)
player.setheading(90)
playerspeed = 15

# Player weapon
weapon = turtle.Turtle()
weapon.speed(0)
weapon.hideturtle()
weapon.shape("arrow")
weapon.shapesize(0.1, 0.5)
weapon.color("white")
weapon.penup()
weapon.goto(0, -400)
weapon.setheading(90)
weaponspeed = 2
weaponstate = 0

# Fire weapon
def fire_weapon():
    # Declare weaponstate as a global if it needs changes
    global weaponstate
    if weaponstate == 0:
        winsound.PlaySound("s_laser.wav", winsound.SND_ASYNC)
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
    if x > 280:
        x = 280
    player.setx(x)

def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

# Keyboard binding
screen.listen()
screen.onkeypress(move_right, "Right")
screen.onkeypress(move_left, "Left")
screen.onkeypress(fire_weapon, "space")

# Main game loop
gameover = False
while not gameover:
    screen.update()

    # Move enemies
    for enemy in enemies:
        x_e = enemy.xcor()
        x_e += x_speed
        enemy.setx(x_e)
        if x_e > 280:
            x_speed *= -1
            for e in enemies:
                y_e = e.ycor()
                y_e -= y_speed
                e.sety(y_e)
        elif x_e < -280:
            x_speed *= -1
            for e in enemies:
                y_e = e.ycor()
                y_e -= y_speed
                e.sety(y_e)

        # Check for a hit
        if is_hit(weapon, enemy):
            winsound.PlaySound("s_explod.wav", winsound.SND_ASYNC)
            weapon.hideturtle()
            weaponstate = 0
            weapon.goto(0, -400)
            x = random.randint(-200, 200)
            y = random.randint(120, 240)
            enemy.goto(x, y)
            # Update score
            score += 10
            score_str = f"Score: {score}"
            score_pen.clear()
            score_pen.write(score_str, False, align="left", font=("Courier", 12, "normal"))

        # Check for enemy reaching player
        if is_hit(player, enemy) or enemy.ycor() <= player.ycor():
            winsound.PlaySound("s_gm_ovr.wav", winsound.SND_ASYNC)
            screen.update()
            print('Game Over')
            gameover = True

    # Move missile
    if weaponstate == 1:
        weapon.showturtle()
        y_w = weapon.ycor()
        y_w += weaponspeed
        weapon.sety(y_w)
    if weapon.ycor() > 280:
        weapon.hideturtle()
        weaponstate = 0
        weapon.goto(0, -400)

input('Press enter to finish')
