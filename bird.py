import os
import random
import pygame
from sys import exit

print("branch with changes")

# Game constants
GAME_HEIGHT = 640
GAME_WIDTH = 360

# bird dimensions (original source image ~408x288 -> scaled)
bird_x = GAME_WIDTH / 8
bird_y = GAME_HEIGHT / 2
bird_width = 34
bird_height = 24

# pipe dimensions
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512


class Bird(pygame.Rect):
    def __init__(self, img):
        super().__init__(bird_x, bird_y, bird_width, bird_height)
        self.img = img


class Pipe(pygame.Rect):
    def __init__(self, img, is_top=False):
        super().__init__(pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False
        self.is_top = is_top


class Game:
    """Encapsulate game state and behavior. Resources are loaded in __init__
    so importing the module doesn't attempt to load images or initialize
    the display unexpectedly.
    """

    def __init__(self):
        pygame.init()

        # load resources (paths relative to project root)
        resource = os.path.join("resource")
        self.background_image = pygame.image.load(os.path.join(resource, "flappybirdbg.png"))
        bird_img = pygame.image.load(os.path.join(resource, "flappybird.png"))
        self.bird_image = pygame.transform.scale(bird_img, (bird_width, bird_height))
        top_img = pygame.image.load(os.path.join(resource, "toppipe.png"))
        self.top_pipe_image = pygame.transform.scale(top_img, (pipe_width, pipe_height))
        bottom_img = pygame.image.load(os.path.join(resource, "bottompipe.png"))
        self.bottom_pipe_image = pygame.transform.scale(bottom_img, (pipe_width, pipe_height))

        # runtime state
        self.window = None
        self.clock = pygame.time.Clock()
        self.bird = Bird(self.bird_image)
        self.pipes = []
        self.velocity_x = -2
        self.velocity_y = 0
        self.gravity = 0.4
        self.score = 0
        self.game_over = False
        self.text_font = pygame.font.SysFont("Arial", 45)

    def draw(self):
        self.window.blit(self.background_image, (0, 0))
        self.window.blit(self.bird.img, self.bird)

        for pipe in self.pipes:
            self.window.blit(pipe.img, pipe)

        text_str = str(int(self.score))
        if self.game_over:
            text_str = "Game over " + text_str
        text_render = self.text_font.render(text_str, True, "white")
        self.window.blit(text_render, (5, 0))

    def move(self):
        self.velocity_y += self.gravity
        self.bird.y += self.velocity_y
        self.bird.y = max(self.bird.y, 0)

        if self.bird.bottom > GAME_HEIGHT:
            self.game_over = True
            return

        for pipe in self.pipes:
            pipe.x += self.velocity_x

            if pipe.is_top and not pipe.passed and self.bird.x > pipe.x + pipe_width:
                self.score += 1
                pipe.passed = True
                print(self.score)

            if self.bird.colliderect(pipe):
                self.game_over = True
                return

        while len(self.pipes) > 0 and self.pipes[0].x + pipe_width < 0:
            self.pipes.pop(0)

    def create_pipes(self):
        random_pipe_y = pipe_y - pipe_height / 4 - random.random() * (pipe_height / 2)
        opening_space = GAME_HEIGHT / 4

        top_pipe = Pipe(self.top_pipe_image, is_top=True)
        top_pipe.y = random_pipe_y
        self.pipes.append(top_pipe)

        bottom_pipe = Pipe(self.bottom_pipe_image)
        bottom_pipe.y = top_pipe.y + pipe_height + opening_space
        self.pipes.append(bottom_pipe)

    def reset_game(self):
        self.bird.y = bird_y
        self.pipes.clear()
        self.score = 0
        self.velocity_y = 0
        self.game_over = False

    def run(self):
        # create display here so importing module doesn't open a window
        self.window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption("birdy flap")

        create_pipes_timer = pygame.USEREVENT + 0
        pygame.time.set_timer(create_pipes_timer, 1500)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == create_pipes_timer and not self.game_over:
                    self.create_pipes()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.velocity_y = -8
                        if self.game_over:
                            self.reset_game()

            if not self.game_over:
                self.move()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        exit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()