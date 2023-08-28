# Simple pygame program

# Import and initialize the pygame library
import pygame
from random import randint

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_x,
)

class snake_node:
    def __init__(self, x = 0, y = 0):
        self.coords = [x, y]
        self.last_coords = [0, 0]
        self.rectangle = pygame.rect.Rect(self.coords[0], self.coords[1], 10, 10)
        self.direction = "up"
        self.color = (255, 255, 255)

class snake_food:
    def __init__(self):
        self.coords = [2, 2]
        self.color = (0, 255, 0)
        self.rectangle = pygame.rect.Rect(20, 20, 10, 10)

class snake:
    def __init__(self, grid):
        self.head = snake_node(randint(0, len(grid[0]) - 1), randint(0, len(grid) - 1))
        self.head.color = (255, 0, 0)
        self.tail = []
        self.tail_len = 0
        self.food = snake_food()
    
    def move(self):
        if self.head.coords[0] == self.food.coords[0] and self.head.coords[1] == self.food.coords[1]:
            self.tail_len += 1
            self.tail.append(snake_node())
            self.food.coords = (randint(0, len(grid[0]) - 1), randint(0, len(grid) - 1))
            self.food.rectangle.left = self.food.coords[0] * 10
            self.food.rectangle.top = self.food.coords[1] * 10
            print(self.food.coords)
        if len(self.tail) != 0:
            self.tail[0].last_coords[0] = self.tail[0].coords[0]
            self.tail[0].last_coords[1] = self.tail[0].coords[1]
            self.tail[0].coords[0] = self.head.coords[0]
            self.tail[0].coords[1] = self.head.coords[1]
            self.tail[0].rectangle.left = self.tail[0].coords[0] * 10
            self.tail[0].rectangle.top = self.tail[0].coords[1] * 10
        for i in range(1, len(self.tail)):
            self.tail[i].last_coords[0] = self.tail[i].coords[0]
            self.tail[i].last_coords[1] = self.tail[i].coords[1]
            self.tail[i].coords[0] = self.tail[i - 1].last_coords[0]
            self.tail[i].coords[1] = self.tail[i - 1].last_coords[1]
            self.tail[i].rectangle.left = self.tail[i].coords[0] * 10
            self.tail[i].rectangle.top = self.tail[i].coords[1] * 10
        self.head.coords = direction_apply(grid, self.head.coords, self.head.direction)
        self.head.rectangle.left = self.head.coords[0] * 10
        self.head.rectangle.top = self.head.coords[1] * 10
    
    def render_snake(self, screen):
        pygame.draw.rect(screen, self.food.color, self.food.rectangle)
        pygame.draw.rect(screen, self.head.color, self.head.rectangle)
        for i in self.tail:
            pygame.draw.rect(screen, i.color, i.rectangle)

colors_snake = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
colors_food = [(255, 255, 0), (255, 0, 255), (0, 255, 255)]

def direction_apply(grid, coordinates, direction):
    if direction == "down" and coordinates[1] < len(grid) - 1:
        coordinates[1] += 1
    if direction == "up" and coordinates[1] > 0:
        coordinates[1] -= 1
    if direction == "right" and coordinates[0] < len(grid[0]) - 1:
        coordinates[0] += 1
    if direction == "left" and coordinates[0] > 0:
        coordinates[0] -= 1
    return coordinates

def cpy(to_cpy):
    return to_cpy

player_amount = 3
direction = "up"
pixel_coords = [5, 5]
screen_size = (250, 200)


pygame.init()

rectangle = pygame.rect.Rect(0, 0, 10, 10)

# Set up the drawing window
grid = [[0 for i in range(int(screen_size[0] / 10))] for i in range(int(screen_size[1] / 10))]
screen = pygame.display.set_mode([screen_size[0], screen_size[1]])
players = [snake(grid) for i in range(player_amount)]
for i in players:
    i.head.color = colors_snake[players.index(i)]
    i.food.color = colors_snake[players.index(i)]
print(len(grid[0]), len(grid))

# Run until the user asks to quit
running = True
while running:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = 0

    #Did the player touch a key ?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                for i in players:
                    i.head.direction = "left"
            if event.key == K_RIGHT:
                for i in players:
                    i.head.direction = "right"
            if event.key == K_UP:
                for i in players:
                    i.head.direction = "up"
            if event.key == K_DOWN:
                for i in players:
                    i.head.direction = "down"

        if event.type == pygame.QUIT:
            running = False

    # Fill the background with black
    screen.fill((0, 0, 0))
    
    # Update player position
    for i in players:
        for j in i.tail:
            grid[j.coords[1]][j.coords[0]] = 1

        i.move()
        if grid[i.head.coords[1]][i.head.coords[0]] == 1:
            print("You loose !")
            running = False
        i.render_snake(screen)
    pygame.time.delay(100)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
