from math import sin, cos, pi, radians, degrees
import random
import pygame
import json


class Circles:
    def __init__(self, center_of_rotation_x, center_of_rotation_y, radius, angle, omega, circles_radius, gap, rgb):
        self.center_of_rotation_x = center_of_rotation_x
        self.center_of_rotation_y = center_of_rotation_y
        self.radius = radius
        self.angle = radians(angle)
        self.omega = omega

        self.x = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle)

        self.circles_radius = circles_radius
        self.circles = []
        self.gap = gap

        self.rgb = rgb

    def update(self, screen):
        self.circles = [{"offset": -self.gap * 1.5},
                        {"offset": -self.gap / 2},
                        {"offset": self.gap / 2},
                        {"offset": self.gap * 1.5}]

        index = 0
        for circle in self.circles:
            offset_x = self.x + circle["offset"]
            pygame.draw.circle(screen, self.rgb, (offset_x, self.y), self.circles_radius)
            index += 1

        self.angle = self.angle + self.omega
        self.x = self.x + (self.radius + Effect.width / 16) * self.omega * cos(self.angle + pi / 2)
        self.y = self.y - self.radius * self.omega * sin(self.angle + pi / 2)


class Effect:
    width = 0
    height = 0

    def __init__(self):
        self.PEAK_before = False

        self.update_counter = 0

        with open("data.json", "r") as f:
            self.s = json.loads(f.read())

        self.allow_updating = False
        self.circleGroups = []

    def start(self, screen, width, height):
        Effect.width = width
        Effect.height = height

        print(width, height)

        self.circleGroups = [
            {
                "class":
                    Circles(
                        center_of_rotation_x=width / 2,
                        center_of_rotation_y=height / 3,
                        radius=height / 4,
                        angle=45,
                        omega=0.07,
                        circles_radius=width / 32,
                        gap=width / 8,
                        rgb=(0, 255, 0)
                    ),

                "starting_angle":
                    0
            },
            {
                "class":
                    Circles(
                        center_of_rotation_x=width / 2,
                        center_of_rotation_y=height / 2 + height / 6,
                        radius=height / 4,
                        angle=-45,
                        omega=-0.07,
                        circles_radius=width / 32,
                        gap=width / 8,
                        rgb=(255, 0, 0)
                    ),

                "starting_angle":
                    0
            },
            # MIRRORED
            {
                "class":
                    Circles(
                        center_of_rotation_x=width / 2,
                        center_of_rotation_y=height / 3,
                        radius=height / 4,
                        angle=135,
                        omega=-0.07,
                        circles_radius=width / 32,
                        gap=width / 8,
                        rgb=(0, 255, 0)
                    ),

                "starting_angle":
                    0
            },
            {
                "class":
                    Circles(
                        center_of_rotation_x=width / 2,
                        center_of_rotation_y=height / 2 + height / 6,
                        radius=height / 4,
                        angle=-135,
                        omega=0.07,
                        circles_radius=width / 32,
                        gap=width / 8,
                        rgb=(255, 0, 0)
                    ),

                "starting_angle":
                    0
            }
        ]

    def update(self, screen, width, height, raw_aud, freq, VOL, PEAK, BASS, MID, HIGH):
        if VOL > 150:
            PEAK = not self.PEAK_before

            for circle in self.circleGroups:
                circle["class"].rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if PEAK is not self.PEAK_before:
            self.allow_updating = True

        if MID is True:
            if self.update_counter % self.s["FPS"] / 4 == 0:
                for circle in self.circleGroups:
                    circle["class"].rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if self.allow_updating:
            screen.fill((0, 0, 0))

            for circle in self.circleGroups:
                circle["class"].update(screen)

            if int(degrees(self.circleGroups[0]["class"].angle)) % 45 == 0:
                for circle in self.circleGroups:
                    circle["class"].angle = radians(int(degrees(circle["class"].angle)))

                rand_1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                rand_2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                self.circleGroups[0]["class"].rgb = rand_1
                self.circleGroups[1]["class"].rgb = rand_2
                self.circleGroups[2]["class"].rgb = rand_1
                self.circleGroups[3]["class"].rgb = rand_2

                self.allow_updating = False

        self.PEAK_before = PEAK

        self.update_counter += 1
        if self.update_counter >= self.s["FPS"]:
            self.update_counter = 0

    def stop(self, screen, width, height):
        pass
