import json
import random

class Effect:
    def __init__(self):
        self.PEAK_before = False
        self.amount = 0

        with open("data.json", "r") as f:
            self.s = json.loads(f.read())

    def start(self, screen, width, height):
        pass

    def update(self, screen, width, height, raw_aud, freq, VOL, PEAK, BASS, MID, HIGH):

        if PEAK is not self.PEAK_before:
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        if VOL > 150:
            if random.choice([True, False]):
                screen.fill((255, 255, 255))
            else:
                screen.fill((0, 0, 0))

        self.PEAK_before = PEAK

    def stop(self):
        pass
