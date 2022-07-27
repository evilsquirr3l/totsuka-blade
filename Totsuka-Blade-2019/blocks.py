from pygame import *
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (255, 98, 98)

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("platform.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockTeleport(Platform):#блок телепорта
    def __init__(self, x, y, goX,goY):
        Platform.__init__(self, x, y)
        self.goX = goX # координаты назначения перемещения
        self.goY = goY # координаты назначения перемещения
        self.image = image.load('portal1.png')

class Lava(Platform):#блок лавы
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("lava.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Water(Platform):#блок воды
    def __init__(self, x , y):
        sprite.Sprite.__init__(self)
        self.image = image.load("water.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
class Logo(Platform):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load("logo.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    
class Play(Platform):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load("play.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
class Quit(Platform):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load("quit.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        





        

