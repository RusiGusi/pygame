import pygame
from pygame.locals import *
import time
import random


SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple1.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 23)*SIZE
        self.y = random.randint(1, 18)*SIZE



class Block:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("block1.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        for i in range(24):
            self.parent_screen.blit(self.image, (0, i*SIZE))
            self.parent_screen.blit(self.image, (24*SIZE, i * SIZE))
        for i in range(24):
            self.parent_screen.blit(self.image, (i*SIZE, 0))
            self.parent_screen.blit(self.image, (i*SIZE, 19 * SIZE))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(2, 23)*SIZE
        self.y = random.randint(2, 18)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("block.png").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [520]
        self.y = [360]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")
        self.game_started = 0
        pygame.mixer.init()
        self.check = False
        self.vol = 1
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))


    def play_background_music(self):
        pygame.mixer.music.load('bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)
        pygame.mixer.music.set_volume(self.vol)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        pause = False
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.block = Block(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("background.png")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.lose = False
        self.render_background()
        self.apple.draw()
        self.snake.walk()
        self.block.draw()
        self.display_score()
        pygame.display.flip()

        # ест яблоко
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # врезается в стенку
        if self.snake.x[0] == 0 or self.snake.y[0] == 0 or self.snake.x[0] == 960 or self.snake.y[0] == 760:
            self.play_sound('crash')
            self.lose = True
            raise "Collision Occurred"
        # врезается в себя
        for i in range(1, self.snake.length):
            if self.snake.length != 100:
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                    self.play_sound('crash')
                    self.lose = True
                    raise "Collision Occurred"

    def menu(self):
        self.start = True
        self.game_started += 1
        self.render_background()
        font = pygame.font.SysFont('8-BIT WONDER.TTF', 40)
        self.render_background()
        line = font.render("MAIN MENU", True, (255, 255, 255))
        self.surface.blit(line, (400, 200))
        line = font.render(f"Your best score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line, (320, 250))
        line = font.render(f"If you want to start - press Q",
                           True, (255, 255, 255))
        self.surface.blit(line, (280, 300))
        line = font.render(f"If you want to quit - press ESCAPE",
                           True, (255, 255, 255))
        self.surface.blit(line, (230, 350))
        line = font.render(f"If you want to high volume - press P, If you want to low volume - press O",
                           True, (255, 255, 255))
        self.surface.blit(line, (20, 400))
        line = font.render(f"HOW TO PLAY?",
                           True, (255, 255, 255))
        self.surface.blit(line, (380, 500))
        line = font.render(f"Moving by ARROWS, R - pause, ESCAPE - quiting",
                           True, (255, 255, 255))
        self.surface.blit(line, (150, 550))
        pygame.display.flip()
        while self.start:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        self.reset()
                        self.start = False
                        self.game_started = True
                    if event.key == K_ESCAPE:
                        pygame.quit()
                    if event.key == K_p:
                        self.vol += 0.05
                        pygame.mixer.music.set_volume(self.vol)
                        self.play_sound("ding")
                        print("Volume =", self.vol)
                    if event.key == K_o:
                        self.vol -= 0.05
                        pygame.mixer.music.set_volume(self.vol)
                        self.play_sound("ding")
                        print("Volume =", self.vol)
                elif event.type == QUIT:
                    pygame.quit()


    def display_score(self):
        font = pygame.font.SysFont('8-BIT WONDER.TTF', 40)
        f = open('save.txt', 'r')
        for line in f:
            self.a = int(line)
        f.close()
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        if self.snake.length > self.a:
            self.a = self.snake.length
            ff = open('save.txt', 'w')
            ff.write(str(self.a))
            ff.close()
        maxi = font.render(f"Max: {self.a}", True, (200, 200, 200))
        self.surface.blit(score, (820, 40))
        self.surface.blit(maxi, (820, 80))

    def win(self):
        self.win1 = True
        self.game_started = 0
        self.render_background()
        font = pygame.font.SysFont('8-BIT WONDER.TTF', 100)
        self.render_background()
        line = font.render("YOU WIN!!!!", True, (255, 255, 255))
        self.surface.blit(line, (350, 200))
        line = font.render(f"Q - restart, ESCAPE - quiting",
                           True, (255, 255, 255))
        self.surface.blit(line, (20, 550))
        pygame.display.flip()
        self.a = self.snake.length
        ff = open('save.txt', 'w')
        ff.write('1')
        ff.close()
        while self.win1:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        self.win1 = False
                        self.snake.length = 1
                        self.play()
                    if event.key == K_ESCAPE:
                        pygame.quit()
                elif event.type == QUIT:
                    pygame.quit()

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('8-BIT WONDER.TTF', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()


    def run(self):
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.block = Block(self.surface)
        self.block.draw()
        pause = False
        pause1 = False
        running = True
        while running:
            if self.snake.length == 100:
                pygame.mixer.music.play()
                pause = False
                pause1 = False
                self.win()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                        pause1 = False

                    if not pause and not pause1:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_r:
                            if not pause and not pause1:
                                pause1 = True
                                pygame.mixer.music.pause()
                            elif not pause and pause1:
                                pause1 = False
                                pygame.mixer.music.unpause()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause and not pause1:
                    if self.game_started > 0:
                        self.play()
                    elif self.game_started == 0:
                        self.menu()
                elif not pause and pause1:
                    pause = True
                    font = pygame.font.SysFont('8-BIT WONDER.TTF', 30)
                    self.render_background()
                    line = font.render("Game is paused", True, (255, 255, 255))
                    self.surface.blit(line, (100, 200))
                    line = font.render(f"Your current score is {self.snake.length}", True, (255, 255, 255))
                    self.surface.blit(line, (100, 250))
                    line = font.render(f"If you want to continue - press R, if you want to quit - press ESCAPE",
                                        True, (255, 255, 255))
                    self.surface.blit(line, (100, 300))
                    line = font.render(f"If you want to high volume - press P, If you want to low volume - press O",
                                       True, (255, 255, 255))
                    self.surface.blit(line, (100, 350))
                    line = font.render(f"If you want to go to the menu - press Q",
                                       True, (255, 255, 255))
                    self.surface.blit(line, (100, 400))

                    pygame.display.flip()
                    while pause:
                        for event in pygame.event.get():
                            if event.type == KEYDOWN:
                                if event.key == K_r:
                                    pause = False
                                    pause1 = False
                                    pygame.mixer.music.set_volume(self.vol)
                                    pygame.mixer.music.unpause()

                                if event.key == K_ESCAPE:
                                    return 0
                                if event.key == K_p:
                                    self.vol += 0.05
                                    pygame.mixer.music.set_volume(self.vol)
                                    self.play_sound("ding")
                                    print("Volume =", self.vol)
                                if event.key == K_o:
                                    self.vol -= 0.05
                                    pygame.mixer.music.set_volume(self.vol)
                                    self.play_sound("ding")
                                    print("Volume =", self.vol)
                                if event.key == K_q:
                                    pygame.mixer.music.play()
                                    pause = False
                                    pause1 = False
                                    self.menu()
                            elif event.type == QUIT:
                                running = False
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.20)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    clock.tick(30)
    game = Game()
    game.run()
