from src import utility
from src import effectmanager
import pygame
import json


class EffectWindow:
    utility.mprint("EffectWindow class is being loaded.")
    pygame.init()

    info = pygame.display.Info()
    WIDTH = 1280
    HEIGHT = 720
    wn = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    FULLSCREEN = False

    with open("data.json", "r") as f:
        s = json.loads(f.read())

    pygame.display.set_caption(s["AppName"] + " | Visualizer")

    wn_clock = pygame.time.Clock()
    fps = s["FPS"]

    @staticmethod
    def updateWindow():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.VIDEORESIZE:
                EffectWindow.wn = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                EffectWindow.WIDTH = event.w
                EffectWindow.HEIGHT = event.h
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    EffectWindow.FULLSCREEN = not EffectWindow.FULLSCREEN

                    if EffectWindow.FULLSCREEN:
                        EffectWindow.wn = pygame.display.set_mode((EffectWindow.WIDTH, EffectWindow.HEIGHT), pygame.FULLSCREEN)
                        info = pygame.display.Info()
                        EffectWindow.WIDTH = info.current_w
                        EffectWindow.HEIGHT = info.current_h
                    else:
                        EffectWindow.wn = pygame.display.set_mode((EffectWindow.WIDTH, EffectWindow.HEIGHT), pygame.RESIZABLE)
                elif event.key == pygame.K_r:
                    current = effectmanager.EffectManager.current_effect["name"]
                    utility.mprint("Restarting effect " + '"' + current + '"')
                    effectmanager.EffectManager.stopEffect()
                    effectmanager.EffectManager.startEffect(current)
                    effectmanager.EffectManager.loopEffect(EffectWindow.wn)

        if effectmanager.EffectManager.current_effect is not None:
            effectmanager.EffectManager.loopEffect(EffectWindow.wn)

        pygame.display.update()
        EffectWindow.wn_clock.tick(EffectWindow.fps)
