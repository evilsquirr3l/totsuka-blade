import pygame
import random

from player import *
from blocks import *
from weapons import *
from background import *
from MenuBack import *

pygame.init()  # Инициация PyGame, обязательная строчка

# window
settings = open("settings.ini")
WIN_WIDTH = int(settings.readline())  # Ширина создаваемого окна
WIN_HEIGHT = int(settings.readline())  # Высота
settings.close()

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = (0, 0, 0)
NAME = "Battle of one"
ANIMATION_DELAY = 0.1  # скорость смены кадров
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
screen = pygame.display.set_mode(DISPLAY, flags)  # Создаем окошко
clock = pygame.time.Clock()
MUSIC = ['sounds/MOON Hydrogen.ogg', 'sounds/MOON Quixotic.ogg',
         'sounds/MOON Paris.ogg', 'sounds/MOON Crystals.ogg']

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.x + int(WIN_WIDTH / 2)
        y = -target.y + int(WIN_HEIGHT / 2)

        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIN_WIDTH), x)  # right
        y = max(-(self.height - WIN_HEIGHT), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)


def play_rand_music():
    n = random.randint(0, len(MUSIC) - 1)
    pygame.mixer.music.load(MUSIC[n])
    pygame.mixer.music.play(0)


def text_objects(text, font, color):  # color (R,G,B)
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button( x, y, w, h,ac, ic,action=None):
    pygame.init()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
       # pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()

       # pygame.draw.rect(screen, ic, (x, y, w, h))

def quitgame():
    pygame.quit()
    quit()


