# DAVID VEITCH MINIPROJECT 7
# program template for Spaceship
# http://www.codeskulptor.org/#user42_C7zCVxPP21_17.py
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
SHIP_THRUST_SPEED = 0.2
SHIP_TURNING_RADIUS = 0.1
FRICTION_MULTIPLIER = .04
MAX_ROCK_SPEED = 1
MAX_ROCK_ANGULAR_VELOCITY = 0.1
MISSILE_SPEED = 3
ROCK_SPAWN_DIST_CHECK = 100 # Min distance from ship rock must spawn
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 100)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def angle_change(self, angle_change):
        # this takes the angle change and adds it to the angle velocity
        self.angle_vel += angle_change
    
    def thruster_control(self, thruster_boolean):
        self.thrust = thruster_boolean
        if self.thrust: ship_thrust_sound.play()
        else: ship_thrust_sound.rewind()
    
    def shoot(self):
        
        # spawns a missle at tip of ships cannon
        a_missile = Sprite([self.pos[0] + angle_to_vector(self.angle)[0]*self.image_size[0]/2, 
                            self.pos[1] + angle_to_vector(self.angle)[1]*self.image_size[1]/2], 
                           [self.vel[0] + angle_to_vector(self.angle)[0] * MISSILE_SPEED,
                            self.vel[1] + angle_to_vector(self.angle)[1] * MISSILE_SPEED], 
                           0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    def draw(self,canvas):
        
        # determines if ship thrusting or not, switches where image centre is based on this
        if self.thrust: canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0], self.image_center[1]), 
                                          self.image_size, self.pos, self.image_size, self.angle)
        else: canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, 
                              self.image_size, self.angle)

    def update(self):
        self.pos = [self.pos[0] % WIDTH + self.vel[0], self.pos[1] % HEIGHT + self.vel[1]]
        self.angle = self.angle + self.angle_vel
        
        # if ship is thrusting, updates the velocity
        if self.thrust:
            self.vel[0] += angle_to_vector(self.angle)[0] * SHIP_THRUST_SPEED
            self.vel[1] += angle_to_vector(self.angle)[1] * SHIP_THRUST_SPEED 	
        
        # slows ship down with friction
        self.vel[0] *= (1 - FRICTION_MULTIPLIER)
        self.vel[1] *= (1 - FRICTION_MULTIPLIER)
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos = [self.pos[0] % WIDTH + self.vel[0], self.pos[1] % HEIGHT + self.vel[1]]
        self.angle = self.angle + self.angle_vel 
        
        # Increments age and checks if age>lifespan, if so returns true
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) < (self.radius + other_object.get_radius()):
            return True
        else:
            return False
    

# function that checks if there are collisions between groups, returns True if collision happens
def group_collide(group, other_object):
    # Will evaluate to True if collision happens
    collision_occur = False
    
    # iterates through the group, removes from set if objects colliding)
    for i in list(group):
        if i.collide(other_object):
            group.remove(i)
            collision_occur = True
            print collision_occur

    if collision_occur:
        return True
            
# function that tests collisions between two groups
def group_group_collide(group1, group2):
    global score
    
    for i in list(group1):
        # evaluates if there is a collision, removes
        # element from set if there is
        if group_collide(group2, i):
            group1.remove(i)
            score += 1
            

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    global lives
    global score
    
    # starts timer for spawning rocks
    timer.start()
    
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
    
    # starts the game soundtrack
    soundtrack.play()

    # resets lives and score and timer if game being restarted
    if lives <= 0:
        lives = 3
        score = 0
        
        
def draw(canvas):
    global time
    global lives
    global started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # updates and draws the rock/missile group
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    
    # draws text on the canvas
    canvas.draw_text("Created by David Veitch --- " + "Lives = " + str(lives) + " Score =  " + str(score), (5, 25), 24, 'Red')

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    # checks collisions between ships and rocks
    # uses a counter to see if # rocks changed, if so decrease life
    temp_rock_count = len(rock_group)
    group_collide(rock_group, my_ship)
    if len(rock_group) < temp_rock_count: 
        lives -= 1
        explosion_sound.play()
        
    # checks collisions between rocks and missiles
    group_group_collide(missile_group, rock_group)
    
    # decides when to reset the game
    if lives <= 0:
        started = False
        
        # kills all the rocks, stops timer
        for i in list(rock_group):
            rock_group.remove(i)
    
        timer.stop()
              
# this function will iterate through a set to update/draw it
def process_sprite_group(process_set, canvas):
    for i in list(process_set):
        i.draw(canvas)
        if i.update():
            process_set.remove(i)
            
        
# timer handler that spawns a rock    
def rock_spawner():
         
    # Spawns a rock with random position/velocity/angular velocity
    a_rock = Sprite([random.random() * WIDTH, random.random() * HEIGHT], 
                    [random.random() * MAX_ROCK_SPEED * score/8 * random.choice([-1,1]), random.random() * MAX_ROCK_SPEED * score/8 * random.choice([-1,1])],
                    0, random.random() * MAX_ROCK_ANGULAR_VELOCITY * random.choice([-1,1]), 
                    asteroid_image, asteroid_info)

    # Adds rock to the rock_group set if less than 12 rocks
    if len(rock_group) < 12 and (dist(a_rock.get_position(), my_ship.get_position())>ROCK_SPAWN_DIST_CHECK):
        rock_group.add(a_rock)
    
# key up & down handlers
def keydown_handler(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_change(-1 * SHIP_TURNING_RADIUS)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.angle_change(SHIP_TURNING_RADIUS)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thruster_control(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def keyup_handler(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_change(SHIP_TURNING_RADIUS)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.angle_change(-1 * SHIP_TURNING_RADIUS)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thruster_control(False)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([]) 
missile_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()
