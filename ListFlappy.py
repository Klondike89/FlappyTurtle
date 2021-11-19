import turtle
import time
import random

delay = 0.05

# Set up Screen
wn = turtle.Screen()
wn.title("Flappy Bird")
wn.bgcolor('black')
wn.setup(width=600, height=600)
wn.tracer(0)# Turns off Screen Updates


###  Try and get a turtle to scroll left then loop back arround ###
Scroll = turtle.Turtle()
Scroll.speed(0)
Scroll.shape("triangle")
Scroll.color("red")
Scroll.goto(0,0)
Scroll.penup()

right_edge = 300
left_edge = -300

def move_Scroll():
    if Scroll.xcor() > left_edge:
        x = Scroll.xcor()
        Scroll.setx(x - 10)

    else:
        Scroll.setx(right_edge)


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
        Bird.sety(y - 5)

# Key Binding
wn.listen()
wn.onkeypress(fly, "f")
wn.onkeyrelease(fall, "f")



# Create PIPE Shape
shapeA = ((0,0), (900,0), (900,50), (0,50))
shapeB = ((0,0), (-900,0), (-900,50), (0,50))

wn.register_shape("pipeA", shapeA)
wn.register_shape("pipeB", shapeB)

next_pipe = 0

# List of pipes
PIPES_TOP = []
PIPES_BOT = []
            #[pos, height, gap, width]
FIRST_PIPE = [  0,   0, 150,     0]

# ADD new Top Pipe to list
def make_top():
    height = FIRST_PIPE[1]
    gap = FIRST_PIPE[2]
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
def make_bot():
    height = FIRST_PIPE[1]
    gap = FIRST_PIPE[2]
    b = turtle.Turtle()
    b.speed(0)
    b.shape("pipeA")
    b.color("green")
    b.penup()
    b.shapesize()
    b.sety(height - (gap * 0.5))
    b.setx(right_edge)
    PIPES_BOT.append(b)

while True:
    wn.update()
        
    # Create Pipes
    # print(PIPES_TOP)
    if len(PIPES_TOP) < 2:
        if Scroll.xcor() < left_edge +50:
            make_top()
            make_bot()
    
    for index in range(len(PIPES_TOP)):
        x = Scroll.xcor()
        PIPES_TOP[index-1].setx(x + (index * 200))
        PIPES_BOT[index-1].setx(x + (index * 200))

    # Collision Detection
    for pipe in range(len(PIPES_TOP)):
        # print(PIPES_TOP[index-1].xcor())
        if Bird.xcor()-5 <= PIPES_TOP[pipe-1].xcor()+25 and Bird.xcor()+5 >= PIPES_TOP[pipe-1].xcor()-25:
            print("PIPE!!!")
            if Bird.ycor()+5 >= PIPES_TOP[pipe-1].ycor():
                print("Collision")
            elif Bird.ycor()-5 <= PIPES_BOT[pipe-1].ycor():
                print("Collision")

    move()
    move_Scroll()
    time.sleep(delay)
wn.mainloop()