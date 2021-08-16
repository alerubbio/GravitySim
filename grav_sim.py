import pygame
import random

# Window and General Seetings
WIDTH, HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Sim :]")
BLACK = 0, 0, 0
WHITE = 255, 255, 255
CENTER = WIDTH/2, HEIGHT/2
EDGE_PADDING = 100

# Planet and Physics Properties
GRAV_CNST = 1.e4
BIG_MASS = 100
SMALL_MASS = 50
FPS = 60

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

def gen_velocity():
    return (random.randint(0, 5), random.randint(0, 5))


# planet collection 
class Planet:
    def __init__(self, pos, velocity, mass):
        self.pos = pos
        self.velocity = velocity
        self.mass = mass

def updateAcceleration():
    list_length = len(planet_list)

    for i in range(0, list_length):
        accelx = 0
        accely = 0
        for j in range(0, list_length):
            if(planet_list[i] != planet_list[j]):
                distx = planet_list[j].pos.x - planet_list[i].pos.x
                disty = planet_list[j].pos.y - planet_list[i].pos.y

                dist_sq = distx**2 + disty**2
                
                force = GRAV_CNST * planet_list[j].mass / (dist_sq)
                
def update_window(big, small):
    WIN.fill(BLACK)
    WIN.blit(BIG_PLANET, (big.pos.x, big.pos.y))
    WIN.blit(SMALL_PLANET, (small.pos.x, small.pos.y))

def main():
    clock = pygame.time.Clock()
    run = True
    #pygame.init()


    big = Planet(gen_big_planet(), gen_velocity(), BIG_MASS)
    small = Planet(gen_small_planet(), gen_velocity(), SMALL_MASS)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False

        
        velocity = big.velocity
        big.pos.x += velocity[0]
        big.pos.y += velocity[1]


        update_window(big, small)
        pygame.display.update()


if __name__ == "__main__":
    main()