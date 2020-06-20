import pygame

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

# Variables
clock = pygame.time.Clock()
base_font = pygame.font.Font(None, 16)
title = pygame.font.Font(None, 42)

# Screen object creation
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GatorHoldEm')


# Loop for name prompt
def intro_loop():
    # Variables
    user_text = ''
    input_rect = pygame.Rect(300, 400, 100, 32)
    color_active = pygame.Color('green')
    color_passive = pygame.Color('aquamarine3')
    color = color_passive

    # Run loop
    intro = True
    text_active = False

    while intro:
        # Check event queue
        for event in pygame.event.get():
            # Check if key was pressed
            if event.type == KEYDOWN:
                if text_active:
                    if event.key == K_BACKSPACE:
                        user_text = user_text[:-1]

                    elif event.key == K_RETURN:
                        room_loop()

                    else:
                        user_text += event.unicode

                if event.key == K_ESCAPE:
                    intro = False
                    continue

            # Check if mouse button was pressed
            elif event.type == MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    text_active = True

                else:
                    text_active = False

            # Check if window was closed
            elif event.type == QUIT:
                print("Bye!!")
                intro = False

        screen.fill((0, 0, 0))

        if text_active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect, 1)

        text_surface = base_font.render(user_text, True, (100, 255, 20))
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        # input_rect.w = max(200, text_surface.get_width() + 10)
        input_rect.w = 200

        pygame.display.flip()
        clock.tick(60)


def room_loop():
    # Variables
    user_text = "You're in a room!"
    input_rect = pygame.Rect(300, 400, 100, 32)
    color_active = pygame.Color('green')
    color_passive = pygame.Color('aquamarine3')
    color = color_passive

    # Run loop
    room = True
    text_active = False

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
                print("Game is being exited!!!")
                room = False

        screen.fill((0, 0, 0))

        if text_active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect, 1)

        text_surface = base_font.render(user_text, True, (100, 255, 20))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        input_rect.w = max(200, text_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(60)


intro_loop()
