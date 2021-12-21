import pygame
from pygame.locals import *
from variables import *
import time



class Apple:
    def __init__(self, surface, apple_image='images/apple.jpg'):
        self.parent_screen = surface
        self.image = pygame.image.load(apple_image).convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))

        self.x = BLOCK_SIZE * 4
        self.y = BLOCK_SIZE * 4

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Snake:
    def __init__(self, surface, window_width, window_height, block_image="images/block.jpg", length=1):
        self.parent_screen = surface
        self.block = pygame.image.load(block_image).convert()
        self.block = pygame.transform.scale(self.block, (window_width // 24, window_height // 24))

        self.length = length
        self.x = [BLOCK_SIZE] * self.length
        self.y = [BLOCK_SIZE] * self.length

        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= BLOCK_SIZE

        if self.direction == 'right':
            self.x[0] += BLOCK_SIZE

        if self.direction == 'up':
            self.y[0] -= BLOCK_SIZE

        if self.direction == 'down':
            self.y[0] += BLOCK_SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill((200, 200, 130))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

        pygame.display.flip()

    def move(self, direction):

        if direction == 'left':
            self.direction = 'left'

        if direction == 'right':
            self.direction = 'right'

        if direction == 'up':
            self.direction = 'up'

        if direction == 'down':
            self.direction = 'down'


class Game:
    def __init__(self, window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT, block_image="images/block.jpg"):
        pygame.init()

        self.surface = pygame.display.set_mode((window_width, window_height))
        self.snake = Snake(self.surface, window_width, window_height, block_image, length=2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play(self):
        self.snake.walk()
        self.apple.draw()

    def run(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_UP:
                        self.snake.move('up')

                    if event.key == K_DOWN:
                        self.snake.move('down')

                    if event.key == K_LEFT:
                        self.snake.move('left')

                    if event.key == K_RIGHT:
                        self.snake.move('right')

                elif event.type == QUIT:
                    running = False

            self.play()
            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()


