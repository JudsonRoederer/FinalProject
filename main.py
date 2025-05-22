# Final Project - Snake Game
# Judson Roederer
# Monday April 28 - Thursday May 22


# I used this website to help me with some of the coding - https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/
# I used some of Solomon's, Ryan's, and Gabriels help.
# Here is the link to my flint sessions: https://app.flintk12.com/activities/pygame-debug-le-1fe068/sessions/a22d7dbd-6ca6-4f4e-9f2b-88bc7eb10346, and https://app.flintk12.com/activities/pygame-debug-le-1fe068/sessions/299fc6bc-e429-470c-9eb6-cbb34422e637

#Imports
import pygame
import sys
import random


#Intialization of clock and screen dimensions, defining colors, font and mixer initalize, and lodaing sounds
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.font.init()
pygame.mixer.init()
apple_eating_sound = pygame.mixer.Sound("sounds/blip3.wav")
game_over_sound = pygame.mixer.Sound("sounds/splat.wav")


# The apple class is the class that repersents the food that the snake eats
class Apple(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/en-apple-red-leaf.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# This class is for a single segment of the snake.
class Segment(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# Main part of the snake that the additinal segments follow it has the movement, collision detection, the growing part,
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speed = 15
        self.score = 0
        self.change_x = self.speed
        self.change_y = 0
        self.segments = []
        self.positions = [(x, y)]
        self.grace_period = 0
    # This handels the directions, and this updates the position of the snake's head and the other segments, lastly it checks for the collision of the snake into itslef or into the wall
    def update(self, keys):

        if keys[pygame.K_LEFT] and self.change_x == 0:
            self.change_x = -self.speed
            self.change_y = 0
        elif keys[pygame.K_RIGHT] and self.change_x == 0:
            self.change_x = self.speed
            self.change_y = 0
        elif keys[pygame.K_UP] and self.change_y == 0:
            self.change_y = -self.speed
            self.change_x = 0
        elif keys[pygame.K_DOWN] and self.change_y == 0:
            self.change_y = self.speed
            self.change_x = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y


        self.positions.insert(0, (self.rect.x, self.rect.y))


        for i, segment in enumerate(self.segments):
            segment.rect.x = self.positions[i + 1][0]
            segment.rect.y = self.positions[i + 1][1]


        if len(self.positions) > len(self.segments) + 1:
            self.positions.pop()


        if self.grace_period > 0:
            self.grace_period -= 1

        if (self.rect.left < 0 or
                self.rect.right > SCREEN_WIDTH or
                self.rect.top < 0 or
                self.rect.bottom > SCREEN_HEIGHT):
            game_over_sound.play()
            return False
        return True
    # This adds a new segment to the body after the snake eats a apple
    def grow(self, all_sprites_group):

        if len(self.segments) > 0:
            last_segment = self.segments[-1]
            pos_x = last_segment.rect.x
            pos_y = last_segment.rect.y
        else:
            pos_x, pos_y = self.positions[-1]


        new_segment = Segment(pos_x, pos_y)


        self.segments.append(new_segment)

        all_sprites_group.add(new_segment)

        self.grace_period = 10

        return new_segment


def main():
    # This is the main function that sets up the game's window, initializes the sprites that are in the other class, and it runs the main game loop.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    all_sprites = pygame.sprite.Group()
    apple_group = pygame.sprite.Group()

    snake = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    all_sprites.add(snake)
    # Function to spawn the apple in a place that isn't on top of the snake.
    def spawn_apple():
        while True:
            x = random.randrange(0, SCREEN_WIDTH - 30)
            y = random.randrange(0, SCREEN_HEIGHT - 30)
            apple = Apple(x, y)
            if not any(snake.rect.colliderect(apple.rect) for segment in snake.segments):
                all_sprites.add(apple)
                apple_group.add(apple)
                break

    spawn_apple()

    font = pygame.font.Font(None, 36)
    # Main game loop that runs the rest of the code
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Updates the snakes poisiton and checks to see if it ran into the wall
        if not snake.update(keys):
            running = False
            game_over_sound.play()
        # Chekcs to see if the snake hit the apple and if it did adds to the score
        collected_apples = pygame.sprite.spritecollide(snake, apple_group, True)
        for apple in collected_apples:
            snake.score += 1
            print(f"Score: {snake.score}")
            apple_eating_sound.play()
            spawn_apple()
            snake.grow(all_sprites)
        # Checks if the snake hit itself and if it did then the game ends
        for segment in snake.segments:
            if len(snake.segments) > 1 and snake.grace_period == 0:
                if snake.rect.colliderect(segment.rect):
                    running = False
                    game_over_sound.play()
        # clears the screen and draws the screen
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Shows the score in the top
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(25)

    # Shows the game over
    screen.fill(BLACK)
    game_over_font = pygame.font.Font(None, 74)
    game_over_text = game_over_font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2,
                                 SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(500)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
