import pyganim
from pygame import *
from game import *

mixer.init()

#Обьявляем константы:
bullet_width = 4 #параметры пулек
bullet_height = 6
bullet_color = "yellow"
move_speed = 15

gravity = 0.045 #гравитация для баллистики(пока не юзается)

gun_width = 10 #параметры пистолета
gun_height = 5
gun_color = "blue"

blade_width = 3 #параметры катаны
blade_height = 18
blade_color = "blue"

hit_sound = mixer.Sound('sounds/other/hit.ogg')
shoot_sound = mixer.Sound('sounds/other/shoot.ogg')


#Прописываем класс weapon
class Weapon(sprite.Sprite):
    def __init__(self, number_of_player): #функция внутренних переменных класса
        sprite.Sprite.__init__(self)
        self.number_of_player = number_of_player
        self.shot = False #переменная для отслеживания момента удара(выстрела)
        self.onGround = False


#Прописываем пистолетик        
class Gun(Weapon):
    def __init__(self, player, number_of_player): #функция внутренних переменных класса
        Weapon.__init__(self, number_of_player) #передаем пистолету переменные дочернего класса weapon
        self.rate_of_fire = 30 #скорострельность
        self.time_to_cooldown = 0
        self.magazine = 10
        self.bullets = []
        self.image = Surface((gun_width, gun_height))
        self.image.fill(Color(gun_color))
        self.rect = Rect(player.rect.x+player.rect.width, player.rect.y+(player.rect.height/2), gun_width, gun_height) #задаем расположение пистолета(начальное)

    def update(self, player, playertwo, platforms): #функция обновления
        #self.rate_of_fire = self.rate_of_fire - 1 #тут должна будет быть скорострельность
        if player.orientation == "right":  #меняем направление и положение пистолета когда герой меняет положение
            self.rect = Rect(player.rect.x+player.rect.width, player.rect.y+(player.rect.height/2), gun_width, gun_height)
        elif player.orientation == "left":
            self.rect = Rect(player.rect.x-gun_width, player.rect.y+(player.rect.height/2), gun_width, gun_height)
        if self.time_to_cooldown == 0:
            self.keyboard(self.number_of_player) #проверяем клавиатуру
        if self.shot:
            self.gun_shot(self.bullets, player.orientation)
            self.shot = False
        for b in self.bullets:
            b.update(platforms, playertwo)
        if self.time_to_cooldown > 0:
            self.time_to_cooldown -= 1

    def keyboard(self, number_of_player): #функция клавиатуры
        keys = key.get_pressed() #обьявляем переменную куда записалась сразу нажатая кнопка
        if number_of_player == 1: #клавиатура для первого игрока
            if keys[K_m]: #выстрел на правом ctrl
                self.shot = True #если нажал кнопку то бабах
                self.time_to_cooldown = self.rate_of_fire
        elif number_of_player == 2: #аналогично для 2 игрока
            if keys[K_v]:
                self.shot = True
                self.time_to_cooldown = self.rate_of_fire

    def gun_shot(self, bullets, orientation):
        if self.magazine > 0:
            mixer.Sound.play(shoot_sound)
            bullet = Bullet(orientation, self)
            self.bullets.append(bullet)
            self.magazine -= 1

