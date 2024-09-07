import turtle
import random


window = turtle.Screen()
window.title("Turtle Game with Moving Walls and Static Obstacles")
window.bgcolor("white")
window.setup(width=600, height=600)


rules_display = turtle.Turtle()
rules_display.hideturtle()
rules_display.penup()
rules_display.goto(0, 250)
rules_display.write("Rules:\n1. Use W, A, S, D to move the triangle.\n2. Collect the red circle to earn points.\n3. Avoid the blue walls and green obstacles.\n4. Colliding with walls or obstacles ends the game.", align="center", font=("Arial", 12, "normal"))


player = turtle.Turtle()
player.shape("triangle")
player.color("black")
player.penup()
player.speed(0)


food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.speed(0)
food.goto(random.randint(-280, 280), random.randint(-280, 280))


walls = []
wall_positions = [(-250, 250, 20, 100), (-150, -150, 20, 100), (100, -250, 100, 20), (200, 150, 100, 20)]
for x, y, width, height in wall_positions:
    wall = turtle.Turtle()
    wall.shape("square")
    wall.color("blue")
    wall.penup()
    wall.speed(0)
    wall.shapesize(stretch_wid=height / 20, stretch_len=width / 20)
    wall.goto(x, y)
    walls.append(wall)


obstacles = []
obstacle_positions = [(-100, 100, 20, 20), (150, -200, 30, 30), (-200, -100, 20, 20), (200, 200, 30, 30)]
for x, y, width, height in obstacle_positions:
    obstacle = turtle.Turtle()
    obstacle.shape("square")
    obstacle.color("green")
    obstacle.penup()
    obstacle.speed(0)
    obstacle.shapesize(stretch_wid=height / 20, stretch_len=width / 20)
    obstacle.goto(x, y)
    obstacles.append(obstacle)


score = 0


score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(0, 220)
score_display.write(f"Score: {score}", align="center", font=("Arial", 16, "normal"))

def move_walls():
    for wall in walls:
        x, y = wall.position()
        new_x = x + random.randint(-20, 20)
        new_y = y + random.randint(-20, 20)
       
        new_x = max(min(new_x, 280), -280)
        new_y = max(min(new_y, 280), -280)
        wall.goto(new_x, new_y)
    
  
    window.ontimer(move_walls, 1000)

def move_up():
    y = player.ycor()
    new_y = y + 30
    if new_y < 280 and not collides_with_walls(player.xcor(), new_y) and not collides_with_obstacles(player.xcor(), new_y):
        player.sety(new_y)

def move_down():
    y = player.ycor()
    new_y = y - 30
    if new_y > -280 and not collides_with_walls(player.xcor(), new_y) and not collides_with_obstacles(player.xcor(), new_y):
        player.sety(new_y)

def move_left():
    x = player.xcor()
    new_x = x - 30
    if new_x > -280 and not collides_with_walls(new_x, player.ycor()) and not collides_with_obstacles(new_x, player.ycor()):
        player.setx(new_x)

def move_right():
    x = player.xcor()
    new_x = x + 30
    if new_x < 280 and not collides_with_walls(new_x, player.ycor()) and not collides_with_obstacles(new_x, player.ycor()):
        player.setx(new_x)

def collides_with_walls(x, y):
    for wall in walls:
        wall_x, wall_y = wall.position()
        wall_width = wall.shapesize()[1] * 20
        wall_height = wall.shapesize()[0] * 20
        wall_rect = (wall_x - wall_width / 2, wall_y - wall_height / 2, wall_width, wall_height)
        
       
        if (wall_rect[0] < x < wall_rect[0] + wall_rect[2] and
            wall_rect[1] < y < wall_rect[1] + wall_rect[3]):
            return True
    return False

def collides_with_obstacles(x, y):
    for obstacle in obstacles:
        obstacle_x, obstacle_y = obstacle.position()
        obstacle_width = obstacle.shapesize()[1] * 20
        obstacle_height = obstacle.shapesize()[0] * 20
        obstacle_rect = (obstacle_x - obstacle_width / 2, obstacle_y - obstacle_height / 2, obstacle_width, obstacle_height)
        
        
        if (obstacle_rect[0] < x < obstacle_rect[0] + obstacle_rect[2] and
            obstacle_rect[1] < y < obstacle_rect[1] + obstacle_rect[3]):
            return True
    return False

def check_collision():
    global score
    if player.distance(food) < 25:
        food.goto(random.randint(-280, 280), random.randint(-280, 280))
        score += 5
        score_display.clear()
        score_display.write(f"Score: {score}", align="center", font=("Arial", 16, "normal"))

  
    if collides_with_walls(player.xcor(), player.ycor()) or collides_with_obstacles(player.xcor(), player.ycor()):
        game_over()
    else:
        
        window.ontimer(check_collision, 100)

def game_over():
    player.hideturtle()
    score_display.goto(0, 0)
    score_display.write(f"Game Over\nFinal Score: {score}", align="center", font=("Arial", 24, "bold"))
    window.update()
    window.bye()


window.listen()
window.onkey(move_up, "w")
window.onkey(move_down, "s")
window.onkey(move_left, "a")
window.onkey(move_right, "d")


move_walls()
check_collision()


window.mainloop()
