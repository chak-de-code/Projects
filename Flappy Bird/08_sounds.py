import pygame, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound
clock = pygame.time.Clock()
fps = 60
# game window
screen_width = 764  
screen_height = 686 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# define font
font = pygame.font.SysFont("Bauhaus 93", 60)
small_font = pygame.font.SysFont("Times New Roman", 45, bold=True)

# define color
white = (255, 255, 255)
green = (0, 128, 0)

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 160
pipe_frequency = 1300  # milliseconds 
last_pipe = pygame.time.get_ticks() - pipe_frequency  
score = 0
pipe_pass = False

# load images
bg = pygame.image.load("bg.png")
ground = pygame.image.load("ground.png")
restart = pygame.image.load("restart.png")
front = pygame.image.load("Front.jpg")
bird_images = [pygame.image.load(f"bird{num}.png") for num in range(1, 4)]

# Load sound
hit_sound = pygame.mixer.Sound("hit.wav") 
point_sound = pygame.mixer.Sound("point.wav")
die_sound = pygame.mixer.Sound("die.wav")
bg_music = pygame.mixer.Sound("mario.mp3")
pygame.mixer.music.set_volume(0.3)  # Set the background music volume to 30%

# print text on screen
def print_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# restart the game
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = screen_height // 2
    return 0  # Reset score = 0

def welcome_screen():
    screen.blit(front, (0, 0))
    print_text("Press any key to start", small_font, green, screen_width // 2 - 120, screen_height // 2 + 50)
    pygame.display.update()

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = bird_images
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False

    def update(self):
        global flying, game_over
        if flying:
            self.velocity += 0.5
            # freeze the velocity after falling
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < 608:
                self.rect.y += int(self.velocity)

        if not game_over:
            # fly when mouse clicked
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.velocity = -10
            # when mouse button is released or not pressed
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
            #  bird position after hitting
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        # up down pipes
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap // 2]
        if position == -1:
            self.rect.topleft = [x, y + pipe_gap // 2]

    def update(self):           # distroy the pipes
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, screen_height // 2)
bird_group.add(flappy)
# restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, restart)
# set flags 
has_played_hit_sound = False
has_played_die_sound = False
game_started = False

while True:
    clock.tick(fps)
    # welcome screen
    if not game_started:
        welcome_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == KEYDOWN:
                pygame.mixer.music.load('mario.mp3')
                pygame.mixer.music.play(-1,0,0)          # Play the background music in a loop
                game_started = True
    else:
        # draw background
        screen.blit(bg, (0, 0))
        # draw bird
        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)
        # ground
        screen.blit(ground, (ground_scroll, 608))

        if len(pipe_group) > 0:
            first_pipe = pipe_group.sprites()[0]
            # bird between pipe
            if flappy.rect.left > first_pipe.rect.left and flappy.rect.left < first_pipe.rect.right and not pipe_pass:
                pipe_pass = True
            # bird cross pipe
            if flappy.rect.left > first_pipe.rect.right and pipe_pass:
                point_sound.play()
                score += 1 
                pipe_pass = False

        print_text(str(score), font, white, screen_width // 2, 20)
        # bird pipe collision
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            if not has_played_hit_sound:  # Only play the sound once
                hit_sound.play()  # Play the sound when a collision occurs
                has_played_hit_sound = True  # Set the flag to True so it doesn't play again
            game_over = True
        # bird hits the ground
        if flappy.rect.bottom > 608 and not has_played_die_sound:
            die_sound.play()
            flying = False
            game_over = True
            has_played_die_sound = True
        # generate pipe
        if not game_over and flying:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, -1)
                top_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            # scroll ground
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            pipe_group.update()
        # game over and reset
        if game_over:
            print_text("GAME OVER", font, white, screen_width // 2 - 150, screen_height // 4)
            button.draw()       # Draw the restart button only when the game is over
            pygame.display.update()
            if button.draw():
                game_over = False
                score = reset_game()
                has_played_hit_sound = False  # Reset the sound flag to allow the hit sound to play again
                has_played_die_sound = False

        pygame.display.update()     # Only update the display once

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                flying = True

    pygame.display.update()