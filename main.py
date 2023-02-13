import pygame
from pygame.locals import *
from variables import *
import time
import random

def generate_random_coordinate(frame_length):
    return random.choice(range(0, frame_length, BLOCK_SIZE))

class Apple:
    def __init__(self, surface):
        self.parent_screen = surface
        self.image = pygame.image.load(random.choice(APPLE_IMAGES)).convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))

        self.x = generate_random_coordinate(WINDOW_WIDTH)
        self.y = generate_random_coordinate(WINDOW_HEIGHT)

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def change_image(self):
        img = random.choice(APPLE_IMAGES)
        self.image = pygame.image.load(img).convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))

    def move(self, change_image=True):
        if change_image is True:
            self.change_image()
        self.x = generate_random_coordinate(WINDOW_WIDTH)
        self.y = generate_random_coordinate(WINDOW_HEIGHT)

class Snake:
    def __init__(self, surface, block_image=DEFAULT_SNAKE_BLOCK_PATH, length=INIT_LENGTH):
        self.parent_screen = surface
        self.block = pygame.image.load(block_image).convert()
        self.block = pygame.transform.scale(self.block, (BLOCK_SIZE, BLOCK_SIZE))

        self.length = length
        self.x = [BLOCK_SIZE] * self.length
        self.y = [BLOCK_SIZE] * self.length

        self.direction = Directions.DOWN

    def update_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == Directions.LEFT:
            self.x[0] -= BLOCK_SIZE
            if self.x[0] < 0:
                self.x[0] = WINDOW_WIDTH - BLOCK_SIZE

        if self.direction == Directions.RIGHT:
            self.x[0] += BLOCK_SIZE
            if self.x[0] >= WINDOW_WIDTH:
                self.x[0] = 0

        if self.direction == Directions.UP:
            self.y[0] -= BLOCK_SIZE
            if self.y[0] < 0:
                self.y[0] = WINDOW_HEIGHT - BLOCK_SIZE

        if self.direction == Directions.DOWN:
            self.y[0] += BLOCK_SIZE
            if self.y[0] >= WINDOW_HEIGHT:
                self.y[0] = 0

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def turn(self, direction):

        if direction == Directions.LEFT:
            if self.direction != Directions.RIGHT:
                self.direction = Directions.LEFT

        elif direction == Directions.RIGHT:
            if self.direction != Directions.LEFT:
                self.direction = Directions.RIGHT

        elif direction == Directions.UP:
            if self.direction != Directions.DOWN:
                self.direction = Directions.UP

        elif direction == Directions.DOWN:
            if self.direction != Directions.UP:
                self.direction = Directions.DOWN


class Game:
    def __init__(self, block_image=DEFAULT_SNAKE_BLOCK_PATH):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.snake = Snake(self.surface, block_image, length=1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

        with open(DATA_FILE_PATH, 'w+') as f:
            f.write(str(self.snake.length))

    @staticmethod
    def is_collision(x1, y1, x2, y2):
        return x2 <= x1 < x2 + BLOCK_SIZE and y2 <= y1 < y2 + BLOCK_SIZE

    def render_background(self):
        bg = pygame.image.load(BACKGROUND_IMAGE_PATH)
        bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface.blit(bg, LEFT_CORNER_COORDINATES)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"sounds/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.apple.draw()
        self.snake.move()
        self.display_score()
        pygame.display.update()


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
        self.snake = Snake(self.surface, block_image=DEFAULT_SNAKE_BLOCK_PATH, length=1)
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
                            self.snake.turn(Directions.UP)

                        if event.key == K_DOWN:
                            self.snake.turn(Directions.DOWN)

                        if event.key == K_LEFT:
                            self.snake.turn(Directions.LEFT)

                        if event.key == K_RIGHT:
                            self.snake.turn(Directions.RIGHT)


                elif event.type == QUIT:
                    running = False

            try:
                if not paused:
                    self.play()

            except ValueError as e:

                with open(DATA_FILE_PATH, 'r') as f:
                    x = f.read().split()
                    current_highest_score = int(x[0])

                if current_highest_score < self.snake.length:
                    current_highest_score = self.snake.length
                    with open(DATA_FILE_PATH, 'w') as f:
                        f.truncate(0)
                        f.write(str(current_highest_score))


                self.game_over(current_highest_score)

                paused = True
                self.reset()

            time.sleep(1 / FPS)


if __name__ == "__main__":
    game = Game()
    game.run()


#TODO: Time calc.


