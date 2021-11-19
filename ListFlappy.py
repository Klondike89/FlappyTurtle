import turtle
import time
import random

delay = 0.05
delta_bg = -10

# Set up Screen
wn = turtle.Screen()
wn.title("Flappy Bird")
wn.bgcolor('black')
wn.setup(width=600, height=600)
wn.tracer(0)# Turns off Screen Updates

right_edge = 300
left_edge = -300

# Create Player "BIRD"
Bird = turtle.Turtle()
Bird.speed(0)
Bird.shape("turtle")
Bird.goto(0,0)
Bird.color("yellow")
Bird.penup()
Bird.direction = "stop"


# Define Player Movment
def fly():
    Bird.direction = "fly"

def fall():
    Bird.direction = "fall"

def move():
    if Bird.direction == "fly":
        y = Bird.ycor()
        Bird.sety(y + 15)

    if Bird.direction == "fall":
        y = Bird.ycor()
        Bird.sety(y - 10)

# Key Binding
wn.listen()
wn.onkeypress(fly, "f")
wn.onkeyrelease(fall, "f")



# Create PIPE Shape
shapeA = ((0,0), (900,0), (900,50), (0,50))
shapeB = ((0,0), (-900,0), (-900,50), (0,50))

wn.register_shape("pipeA", shapeA)
wn.register_shape("pipeB", shapeB)

# Define Random Pipe Variables
p_close = 150
p_far = 400
gap_small = 50
gap_large = 200
h_min = -300
h_max = 300


# List of pipes
PIPES_TOP = []
PIPES_BOT = []
            #[pos, height, gap, width]
FIRST_PIPE = [  0,   0, 150,     0]

def move_pipes():
    for index in range (len(PIPES_TOP)):
        x = PIPES_TOP[index-1].xcor()
        x += delta_bg
        PIPES_TOP[index-1].setx(x)
        PIPES_BOT[index-1].setx(x)

# ADD new Top Pipe to list
def make_top(gap, height):
    # height = FIRST_PIPE[1]
    # gap = FIRST_PIPE[2]
    t = turtle.Turtle()
    t.speed(0)
    t.shape("pipeB")
    t.color("green")
    t.penup()
    t.shapesize()
    t.sety(height + (gap * 0.5))
    t.setx(right_edge)
    PIPES_TOP.append(t)
  
# ADD new Bottom Pipe to list
def make_bot(gap, height):
    # height = FIRST_PIPE[1]
    # gap = FIRST_PIPE[2]
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
# spacing = 100
def check_pipes():
    spacing = random.randint(p_close,p_far)
    if PIPES_TOP[len(PIPES_TOP)-1].xcor() + spacing < right_edge:
        create_pipe()
    
    if PIPES_TOP[0].xcor() + 100 < left_edge:
        PIPES_TOP.remove(PIPES_TOP[0])
        PIPES_BOT.remove(PIPES_BOT[0])
    
# Define Collision Detection
def detect_ouch():
    # Collision Detection
    for pipe in range(len(PIPES_TOP)):
        # print(PIPES_TOP[index-1].xcor())
        if Bird.xcor()-5 <= PIPES_TOP[pipe-1].xcor()+25 and Bird.xcor()+5 >= PIPES_TOP[pipe-1].xcor()-25:
            print("PIPE!!!")
            print(len(PIPES_TOP))
            if Bird.ycor()+5 >= PIPES_TOP[pipe-1].ycor():
                print("Collision")
            elif Bird.ycor()-5 <= PIPES_BOT[pipe-1].ycor():
                print("Collision")

make_top(150,0)
make_bot(150,0)

while True:
    wn.update()   
    detect_ouch()
    move()
    move_pipes()
    check_pipes()
    time.sleep(delay)
wn.mainloop()