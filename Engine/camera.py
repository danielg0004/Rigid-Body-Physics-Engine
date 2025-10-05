# camera.py

import math
class Camera:
    def __init__(self, position=[0,0,0], focal_length=5, scale=130, pitch=0, yaw=0, roll=0):
        self.position = position
        self.focal_length = focal_length
        self.scale = scale #
        self.pitch = pitch # x-axis rotation (up/down)
        self.yaw = yaw # y-axis rotation (left/right)
        self.roll = roll # z-axis rotation
    def move(self, dx, dy, dz):
        self.position[0] += dz*-math.sin(self.yaw) + dx*math.cos(self.yaw)
        self.position[1] += dy
        self.position[2] += dz*math.cos(self.yaw) + dx*math.sin(self.yaw)

    def rotate(self, d_pitch, d_yaw, d_roll):
        self.pitch += d_pitch
        self.yaw += d_yaw
        self.roll += d_roll