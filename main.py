import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random

from ObjLoader import *
import sys
from mss import mss

def cube(vertices, edges, surfaces, colors, color_position):
    glBegin(GL_QUADS)

    for surface in surfaces:
        for vertex in surface:
            glColor3fv(colors[color_position])
            glVertex3fv(vertices[vertex])
        color_position += 1
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def random_vertices(vertices, distance, platform_size):
    x = random.randrange(-platform_size, platform_size)
    y = random.randrange(-platform_size, platform_size)
    z = random.randrange(distance, 0)

    vertices_random = []

    for vertice in vertices:
        vertices_random.append([vertice[0] + x, vertice[1] + y, vertice[2] + z])

    return vertices_random


def generate_player_vertices(x, y, z, vertices):
    new_player_vertices = []

    for vertice in vertices:
        new_player_vertices.append([vertice[0] + x, vertice[1] + y, vertice[2] + z])

    return new_player_vertices


def main():
    vertices_1 = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1))

    vertices_2 = (
        (2, -2, -2),
        (2, 2, -2),
        (-2, 2, -2),
        (-2, -2, -2),
        (2, -2, 2),
        (2, 2, 2),
        (-2, -2, 2),
        (-2, 2, 2))

    vertices = (
        (4, -4, -4),
        (4, 4, -4),
        (-4, 4, -4),
        (-4, -4, -4),
        (4, -4, 4),
        (4, 4, 4),
        (-4, -4, 4),
        (-4, 4, 4))

    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7))

    surfaces = (
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6))

    colors = (
        (0.5, 0.0, 0.0),
        (0.0, 0.5, 0.0),
        (0.0, 0.0, 0.5),
        (0.5, 0.5, 0.0),
        (0.0, 0.5, 0.5),
        (0.5, 0.0, 0.5))

    distance = -1000
    view_distance = 150.0
    platform_size = 20
    cubes_amount = 100
    speed = 0.5
    cubes = []
    cubes_colors = []

    color_position = 0
    for i in range(cubes_amount):
        cubes.append(random_vertices(vertices, distance, platform_size))

    for u in range((cubes_amount * 4) + 2):
        i = random.randrange(0, 6)
        cubes_colors.append(colors[i])

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, OPENGL | DOUBLEBUF)

    gluPerspective(45, (display[0] / display[1]), 0.1, view_distance)
    glTranslatef(0.0, 0.0, -40)

    x_move = 0
    y_move = 0
    color_i = 0
    glRotatef(0, 0, 0, 0)
    loop_variable = False

    obj = OBJ('simple_space_ship.obj', swapyz=True)

    #glMatrixMode(GL_PROJECTION)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    ship_verticies = obj.vertices
    we = 0
    wr = 0

    while not loop_variable:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = speed
                    we += 1
                if event.key == pygame.K_RIGHT:
                    x_move = -speed
                    we -= 1
                if event.key == pygame.K_UP:
                    y_move = -speed
                    wr -= 1
                if event.key == pygame.K_DOWN:
                    y_move = speed
                    wr += 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1)
                if event.button == 5:
                    glTranslatef(0, 0, -1)

        position = glGetDoublev(GL_MODELVIEW_MATRIX)

        position_x = position[3][0]
        position_y = position[3][1]
        position_z = position[3][2]

        if -platform_size <= position_x + x_move <= platform_size:
            glTranslatef(x_move, 0, 0)
        else:
            x_move = 0

        if -platform_size <= position_y + y_move * 2 <= platform_size:
            glTranslatef(0, y_move, 0)
        else:
            y_move = 0

        glTranslatef(0, 0, speed * 3)

        collision_x = obj.vertices[0][0]
        collision_y = obj.vertices[0][1]
        collision_z = obj.vertices[0][2]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for vertices_array in cubes:
            if position_z > vertices_array[0][2] > position_z - view_distance:
                cube(vertices_array, edges, surfaces, cubes_colors, color_position)
                if vertices_array[7][0] <= collision_x <= vertices_array[7][0] + 8 or vertices_array[7][0] <= collision_x + 1 <= vertices_array[7][0] + 8:
                    if vertices_array[7][1] >= collision_y >= vertices_array[7][1] - 8 or vertices_array[7][1] >= collision_y - 1 >= vertices_array[7][1] - 8:
                        if vertices_array[7][2] >= collision_z >= vertices_array[7][2] - 8 or vertices_array[7][2] >= collision_z - 1 >= vertices_array[7][2] - 8:
                            with mss() as sct:
                                sct.shot()
                            print('Inside Cube')
                            print(str(vertices_array[7][0]) + ' ' + str(collision_x))
                            print(str(vertices_array[7][1]) + ' ' + str(collision_y))
                            print(str(vertices_array[7][2]) + ' ' + str(collision_z))
                            print('Game Over')
                            loop_variable = True
            color_position += 4
        color_position = 0

        obj.vertices = generate_player_vertices(-position_x, -position_y / 1.5, position_z - 20, ship_verticies)
        obj.update()

        glCallList(obj.gl_list)

        pygame.display.flip()
        pygame.time.wait(20)


if __name__ == '__main__':
    main()

# todo
# 1. Fix ship texture color.
# 2. Points
# 3. Walls
# 4. replace cubes with asteroids?
# 5. Lasers
