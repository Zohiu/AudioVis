class Effect:
    def __init__(self):
        pass

    def start(self, screen, width, height):
        screen.fill((0, 0, 0))

    def update(self, screen, width, height, raw_aud, freq, VOL, PEAK, BASS, MID, HIGH):
        pass

    def stop(self):
        pass
