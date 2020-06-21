import pygame
import sys

# Import constants
from pygame.locals import (
    MOUSEBUTTONDOWN,
    KEYDOWN,
    K_ESCAPE,
    K_BACKSPACE,
    K_RETURN,
    QUIT
)

# Initialize game
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
black = (0, 0, 0)
white = (255, 255, 255)
red = (0, 255, 0)

# Variables
# 1. Clock variables
clock = pygame.time.Clock()
# 2. Font variables
base_font = pygame.font.Font(None, 16)
title_font = pygame.font.Font(None, 108)
label_font = pygame.font.Font(None, 30)
# 3. Game variables
name_input = ''
room_name_input = ''

# Screen object creation
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GatorHoldEm')


# Function to draw menu.
# Passed in variables:
# 1. Input box rectangle
# 2. Input box contents
# 3. Input box activity
def menu_draw(input_rect, user_text, label_text, text_active):
    color_active = pygame.Color('green')
    color_passive = pygame.Color('aquamarine3')
    color = color_passive

    if text_active:
        color = color_active
    else:
        color = color_passive

    # Draw title on screen
    title_surface = title_font.render("GatorHoldEm", True, white)
    title_rect = title_surface.get_rect(center=(round(SCREEN_WIDTH / 2), round(SCREEN_HEIGHT / 4)))
    screen.blit(title_surface, title_rect)

    # Draw label on screen
    label_surface = label_font.render(label_text, True, white)
    label_rect = label_surface.get_rect(center=(input_rect.centerx, input_rect.centery - 50))
    screen.blit(label_surface, label_rect)

    # Draw input box on screen
    pygame.draw.rect(screen, color, input_rect, 1)

    input_surface = base_font.render(user_text, True, (100, 255, 20))
    screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))

    input_rect.w = max(200, input_surface.get_width() + 10)
    pygame.display.update(input_rect)


# Loop for name prompt
def intro_loop():
    # Variables
    user_text = ''
    label_text = 'Please enter your name:'
    input_rect = pygame.Rect(300, 400, 100, 32)
    text_active = False
    intro = True

    # Run loop
    while intro:
        # Check event queue
        for event in pygame.event.get():
            # Check if key was pressed
            if event.type == KEYDOWN:
                if text_active:
                    if event.key == K_BACKSPACE:
                        user_text = user_text[:-1]

                    elif event.key == K_RETURN:
                        global name_input
                        name_input = user_text
                        room_name_loop()

                    else:
                        user_text += event.unicode

            # Check if mouse button was pressed
            elif event.type == MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    text_active = True

                else:
                    text_active = False

            # Check if window was closed
            elif event.type == QUIT:
                intro = False
                pygame.quit()
                sys.exit()

        screen.fill(black)

        menu_draw(input_rect, user_text, label_text, text_active)

        pygame.display.flip()
        clock.tick(60)


# Loop for room name prompt
def room_name_loop():
    # Variables
    user_text = "Room name prompt!"
    label_text = 'Enter room name to join:'
    input_rect = pygame.Rect(300, 400, 100, 32)
    text_active = False
    room = True

    # Run loop
    while room:
        # Check event queue
        for event in pygame.event.get():
            # Check if key was pressed
            if event.type == KEYDOWN:
                if text_active:
                    if event.key == K_BACKSPACE:
                        user_text = user_text[:-1]

                    elif event.key == K_RETURN:
                        global room_name_input
                        room_name_input = user_text
                        room_loop()

                    else:
                        user_text += event.unicode

                if event.key == K_ESCAPE:
                    room = False
                    continue

            # Check if mouse button was pressed
            elif event.type == MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    text_active = True

                else:
                    text_active = False

            # Check if window was closed
            elif event.type == QUIT:
                intro = False
                pygame.quit()
                sys.exit()

        screen.fill(black)

        menu_draw(input_rect, user_text, label_text, text_active)

        pygame.display.flip()
        clock.tick(60)


# Loop for lobby
def room_loop():
    # Variables
    room = True

    # Run loop
    while room:
        # Check event queue
        for event in pygame.event.get():
            # Check if key was pressed
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    room = False
                    continue

            # Check if mouse button was pressed
            elif event.type == MOUSEBUTTONDOWN:
                print('Mouse pressed!')
                # if input_rect.collidepoint(event.pos):

            # Check if window was closed
            elif event.type == QUIT:
                intro = False
                pygame.quit()
                sys.exit()

        screen.fill(black)

        #Room lobby title
        lobby_title_font = pygame.font.Font(None, 40)
        lobby_title_surface = lobby_title_font.render("Room: " + room_name_input, True, white)
        title_rect = lobby_title_surface.get_rect(center=(round(SCREEN_WIDTH / 2), round(SCREEN_HEIGHT / 5)))
        screen.blit(lobby_title_surface, title_rect)


        pygame.display.flip()
        clock.tick(60)


intro_loop()
