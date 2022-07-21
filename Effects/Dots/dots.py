import pygame
import random


def drawCircle(screen, width, height):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    radius = random.randint(50, 100)

    temp_WIDTH = width - radius * 2
    temp_HEIGHT = height - radius * 2

    x = random.randint(-temp_WIDTH, temp_WIDTH)
    y = random.randint(-temp_HEIGHT, temp_HEIGHT)

    pygame.draw.circle(screen, (r, g, b), (x, y), radius)


class Effect:
    def __init__(self):
        self.PEAK_before = False
        self.amount = 0

    def start(self, screen, width, height):
        pass

    def update(self, screen, width, height, raw_aud, freq, VOL, PEAK, BASS, MID, HIGH):

        if PEAK is not self.PEAK_before:
            self.amount = random.randint(0, 5)
            screen.fill((0, 0, 0))

            for i in range(self.amount):
                drawCircle(screen, width, height)

        if VOL > 150:
            drawCircle(screen, width, height)

        self.PEAK_before = PEAK

    def stop(self):
        pass
