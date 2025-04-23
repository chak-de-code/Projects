import pygame, sys, random
import os           # for highscore text file

pygame.init()
pygame.mixer.init()                  # Initialize the Pygame mixer module for sound/music

# define colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
green = (0,255,0)
blue = (0,0,200)

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# background image
bgimg = pygame.image.load('back.png')
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

# welcome image
frontimg = pygame.image.load('front.png')
frontimg = pygame.transform.scale(frontimg,(screen_width,screen_height)).convert_alpha()

''' Function to check if the snake goes out of screen'''
def check_out_of_screen(snake_head, screen_width, screen_height):
    x, y = snake_head
    if x < 0 or x >= screen_width or y < 0 or y >= screen_height:
        return True
    return False

font = pygame.font.Font(None,50)                  # arial / serif / script
# Function to print text on screen
def display_text(text,color,position):
    screen_text = font.render(text,True,color)
    screen.blit(screen_text,position)   

def welcome():
    while True:
        screen.fill(black)
        screen.blit(frontimg,(0,0))

        display_text("Press  Enter To Play ",blue,(130,480))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()

        pygame.display.flip()
        clock.tick(10)

def gameloop():

    snake_x = 200
    snake_y = 200
    score = 0
    snake = [(snake_x, snake_y)]
    direction = (20, 0)
    food = (random.randrange(100, 600, 20), random.randrange(100, 600, 20))

    # load background music
    pygame.mixer.music.load("Gangsta-Paradise.mp3")
    pygame.mixer.music.play(-1,0.0)                     # Play the music looped (-1 means loop indefinitely)

    # load eat sound
    crunch = pygame.mixer.Sound('crunch.wav')  

    ''' check whether highscore file exist or not'''
    if (not os.path.exists("highscore.txt")) :
        with open("highscore.txt","w") as f:
            f.write("0")

    with open("highscore.txt","r") as f:
        highscore = f.read()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0,20): direction = (0, -20)       # Prevent moving down if moving up
                if event.key == pygame.K_DOWN and direction!=(0, -20): direction = (0, 20)      # Prevent moving up if moving down
                if event.key == pygame.K_LEFT and direction!=(20,0) : direction = (-20, 0)      # Prevent moving right if moving left
                if event.key == pygame.K_RIGHT and direction !=(-20,0): direction = (20, 0)     # Prevent moving left if moving right
        
        # Move the snake       
        snake = [(snake[0][0] + direction[0], snake[0][1] + direction[1])] + snake[:-1]

        '''Check if snake has gone out of bounds'''
        if check_out_of_screen(snake[0], screen_width, screen_height):
            display_text("Game Over!",red, (220, 250))
            display_text(f"Score : {score} Highscore : {highscore}",white,(100,300))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds to show the message before exiting
            sys.exit()

        ''' Check if snake eats itself'''
        if snake[0] in snake[1:]:
            display_text("Game Over !",red,(220,250))
            display_text(f"Score : {score} Highscore : {highscore}",blue,(100,300))
            pygame.display.flip()
            pygame.time.wait(2000)
            sys.exit()

        '''Check if snake eats the food'''
        if snake[0] == food:
            # food eating sound
            crunch.play()
            score += 10
            # New food position
            food = (random.randrange(100, 600, 20), random.randrange(100, 600, 20))
            while food in snake:
                food = (random.randrange(100, 600, 20), random.randrange(100, 600, 20))

            snake.append(snake[-1])          # Grow the snake
            if score > int(highscore):
                highscore = score
                with open("highscore.txt", "w") as f:
                    f.write(str(score))

            
        screen.fill(black)
        screen.blit(bgimg,(0,0))
        
        # display score on screen
        display_text(f"Score : {score} ",green,(5,5))

        '''(*segment, 20, 20): This is the rectangle position and size. segment is a tuple like(x, y),which specifies top-left corner of rectangle.
        20, 20: These are the width and height of the rectangle(both 20 pixel). Each segment of snake is a square with dimensions of 20x20 pixels.'''
        for segment in snake: pygame.draw.rect(screen, green, (*segment, 20, 20))     
        pygame.draw.rect(screen, red, (*food, 20, 20))       # Draw food in red
        pygame.display.flip()
        clock.tick(10)               # Control the speed of the gam

welcome()