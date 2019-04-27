import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from ObjLoader import *
import sys
from mss import mss


# draw cube on screen
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


# generate random verticies for cubes
def random_vertices(vertices, distance, platform_size):
    platform_size -= 3
    x = random.randrange(-platform_size, platform_size)
    y = random.randrange(-platform_size, platform_size)
    z = random.randrange(distance[0], distance[1])

    vertices_random = []

    for vertice in vertices:
        vertices_random.append([vertice[0] + x, vertice[1] + y, vertice[2] + z])

    return vertices_random


# generate new verticies for object / used only for player ship
def generate_player_vertices(x, y, z, vertices):
    new_player_vertices = []

    for vertice in vertices:
        new_player_vertices.append([vertice[0] + x, vertice[1] + y, vertice[2] + z])

    return new_player_vertices


# generate laser verticies acording to player pos
def generate_laser_vertices(verticies, x, y, z):
    laser_verticies = []

    for verticie in verticies:
        laser_verticies.append([verticie[0] + x, verticie[1] + y, verticie[2] + z - 10])

    return laser_verticies


# generate new laser pos / z - 5 per frame
def generate_new_laser_pos(verticies, number):
    laser_verticies = []

    for verticie in verticies:
        laser_verticies.append([verticie[0], verticie[1], verticie[2] + number])

    return laser_verticies


def generate_new_enemy_laser_pos(verticies, z, pz, px, py):
    laser_verticies = []

    if verticies[7][2] <= pz:
        if verticies[7][0] <= px:
            tempx = 0.3
        elif verticies[7][0] > px:
            tempx = -0.3

        if verticies[7][1] <= py:
            tempy = 0.3
        elif verticies[7][1] > py:
            tempy = -0.3

        for verticie in verticies:
            laser_verticies.append([verticie[0] + tempx, verticie[1] + tempy, verticie[2] + z])
    else:
        for verticie in verticies:
            laser_verticies.append([verticie[0], verticie[1], verticie[2] + z])

    return laser_verticies


def text_objects(text, text_color, size):
    smallfont = pygame.font.SysFont("comicsansms", 25)
    medfont = pygame.font.SysFont("comicsansms", 50)
    largefont = pygame.font.SysFont("comicsansms", 80)

    if size == "small":
        textSurface = smallfont.render(text, True, text_color)
    elif size == "medium":
        textSurface = medfont.render(text, True, text_color)
    elif size == "large":
        textSurface = largefont.render(text, True, text_color)

    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, display_width, display_height, gameDisplay, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


# show main menu
def main():
    # INIT
    pygame.init()
    display = (800, 600)

    # start menu
    game_over_display = pygame.display.set_mode(display)
    game_over_display.fill((0, 0, 0))
    bg = pygame.image.load("background.jpg")

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_over_display.blit(bg, (0, 0))
        message_to_screen("Welcome to space adventure", (255, 0, 0), display[0], display[1], game_over_display, -180,
                          "medium")
        message_to_screen("arrows = move", (255, 0, 0), display[0], display[1], game_over_display, -120, "medium")
        message_to_screen("space = shot", (255, 0, 0), display[0], display[1], game_over_display, -60, "medium")
        message_to_screen("To start the game press space", (255, 0, 0), display[0], display[1], game_over_display, -0,
                          "small")
        pygame.display.update()

    game_start(display)


