import os
import turtle

# Screen
screen = turtle.Screen()
screen.title("Space Invaders")
screen.bgcolor("black")
screen.setup(width = 800, height = 700)
screen.tracer(0)

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

# Enemy
enemy = turtle.Turtle()
enemy.speed(0)
enemy.shape("circle")
enemy.color("yellow")
enemy.penup()
enemy.goto(-200, 240)
x_speed = 0.2
y_speed = 40

# Player
player = turtle.Turtle()
player.speed(0)
player.shape("triangle")
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
weapon.setheading(90)
weaponspeed = 2
weaponstate = 0
weapon.goto(0, -400)

# Fire weapon
def fire_weapon():
    # Declare weaponstate as a global if it needs changes
    global weaponstate
    if weaponstate == 0:
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
while True:
    screen.update()
    
    # Move enemy
    x_e = enemy.xcor()
    x_e += x_speed
    enemy.setx(x_e)
    if x_e > 280:
        y_e = enemy.ycor()
        y_e -= y_speed
        x_speed *= -1
        enemy.sety(y_e)
    elif x_e < -280:
        y_e = enemy.ycor()
        y_e -= y_speed
        x_speed *= -1
        enemy.sety(y_e)
    
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
    
    # Check for a hit
    if is_hit(weapon, enemy):
        weapon.hideturtle()
        weaponstate = 0
        weapon.goto(0, -400)
        enemy.goto(-200, 240)

    # Check for enemy reaching player
    if is_hit(player, enemy):
        player.hideturtle()
        enemy.hideturtle()
        print('Game Over')
        break

input('Press enter to finish')
