from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Camera-related variables
camera_pos = (0, 500, 500)
camera_angle = 0  
camera_height = 500
camera_mode = 'third'  

# Game state variables
player_pos = [0, 0, 30]  
player_angle = 0  
life = 5  # Player life
score = 0  # Game score
bullets_missed = 0  # Missed bullets
game_over = False
cheat_mode = False
cheat_vision = False

# Grid and game constants
GRID_LENGTH = 600
GRID_SIZE = 50  # Size of each grid square
fovY = 120

# Bullet and enemy data
bullets = []  # List of [x, y, z, angle]
enemies = []  # List of [x, y, z, scale_factor]
ENEMY_COUNT = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2
last_time = time.time()


def init_game():
    """Initialize or reset game state."""
    global player_pos, player_angle, life, score, bullets_missed, game_over, bullets, enemies, cheat_mode, cheat_vision, camera_mode, camera_pos, camera_height, camera_angle
    player_pos = [0, 0, 30]
    player_angle = 0
    life = 5
    score = 0
    bullets_missed = 0
    game_over = False
    cheat_mode = False
    cheat_vision = False
    camera_mode = 'third'
    camera_pos = (0, 500, 500)
    camera_height = 500
    camera_angle = 0
    bullets = []
    enemies = []
    
    for _ in range(ENEMY_COUNT):
        spawn_enemy()


def spawn_enemy():
    """Spawn an enemy at a random position on the grid."""
    while True:
        x = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        y = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        
        if math.hypot(x - player_pos[0], y - player_pos[1]) > 100:
            enemies.append([x, y, 30, 1.0])  # [x, y, z, scale_factor]
            break


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_player():
    """Draw the player rotated to face 90° around Y-axis, standing upright on the floor."""
    glPushMatrix()

    # Move to player's position
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])

    # 🔄 Rotate player 90 degrees around Y-axis (still standing upright)
    glRotatef(90, 1, 0, 0)

    # Optional: player lies down when game over
    if game_over:
        glRotatef(90, 0, 0, 1)

    # Head
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(0, 25, 0)
    gluSphere(gluNewQuadric(), 8, 16, 16)
    glPopMatrix()

    # Torso
    glPushMatrix()
    glColor3f(0, 0.5, 0)
    glScalef(1.5, 2.5, 1)
    glutSolidCube(15)
    glPopMatrix()

    # Left Arm
    glPushMatrix()
    glTranslatef(-12, 15, 0)
    glColor3f(1, 0.8, 0.6)
    glRotatef(90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 2.5, 2.5, 12, 12, 12)
    glTranslatef(0, 0, 12)
    gluSphere(gluNewQuadric(), 3.5, 12, 12)
    glPopMatrix()

    # Right Arm
    glPushMatrix()
    glTranslatef(12, 15, 0)
    glColor3f(1, 0.8, 0.6)
    glRotatef(-90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 2.5, 2.5, 12, 12, 12)
    glTranslatef(0, 0, 12)
    gluSphere(gluNewQuadric(), 3.5, 12, 12)
    glPopMatrix()

    # gun
    glPushMatrix()
    glTranslatef(0, 15, 0)
    glColor3f(0, 1, 0.6)
    glRotatef(-90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 2.5, 2.5, 12, 12, 12)
    glTranslatef(0, 0, 12)
    gluSphere(gluNewQuadric(), 3.5, 12, 12)
    glPopMatrix()

    # Left Leg
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(-5, -20, 0)
    glScalef(0.7, 2, 0.7)
    glutSolidCube(10)
    glPopMatrix()

    # Right Leg
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(5, -20, 0)
    glScalef(0.7, 2, 0.7)
    glutSolidCube(10)
    glPopMatrix()

    glPopMatrix()


