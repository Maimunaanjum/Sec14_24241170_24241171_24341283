from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import time

width, height = 800, 600


original_arena_radius = 10.0
arena_radius = original_arena_radius

player_size = 0.5
player_speed = 0.1
player1_pos = [-3.0, 0.0, 0.0]
player2_pos = [3.0, 0.0, 0.0]

normal_keys = {}
special_keys = {}

winner = None
last_time = time.time()
game_start_time = None
game_end_time = None
shrink_started = False

rounds_played = 0
p1_round_wins = 0
p2_round_wins = 0
round_draws   = 0
overall_winner = None

TOTAL_TIME = 30
SHRINK_START_TIME = 20
SHRINK_INTERVAL = 2
SHRINK_AMOUNT = 0.5
MIN_RADIUS = 2.0


def init():
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 1, 100)
    glMatrixMode(GL_MODELVIEW)


def draw_arena():
    glColor3f(0.9, 0.7, 0.5)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(101):
        angle = 2 * math.pi * i / 100
        x = arena_radius * math.cos(angle)
        z = arena_radius * math.sin(angle)
        glVertex3f(x, 0, z)
    glEnd()

    glColor3f(0.6, 0.4, 0.2)
    glBegin(GL_LINE_LOOP)
    for i in range(100):
        angle = 2 * math.pi * i / 100
        x = arena_radius * math.cos(angle)
        z = arena_radius * math.sin(angle)
        glVertex3f(x, 0.05, z)
    glEnd()


def draw_crowd():
    layers = 3
    people_per_layer = 30
    current_time = time.time()

    for layer in range(layers):
        radius = arena_radius + 2.0 + layer * 1.5
        for i in range(people_per_layer):
            angle = 2 * math.pi * i / people_per_layer
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)

            cheer_offset = 0.15 * math.sin(current_time * 4 + i)

            glPushMatrix()
            glTranslatef(x, cheer_offset, z)
            glRotatef(math.degrees(-angle), 0, 1, 0)

            body_height = 0.8
            body_width = 0.3
            arm_length = 0.4
            arm_thickness = 0.08

            # Body
            glColor3f(0.3 + 0.2 * (layer % 2), 0.2, 0.3)
            glPushMatrix()
            glScalef(body_width, body_height, body_width)
            glutSolidCube(1)
            glPopMatrix()

            glColor3f(1.0, 0.8, 0.6)
            glPushMatrix()
            glTranslatef(0, body_height / 2 + 0.2, 0)
            glutSolidSphere(0.2, 10, 10)
            glPopMatrix()

            wave_angle = 30 * math.sin(current_time * 5 + i)

            glColor3f(0.3 + 0.2 * (layer % 2), 0.2, 0.3)
            glPushMatrix()
            glTranslatef(-body_width / 2 - arm_thickness / 2, body_height / 2, 0)
            glRotatef(-60 + wave_angle, 0, 0, 1)
            glScalef(arm_length, arm_thickness, arm_thickness)
            glutSolidCube(1)
            glPopMatrix()

            glPushMatrix()
            glTranslatef(body_width / 2 + arm_thickness / 2, body_height / 2, 0)
            glRotatef(60 - wave_angle, 0, 0, 1)
            glScalef(arm_length, arm_thickness, arm_thickness)
            glutSolidCube(1)
            glPopMatrix()

            glPopMatrix()


def draw_stadium_walls():
    glColor3f(0.3, 0.3, 0.3)
    height = 2.5
    thickness = 1.0
    halfExt = arena_radius + 6.0

    #wall
    glPushMatrix()
    glTranslatef(0.0, height / 2, -halfExt)
    glScalef(2 * halfExt, height, thickness)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, height / 2, halfExt)
    glScalef(2 * halfExt, height, thickness)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-halfExt, height / 2, 0.0)
    glScalef(thickness, height, 2 * halfExt)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(halfExt, height / 2, 0.0)
    glScalef(thickness, height, 2 * halfExt)
    glutSolidCube(1.0)
    glPopMatrix()

