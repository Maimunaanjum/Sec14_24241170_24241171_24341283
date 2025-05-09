from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import time


# Window dimensions
width, height = 800, 600

# Arena settings
arena_radius = 10.0

# Player settings
player_size = 0.5
player_speed = 0.1
player1_pos = [-3.0, 0.0, 0.0]
player2_pos = [3.0, 0.0, 0.0]

# Key states
normal_keys = {}
special_keys = {}

# Game state
winner = None

last_time = time.time()


def init():
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 1, 100)
    glMatrixMode(GL_MODELVIEW)

def draw_arena():
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    for i in range(100):
        angle = 2 * math.pi * i / 100
        x = arena_radius * math.cos(angle)
        z = arena_radius * math.sin(angle)
        glVertex3f(x, 0, z)
    glEnd()

def draw_crowd():
    glColor3f(0.2, 0.2, 0.2)
    radius = arena_radius + 1.5
    for i in range(50):
        angle = 2 * math.pi * i / 50
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        glPushMatrix()
        glTranslatef(x, 0, z)
        glutSolidSphere(0.3, 10, 10)
        glPopMatrix()

def draw_player(pos, body_color, belt_color):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])

    # Draw body (lower half sphere)
    glPushMatrix()
    glColor3f(*body_color)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluPartialDisk(quad, 0, 1.0, 30, 1, 0, 180)  # lower hemisphere-like
    glPopMatrix()

    # Draw upper body (sphere)
    glPushMatrix()
    glColor3f(*body_color)
    glTranslatef(0, 0.6, 0)
    glutSolidSphere(1.0, 20, 20)
    glPopMatrix()

    # Draw belt
    glPushMatrix()
    glColor3f(*belt_color)
    glTranslatef(0, 0.5, 0)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, 1.05, 1.05, 0.25, 20, 1)  # Thicker belt
    glPopMatrix()

    # Draw head
    glPushMatrix()
    glColor3f(1.0, 0.8, 0.6)  # skin color
    glTranslatef(0, 1.9, 0)
    glutSolidSphere(0.5, 20, 20)
    glPopMatrix()

    # Draw hair (tilted sphere)
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)  # hair color
    glTranslatef(0.1, 2.4, 0.1)
    glRotatef(20, 0, 0, 1)
    glutSolidSphere(0.2, 10, 10)  # Small sphere for hair
    glPopMatrix()

    glPopMatrix()



def draw_text(x, y, text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1, 0, 0)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[2] - p2[2]) ** 2)

def check_collision():
    dist = distance(player1_pos, player2_pos)
    if dist < player_size * 2:
        dx = player1_pos[0] - player2_pos[0]
        dz = player1_pos[2] - player2_pos[2]
        length = math.sqrt(dx ** 2 + dz ** 2)
        if length == 0:
            dx, dz = 1, 0
            length = 1
        dx /= length
        dz /= length
        overlap = (player_size * 2 - dist) / 2 + 0.02
        player1_pos[0] += dx * overlap
        player1_pos[2] += dz * overlap
        player2_pos[0] -= dx * overlap
        player2_pos[2] -= dz * overlap

def check_win():
    global winner
    d1 = math.sqrt(player1_pos[0] ** 2 + player1_pos[2] ** 2)
    d2 = math.sqrt(player2_pos[0] ** 2 + player2_pos[2] ** 2)
    if d1 > arena_radius:
        winner = "Player 2"
    elif d2 > arena_radius:
        winner = "Player 1"

def move_players():
    # Player 1 (WASD)
    if normal_keys.get(b'w'): player1_pos[2] -= player_speed
    if normal_keys.get(b's'): player1_pos[2] += player_speed
    if normal_keys.get(b'a'): player1_pos[0] -= player_speed
    if normal_keys.get(b'd'): player1_pos[0] += player_speed

    # Player 2 (Arrow Keys)
    if special_keys.get(GLUT_KEY_UP): player2_pos[2] -= player_speed
    if special_keys.get(GLUT_KEY_DOWN): player2_pos[2] += player_speed
    if special_keys.get(GLUT_KEY_LEFT): player2_pos[0] -= player_speed
    if special_keys.get(GLUT_KEY_RIGHT): player2_pos[0] += player_speed

def reset_game():
    global player1_pos, player2_pos, winner
    player1_pos = [-3.0, 0.0, 0.0]
    player2_pos = [3.0, 0.0, 0.0]
    winner = None



def keyboard(key, x, y):
    global winner
    if key == b'r' and winner:
        reset_game()
    normal_keys[key] = True

def keyboard_up(key, x, y):
    normal_keys[key] = False

def special_key_down(key, x, y):
    special_keys[key] = True

def special_key_up(key, x, y):
    special_keys[key] = False

def set_camera():
    glLoadIdentity()
    gluLookAt(0, 20, 20, 0, 0, 0, 0, 1, 0)

def idle():
    global last_time
    current_time = time.time()
    delta = current_time - last_time

    if delta >= 1 / 60:  # Limit to ~60 FPS
        if not winner:
            move_players()
            check_collision()
            check_win()
        glutPostRedisplay()
        last_time = current_time



def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    set_camera()
    
    draw_arena()
    draw_crowd()
    #draw_player(player1_pos, (1, 0, 0))  # Red
    #draw_player(player2_pos, (0, 0, 1))  # Blue
    
    draw_player(player1_pos, (1.0, 0.6, 0.6), (1, 0, 0))  # red belt
    draw_player(player2_pos, (0.6, 0.6, 1.0), (0, 0, 1))  # blue belt



    if winner:
        draw_text(300, 300, f"{winner} Wins! Press 'R' to Restart")

    glutSwapBuffers()




def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"3D Sumo Game")
    init()
    glutDisplayFunc(show_screen)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutSpecialFunc(special_key_down)
    glutSpecialUpFunc(special_key_up)
    
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