def draw_enemy(x, y, z, scale):
    """Draw an enemy flipped upside down with a black head and red body."""
    glPushMatrix()
    glTranslatef(x, y, z)

    
    glRotatef(90, 1, 1, 1)

    
    glScalef(scale, scale, scale)

    # Draw body 
    glColor3f(1, 0, 0) 
    glPushMatrix()
    glTranslatef(0, 0, 0)
    gluSphere(gluNewQuadric(), 12, 16, 16)
    glPopMatrix()

    # Draw head 
    glColor3f(0, 0, 0)  # Black
    glPushMatrix()
    glTranslatef(0, 18, 0)
    gluSphere(gluNewQuadric(), 10, 16, 16)
    glPopMatrix()

    glPopMatrix()


def draw_grid():
    
    # Draw grid floor
    glBegin(GL_QUADS)
    for x in range(-GRID_LENGTH, GRID_LENGTH, GRID_SIZE):
        for y in range(-GRID_LENGTH, GRID_LENGTH, GRID_SIZE):
            if (x // GRID_SIZE + y // GRID_SIZE) % 2 == 0:
                glColor3f(1, 1, 1)  # White
            else:
                glColor3f(0.7, 0.5, 0.95)  # Purple-ish
            glVertex3f(x, y, 0)
            glVertex3f(x + GRID_SIZE, y, 0)
            glVertex3f(x + GRID_SIZE, y + GRID_SIZE, 0)
            glVertex3f(x, y + GRID_SIZE, 0)
    glEnd()

    # Wall height
    height = 80

    glBegin(GL_QUADS)

    
    glColor3f(0.56, 0.93, 0.56)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, height)

    
    glColor3f(0, 0, 0.5)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, height)

    
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, height)

    
    glColor3f(0.53, 0.81, 0.98)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, height)
    glVertex3
        rad = math.radians(camera_anglef(GRID_LENGTH, -GRID_LENGTH, height)

    glEnd()


def draw_bullet(x, y, z):
    
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0, 0, 0)  # black
    glutSolidCube(5)
    glPopMatrix()


def keyboardListener(key, x, y):
    
    global player_pos, player_angle, cheat_mode, cheat_vision, game_over

    if game_over:
        if key == b'r':
            init_game()
        return

    rad = math.radians(player_angle)

    if key == b's':  # Move backward
        new_x = player_pos[0] + 5 * math.sin(rad)
        new_y = player_pos[1] + 5 * math.cos(rad)
        if -GRID_LENGTH + 30 < new_x < GRID_LENGTH - 30 and -GRID_LENGTH + 30 < new_y < GRID_LENGTH - 30:
            player_pos[0] = new_x
            player_pos[1] = new_y

    elif key == b'w':  # Move forward
        new_x = player_pos[0] - 5 * math.sin(rad)
        new_y = player_pos[1] - 5 * math.cos(rad)
        if -GRID_LENGTH + 30 < new_x < GRID_LENGTH - 30 and -GRID_LENGTH + 30 < new_y < GRID_LENGTH - 30:
            player_pos[0] = new_x
            player_pos[1] = new_y

    elif key == b'a':  
        player_angle = (player_angle + 5) % 360

    elif key == b'd':  
        player_angle = (player_angle - 5) % 360

    elif key == b'c':  
        cheat_mode = not cheat_mode

    elif key == b'v':  
        cheat_vision = not cheat_vision

    elif key == b'r':  
        init_game()





def mouseListener(button, state, x, y):
    """Handle mouse inputs."""
    global camera_mode
    if game_over:
        return

   
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        rad = math.radians(player_angle)
        
        bx = player_pos[0] + 20 * math.sin(rad)
        by = player_pos[1] + 20 * math.cos(rad)
        bz = player_pos[2]
        bullets.append([bx, by, bz, player_angle])

    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = 'first' if camera_mode == 'third' else 'third'