def draw_player(pos, body_color, belt_color):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])

    glPushMatrix()
    glColor3f(*body_color)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluPartialDisk(quad, 0, 1.0, 30, 1, 0, 180)
    glPopMatrix()

    glPushMatrix()
    glColor3f(*body_color)
    glTranslatef(0, 0.6, 0)
    glutSolidSphere(1.0, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(*belt_color)
    glTranslatef(0, 0.5, 0)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, 1.05, 1.05, 0.25, 20, 1)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1.0, 0.8, 0.6)
    glTranslatef(0, 1.9, 0)
    glutSolidSphere(0.5, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(0.1, 2.4, 0.1)
    glRotatef(20, 0, 0, 1)
    glutSolidSphere(0.2, 10, 10)
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

    glColor3f(0, 0, 0)  
    glRasterPos2f(x, y)

    
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch)) 

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
    if normal_keys.get(b'w'): player1_pos[2] -= player_speed
    if normal_keys.get(b's'): player1_pos[2] += player_speed
    if normal_keys.get(b'a'): player1_pos[0] -= player_speed
    if normal_keys.get(b'd'): player1_pos[0] += player_speed

    if special_keys.get(GLUT_KEY_UP): player2_pos[2] -= player_speed
    if special_keys.get(GLUT_KEY_DOWN): player2_pos[2] += player_speed
    if special_keys.get(GLUT_KEY_LEFT): player2_pos[0] -= player_speed
    if special_keys.get(GLUT_KEY_RIGHT): player2_pos[0] += player_speed

def reset_round():
    global winner, game_start_time, game_end_time, arena_radius, shrink_started
    winner = None
    game_start_time = time.time()
    game_end_time = None
    arena_radius = original_arena_radius
    shrink_started = False


def reset_game():
    global player1_pos, player2_pos, winner, arena_radius, shrink_started, game_start_time, game_end_time
    player1_pos = [-3.0, 0.0, 0.0]
    player2_pos = [3.0, 0.0, 0.0]
    winner = None
    arena_radius = original_arena_radius
    shrink_started = False
    game_start_time = time.time()
    game_end_time = None


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
    
    cx = (player1_pos[0] + player2_pos[0]) / 2.0
    cz = (player1_pos[2] + player2_pos[2]) / 2.0
    cam_y = 15.0
    cam_z_offset = 20.0

    glLoadIdentity()
    glLoadIdentity()
    gluLookAt(
        cx, cam_y, cz + cam_z_offset,   
        cx, 0.0, cz,                    
        0.0, 1.0, 0.0   
    )



def idle():
    global last_time, game_start_time, game_end_time, arena_radius, shrink_started, winner

    current_time = time.time()
    delta = current_time - last_time

    if game_start_time is None:
        game_start_time = current_time

    elapsed = current_time - game_start_time

    if delta >= 1/60:
        if winner is None:     
            move_players()
            check_collision()
            check_win()

            if elapsed > SHRINK_START_TIME and not shrink_started:
                shrink_started = True

            if shrink_started:
                shrink_steps = int((elapsed - SHRINK_START_TIME) // SHRINK_INTERVAL)
                arena_radius = max(MIN_RADIUS,
                                   original_arena_radius - shrink_steps * SHRINK_AMOUNT)

            if elapsed >= TOTAL_TIME and winner is None:
                winner = "Draw"

        
        if winner is not None and game_end_time is None:
            game_end_time = current_time

        
        if elapsed >= SHRINK_START_TIME:
            glClearColor(1.0, 0.0, 0.0, 1.0)
        else:
            glClearColor(0.5, 0.7, 1.0, 1.0)

        glutPostRedisplay()
        last_time = current_time

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    set_camera()
    draw_stadium_walls()
    draw_arena()
    draw_crowd()

    draw_player(player1_pos, (1.0, 0.6, 0.6), (1, 0, 0))
    draw_player(player2_pos, (0.6, 0.6, 1.0), (0, 0, 1))

    if game_start_time:
        
        current = game_end_time if game_end_time is not None else time.time()
        elapsed = int(current - game_start_time)

        draw_text(10, height - 30, f"Time: {elapsed}s")
        if shrink_started:
            draw_text(10, height - 60, "SPEED UP!")

    if winner:
        if winner == "Draw":
            draw_text(300, 300, "Draw! Press 'R' to Restart")
        else:
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
    reset_game()
    glutMainLoop()


if __name__ == "__main__":
    main()
