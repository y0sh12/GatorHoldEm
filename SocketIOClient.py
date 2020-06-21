import sys
import socketio
import pygame

sio = socketio.Client()
name = ""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
black = (0, 0, 0)
white = (255, 255, 255)
red = (0, 255, 0)
screen = ""
clock = ""

base_font = ""
title_font = ""
label_font = ""

name_input = ''
room_name_input = ''


from pygame.locals import (
    MOUSEBUTTONDOWN,
    KEYDOWN,
    K_ESCAPE,
    K_BACKSPACE,
    K_RETURN,
    QUIT
)

@sio.event
def connect():
    print("Welcome", name + "!")
    print("You have successfully connected to the Gator Hold \'em server!")
    print("Good Luck!")


@sio.event
def connect_error(data):
    if str(data) == "Unauthorized":
        print("The game has started or has reached maximum player limit")
    else:
        print("The connection failed!")


@sio.event
def disconnect():
    print("You have left the game. Come back soon!")


@sio.on('user_connection')
def on_event(message):
    print(message)


@sio.on('user_disconnect')
def on_event(message):
    print(message)


@sio.on('joined_room')
def on_event(message, room):
    sio.emit('my_name', (name, room))
    print(message)


@sio.on('your_turn')
def on_event(message):
    print(message)

@sio.on('message')
def on_event(message):
    print(message)

@sio.on('emit_hand')
def on_event(card1, card2):
    print(card1, card2)
    

@sio.on('connection_error')
def on_event(error):
    print("The game has started or has reached maximum player limit")

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

        pygame.display.flip()
        clock.tick(60)



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

def main():
    global screen
    global clock
    global base_font
    global title_font
    global label_font
    global name_input
    global room_name_input
    pygame.init()
    clock = pygame.time.Clock()
    base_font = pygame.font.Font(None, 16)
    title_font = pygame.font.Font(None, 108)
    label_font = pygame.font.Font(None, 30)
    # 3. Game variables
    name_input = ''
    room_name_input = ''

    # Screen object creation
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('GatorHoldEm')
    intro_loop()

    # global name
    # name = input("What is your name?\n")
    # sio.connect('http://localhost:5000')
    # # sio.connect('http://172.105.150.126:5000')
    # print('Your sid is', sio.sid)
    # print("You are now in the lobby")
    # room = input("What room would you like to join?\n")
    # sio.emit('goto_room', room)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(0)
