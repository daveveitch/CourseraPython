# DAVID VEITCH COURSEARA PONG
# Implementation of classic arcade game Pong
# http://www.codeskulptor.org/#user40_AZvhTjsosa_14.py

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 15
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PADDLE_SPEED = 4
INITIAL_BALL_SPEED = 4

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global LEFT, RIGHT
    
    ball_pos = [WIDTH/2,HEIGHT/2]
    
    # randomly assigns a up/down velocity to the ball and serves to a side
    if direction == "Left":
        ball_vel = [ INITIAL_BALL_SPEED, random.choice([-2, 2]) * random.random() ]
    elif direction == "Right":
        ball_vel = [ -1 * INITIAL_BALL_SPEED, random.choice([-2, 2]) * random.random() ] 
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # Sets paddles to middle of screen @ start of game
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    
    # sets paddle velocity to 0 at start of game
    paddle1_vel = 0
    paddle2_vel =  0

    # sets scores to 0
    score1 = 0
    score2 = 0
    
    spawn_ball('Left')
       
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, LEFT, RIGHT
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
        
    # bounces ball off top and bottom of screen
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - BALL_RADIUS)):
        ball_vel[1] = ball_vel[1] * -1                                            
    
    # draw ball
    canvas.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 2, 'White', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    # checks if it would put it off the screen before changing
    if (paddle1_pos + paddle1_vel) >= (HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos = paddle1_pos
    elif (paddle1_pos + paddle1_vel) <= (HALF_PAD_HEIGHT):
        paddle1_pos = paddle1_pos
    else:
        paddle1_pos += paddle1_vel
    
    if (paddle2_pos + paddle2_vel) >= (HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos = paddle2_pos
    elif (paddle2_pos + paddle2_vel) <= (HALF_PAD_HEIGHT):
        paddle2_pos = paddle2_pos
    else:
        paddle2_pos += paddle2_vel
        
    # draw paddles
    canvas.draw_line((0, paddle1_pos + HALF_PAD_HEIGHT ), (0, paddle1_pos - HALF_PAD_HEIGHT ), PAD_WIDTH+8, 'White')
    canvas.draw_line((WIDTH-4, paddle2_pos + HALF_PAD_HEIGHT ), (WIDTH-4, paddle2_pos - HALF_PAD_HEIGHT ), PAD_WIDTH, 'White')
    
    # determine whether paddle and ball collide
    # checks if ball is on the gutter and within range of paddle height if so reverses balll velocity
    
    if ball_pos[0] <= (PAD_WIDTH + BALL_RADIUS):
        if (ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT + BALL_RADIUS)) and (ball_pos[1] >= (paddle1_pos - HALF_PAD_HEIGHT - BALL_RADIUS)):
            ball_vel[0] = ball_vel[0] * -1
            # changes vertical direction of ball based on where it hits the paddle
            ball_vel[1] = ball_vel[1] + ( (ball_pos[1] - paddle1_pos) / (HALF_PAD_HEIGHT) )
            # adds a little bit of speed to the ball
            ball_vel[0] += 0.1
        else:
            score2 += 1
            spawn_ball('Left')            
        
    elif ball_pos[0] >= (WIDTH - (PAD_WIDTH + BALL_RADIUS)):
        if (ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT + BALL_RADIUS)) and (ball_pos[1] >= (paddle2_pos - HALF_PAD_HEIGHT - BALL_RADIUS)):
            ball_vel[0] = ball_vel[0] * -1 
            # changes vertical direction of ball based on where it hits the paddle
            ball_vel[1] = ball_vel[1] + ( (ball_pos[1] - paddle2_pos) / (HALF_PAD_HEIGHT) )
            # adds a little bit of speed to the ball
            ball_vel[0] -= 0.1
        else:
            score1 += 1
            spawn_ball('Right')            
    
    # draw scores
    canvas.draw_text(str(score1), [125,100], 64, 'White')
    canvas.draw_text(str(score2), [450,100], 64, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    #increases velocity to PADDLE_SPEED on a key press
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += -1 * PADDLE_SPEED
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 1 * PADDLE_SPEED
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel += -1 * PADDLE_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 1 * PADDLE_SPEED                                     
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    #decreases velocity by PADDLE_SPEED on key up
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= -1 * PADDLE_SPEED
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= 1 * PADDLE_SPEED
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= -1 * PADDLE_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= 1 * PADDLE_SPEED 
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game)

# start frame
new_game()
frame.start()