# initialize game
def game_start(display):
    # variables
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

    wall_vertices = (
        (20, -20, -1200),
        (20, 20, -1200),
        (-20, 20, -1200),
        (-20, -20, -1200),
        (20, -20, 100),
        (20, 20, 100),
        (-20, -20, 100),
        (-20, 20, 100))

    laser_vertices = (
        (0.1, -0.1, -1),
        (0.1, 0.1, -1),
        (-0.1, 0.1, -1),
        (-0.1, -0.1, -1),
        (0.1, -0.1, 1),
        (0.1, 0.1, 1),
        (-0.1, -0.1, 1),
        (-0.1, 0.1, 1))

    enemy_laser_vertices = (
        (0.6, -0.6, -1.5),
        (0.6, 0.6, -1.5),
        (-0.6, 0.6, -1.5),
        (-0.6, -0.6, -1.5),
        (0.6, -0.6, 1.5),
        (0.6, 0.6, 1.5),
        (-0.6, -0.6, 1.5),
        (-0.6, 0.6, 1.5))

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

    laser_colors = (
        (1.0, 0.0, 0.0),
        (1.0, 0.0, 0.2),
        (1.0, 0.2, 0.0),
        (1.0, 0.2, 0.2),
        (1.0, 0.3, 0.3),
        (1.0, 0.4, 0.4))

    enemy_laser_colors = (
        (0.0, 1.0, 0.0),
        (0.0, 1.0, 0.1),
        (0.1, 1.0, 0.0),
        (0.1, 1.0, 0.1),
        (0.2, 1.0, 0.2),
        (0.3, 1.0, 0.3))

    wall_color = (
        (0.0, 0.0, 1.0),
        (0.2, 0.0, 1.0),
        (0.0, 0.2, 1.0),
        (0.2, 0.2, 1.0),
        (0.3, 0.3, 1.0),
        (0.4, 0.4, 1.0)
    )

    distance = (-400, -0)
    view_distance = 150.0
    platform_size = 20
    cubes_amount = 100
    speed = 0.3
    cubes = []
    cubes_colors = []
    lasers = []
    color_position = 0
    score = 0
    game_lost = False
    victory = False
    # genarate random cubes
    for i in range(cubes_amount):
        cubes.append(random_vertices(vertices, distance, platform_size))

    # genarate random cubes colors
    for u in range((cubes_amount * 4) + 2):
        i = random.randrange(0, 6)
        cubes_colors.append(colors[i])

    enemy_ships = []
    enemy_lasers = []
    ship_amount = 50
    ship_distance = (-1000, -500)
    finnish = -1200
    for i in range(ship_amount):
        enemy_ships.append(random_vertices(vertices_2, ship_distance, platform_size))

    game_display = pygame.display.set_mode(display, OPENGL | DOUBLEBUF)
    pygame.display.set_caption('Flight')

    gluPerspective(45, (display[0] / display[1]), 0.1, view_distance)
    glTranslatef(0.0, 0.0, -100)

    x_move = 0
    y_move = 0
    glRotatef(0, 0, 0, 0)
    loop_variable = False

    obj = OBJ('simple_space_ship.obj', swapyz=True)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    ship_verticies = obj.vertices

    while not loop_variable:

        # move ahead
        glTranslatef(0, 0, speed * 6)

        # +1 score per frame
        score += 1

        # position of ship
        collision_x = obj.vertices[0][0] - 1.0
        collision_y = obj.vertices[0][1] + 0.2
        collision_z = obj.vertices[0][2] - 2.0

        # position of perspective
        position = glGetDoublev(GL_MODELVIEW_MATRIX)

        position_x = position[3][0]
        position_y = position[3][1]
        position_z = position[3][2]

        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = speed
                if event.key == pygame.K_RIGHT:
                    x_move = -speed
                if event.key == pygame.K_UP:
                    y_move = -speed
                if event.key == pygame.K_DOWN:
                    y_move = speed
                if event.key == pygame.K_SPACE:
                    lasers.append(generate_laser_vertices(laser_vertices, collision_x + 1.0, collision_y - 0.6, collision_z))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 10)
                if event.button == 5:
                    glTranslatef(0, 0, -10)

        # block ship from moving outside

        if -platform_size <= position_x + x_move * 6 <= platform_size:
            glTranslatef(x_move, 0, 0)
        else:
            x_move = 0

        if -platform_size <= position_y + y_move * 2 <= platform_size:
            glTranslatef(0, y_move, 0)
        else:
            y_move = 0

        # clear
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw wall
        cube(wall_vertices, edges, surfaces, wall_color, 0)

        # enemy ships logic
        if ship_distance[0] < position_z < ship_distance[1] + view_distance:
            # draw ships
            for vertices_array in enemy_ships:
                if position_z > vertices_array[0][2] > position_z - view_distance:
                    cube(vertices_array, edges, surfaces, cubes_colors, color_position)
                    random_chance_for_laser = random.randint(0, 5)
                    if vertices_array[7][0] <= collision_x <= vertices_array[0][0] or \
                            vertices_array[7][0] <= collision_x + 2.5 <= vertices_array[0][0]:
                        if vertices_array[7][1] >= collision_y >= vertices_array[0][1] or \
                                vertices_array[7][1] >= collision_y - 0.4 >= vertices_array[0][1]:
                            if vertices_array[7][2] >= collision_z >= vertices_array[0][2] or \
                                    vertices_array[7][2] >= collision_z - 4 >= vertices_array[0][2]:
                                print('Collide with enemy ship')
                                game_lost = True
                    if random_chance_for_laser == 1:
                        enemy_lasers.append(generate_laser_vertices(enemy_laser_vertices, vertices_array[0][0], vertices_array[0][1], vertices_array[0][2]))

            # draw enemy lasers
            temp_laser_counter = 0

            for vertices_array_laser in enemy_lasers:
                enemy_lasers[temp_laser_counter] = generate_new_enemy_laser_pos(enemy_lasers[temp_laser_counter], 3, collision_z, collision_x, collision_y)
                if position_z > vertices_array_laser[0][2] > position_z - view_distance:
                    cube(vertices_array_laser, edges, surfaces, enemy_laser_colors, 0)

                if position_z + 10 < vertices_array_laser[0][2]:
                    enemy_lasers.pop(temp_laser_counter)
                    continue
                else:
                    temp_laser_counter += 1

                collision_x_laser = vertices_array_laser[7][0]
                collision_y_laser = vertices_array_laser[7][1]
                collision_z_laser = vertices_array_laser[7][2]

                collision_x2_laser = vertices_array_laser[0][0]
                collision_y2_laser = vertices_array_laser[0][1]
                collision_z2_laser = vertices_array_laser[0][2]

                if collision_x_laser <= collision_x <= collision_x2_laser or \
                        collision_x_laser <= collision_x + 2.5 <= collision_x2_laser:
                    if collision_y_laser >= collision_y >= collision_y2_laser or \
                            collision_y_laser >= collision_y - 0.4 >= collision_y2_laser:
                        if collision_z_laser >= collision_z >= collision_z2_laser or \
                                collision_z_laser >= collision_z - 4 >= collision_z2_laser:
                            print('Shot by laser')
                            game_lost = True

        # draw lasers
        temp_laser_counter = 0

        # for every laser check collision with cube
        for vertices_array_laser in lasers:
            lasers[temp_laser_counter] = generate_new_laser_pos(vertices_array_laser, -5)
            if position_z > vertices_array_laser[0][2] > position_z - view_distance:
                cube(vertices_array_laser, edges, surfaces, laser_colors, 0)

            collision_x_laser = vertices_array_laser[0][0]
            collision_y_laser = vertices_array_laser[0][1]
            collision_z_laser = vertices_array_laser[0][2]

            cube_counter = 0
            for vertices_array in cubes:
                if position_z > vertices_array[0][2] > position_z - view_distance:
                    if vertices_array[7][0] <= collision_x_laser <= vertices_array[0][0] or \
                            vertices_array[7][0] <= collision_x_laser + 0.3 <= vertices_array[0][0]:
                        if vertices_array[7][1] >= collision_y_laser >= vertices_array[0][1] or \
                                vertices_array[7][1] >= collision_y_laser - 0.3 >= vertices_array[0][1]:
                            if vertices_array[7][2] >= collision_z_laser >= vertices_array[0][2] or \
                                    vertices_array[7][2] >= collision_z_laser - 0.3 >= vertices_array[0][2]:
                                cubes.pop(cube_counter)
                                cubes_colors.pop(cube_counter)
                                cubes_colors.pop(cube_counter + 1)
                                cubes_colors.pop(cube_counter + 2)
                                cubes_colors.pop(cube_counter + 3)
                cube_counter += 1
            cube_counter = 0
            for vertices_array in enemy_ships:
                if position_z > vertices_array[0][2] > position_z - view_distance:
                    if vertices_array[7][0] <= collision_x_laser <= vertices_array[7][0] + 8 or \
                            vertices_array[7][0] <= collision_x_laser + 0.1 <= vertices_array[7][0] + 8:
                        if vertices_array[7][1] >= collision_y_laser >= vertices_array[7][1] - 8 or \
                                vertices_array[7][1] >= collision_y_laser - 0.1 >= vertices_array[7][1] - 8:
                            if vertices_array[7][2] >= collision_z_laser >= vertices_array[7][2] - 8 or \
                                    vertices_array[7][2] >= collision_z_laser - 1 >= vertices_array[7][2] - 8:
                                enemy_ships.pop(cube_counter)
                if position_z < vertices_array[0][2]:
                    enemy_ships.pop(cube_counter)
                else:
                    cube_counter += 1
            temp_laser_counter += 1

        # update ship position
        obj.vertices = generate_player_vertices(-position_x, -position_y / 1.5, position_z - 20, ship_verticies)
        obj.update()

        glCallList(obj.gl_list)

        # draw cubes
        cube_counter = 0
        for vertices_array in cubes:
            if position_z > vertices_array[0][2] > position_z - view_distance:
                cube(vertices_array, edges, surfaces, cubes_colors, color_position)
                if vertices_array[7][0] <= collision_x <= vertices_array[0][0] or \
                        vertices_array[7][0] <= collision_x + 2.5 <= vertices_array[0][0]:
                    if vertices_array[7][1] >= collision_y >= vertices_array[0][1] or \
                            vertices_array[7][1] >= collision_y - 0.4 >= vertices_array[0][1]:
                        if vertices_array[7][2] >= collision_z >= vertices_array[0][2] or \
                                vertices_array[7][2] >= collision_z - 4 >= vertices_array[0][2]:
                            print('Inside Cube')
                            game_lost = True
            if position_z < vertices_array[0][2]:
                cubes.pop(cube_counter)
            else:
                cube_counter += 1
            color_position += 4
        color_position = 0

        if game_lost:
            pygame.image.save(game_display, "lost.jpg")
            print('Game Over')
            loop_variable = True

        if collision_z < finnish:
            game_lost = True
            victory = True

        pygame.display.flip()
        pygame.time.wait(20)

    game_over_menu(display, score, victory)


# game over menu
def game_over_menu(display, score, victory):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    game_over_display = pygame.display.set_mode(display)
    game_over_display.fill((0, 0, 0))
    bg = pygame.image.load("background.jpg")

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_over_display.blit(bg, (0, 0))
        if victory:
            message_to_screen("Victory", (255, 0, 0), display[0], display[1], game_over_display, -180, "medium")
        else:
            message_to_screen("Game over", (255, 0, 0), display[0], display[1], game_over_display, -180, "medium")
        message_to_screen("Your score: ", (255, 0, 0), display[0], display[1], game_over_display, -120, "medium")
        message_to_screen(str(score), (255, 0, 0), display[0], display[1], game_over_display, -60, "medium")
        pygame.display.update()

    game_start(display)


if __name__ == '__main__':
    main()

# todo
# 1. Points // done
# 2. Walls // done
# 3. replace cubes with asteroids // wip
# 4. Lasers // done
# 5. Scenes // done
# 6. Fix ship texture color. // no idea
# 7. Difficulty // wip
