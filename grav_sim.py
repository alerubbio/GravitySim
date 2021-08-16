import pygame
import random
import math
# Window and General Seetings
WIDTH, HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Sim :]")
BLACK = 0, 0, 0
WHITE = 255, 255, 255
CENTER = WIDTH/2, HEIGHT/2
EDGE_PADDING = 100

# Planet and Physics Properties
GRAV_CNST = 6.67408
BIG_MASS = 33300
SMALL_MASS = 1
FPS = 60
TIME_PASSED = 0.2
SMOOTHING_OPERATOR = .50

planet_list = []

BIG_PLANET_WIDTH, BIG_PLANET_HEIGHT = 40, 40
BIG_PLANET = pygame.transform.scale(
            pygame.image.load('Assets\Ice.png'), 
            (BIG_PLANET_WIDTH, BIG_PLANET_HEIGHT))

SMALL_PLANET_WIDTH, SMALL_PLANET_HEIGHT = 20, 20
SMALL_PLANET = pygame.transform.scale(
            pygame.image.load('Assets\Baren.png'), 
            (SMALL_PLANET_WIDTH, SMALL_PLANET_HEIGHT))


def rand_pos():
    return (random.randint(EDGE_PADDING, WIDTH - EDGE_PADDING), 
            random.randint(EDGE_PADDING, HEIGHT - EDGE_PADDING))

def gen_big_planet():
    return pygame.draw.circle(WIN, WHITE, rand_pos(), BIG_PLANET_WIDTH/2)

def gen_small_planet():
    return pygame.draw.circle(WIN, WHITE, rand_pos(), SMALL_PLANET_WIDTH/2)

def rand_velocity():
    return (float(random.randint(0, 300)/100.)-1.5,
               float(random.randint(0, 300)/100.)-1.5)

# Controls position, velocity and acceleration of planets
class State:
    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.accel_x = 0
        self.accel_y = 0

# Contstructs planets either by given parameters or random ones
class Planet:
    def __init__(self, num):
        x,y = rand_pos()
        vel_x, vel_y = rand_velocity()

        self.state = State(x, y, vel_x, vel_y)

        if num == 0: 
            self.mass = BIG_MASS
            self.state.pos_x = 540
            self.state.pos_y = 360
            self.state.vel_x = 0
            self.state.vel_y = 0

        if num == 1: self.mass = SMALL_MASS


# Update vector properties of planets
def updateAcceleration():
    list_length = len(planet_list)

    for i in range(0, list_length):
        accel_x = 0
        accel_y = 0
        for j in range(0, list_length):
            if(planet_list[i] != planet_list[j] and planet_list[i].mass == BIG_MASS):
                distx = planet_list[j].state.pos_x - planet_list[i].state.pos_x
                disty = planet_list[j].state.pos_y - planet_list[i].state.pos_y

                dist_sq = distx**2 + disty**2
                
                # normalize the direction of this force and apply softening as a smoothing operation
                force = ( (GRAV_CNST * planet_list[j].mass) / 
                        (dist_sq * math.sqrt(dist_sq + SMOOTHING_OPERATOR)) )

                accel_x += force * distx
                accel_y += force * disty

        planet_list[i].state.accel_x = accel_x
        planet_list[i].state.accel_y = accel_y

def updateVelocity():
    for planet in planet_list:
        planet.state.vel_x += planet.state.accel_x * TIME_PASSED
        planet.state.vel_y += planet.state.accel_y * TIME_PASSED
    
def updatePosition():
    for planet in planet_list:
        planet.state.pos_x += planet.state.vel_x * TIME_PASSED
        planet.state.pos_y += planet.state.vel_y * TIME_PASSED

# adds a planet to our solar system (planet_list)
def populate_system(planet):
    planet_list.append(planet)

def update_window(big, small):
    WIN.fill(BLACK)
    WIN.blit(BIG_PLANET, (big.state.pos_x, big.state.pos_y))
    WIN.blit(SMALL_PLANET, (small.state.pos_x, small.state.pos_y))

def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True


    big = Planet(0)
    small = Planet(1)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False

        populate_system(big)
        populate_system(small)
        
        updateAcceleration()
        updateVelocity()
        updatePosition()

        update_window(big, small)
        pygame.display.update()




if __name__ == "__main__":
    main()