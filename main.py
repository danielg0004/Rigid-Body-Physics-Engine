# main.py

import pygame
import sys
from GUI.create import open_creation_window
from GUI.screen import FPS, UPDATE_EVENT, updateScreen, clock
from Engine.camera import Camera
from Engine.shapes import shape_map
from Engine.body import Body
import ast


camera = Camera()
bodies = []

tracking_mouse = False
last_x, last_y = 0, 0
sensitivity_x, sensitivity_y = 0.0013, 0.0013

print("MOVEMENT\n\nLeft: 'a'\nRight: 'd'\nBack: 's'\nForward: 'w'\nUp: Up arrow\nDown: Down arrow \n\nLook up: 'z'\nLook down: 'x'\nLook left: 'c'\nLook right: 'v'\nIncrease roll: 'b'\nDecrease roll: 'n'\n\nIncrease zoom: '+'\nDecrease zoom: '-'\n\nReset camera: 'r'\nCreate new body: 'm'\nDelete last added body: 'p'")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == UPDATE_EVENT:
            updateScreen(bodies, camera)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tracking_mouse = True
                last_x, last_y = event.pos 
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                tracking_mouse = False
        elif event.type == pygame.MOUSEMOTION and tracking_mouse:
            dx, dy = event.pos[0] - last_x, event.pos[1] - last_y
            last_x, last_y = event.pos
            camera.rotate(dy * sensitivity_y, dx * sensitivity_x, 0)
        elif event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key)=="r":
                camera.position = [0,0,0] # Reset camera's position
                camera.pitch, camera.yaw, camera.roll = 0,0,0 # Reset camera's rotations
                sensitivity_x, sensitivity_y = 0.0013, 0.0013 # Reset camera sensitivity
                camera.scale = 130 # Reset scale
            elif pygame.key.name(event.key)=="p":
                # Delete the lastly-added body
                try:
                    bodies.pop()
                except IndexError:
                    print("No bodies to delete.")
    keys = pygame.key.get_pressed()
    
    if  keys[pygame.K_w]:
        camera.move(0, 0, 0.1*(60/FPS))  # Move camera forward
    if keys[pygame.K_s]:
        camera.move(0, 0, -0.1*(60/FPS))  # Move camera backward
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        camera.move(-0.1*(60/FPS), 0, 0)  # Move camera left
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        camera.move(0.1*(60/FPS), 0, 0)  # Move camera right
    if keys[pygame.K_DOWN]:
        camera.move(0,-0.1*(60/FPS),0) # Move camera downward
    if keys[pygame.K_UP]:
        camera.move(0,0.1*(60/FPS),0) # Move camera upward
    if keys[pygame.K_z]:
        camera.rotate(0.05*(60/FPS),0,0)
    if keys[pygame.K_x]:
        camera.rotate(-0.05*(60/FPS),0,0)
    if keys[pygame.K_c]:
        camera.rotate(0,0.05*(60/FPS),0)
    if keys[pygame.K_v]:
        camera.rotate(0,-0.05*(60/FPS),0)
    if keys[pygame.K_b]:
        camera.rotate(0,0,0.05*(60/FPS))
    if keys[pygame.K_n]:
        camera.rotate(0,0,-0.05*(60/FPS))
    if keys[pygame.K_PLUS]:
        camera.scale*=1.01
        sensitivity_x/=1.01
        sensitivity_y/=1.01
    if keys[pygame.K_MINUS]:
        camera.scale/=1.01
        sensitivity_x*=1.01
        sensitivity_y*=1.01
    if keys[pygame.K_m]:
        values = open_creation_window()
        if "Vertices" in values:
            vertices = ast.literal_eval("["+values["Vertices"]+"]")
            edges = ast.literal_eval("["+values["Edges"]+"]")
            if vertices==[] or edges==[]:
                print("No body created.")
        elif "Shape" in values:
            vertices, edges, faces = shape_map[values["Shape"]]
        else:
            # "Done" button wasn't pressed
            continue
        try:
            new_body = Body(vertices=vertices, edges=edges, faces=faces, position=values["Position"], angular_velocity=values["Angular Velocity"], angular_acceleration=values["Angular Acceleration"], translational_acceleration=values["Translational Acceleration"], translational_velocity=values["Translational Velocity"])
            bodies.append(new_body)
        except Exception:
            pass
        
    clock.tick(FPS)  # FPS cap

pygame.quit()
sys.exit()