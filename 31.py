import os
import random
import pygame_menu
from pygame.examples.cursors import image

from maadad import menu
import pygame

pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
pygame.display.flip()
state = "menu"
food_x = random.randint(0, WIDTH-10)
food_y = random.randint(0, HEIGHT-10)
label_id = None
bg_music = pygame.mixer.Sound("music/background.mp3")
bg_music.set_volume(0.2)
eat_music = pygame.mixer.Sound("music/eat.mp3")
eat_music.set_volume(0.5)
gameover_music = pygame.mixer.Sound("music/gameover.mp3")
gameover_music.set_volume(0.2)
bite_music = pygame.mixer.Sound("music/bite.mp3")
bite_music.set_volume(10)
difficulty = 1
bg_image = pygame.image.load("image/bg.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
bg_rect = bg_image.get_rect()
food_names = os.listdir("image/food")
foods = []
head_sprites = [pygame.image.load("image/snake/HeadR.png"),
                pygame.image.load("image/snake/HeadL.png"),
                pygame.image.load("image/snake/HeadB.png"),
                pygame.image.load("image/snake/HeadT.png")]

tail_sprites = [pygame.image.load("image/snake/tailup.png"),
                pygame.image.load("image/snake/taildown.png"),
                pygame.image.load("image/snake/tailright.png"),
                pygame.image.load("image/snake/tailleft.png")]

i = 0

for x in food_names:
    foods.append(pygame.image.load(f"image/food/{x}"))

food = pygame.transform.scale(random.choice(foods), (10, 10))
food_rect = food.get_rect(x=food_x, y=food_y)


def disable():
    global state
    mainmenu.disable()
    state = "game"
    bg_music.play(loops= -1)

def eating_check(food_x, food_y, x, y):
    if food_x-10 <= x <= food_x+10:
        if food_y-10 <= y <= food_y+10:
            eat_music.play()
            return True
    else:
        return False

mainmenu = menu.Menu(screen, pygame_menu.themes.THEME_GREEN)
mainmenu.add.range_slider("Сложность ", 1, (1, 2, 3, 4, 5))
play_btn = mainmenu.add.button("Играть", disable)

def set_difficulty():
    global difficulty, FPS


def lose():
    bg_music.stop()
    bite_music.play()
    pygame.time.delay(500)
    gameover_music.play()
    global play_btn, label_id
    try:
        label = mainmenu.get_widget(label_id)
        label.set_title(f"Счет: {length}")
    except:
        label = mainmenu.add.label(f"Счет: {length}")
        label_id = label.get_id()
        mainmenu.move_widget_index(label, 0)
    mainmenu.set_title("Проиграл")
    play_btn.set_title("Играть заново")
    new_game()
    mainmenu.enable()

def draw_head(i, snake_list):
    snake_head_image = head_sprites[i]
    snake_head = pygame.transform.scale(snake_head_image, (10, 10))
    snake_head_rect = snake_head.get_rect(x= snake_list[-1][0], y= snake_list[-1][1])
    screen.blit(snake_head, snake_head_rect)

def draw_tail(snake_list):
    if len(snake_list) < 2:
        return

    tail_x, tail_y = snake_list[0]
    next_x, next_y = snake_list[1]

    if tail_x < next_x:
        tail_image = tail_sprites[2]
    elif tail_x > next_x:
        tail_image = tail_sprites[3]
    elif tail_y < next_y:
        tail_image = tail_sprites[1]
    elif tail_y > next_y:
        tail_image = tail_sprites[0]

    tail = pygame.transform.scale(tail_image, (10, 10))
    tail.set_colorkey("white")
    tail_rect = tail.get_rect(x = snake_list[0][0], y = snake_list[0][1])
    screen.blit(tail, tail_rect)

def new_game():
    global x1, y1, length, y1_change, x1_change
    global food_x, food_y, food, food_rect
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0
    length = 1
    food_x = random.randint(0, WIDTH - 10)
    food_y = random.randint(0, HEIGHT - 10)
    food = pygame.transform.scale(random.choice(foods), (10, 10))
    food_rect = food.get_rect(x=food_x, y=food_y)
    snake_list.clear()

def create_sms(message, color, x, y, font, size):
    font_style = pygame.font.SysFont(font, size)
    msg = font_style.render(message, True, color)
    screen.blit(msg, [x, y])

mainmenu.add.button("Выход", quit)
FPS = 5
clock = pygame.time.Clock()

snake_list = []
x1 = WIDTH/2
y1 = HEIGHT/2
x1_change = 0
y1_change = 0
length = 1
run = True

while run:
    events = pygame.event.get()
    clock.tick(FPS)
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -10
                y1_change = 0
                i = 1
            elif event.key == pygame.K_RIGHT:
                x1_change = 10
                y1_change = 0
                i = 0
            if event.key == pygame.K_UP:
                x1_change = 0
                y1_change = -10
                i = 3
            elif event.key == pygame.K_DOWN:
                x1_change = 0
                y1_change = 10
                i = 2
            elif event.key == pygame.K_m:
                mainmenu.enable()
                state = "menu"

    x1 += x1_change
    y1 += y1_change

    #screen.fill("white")
    screen.blit(bg_image, bg_rect)
    create_sms(f"Счет: {length}", "black", 0, 0, "Comic Sans", 25)

    if eating_check(food_x, food_y, x1, y1):
        food_x = random.randint(0, WIDTH-10)
        food_y = random.randint(0, HEIGHT-10)
        food = pygame.transform.scale(random.choice(foods), (10, 10))
        food_rect = food.get_rect(x=food_x, y=food_y)
        length += 1

    screen.blit(food, food_rect)
    snake_head = [x1, y1]
    snake_list.append(snake_head)

    if len(snake_list) > length:
        del snake_list[0]

    for x in snake_list[0:]:
        #pygame.draw.rect(screen, "black", [x[0], x[1], 10, 10])
        snake_image = pygame.image.load("image/snake/body.png")
        snake = pygame.transform.scale(snake_image, (10, 10))
        snake.set_colorkey("white")
        screen.blit(snake, (x[0], x[1]))


    draw_head(i, snake_list)
    draw_tail(snake_list)

    for x in snake_list[:-1]:
       if x == snake_head:
            lose()

    if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
        lose()

    mainmenu.flip(events)
    pygame.display.flip()

pygame.quit()
