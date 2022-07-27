import pyganim
from pygame import *
import blocks

mixer.init()

jump_sound = mixer.Sound('sounds/other/jump.ogg')
landing_sound = mixer.Sound('sounds/other/landing.ogg')

MOVE_SPEED = 7
WIDTH = 50
HEIGHT = 32
COLOR = (0, 0, 0)
JUMP_POWER = 10
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.1 # скорость смены кадров
ANIMATION_RIGHT = [('mario/r1.png'),
            ('mario/r2.png'),
            ('mario/r3.png'),
            ('mario/r4.png'),
            ('mario/r5.png')]
ANIMATION_LEFT = [('mario/l1.png'),
            ('mario/l2.png'),
            ('mario/l3.png'),
            ('mario/l4.png'),
            ('mario/l5.png')]
ANIMATION_HIT_RIGHT = [('mario/atkR1.png'),
            ('mario/atkR2.png'),
            ('mario/atkR3.png'),
            ('mario/atkR4.png'),
            ('mario/atkR5.png')]
ANIMATION_HIT_LEFT = [('mario/atkL1.png'),
            ('mario/atkL2.png'),
            ('mario/atkL3.png'),
            ('mario/atkL4.png'),
            ('mario/atkL5.png'),]
ANIMATION_JUMP_LEFT = [('mario/jl.png', 0.1)]
ANIMATION_JUMP_RIGHT = [('mario/jr.png', 0.1)]
ANIMATION_JUMP = [('mario/j.png', 0.1)]
ANIMATION_STAY_RIGHT = [('mario/0r.png', 0.1)]
ANIMATION_STAY_LEFT = [('mario/0l.png', 0.1)]



class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.orientation = "right" #направление лица
        self.health = 5; #hp перса
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(COLOR)
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.i = 15
        self.hitted = False
        self.image.set_colorkey((COLOR))  # делаем фон прозрачным
        #        Анимация движения вправо:
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
###
        boltAnim = []
        for anim in ANIMATION_HIT_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimHitLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimHitLeft.play()

        boltAnim = []
        for anim in ANIMATION_HIT_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimHitRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimHitRight.play()
###        
        #        Анимация движения влево:
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay_RIGHT = pyganim.PygAnimation(ANIMATION_STAY_RIGHT)
        self.boltAnimStay_RIGHT.play()
        self.boltAnimStay_RIGHT.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimStay_LEFT = pyganim.PygAnimation(ANIMATION_STAY_LEFT)
        self.boltAnimStay_LEFT.play()
        self.boltAnimStay_LEFT.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, hit, platforms):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                mixer.Sound.play(jump_sound)

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n


        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False;  # Мы не знаем, когда мы на земле :(

        self.rect.y += self.yvel #переносим свои положение на yvel с учетом платформ

        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel с учетом платформ
        self.collide(self.xvel, 0, platforms)
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            self.image.fill((COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.orientation = "left" 
            self.image.fill((COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.orientation = "right" 
            self.image.fill((COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))


        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not (up or hit):
                self.image.fill((COLOR))
                if self.orientation == "right":
                    self.boltAnimStay_RIGHT.blit(self.image, (0, 0))
                elif self.orientation == "left":
                    self.boltAnimStay_LEFT.blit(self.image, (0, 0))

        if hit and self.orientation == "right":
            self.boltAnimHitRight.blit(self.image, (0, 0))
            self.i -= 1
            if self.i == 0:
                self.rect.width = WIDTH - 18
                self.i = 15
        elif hit and self.orientation == "left":
            self.boltAnimHitLeft.blit(self.image, (0, 0))
        else:
            self.rect.width = WIDTH

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if isinstance(p, blocks.BlockTeleport):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, blocks.Lava) or isinstance(p, blocks.Water):
                    self.die()
                else:
                        if xvel > 0:  # если движется вправо
                            self.rect.right = p.rect.left  # то не движется вправо

                        if xvel < 0:  # если движется влево
                            self.rect.left = p.rect.right  # то не движется влево

                        if yvel > 0:  # если падает вниз
                            self.rect.bottom = p.rect.top  # то не падает вниз
                            self.onGround = True  # и становится на что-то твердое
                            self.yvel = 0  # и энергия падения пропадает

                        if yvel < 0:  # если движется вверх
                            self.rect.top = p.rect.bottom  # то не движется вверх
                            self.yvel = 0  # и энергия прыжка пропадает

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def die(self):
        self.teleporting(self.startX, self.startY)
        self.health -= 1
        mixer.Sound.play(landing_sound)
