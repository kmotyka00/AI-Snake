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

        self.change_image()
        self.respawn()

    def respawn(self):
        self.x_pos = generate_random_coordinate(WINDOW_WIDTH)
        self.y_pos = generate_random_coordinate(WINDOW_HEIGHT)

    def draw(self):
        self.parent_screen.blit(self.image, (self.x_pos, self.y_pos))
        pygame.display.flip()

    def change_image(self):
        self.image = pygame.image.load(random.choice(APPLE_IMAGES)).convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))

    def move(self, change_image=True):
        if change_image is True:
            self.change_image()
        self.respawn()

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
        self.x.append(EMPTY_POSITION)
        self.y.append(EMPTY_POSITION)

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

class Score:
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.SysFont('arial', 30)
        self.highest_score = 0

    def display(self, snake_length):
        score = self.font.render(f"Score: {snake_length}", True, BLACK)
        self.surface.blit(score, (int(WINDOW_WIDTH*4/5), 10))

    def update_highest_score(self, snake_length):
        if self.highest_score < snake_length:
            self.highest_score = snake_length

        return self.highest_score

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

        self.score = Score(self.surface)
        self.score.display(self.snake.length)

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

    def update_screen(self):
        self.render_background()
        self.apple.draw()
        self.snake.move()
        self.score.display(self.snake.length)
        pygame.display.update()

    def play(self):
        self.update_screen()

        # snake finds apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x_pos, self.apple.y_pos):
            self.play_sound(DING_SOUND_FILENAME)
            self.snake.update_length()
            self.apple.move()

        # game over - collision between head and snake's body
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound(CRASH_SOUND_FILENAME)
                raise ValueError("GAME OVER")

    def game_over(self, highest_score):
        self.render_background()
        font = pygame.font.SysFont('arial', 20)
        line = font.render(f"GAME OVER. YOUR SCORE: {self.snake.length}", True, BLACK)
        self.surface.blit(line, (160, 250))
        line = font.render(f"HIGHEST SCORE: {highest_score}", True, BLACK)
        self.surface.blit(line, (200, 300))
        line = font.render("To play again press Space. To exit press Escape.", True, BLACK)
        self.surface.blit(line, (110, 350))
        pygame.display.update()

    def reset(self):
        self.snake = Snake(self.surface)
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
                        elif event.key == K_DOWN:
                            self.snake.turn(Directions.DOWN)
                        elif event.key == K_LEFT:
                            self.snake.turn(Directions.LEFT)
                        elif event.key == K_RIGHT:
                            self.snake.turn(Directions.RIGHT)

                elif event.type == QUIT:
                    running = False

            try:
                if not paused:
                    self.play()

            except ValueError as e:

                highest_score = self.score.update_highest_score(self.snake.length)
                self.game_over(highest_score)

                paused = True
                self.reset()

            time.sleep(1 / FPS)

    

if __name__ == "__main__":
    game = Game()
    game.run()


#TODO: Time calc.