class Blade(Weapon):
    def __init__(self, player, number_of_player):
        Weapon.__init__(self, number_of_player)
        self.winGame = False
        self.shot_zam = 0
        self.time_to_kulldown = 0
        self.width = blade_width
        self.height = blade_height
        self.image = Surface((self.width, self.height))
        self.image.fill(Color(blade_color)) 
        self.rect = Rect(player.rect.x, player.rect.y, self.width, self.height)
        radius = blade_height
    def update(self, player, platforms, playertwo, bullets, screen, camera):
        self.rect = Rect(player.rect.x, player.rect.y, self.width, self.height)
        if self.time_to_kulldown == 0:
            self.keyboard(self.number_of_player)
        if self.time_to_kulldown == 60:
            self.shot = True
        elif self.time_to_kulldown < 45:
            self.shot = False
        if player.orientation == "right":
            if self.time_to_kulldown > 55:
                self.rect = Rect(player.rect.x, player.rect.y, self.width, self.height)
                blade_hit = BladeHitBox(self.rect.x+player.rect.width-18, self.rect.y+(player.rect.height*2)/3, self.height*0.6, player.rect.height/3)
                #blade_hit.draw(screen, camera)
                blade_hit.collide(platforms, playertwo, bullets)
                if blade_hit.winGame:
                    self.winGame = True
            if self.time_to_kulldown > 50 and self.time_to_kulldown < 55:
                self.rect = Rect(player.rect.x, player.rect.y, self.width, self.height)
                blade_hit = BladeHitBox(self.rect.x+player.rect.width-18, self.rect.y+player.rect.height/3, self.height, player.rect.height/3)
                #blade_hit.draw(screen, camera)
                blade_hit.collide(platforms, playertwo, bullets)
                if blade_hit.winGame:
                    self.winGame = True
            if self.time_to_kulldown > 45 and self.time_to_kulldown < 50:
                self.rect = Rect(player.rect.x, player.rect.y, self.width, self.height)
                blade_hit = BladeHitBox(self.rect.x+player.rect.width-18, self.rect.y, self.height*0.6, player.rect.height/3)
                #blade_hit.draw(screen, camera)
                blade_hit.collide(platforms, playertwo, bullets)
                if blade_hit.winGame:
                    self.winGame = True
        elif player.orientation == "left":
            if self.time_to_kulldown > 55:
                self.rect = Rect(player.rect.x, player.rect.y, self.width, self.height)
                blade_hit = BladeHitBox(self.rect.x+self.height*0.4, self.rect.y+(player.rect.height*2)/3, self.height*0.6, player.rect.height/3)
                #blade_hit.draw(screen, camera)
                blade_hit.collide(platforms, playertwo, bullets)
                if blade_hit.winGame:
                    self.winGame = True
            if self.time_to_kulldown > 50 and self.time_to_kulldown < 55:
                self.rect = Rect(player.rect.x, player.rect.y, self.width, self.height)
                blade_hit = BladeHitBox(self.rect.x, self.rect.y+player.rect.height/3, self.height, player.rect.height/3)
                #blade_hit.draw(screen, camera)
                blade_hit.collide(platforms, playertwo, bullets)
                if blade_hit.winGame:
                    self.winGame = True
            if self.time_to_kulldown > 45 and self.time_to_kulldown < 50:
                self.rect = Rect(player.rect.x, player.rect.y, self.width, self.height)
                blade_hit = BladeHitBox(self.rect.x+self.height*0.4, self.rect.y, self.height*0.6, player.rect.height/3)
                #blade_hit.draw(screen, camera)
                blade_hit.collide(platforms, playertwo, bullets)
                if blade_hit.winGame:
                    self.winGame = True
        if self.time_to_kulldown > 0:
            self.time_to_kulldown -= 1;
    def keyboard(self, number_of_player):
        keys = key.get_pressed() #обьявляем переменную куда записалась сразу нажатая кнопка
        if number_of_player == 1: #клавиатура для первого игрока
            if keys[K_n]: #выстрел на правом ctrl
                self.time_to_kulldown = 60
        elif number_of_player == 2: #аналогично для 2 игрока
            if keys[K_c]:
                self.time_to_kulldown = 60
                
#прописываем класс пульки
class Bullet(sprite.Sprite):
    def __init__(self, orientation, gun): #функция внутренних переменных
        sprite.Sprite.__init__(self)
        #self.yvelocity = 0 #это для баллистики
        self.onGame = True #пуля в игре или нет
        self.winGame = False #это для победы
        if orientation == "right": #направление выстрела
            self.xvelocity = move_speed
        elif orientation == "left":
            self.xvelocity = -move_speed
        self.image = Surface((bullet_width, bullet_height))
        self.image.fill(Color(bullet_color))
        self.rect = Rect(gun.rect.x, gun.rect.y, bullet_width, bullet_height) #стартуем из дула пушки

    def update(self, platforms, playertwo): #функция обновления
        if self.onGame: #когда пуля летит проверяем столкновения
            self.collide(platforms,playertwo)
            #self.yvelocity = self.yvelocity + gravity #это для баллистики
            #self.rect.y = self.rect.y + self.yvelocity
            self.rect.x = self.rect.x + self.xvelocity #тут меняем координаты по иксу

    def collide(self, platforms, playertwo): #функция столкновений
        for i in platforms: #проверяем по платформам
            if sprite.collide_rect(self, i): #если стукнулись об платформу то минус пулька
                self.onGame = False
        if sprite.collide_rect(self, playertwo): #eсли стукнулись об челика то все
            self.onGame = False
            self.winGame = True
            mixer.Sound.play(hit_sound)

    def draw(self, screen, camera): #функция рисовки пульки
        if self.onGame:
            screen.blit(self.image, camera.apply(self))

class BladeHitBox(sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.onGame = True
        self.winGame = False
        self.image = Surface((width, height))
        self.image.fill(Color(blade_color))
        self.rect = Rect(x, y, width, height)
        
    def collide(self, platforms, playertwo, bullets): #функция столкновений
        for i in platforms: #проверяем по платформам
            if sprite.collide_rect(self, i): #если стукнулись об платформу то минус пулька
                self.onGame = False
        if sprite.collide_rect(self, playertwo): #eсли стукнулись об челика то все
            self.onGame = False
            self.winGame = True
            mixer.Sound.play(hit_sound)
        for b in bullets:
            if sprite.collide_rect(self, b):
                b.onGame = False
                self.onGame = False
                mixer.Sound.play(hit_sound)

    def draw(self, screen, camera): #функция рисовки пульки
        if self.onGame:
            screen.blit(self.image, camera.apply(self))
        
        
