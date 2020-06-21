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
clock = pygame.time.Clock()
base_font = pygame.font.Font(None, 16)
title_font = pygame.font.Font(None, 108)

# Screen object creation
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GatorHoldEm')


# Function to draw menu.
# Passed in variables:
# 1. Input box rectangle
# 2. Input box contents
# 3. Input box activity
def menu_draw(input_rect, user_text, text_active):
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
                pygame.quit()
                sys.exit()
                intro = False

        screen.fill(black)

        menu_draw(input_rect, user_text, text_active)

        pygame.display.flip()
        clock.tick(3)


def room_name_loop():
    # Variables
    user_text = "Room name prompt!"
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
                pygame.quit()
                sys.exit()
                intro = False

        screen.fill(black)

        if text_active:
            color = color_active
        else:
            color = color_passive

        menu_draw(input_rect, user_text, text_active)

        pygame.display.flip()
        clock.tick(3)


intro_loop()
