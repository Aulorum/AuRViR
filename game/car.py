import numpy as np


class Car:

    def __init__(self, acceleration=3, max_velocity=10):
        self.position = 0
        self.velocity = 0
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.marker = 0

    def setPosition(self, position):
        self.position = position

    def getPosition(self):
        return self.position

    def setVelocity(self, velocity):
        self.velocity = velocity

    def getVelocity(self):
        return self.velocity

    def step(self, accelerate):
        if accelerate:
            if self.velocity < self.max_velocity:
                self.velocity += self.acceleration
        else:
            if self.velocity > 0:
                self.velocity -= self.acceleration
        self.position += self.velocity