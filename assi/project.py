from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math

# Window size
width, height = 800, 600

# Arena
arena_radius = 10.0

# Player properties
player_size = 0.5
player1_pos = [-3.0, 0.0, 0.0]
player2_pos = [3.0, 0.0, 0.0]
player_speed = 0.1

# Movement state
normal_keys_pressed = {}
special_keys_pressed = {}

def init():
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 1, 50)
    glMatrixMode(GL_MODELVIEW)

def draw_circle(radius, segments=50):
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        glVertex3f(x, 0, z)
    glEnd()

def draw_player(position, color):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glColor3fv(color)
    glutSolidSphere(player_size, 20, 20)
    glPopMatrix()

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * 2 + (p1[2] - p2[2]) * 2)

def check_push():
    dist = distance(player1_pos, player2_pos)
    if dist < player_size * 2:
        dx = player1_pos[0] - player2_pos[0]
        dz = player1_pos[2] - player2_pos[2]
        length = math.sqrt(dx * dx + dz * dz)
        if length == 0:
            return
        push_strength = 0.05
        dx /= length
        dz /= length
        player1_pos[0] += dx * push_strength
        player1_pos[2] += dz * push_strength
        player2_pos[0] -= dx * push_strength
        player2_pos[2] -= dz * push_strength

def check_win():
    d1 = math.sqrt(player1_pos[0] * 2 + player1_pos[2] * 2)
    d2 = math.sqrt(player2_pos[0] * 2 + player2_pos[2] * 2)
    if d1 > arena_radius:
        print("Player 2 Wins!")
        sys.exit()
    if d2 > arena_radius:
        print("Player 1 Wins!")
        sys.exit()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 15, 15, 0, 0, 0, 0, 1, 0)

    glColor3f(1, 1, 1)
    draw_circle(arena_radius)

    draw_player(player1_pos, (1, 0, 0))
    draw_player(player2_pos, (0, 0, 1))

    glutSwapBuffers()

def update(value):
    move_players()
    check_push()
    check_win()
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def move_players():
    # Player 1 - WASD
    if normal_keys_pressed.get(b'w', False):
        player1_pos[2] -= player_speed
    if normal_keys_pressed.get(b's', False):
        player1_pos[2] += player_speed
    if normal_keys_pressed.get(b'a', False):
        player1_pos[0] -= player_speed
    if normal_keys_pressed.get(b'd', False):
        player1_pos[0] += player_speed

    # Player 2 - Arrow Keys
    if special_keys_pressed.get(GLUT_KEY_UP, False):
        player2_pos[2] -= player_speed
    if special_keys_pressed.get(GLUT_KEY_DOWN, False):
        player2_pos[2] += player_speed
    if special_keys_pressed.get(GLUT_KEY_LEFT, False):
        player2_pos[0] -= player_speed
    if special_keys_pressed.get(GLUT_KEY_RIGHT, False):
        player2_pos[0] += player_speed

def key_down(key, x, y):
    normal_keys_pressed[key] = True

def key_up(key, x, y):
    normal_keys_pressed[key] = False

def special_down(key, x, y):
    special_keys_pressed[key] = True

def special_up(key, x, y):
    special_keys_pressed[key] = False

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"3D Sumo Game")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(key_down)
    glutKeyboardUpFunc(key_up)
    glutSpecialFunc(special_down)
    glutSpecialUpFunc(special_up)
    glutTimerFunc(16, update, 0)
    glutMainLoop()

if __name__ == "_main_":
    main()