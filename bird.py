import pygame
from sys import exit
import random

print("branch with changes")

GAME_HEIGHT = 640
GAME_WIDTH = 360

#bird class
bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
#bird pixels: 408 x 288
bird_width = 34 #should maintain ratio, 17 to 12
bird_height = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img
        self.passed = False

#pipe class
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512 #part of pipe will be cut off

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False

#game images
background_image = pygame.image.load("flappybirdbg.png")
bird_image = pygame.image.load("flappybird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
top_pipe_image = pygame.image.load("toppipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bottom_pipe_image = pygame.image.load("bottompipe.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width, pipe_height))

#game logic
bird = Bird(bird_image)
pipes = []
velocity_x = -2 #move pipes to the left speed (simulates bird moving right)
velocity_y = 0 #move bird up and down speed
gravity = 0.4
score = 0
game_over = False

def draw():
    window.blit(background_image, (0, 0))
    window.blit(bird.img, bird)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    text_str = str(int(score))

    if game_over:
        text_str = "Game over " + text_str

    text_font = pygame.font.SysFont("Arial", 45)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render, (5, 0))
 
def move():
    global velocity_y, score, game_over, pipes
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y > GAME_HEIGHT:
        game_over = True
        return

    for pipe in pipes:
        pipe.x += velocity_x

        if not bird.passed and bird.x > pipe.x + pipe_width:
            score += 1
            bird.passed = True
            print(score)

        if bird.colliderect(pipe):
            game_over = True
            return


    while len(pipes) > 0 and pipes[0].x + pipe_width < 0:
        pipes.pop(0) #removes first element of the list
        bird.passed = False


def create_pipes():
    random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2) #0-h/2
    opening_space = GAME_HEIGHT/4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + pipe_height + opening_space
    pipes.append(bottom_pipe)

    #print(len(pipes))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("birdy flap")
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT + 0 #+0 is to signify that it's the first event
pygame.time.set_timer(create_pipes_timer, 1500) #marks every 1.5 seconds, calles create_pipes_timer every 1.5 s

running = True
while running: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == create_pipes_timer and not game_over:
            create_pipes()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                velocity_y = -8

                #reset game
                if game_over:
                    bird.y = bird_y
                    pipes.clear()
                    score = 0
                    game_over = False

    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60) #60 fps

pygame.KEYDOWN()
pygame.quit()
exit()