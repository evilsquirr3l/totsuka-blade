import pyganim
from pygame import *
import blocks

ANIMATION = []
ANIMATION_DELAY = 0.1

settings = open("settings.ini")
WIDTH = int(settings.readline())  # Ширина создаваемого окна
HEIGHT = int(settings.readline())  # Высота
settings.close()
ANIMATION=['MenuBackground/frame_01_delay-0.1s.png', 'MenuBackground/frame_02_delay-0.1s.png', 'MenuBackground/frame_03_delay-0.1s.png', 'MenuBackground/frame_04_delay-0.1s.png', 'MenuBackground/frame_05_delay-0.1s.png', 'MenuBackground/frame_06_delay-0.1s.png', 'MenuBackground/frame_07_delay-0.1s.png', 'MenuBackground/frame_08_delay-0.1s.png', 'MenuBackground/frame_09_delay-0.1s.png', 'MenuBackground/frame_11_delay-0.1s.png', 'MenuBackground/frame_12_delay-0.1s.png', 'MenuBackground/frame_13_delay-0.1s.png', 'MenuBackground/frame_14_delay-0.1s.png', 'MenuBackground/frame_15_delay-0.1s.png', 'MenuBackground/frame_16_delay-0.1s.png', 'MenuBackground/frame_17_delay-0.1s.png', 'MenuBackground/frame_18_delay-0.1s.png', 'MenuBackground/frame_19_delay-0.1s.png', 'MenuBackground/frame_21_delay-0.1s.png', 'MenuBackground/frame_22_delay-0.1s.png', 'MenuBackground/frame_23_delay-0.1s.png', 'MenuBackground/frame_24_delay-0.1s.png', 'MenuBackground/frame_25_delay-0.1s.png', 'MenuBackground/frame_26_delay-0.1s.png', 'MenuBackground/frame_27_delay-0.1s.png', 'MenuBackground/frame_28_delay-0.1s.png', 'MenuBackground/frame_29_delay-0.1s.png', 'MenuBackground/frame_31_delay-0.1s.png', 'MenuBackground/frame_32_delay-0.1s.png', 'MenuBackground/frame_33_delay-0.1s.png', 'MenuBackground/frame_34_delay-0.1s.png', 'MenuBackground/frame_35_delay-0.1s.png', 'MenuBackground/frame_36_delay-0.1s.png', 'MenuBackground/frame_37_delay-0.1s.png', 'MenuBackground/frame_38_delay-0.1s.png', 'MenuBackground/frame_39_delay-0.1s.png', 'MenuBackground/frame_41_delay-0.1s.png', 'MenuBackground/frame_42_delay-0.1s.png', 'MenuBackground/frame_43_delay-0.1s.png', 'MenuBackground/frame_44_delay-0.1s.png', 'MenuBackground/frame_45_delay-0.1s.png', 'MenuBackground/frame_46_delay-0.1s.png', 'MenuBackground/frame_47_delay-0.1s.png', 'MenuBackground/frame_48_delay-0.1s.png', 'MenuBackground/frame_49_delay-0.1s.png', 'MenuBackground/frame_51_delay-0.1s.png', 'MenuBackground/frame_52_delay-0.1s.png', 'MenuBackground/frame_53_delay-0.1s.png', 'MenuBackground/frame_54_delay-0.1s.png', 'MenuBackground/frame_55_delay-0.1s.png', 'MenuBackground/frame_56_delay-0.1s.png', 'MenuBackground/frame_57_delay-0.1s.png', 'MenuBackground/frame_58_delay-0.1s.png', 'MenuBackground/frame_59_delay-0.1s.png', 'MenuBackground/frame_61_delay-0.1s.png', 'MenuBackground/frame_62_delay-0.1s.png', 'MenuBackground/frame_63_delay-0.1s.png', 'MenuBackground/frame_64_delay-0.1s.png', 'MenuBackground/frame_65_delay-0.1s.png', 'MenuBackground/frame_66_delay-0.1s.png', 'MenuBackground/frame_67_delay-0.1s.png', 'MenuBackground/frame_68_delay-0.1s.png', 'MenuBackground/frame_69_delay-0.1s.png', 'MenuBackground/frame_71_delay-0.1s.png']

class MenuBackground(sprite.Sprite):
    def __init__(self, total_width, total_height):
        sprite.Sprite.__init__(self)
        self.rect = Rect(0, 0, total_width, total_height)
        self.image = Surface((total_width, total_height))
        boltAnim = []
        for anim in ANIMATION:
            frame = image.load(anim)
            scaled_frame = transform.scale(frame, (total_width, total_height))
            boltAnim.append((scaled_frame, ANIMATION_DELAY))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.boltAnim.blit(self.image, (0, 0))
