import turtle
import time
import random

running = True
mem_goal = True
goal = False

# Cheat mode for testing.... or sneaky high scores!
CHEATS_ON = False

# Game Variables, Changing delay or delta_bg will effect how fast the bird "flys"
# delay effects speed of both flying through the pipes and flapping/falling
# delta_bg only effects speed of pipes 
delay = 0.05
screen_speed = 0
delta_bg = -5

# Score
score = 0
high_score = 0

# Set up Screen
wn = turtle.Screen()
wn.title("Flappy Bird")
wn.bgcolor('black')
wn.setup(width=600, height=600)
wn.tracer(0)# Turns off Screen Updates

right_edge = 300
left_edge = -300

# Def Quit, Gracefully exit game with Escape key
def quit():
    global running
    running = False

# Create ScoreBoard
board = turtle.Turtle()
board.speed(0)
board.shape("square")
board.color("white")
board.penup()
board.hideturtle()
board.goto(0,200)
board.write("Score: {} High score: {}".format(score, high_score),
                align="center", font=("Courier", 24, "normal"))

# Create Directions Splash
tip = turtle.Turtle()
tip.speed(0)
tip.shape("square")
tip.color("white")
tip.penup()
tip.hideturtle()
tip.goto(0,-200)
tip.write("Use 'Space' key to play", align="center",font=("Courier", 26, "bold"))

# Create Player "BIRD"
Bird = turtle.Turtle()
Bird.speed(0)
Bird.shape("turtle")
Bird.color("yellow")
Bird.penup()
Bird.turtlesize(1.5,1.5)

def hatch_bird():
    Bird.goto(0,0)
    Bird.direction = "stop"
    
hatch_bird()

# Define Bird Movment and clear Directions Splash on first use
def fly():
    Bird.direction = "fly"
    tip.setx(left_edge*3)
    tip.clear()
def fall():
    Bird.direction = "fall"
def move():
    if Bird.direction == "fly":
        y = Bird.ycor()
        Bird.sety(y + 15)
    if Bird.direction == "fall":
        y = Bird.ycor()
        Bird.sety(y - 10)

# Bird Key Binding
wn.listen()
wn.onkeypress(fly, "space")
wn.onkeyrelease(fall, "space")
wn.onkeypress(quit, "Escape")

# Create PIPE Shape
shapeA = ((0,0), (900,0), (900,50), (0,50))
shapeB = ((0,0), (-900,0), (-900,50), (0,50))
wn.register_shape("pipeA", shapeA)
wn.register_shape("pipeB", shapeB)

# Define Random Pipe Variables
p_close = 250
p_far = 400
gap_small = 100
gap_large = 200
h_min = -200
h_max = 200

# List of pipes
PIPES_TOP = []
PIPES_BOT = []
PIPES_NXT = []

# Move Pipes
def move_pipes():
    if Bird.direction != "stop":
        for index in range (len(PIPES_TOP)):
            x = PIPES_TOP[index-1].xcor()
            x += delta_bg
            PIPES_TOP[index-1].setx(x)
            PIPES_BOT[index-1].setx(x)

# ADD new Top Pipe to list
def make_top(gap, height):
    t = turtle.Turtle()
    t.speed(0)
    t.shape("pipeB")
    t.color("green")
    t.penup()
    t.shapesize()
    t.sety(height + (gap * 0.5))
    t.setx(right_edge)
    PIPES_TOP.append(t)
    PIPES_NXT.append(t)
  
# ADD new Bottom Pipe to list
def make_bot(gap, height):
    b = turtle.Turtle()
    b.speed(0)
    b.shape("pipeA")
    b.color("green")
    b.penup()
    b.shapesize()
    b.sety(height - (gap * 0.5))
    b.setx(right_edge)
    PIPES_BOT.append(b)

# Define Create Pipe
def create_pipe():
    if len(PIPES_TOP) < 5:
        gap = random.randint(gap_small,gap_large)
        height = random.randint(h_min,h_max)
        make_top(gap, height)
        make_bot(gap, height)

# Check if ready for new pipe
def check_pipes():
    spacing = random.randint(p_close,p_far)
    if PIPES_TOP[len(PIPES_TOP)-1].xcor() + spacing < right_edge:
        create_pipe()
    if PIPES_TOP[0].xcor() + 100 < left_edge:
        PIPES_TOP.remove(PIPES_TOP[0])
        PIPES_BOT.remove(PIPES_BOT[0])

# Start State
def pipes_start():
    make_top(150,0)
    make_bot(150,0)
    
# ReStart State
def game_restart():
    global score
    for pipe in range(len(PIPES_TOP)):
        PIPES_TOP[pipe-1].setx(left_edge*2)
        PIPES_BOT[pipe-1].setx(left_edge*2)

    PIPES_TOP.clear()
    PIPES_BOT.clear()
    PIPES_NXT.clear()
    score = 0
    board.setx(left_edge*3)
    board.clear()
    time.sleep(1.5)
    hatch_bird()
    pipes_start()

# Define Collision Detection
def detect_ouch():
    global goal, mem_goal
    # Detect collision with floor or cieling
    if Bird.ycor()-10 < -300 or Bird.ycor()+10 > 300:
        if CHEATS_ON == True:
            if Bird.ycor()-10 < -200:
                Bird.sety(-200)
            if Bird.ycor()+10 > 200:
                Bird.sety(200)
        else:
            game_restart()
    # Detect collision with pipes
    for pipe in range(len(PIPES_TOP)):
        if Bird.xcor()-40 <= PIPES_TOP[pipe-1].xcor()+25 and Bird.xcor() >= PIPES_TOP[pipe-1].xcor()-25:
            # Prime variables for use in registering Scoring
            goal = True
            mem_goal = True
            if CHEATS_ON != True:
                if Bird.ycor()+10 >= PIPES_TOP[pipe-1].ycor():
                    print("Collision")
                    game_restart()
                elif Bird.ycor()-10 <= PIPES_BOT[pipe-1].ycor():
                    print("Collision")
                    game_restart()
        else:
            # Reset variable used in Scoring
            goal = False   

# Update Score when Bird Fully Passes Pipe
def update_score():
    global score, high_score, mem_goal
    for index in range(len(PIPES_NXT)):
        if Bird.xcor()-40 > PIPES_NXT[0].xcor()+25:
            if mem_goal == True:
                board.setx(left_edge*3)
                board.clear()
                score += 1
                if score > high_score:
                    high_score = score
            mem_goal = False
        if Bird.xcor()-40 > PIPES_NXT[0].xcor()+50:
            PIPES_NXT.remove(PIPES_NXT[0])

    else:
        board.goto(0,200)
        board.write("Score: {} High score: {}".format(score, high_score),
                    align="center", font=("Courier", 24, "normal"))

pipes_start()

# Main Loop
while running:
    wn.update()
    detect_ouch()
    move()
    move_pipes()
    check_pipes()
    update_score()
    time.sleep(delay)
wn.bye()