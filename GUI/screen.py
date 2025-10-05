# screen.py

import pygame
# Set up the window
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w-40, pygame.display.Info().current_h-40

FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

BLACK = (0,0,0)
WHITE = (255,255,255)

clock = pygame.time.Clock()

pygame.display.set_caption("3D Rigid Body Physics Simulator")

# change to body
def draw(body, camera):
    for edge in body.edges:
        vertex1 = body.vertices[edge[0]]
        vertex2 = body.vertices[edge[1]]
        x1, y1, draw1 = body.projectVertex(vertex1[0]+body.position[0],vertex1[1]+body.position[1],vertex1[2]+body.position[2], camera)
        x2, y2, draw2 = body.projectVertex(vertex2[0]+body.position[0],vertex2[1]+body.position[1],vertex2[2]+body.position[2], camera)
        if draw1 and draw2:
            pygame.draw.line(screen, BLACK, (x1,SCREEN_HEIGHT-y1), (x2,SCREEN_HEIGHT-y2), 1)
    for face in body.faces:
        vertices = []
        for vertexIndex in face:
            x, y, draw = body.projectVertex(body.vertices[vertexIndex][0]+body.position[0],body.vertices[vertexIndex][1]+body.position[1],body.vertices[vertexIndex][2]+body.position[2], camera)
            if draw:
                vertices.append((x,SCREEN_HEIGHT-y))
        try:
            pygame.draw.polygon(screen, BLACK, vertices)
        except Exception:
            pass # E.g. no vertices rendered
        
def updateScreen(bodies, camera):
    screen.fill(WHITE)
    for body in bodies:
        body.updatePosition()
        body.updateRotation()
        body.runCollisions(bodies)
        draw(body, camera)
    pygame.display.flip()
    
UPDATE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(UPDATE_EVENT, 1000//FPS)  # Runs every 1000//FPS miliseconds