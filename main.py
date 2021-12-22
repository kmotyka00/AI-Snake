import pygame
from pygame.locals import *
from variables import *
import time
import random

class Apple:
    def __init__(self, surface, apple_image='images/gem2.png'):
        self.parent_screen = surface
        self.image = pygame.image.load(apple_image).convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))

        self.x = random.randint(0, 24-1) * BLOCK_SIZE
        self.y = random.randint(0, 24 - 1) * BLOCK_SIZE

    def draw(self):
        #self.parent_screen.fill(BACKGROUND_COLOR)
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def change_image(self, img_lst=None):
        if img_lst is None:
            img_lst = ['images\gem.png', 'images\gem2.png']
            img_lst = ['images\gem.png', 'images\gem2.png']
        img = random.choice(img_lst)
        self.image = pygame.image.load(img).convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))

    def move(self, change_image=True):
        if change_image is True:
            self.change_image()
        self.x = random.randint(0, 24-1) * BLOCK_SIZE
        self.y = random.randint(0, 24-1) * BLOCK_SIZE

class Snake:
    def __init__(self, surface, window_width, window_height, block_image="images/block.jpg", length=1):
        self.parent_screen = surface
        self.block = pygame.image.load(block_image).convert()
        self.block = pygame.transform.scale(self.block, (window_width // 24, window_height // 24))

        self.length = length
        self.x = [BLOCK_SIZE] * self.length
        self.y = [BLOCK_SIZE] * self.length

        self.direction = 'down'

    def update_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= BLOCK_SIZE
            if self.x[0] < 0:
                self.x[0] = WINDOW_WIDTH - BLOCK_SIZE

        if self.direction == 'right':
            self.x[0] += BLOCK_SIZE
            if self.x[0] >= 600:
                self.x[0] = 0

        if self.direction == 'up':
            self.y[0] -= BLOCK_SIZE
            if self.y[0] < 0:
                self.y[0] = WINDOW_HEIGHT - BLOCK_SIZE

        if self.direction == 'down':
            self.y[0] += BLOCK_SIZE
            if self.y[0] >= 600:
                self.y[0] = 0

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def turn(self, direction):

        if direction == 'left':
            if self.direction != 'right':
                self.direction = 'left'

        if direction == 'right':
            if self.direction != 'left':
                self.direction = 'right'

        if direction == 'up':
            if self.direction != 'down':
                self.direction = 'up'

        if direction == 'down':
            if self.direction != 'up':
                self.direction = 'down'


class Game:
    def __init__(self, window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT, block_image="images/block.jpg"):
        pygame.init()
        pygame.display.set_caption('AI Snake')

        pygame.mixer.init()

        self.surface = pygame.display.set_mode((window_width, window_height))
        self.snake = Snake(self.surface, window_width, window_height, block_image, length=1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

        with open('data/highest_score.txt', 'w+') as f:
            f.write(str(self.snake.length))

    @staticmethod
    def is_collision(x1, y1, x2, y2):
        return x2 <= x1 < x2 + BLOCK_SIZE and y2 <= y1 < y2 + BLOCK_SIZE

    def render_background(self):
        bg = pygame.image.load("images/yellow_background.jpg")
        bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface.blit(bg, (0, 0))

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"sounds/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.apple.draw()
        self.snake.move()
        self.display_score()
        pygame.display.update()

        #print(f'SNAKE ({self.snake.x[0]}, {self.snake.y[0]}), APPLE ({self.apple.x}, {self.apple.y})')

        # snake finds apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.snake.update_length()
            self.apple.move()

        # game over - collision between head and snake's body
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise ValueError("GAME OVER")

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(score, (int(WINDOW_WIDTH*4/5), 10))

    def game_over(self, highest_score):
        self.render_background()
        font = pygame.font.SysFont('arial', 20)
        line1 = font.render(f"GAME OVER. YOUR SCORE: {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(line1, (160, 250))
        line2 = font.render(f"HIGHEST SCORE: {highest_score}", True, (0, 0, 0))
        self.surface.blit(line2, (200, 300))
        line2 = font.render("To play again press Space. To exit press Escape.", True, (0, 0, 0))
        self.surface.blit(line2, (110, 350))
        pygame.display.update()

    def reset(self):
        self.snake = Snake(self.surface, WINDOW_WIDTH, WINDOW_HEIGHT, block_image='images/block.jpg', length=1)
        self.apple = Apple(self.surface)

    def run(self):

        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_SPACE:
                        paused = False

                    if not paused:
                        if event.key == K_UP:
                            self.snake.turn('up')

                        if event.key == K_DOWN:
                            self.snake.turn('down')

                        if event.key == K_LEFT:
                            self.snake.turn('left')

                        if event.key == K_RIGHT:
                            self.snake.turn('right')


                elif event.type == QUIT:
                    running = False

            try:
                if not paused:
                    self.play()

            except ValueError as e:

                with open('data/highest_score.txt', 'r') as f:
                    x = f.read().split()
                    current_highest_score = int(x[0])

                if current_highest_score < self.snake.length:
                    current_highest_score = self.snake.length
                    with open('data/highest_score.txt', 'w') as f:
                        f.truncate(0)
                        f.write(str(current_highest_score))


                self.game_over(current_highest_score)

                paused = True
                self.reset()

            time.sleep(1/FPS)


if __name__ == "__main__":
    game = Game()
    game.run()


#TODO: Time calc.


