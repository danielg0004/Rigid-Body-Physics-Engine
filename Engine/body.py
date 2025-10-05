# body.py

import math
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w-40, pygame.display.Info().current_h-40

# Main class - instances represent a single rigid body in 3D space
class Body:
    def __init__(self, vertices, edges, faces=[], position=[0,0,0], angular_velocity=[0,0,0], translational_velocity=[0,0,0], angular_acceleration=[0,0,0], translational_acceleration=[0,0,0], mass=1):
        # Definition of the shape
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        
        # Current position
        self.position = position
        
        # Kinematics and rotational mechanics
        self.angular_velocity = angular_velocity
        self.translational_velocity = translational_velocity
        
        self.angular_acceleration = angular_acceleration
        self.translational_acceleration = translational_acceleration
        
        self.mass = mass # For collisions
        
        ####
        self.moment_of_inertia = [1,1,1]
        self.farthest_dist_from_center = self.maxDistFromCenter()
        self.AABB = self.getAABB()
    def getAABB(self):
        min_x = float("inf")
        min_y = float("inf")
        min_z = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")
        max_z = float("-inf")
        for vertex in self.vertices:
            if vertex[0]>max_x:
                max_x = vertex[0]
            if vertex[1]>max_y:
                max_y = vertex[1]
            if vertex[2]>max_z:
                max_z = vertex[2]
            if vertex[0]<min_x:
                min_x = vertex[0]
            if vertex[1]<min_y:
                min_y = vertex[1]
            if vertex[2]<min_z:
                min_z = vertex[2]
        AABB = [(min_x,min_y,min_z),(max_x,max_y,max_z)]
        return AABB
    def updateRotation(self):
        self.angular_velocity = [self.angular_velocity[0]+self.angular_acceleration[0],self.angular_velocity[1]+self.angular_acceleration[1],self.angular_velocity[2]+self.angular_acceleration[2]]
        self.vertices = [self.rotateVertex(vertex[0],vertex[1],vertex[2],self.angular_velocity[0],self.angular_velocity[1],self.angular_velocity[2]) for vertex in self.vertices]
    def updatePosition(self):
        self.translational_velocity = [self.translational_velocity[0]+self.translational_acceleration[0],self.translational_velocity[1]+self.translational_acceleration[1],self.translational_velocity[2]+self.translational_acceleration[2]]
        self.position = [self.position[0]+self.translational_velocity[0],self.position[1]+self.translational_velocity[1],self.position[2]+self.translational_velocity[2]]
    @staticmethod
    def rotateVertex(x, y, z, angle_x, angle_y, angle_z):
        # z axis
        cosz, sinz = math.cos(angle_z), math.sin(angle_z)
        x_rot = x * cosz - y * sinz
        y_rot = y * cosz + x * sinz

        # y axis
        cosy, siny = math.cos(angle_y), math.sin(angle_y)
        x_rot2 = x_rot * cosy - z * siny
        z_rot = z * cosy + x_rot * siny

        # x axis
        cosx, sinx = math.cos(angle_x), math.sin(angle_x)
        y_rot2 = y_rot * cosx - z_rot * sinx
        z_rot = z_rot * cosx + y_rot * sinx
        # 8 decimals of precision
        return (round(x_rot2, 8), round(y_rot2, 8), round(z_rot, 8))
    @staticmethod
    def projectVertex(x,y,z,camera):
        x_relative = x-camera.position[0]
        y_relative = y-camera.position[1]
        z_relative = z-camera.position[2]
        
        x_relative, y_relative, z_relative = Body.rotateVertex(x_relative, y_relative, z_relative, camera.pitch, -camera.yaw, -camera.roll)

        if z_relative<=0:
            return 0, 0, False

        x_projected = camera.scale*(x_relative*camera.focal_length)/(z_relative)
        y_projected = camera.scale*(y_relative*camera.focal_length)/(z_relative)
        
        return x_projected + SCREEN_WIDTH/2, y_projected + SCREEN_HEIGHT/2, True
    def applyImpulse(self, Jx, Jy, Jz, coords):
        # Update translational velocity
        self.translational_velocity[0] += Jx / self.mass
        self.translational_velocity[1] += Jy / self.mass
        self.translational_velocity[2] += Jz / self.mass
        # Calculate torque as the cross product of coords and force
        torquex = coords[1]*Jz - coords[2]*Jy
        torquey = coords[2]*Jx - coords[0]*Jz
        torquez = coords[0]*Jy - coords[1]*Jx
        # Update angular velocity
        self.angular_velocity[0] += torquex / self.moment_of_inertia[0]
        self.angular_velocity[1] += torquey / self.moment_of_inertia[1]
        self.angular_velocity[2] += torquez / self.moment_of_inertia[2]
    def deepCollisions(self, other):
        midpoint = [(self.position[i]+other.position[i])/2 for i in range(3)]
        attack_point_self = [midpoint[i]-self.position[i] for i in range(3)]
        attack_point_other = [midpoint[i]-other.position[i] for i in range(3)]
        
        min_self, max_self = self.AABB
        min_other, max_other = other.AABB
        
        min_self = [min_self[i] + self.position[i] for i in range(3)]
        max_self = [max_self[i] + self.position[i] for i in range(3)]
        min_other = [min_other[i] + other.position[i] for i in range(3)]
        max_other = [max_other[i] + other.position[i] for i in range(3)]
        
        # X-axis collision
        if max_self[0] >= min_other[0] and min_self[0] <= max_other[0] and not (max_self[1] <= min_other[1]):
            v_rel_x = other.translational_velocity[0] - self.translational_velocity[0]
            Jx = -(1 + 1) * v_rel_x / (1/self.mass + 1/other.mass)  # e=1 for perfectly elastic
            self.applyImpulse(-Jx, 0, 0, attack_point_self)
            other.applyImpulse(Jx, 0, 0, attack_point_other)
        
        # Y-axis collision
        if max_self[1] >= min_other[1] and min_self[1] <= max_other[1]:
            v_rel_y = other.translational_velocity[1] - self.translational_velocity[1]
            Jy = -(1 + 1) * v_rel_y / (1/self.mass + 1/other.mass)
            self.applyImpulse(0, -Jy, 0, attack_point_self)
            other.applyImpulse(0, Jy, 0, attack_point_other)
        
        # Z-axis collision
        if max_self[2] >= min_other[2] and min_self[2] <= max_other[2] and not (max_self[1] <= min_other[1]):
            v_rel_z = other.translational_velocity[2] - self.translational_velocity[2]
            Jz = -(1 + 1) * v_rel_z / (1/self.mass + 1/other.mass)
            self.applyImpulse(0, 0, -Jz, attack_point_self)
            other.applyImpulse(0, 0, Jz, attack_point_other)


    def runCollisions(self, bodies):
        for body in bodies:
            if body==self:
                continue
            min_dist = body.farthest_dist_from_center + self.farthest_dist_from_center
            actual_dist = math.sqrt(abs(body.position[0]-self.position[0])**2+abs(body.position[1]-self.position[1])**2+abs(body.position[2]-self.position[2])**2)
            if actual_dist <= min_dist:
                Body.deepCollisions(self, body)
                #esto te dice si colisionan o pueden colisionar pero no es seguro y no sabes donde
    def maxDistFromCenter(self):
        maxDist = 0
        for vertex in self.vertices:
            distance = math.sqrt(vertex[0]**2+vertex[1]**2+vertex[2]**2)
            if distance>maxDist:
                maxDist = distance
        return maxDist
