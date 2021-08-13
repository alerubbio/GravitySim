import pygame
import random

WIDTH, HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity")

FPS = 60

BLACK = 0, 0, 0
WHITE = 255, 255, 255

CENTER = WIDTH/2, HEIGHT/2
EDGE_PADDING = 30

GRAV_CNST = 1.e4

# fixed to density later
BIG_MASS = 100

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
    return (randint(0, 5), randint(0, 5))

class Planet:
    def __init__(self, pos, velocity, mass):
        self.pos = pos
        self.velocity = velocity
        self.mass = mass

def update_window(big, small):
    WIN.fill(BLACK)
    WIN.blit(BIG_PLANET, (big.pos.x, big.pos.y))
    WIN.blit(SMALL_PLANET, (small.pos.x, small.pos.y))

def main():
    clock = pygame.time.Clock()
    run = True
    #pygame.init()


    big = Planet(gen_big_planet(), gen_velocity, BIG_MASS)
    small = gen_small_planet()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False

        
        update_window(big, small)
        
        pygame.display.update()
    pygame.QUIT()


if __name__ == "__main__":
    main()