def start():
    
    time.wait(2000) # подождать 2 секунди, шоб усе прогрузилось і не лагало
    # собсна сама фіча. букви появляються
    i = 0
    while i < 220:
        clock.tick(60)
        screen.fill((0, 0, 0))
        largeText = pygame.font.SysFont("freesansbold.ttf", 115)
        TextSurf, TextRect = text_objects("Team 7 Entertainment", largeText, (i, i, i))
        TextRect.center = ((WIN_WIDTH / 2), (WIN_HEIGHT / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        i += 1

    while i >= 0:
        clock.tick(80)
        screen.fill((0, 0, 0))
        largeText = pygame.font.SysFont("freesansbold.ttf", 115)
        TextSurf, TextRect = text_objects("Team 7 Entertainment", largeText, (i, i, i))
        TextRect.center = ((WIN_WIDTH / 2), (WIN_HEIGHT / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        i -= 1

    time.wait(500)


def game_intro():
    entities = pygame.sprite.Group()  # Все объекты
    backgroundMenu=MenuBackground(WIN_WIDTH,WIN_HEIGHT)
    entities.add(backgroundMenu)
    logo = Logo((WIN_WIDTH/2)-300, (WIN_HEIGHT-475))
    entities.add(logo)
    play = Play(0,WIN_HEIGHT-70)
    entities.add(play)
    quit1 = Quit(WIN_WIDTH-225,WIN_HEIGHT-70)
    entities.add(quit1)
    timer = pygame.time.Clock()
    intro = True
    camera = Camera(WIN_WIDTH, WIN_HEIGHT)

    pygame.mixer.music.stop()
    pygame.mixer.music.load('sounds/MOON Dust.ogg')
    pygame.mixer.music.play(-1)       # музика грає нескінченно

    while intro:
        timer.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        backgroundMenu.update()
        button(0, WIN_HEIGHT-70, 300, 250, green, bright_green, main)
        button(WIN_WIDTH-225, WIN_HEIGHT-70, 300, 250, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def main():
    # GUI Elements
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN  # полноэкранный режим, двойная буферизация, аппаратное ускорение
    screen = pygame.display.set_mode(DISPLAY, flags)  # Создаем окошко
    pygame.display.set_caption(NAME)  # Пишем в шапку
    surf = pygame.Surface(DISPLAY)

    hero = Player(32, 32)  # создаем героя по (x,y) координатам
    herotwo = Player(990, 32)

    gun = Gun(hero, 1)  # Создаем первый пистолет
    guntwo = Gun(herotwo, 2)  # И второй тоже

    blade = Blade(hero, 1)
    bladetwo = Blade(herotwo, 2)

    left = right = up = False
    left2 = right2 = up2 = False
    entities =[]
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться


    def preparemap():
        f = open("tilemap.tmx", "r")
        lines = f.readlines()
        f.close()
        f = open("timetilemap.txt", "w")
        for line in lines:
            if line != """<?xml version="1.0" encoding="UTF-8"?>""" + "\n" and \
                    line != """<map version="1.2" tiledversion="1.2.1" orientation="orthogonal" renderorder="right-down" width="34" height="24" tilewidth="32" tileheight="32" infinite="0" nextlayerid="18" nextobjectid="16">""" + "\n" and \
                    line != """ <tileset firstgid="1" source="platform.tsx"/>""" + "\n" and \
                    line != """ <tileset firstgid="2" source="lava.tsx"/>""" + "\n" and \
                    line != """ <tileset firstgid="3" source="water.tsx"/>""" + "\n" and \
                    line != """ <tileset firstgid="4" source="portal1.tsx"/>""" + "\n" and \
                    line != """ <tileset firstgid="5" source="portal2.tsx"/>""" + "\n" and \
                    line != """ <layer id="17" name="Tile Layer 1" width="34" height="24">""" + "\n" and \
                    line != """  <data encoding="csv">""" + "\n" and \
                    line != """</data>""" + "\n" and \
                    line != """ </layer>""" + "\n" and \
                    line != """ <objectgroup id="5" name="Object Layer 1"/>""" + "\n" and \
                    line != """</map>""" + "\n":
                f.write(line)
        f.close()

        f = open("timetilemap.txt", 'r')
        filedata = f.read()
        f.close()
        newdata = filedata.replace(",", "")
        f = open("timetilemap.txt", 'w')
        f.write(newdata)
        f.close()

        f = open("timetilemap.txt", "r")
        lines = f.readlines()
        f.close()
        level = lines
        return level

    level = preparemap()


    timer = pygame.time.Clock()

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    background = Background(total_level_width, total_level_height)
    entities.add(background)
    entities.add(hero)
    entities.add(herotwo)

    x = y = 0  # координаты
    for row in level:
        for col in row:
            if col == "1":
                platform = Platform(x, y)
                entities.add(platform)
                platforms.append(platform)

            if col == "2":
                lv = Lava(x, y)
                entities.add(lv)
                platforms.append(lv)

            if col == "3":
                wt = Water(x, y)
                entities.add(wt)
                platforms.append(wt)

            x = x + PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y = y + PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля


    camera = Camera(total_level_width, total_level_height)

    pygame.mixer.music.stop()
    play_rand_music()

    while 1:  # Основной цикл программы
        timer.tick(60)  # fps = 60
        # keys = pygame.key.get_pressed() - conflict
        events = pygame.event.get()
        for e in events:

            if e.type == KEYDOWN and e.key == K_UP:
                up = True

            if e.type == KEYUP and e.key == K_UP:
                up = False

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        for i in events:

            if i.type == KEYDOWN and i.key == K_w:
                up2 = True

            if i.type == KEYUP and i.key == K_w:
                up2 = False

            if i.type == KEYDOWN and i.key == K_a:
                left2 = True
            if i.type == KEYDOWN and i.key == K_d:
                right2 = True

            if i.type == KEYUP and i.key == K_d:
                right2 = False
            if i.type == KEYUP and i.key == K_a:
                left2 = False
            if i.type == KEYUP and i.key == K_ESCAPE:
                game_intro()

        if not pygame.mixer.music.get_busy:
            play_rand_music()

        screen.blit(surf, (0, 0))  # перерисовка на каждой итерации

        background.update()
        hero.update(left, right, up, blade.shot, platforms)  # передвижение
        herotwo.update(left2, right2, up2, bladetwo.shot, platforms)
        gun.update(hero, herotwo, platforms)  # Прописали updatе
        guntwo.update(herotwo, hero, platforms)

        center_rect = pygame.Rect(int((hero.rect.x + herotwo.rect.x)/2), int((hero.rect.y + herotwo.rect.y)/2), 0, 0)
        camera.update(center_rect)

        for e in entities:  # отображение всего
            screen.blit(e.image, camera.apply(e))

        blade.update(hero, platforms, herotwo, guntwo.bullets, screen, camera)
        bladetwo.update(herotwo, platforms, hero, gun.bullets, screen, camera)

        for b in gun.bullets:
            b.draw(screen, camera)
        for b in guntwo.bullets:
            b.draw(screen, camera)
        
# Условия победы
        if blade.winGame:
            herotwo.die()
            blade.winGame = False
            guntwo.magazine = 10   
        elif bladetwo.winGame:
            hero.die()
            bladetwo.winGame = False
            gun.magazine = 10

        for b in gun.bullets:
                if b.winGame:
                    herotwo.die()
                    b.winGame = False
                    guntwo.magazine = 10
        for b in guntwo.bullets:
                if b.winGame:
                    hero.die()
                    b.winGame = False
                    gun.magazine = 10
        if hero.health == 0:
            game_intro()
        if herotwo.health == 0:
            game_intro()

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    start()
    game_intro()
    main()
    pygame.quit()