def setupCamera():
    """Configure the camera's projection and view settings."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == 'third':
        )
        cx = 500 * math.sin(rad)
        cy = 500 * math.cos(rad)
        cz = camera_height
        gluLookAt(cx, cy, cz, 0, 0, 0, 0, 0, 1)
    else:
        
        rad = math.radians(player_angle)
        cx = player_pos[0] - 50 * math.sin(rad) 
        cy = player_pos[1] - 50 * math.cos(rad)
        cz = player_pos[2] + 20  
        tx = player_pos[0] + 100 * math.sin(rad)  
        ty = player_pos[1] + 100 * math.cos(rad)
        tz = player_pos[2]
        gluLookAt(cx, cy, cz, tx, ty, tz, 0, 0, 1)


def update_game():
    """Update game state: bullets, enemies, collisions."""
    global bullets, enemies, life, bullets_missed, game_over, score, last_time
    if game_over:
        return

    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time


    new_bullets = []
    for bullet in bullets:
        bx, by, bz, angle = bullet
        rad = math.radians(angle)
        bx += BULLET_SPEED * math.sin(rad) * dt * 60
        by += BULLET_SPEED * math.cos(rad) * dt * 60
        
        if -GRID_LENGTH < bx < GRID_LENGTH and -GRID_LENGTH < by < GRID_LENGTH:
            new_bullets.append([bx, by, bz, angle])
        else:
            bullets_missed += 1
            if bullets_missed >= 10:
                game_over = True
    bullets = new_bullets

    
    for enemy in enemies:
        ex, ey, ez, scale = enemy
        
        dx = player_pos[0] - ex
        dy = player_pos[1] - ey
        dist = math.hypot(dx, dy)
        if dist > 1:  
            dx /= dist
            dy /= dist
            ex += ENEMY_SPEED * dx * dt * 5
            ey += ENEMY_SPEED * dy * dt * 5
        
        scale = 0.8 + 0.2 * math.sin(current_time * 2)
        enemy[0], enemy[1], enemy[3] = ex, ey, scale

    # Check collisions
    new_enemies = []
    for enemy in enemies:
        ex, ey, ez, scale = enemy
        hit = False
        
        for bullet in bullets:
            bx, by, bz, _ = bullet
            if math.hypot(bx - ex, by - ey) < 15 * scale and abs(bz - ez) < 30:
                hit = True
                bullets.remove(bullet)
                score += 1
                break
        
        if math.hypot(ex - player_pos[0], ey - player_pos[1]) < 35 and abs(ez - player_pos[2]) < 30:
            life -= 1
            hit = True
            if life <= 0:
                game_over = True
        if not hit:
            new_enemies.append(enemy)
        else:
            spawn_enemy()
    enemies = new_enemies

    # Cheat mode: auto-rotate and fire
    #if cheat_mode:
        #global player_angle
        #player_angle = (player_angle + 5 * dt * 60) % 360
    
        #rad = math.radians(player_angle)
        #px, py = player_pos[0], player_pos[1]
        #for enemy in enemies:
            #ex, ey, ez, _ = enemy
            
            #dx = ex - px
            #dy = ey - py
            
            #angle_to_enemy = math.degrees(math.atan2(dx, dy)) % 360
            
            #if abs((angle_to_enemy - player_angle) % 360) < 10:
                
                #bx = px + 20 * math.sin(rad)
                #by = py + 20 * math.cos(rad)
                #bz = player_pos[2]
                #bullets.append([bx, by, bz, player_angle])
                #break


def idle():
    """Idle function to update game and trigger redraw."""
    update_game()
    glutPostRedisplay()


def showScreen():
    """Render the game scene."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    # Draw grid and boundaries
    draw_grid()

    # Draw player
    draw_player()

    # Draw enemies
    for enemy in enemies:
        draw_enemy(*enemy)

    # Draw bullets
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1], bullet[2])

    # Draw HUD
    draw_text(10, 740, f"player Life remaining: {life}")
    draw_text(10, 720, f"Game Score: {score}")
    draw_text(10, 700, f"Player Bullets Missed: {bullets_missed}")
    
    if game_over:
        draw_text(400, 400, "Game Over! Press R to Restart")

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy")

    glEnable(GL_DEPTH_TEST)  

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    #glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    init_game()

    glutMainLoop()

main()