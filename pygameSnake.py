import sys
import threading
import queue
import pygame
import pygame_menu
from pynput.keyboard import Key, Controller
import random
import controller

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

dis_width = 400
dis_height = 300
bluetooth_device = controller.get_user_device()

pygame.init()
surface = pygame.display.set_mode((dis_width, dis_height))

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Game With Bluetooth Controller")

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

font_style = pygame.font.SysFont("spendthrift", 25)
score_font = pygame.font.SysFont("cosmeticians", 35)


def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def start_game():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    surface.fill((0, 0, 0))
    while not game_over:

        while game_close:
            dis.fill(blue)
            message("Your Lost! Press A-Play Again or B-Quit", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_a:
                        menu_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(green)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

        # pygame.draw.rect(surface, blue, [200, 150, 10, 10])
        # pygame.display.update()
    pygame.quit()
    sys.exit()


def game_over():
    pass


def start():
    return True


menu = pygame_menu.Menu('Snake Game', dis_width, dis_height,
                        theme=pygame_menu.themes.THEME_DARK)

menu.add.button('Play', start_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

q = queue.Queue()


def menu_loop():
    menu.mainloop(surface)



keyboard = Controller()

aBtn = 304
bBtn = 305
startBtn = 315
LR_Dpad = 16
UD_Dpad = 17


def read_input():
    for controller_event in bluetooth_device.read_loop():
        if controller_event.code == 40:
            print("The controller went to sleep")
            # while os.path.exists()
        elif controller_event.value == 1:
            if controller_event.code == aBtn:
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                keyboard.press("a")
                keyboard.release("a")
            elif controller_event.code == bBtn:
                keyboard.press("b")
                keyboard.release("b")
            elif controller_event.code == LR_Dpad:
                keyboard.press(Key.right)
                keyboard.release(Key.right)
            elif controller_event.code == UD_Dpad:
                keyboard.press(Key.down)
                keyboard.release(Key.down)
        elif controller_event.value == -1:
            if controller_event.code == LR_Dpad:
                keyboard.press(Key.left)
                keyboard.release(Key.left)
            elif controller_event.code == UD_Dpad:
                keyboard.press(Key.up)
                keyboard.release(Key.up)


input_thread = threading.Thread(target=read_input, daemon=True, name='input_thread')
menu_main = threading.Thread(target=menu_loop, daemon=True, name='menu_main')

input_thread.start()
menu_main.start()

input_thread.join()
menu_main.join()
