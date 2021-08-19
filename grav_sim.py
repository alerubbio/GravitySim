import pygame
import random
import math
pygame.init()
clock = pygame.time.Clock()

# Window and General Seetings
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Sim :]")
BLACK = 0, 0, 0
WHITE = 255, 255, 255
CENTER = WIDTH/2, HEIGHT/2
EDGE_PADDING = 100

# Planet and Physics Properties
# Currently defaults to Earth and Moon
GRAV_CNST = 7e-7
BIG_MASS = 7.35e22 * 70
SMALL_MASS = 7.35e20
RADIUS_PADDING = 600e6
FPS = 120
TIME_PASSED = .8
SMOOTHING_OPERATOR = .15
GALAXY_SIZE = 50

planet_list = []

BIG_PLANET_WIDTH, BIG_PLANET_HEIGHT = 30, 30
BIG_PLANET = pygame.transform.scale(
            pygame.image.load('Assets\Ice.png'), 
            (BIG_PLANET_WIDTH, BIG_PLANET_HEIGHT))

SMALL_PLANET_WIDTH, SMALL_PLANET_HEIGHT = 12, 12
SMALL_PLANET = pygame.transform.scale(
            pygame.image.load('Assets\Baren.png'), 
            (SMALL_PLANET_WIDTH, SMALL_PLANET_HEIGHT))


def rand_pos():
    return (random.randint(EDGE_PADDING, WIDTH - EDGE_PADDING), 
            random.randint(EDGE_PADDING, HEIGHT - EDGE_PADDING))

def rand_velocity():
    return (float(random.randint(0, 30)/10.)-1.,
               float(random.randint(0, 30)/10.)-1.)

# Controls position, velocity and acceleration of planets
class State:
    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.accel_x = 0
        self.accel_y = 0
        self.has_collided = False

    
# Contstructs planets either by given parameters or random ones
# parameter num = 0 is the Earth preset
class Planet:
    def __init__(self, num):
        x,y = rand_pos()
        vel_x, vel_y = rand_velocity()

        self.state = State(x, y, vel_x, vel_y)
        if num == 0: 
            self.mass = BIG_MASS
            self.state.pos_x = WIDTH/2
            self.state.pos_y = HEIGHT/2
            self.state.vel_x = 0
            self.state.vel_y = 0
            self.radius = BIG_PLANET_WIDTH/2

        if num == 1: 
            self.mass = SMALL_MASS
            self.radius = SMALL_PLANET_WIDTH/2
        


# Update vector properties of planets
def updateAcceleration():
    list_length = len(planet_list)

    for i in range(0, list_length):
        accel_x = 0
        accel_y = 0
        for j in range(0, list_length):
            if(planet_list[i] != planet_list[j] and planet_list[i].mass != BIG_MASS):
                distx = (planet_list[j].state.pos_x - planet_list[i].state.pos_x) * RADIUS_PADDING
                disty = (planet_list[j].state.pos_y - planet_list[i].state.pos_y) * RADIUS_PADDING

                dist_sq = distx**2 + disty**2
                
                # normalize the direction of this force and apply softening as a smoothing operation
                force = ( (GRAV_CNST * planet_list[j].mass) / 
                        (dist_sq * math.sqrt(dist_sq + SMOOTHING_OPERATOR)) )

                accel_x += force * distx
                accel_y += force * disty

        planet_list[i].state.accel_x = accel_x
        planet_list[i].state.accel_y = accel_y

        updateVelocity()

def updateVelocity():
    for planet in planet_list:
        planet.state.vel_x += planet.state.accel_x * TIME_PASSED
        planet.state.vel_y += planet.state.accel_y * TIME_PASSED
    
def updatePosition():
    for planet in planet_list:
        planet.state.pos_x += planet.state.vel_x * TIME_PASSED
        planet.state.pos_y += planet.state.vel_y * TIME_PASSED

# adds a planet to our solar system (planet_list)
def populate_galaxy(planet):
    planet_list.append(planet)
    return planet

def planets_collide(planet1, planet2):
    distx = planet1.state.pos_x - planet2.state.pos_x
    disty = planet1.state.pos_y - planet2.state.pos_y

    dist_sq = distx**2 + disty**2

    return math.sqrt(dist_sq)  <= (planet1.radius + planet2.radius) * .9

def combine_collisions():
    for planet1 in planet_list:
        if planet1.state.has_collided:
            continue
        for planet2 in planet_list:
            if planet1 is planet2 or planet2.state.has_collided:
                continue
            if planets_collide(planet1, planet2):
                if planet1.mass < planet2.mass:
                    planet1, planet2 = planet2, planet1
                    
                planet2.state.has_collided = True
                if planet1.mass == BIG_MASS:
                    continue
                vel_x = ((planet1.state.vel_x * planet1.mass + planet2.state.vel_x * planet2.mass)
                        /planet1.mass + planet2.mass)
                vel_y = ((planet1.state.vel_y * planet1.mass + planet2.state.vel_y * planet2.mass)
                        /planet1.mass + planet2.mass)

                planet1.mass += planet2.mass
        
def update_window(big_flag, big):
    WIN.fill(BLACK)
    if big_flag == True:
      WIN.blit(BIG_PLANET, (big.state.pos_x, big.state.pos_y))

    for planet in planet_list:
        if planet is big or planet.state.has_collided:
            continue
        WIN.blit(SMALL_PLANET, (planet.state.pos_x, planet.state.pos_y))


def create_big_mass(big_flag):
    if big_flag is True:
        big = Planet(0)
        populate_galaxy(big)

def main():
    run = True

    # create a large center mass
    big_flag = True
    create_big_mass(big_flag)

    # populates system with lots of small bodies
    for i in range(0, GALAXY_SIZE):
        small = Planet(1)
        populate_galaxy(small)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False


        update_window(big_flag, planet_list[0])
        updateAcceleration()
        updatePosition()
        combine_collisions()
        
        pygame.display.update()

if __name__ == "__main__":
    main()