from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
import time

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 800
REFRESH_RATE = 16

delta_time = 0
last_time = time.time()


class Utils:
    @staticmethod
    def find_zone(x1, y1, x2, y2):
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) > abs(dy):
            if dx >= 0 and dy >= 0: return 0
            if dx < 0 and dy >= 0: return 3
            if dx < 0 and dy < 0: return 4
            if dx >= 0 and dy < 0: return 7
        else:
            if dx >= 0 and dy >= 0: return 1
            if dx < 0 and dy >= 0: return 2
            if dx < 0 and dy < 0: return 5
            if dx >= 0 and dy < 0: return 6

    @staticmethod
    def to_zone_0(zone, x, y):
        match zone:
            case 0: return x, y
            case 1: return y, x
            case 2: return y, -x
            case 3: return -x, y
            case 4: return -x, -y
            case 5: return -y, -x
            case 6: return -y, x
            case 7: return x, -y

    @staticmethod
    def from_zone_0(zone, x, y):
        match zone:
            case 0: return x, y
            case 1: return y, x
            case 2: return -y, x
            case 3: return -x, y
            case 4: return -x, -y
            case 5: return -y, -x
            case 6: return y, -x
            case 7: return x, -y

    @staticmethod
    def draw_line(x1, y1, x2, y2):
        zone = Utils.find_zone(x1, y1, x2, y2)
        x1_z, y1_z = Utils.to_zone_0(zone, x1, y1)
        x2_z, y2_z = Utils.to_zone_0(zone, x2, y2)

        dx, dy = x2_z - x1_z, y2_z - y1_z
        d = 2 * dy - dx
        dE = 2 * dy
        dNE = 2 * (dy - dx)

        x, y = x1_z, y1_z
        while x <= x2_z:
            ox, oy = Utils.from_zone_0(zone, x, y)
            glVertex2i(int(ox), int(oy))
            if d < 0:
                d += dE
            else:
                d += dNE
                y += 1
            x += 1


class Catcher:
    def __init__(self):
        self.width = 80
        self.height = 20
        self.x = -self.width // 2
        self.y = -WINDOW_HEIGHT // 2 + 50
        self.color = (1.0, 1.0, 1.0)

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        Utils.draw_line(self.x, self.y + self.height, self.x + self.width, self.y + self.height)
        Utils.draw_line(self.x, self.y + self.height, self.x + 30, self.y)
        Utils.draw_line(self.x + self.width, self.y + self.height, self.x + self.width - 30, self.y)
        Utils.draw_line(self.x + 30, self.y, self.x + self.width - 30, self.y)
        glEnd()

    def move(self, direction, speed):
        if direction == "left":
            self.x = max(self.x - speed, -WINDOW_WIDTH // 2)
        elif direction == "right":
            self.x = min(self.x + speed, WINDOW_WIDTH // 2 - self.width)


    def get_box(self):
        return (self.x, self.y, self.width, self.height)


class Diamond:
    def __init__(self):
        self.size = 20
        self.x = random.randint(-WINDOW_WIDTH // 2 + self.size, WINDOW_WIDTH // 2 - self.size)
        self.y = WINDOW_HEIGHT // 2
        self.color = [random.random() for _ in range(3)]

    def draw(self):
        glColor3f(*self.color)
        cx, cy = self.x, self.y
        glBegin(GL_POINTS)
        Utils.draw_line(cx, cy + 10, cx + 10, cy)
        Utils.draw_line(cx + 10, cy, cx, cy - 10)
        Utils.draw_line(cx, cy - 10, cx - 10, cy)
        Utils.draw_line(cx - 10, cy, cx, cy + 10)
        glEnd()

    def update(self, speed):
        self.y -= speed * delta_time

    

    def get_box(self):
        return (self.x - 10, self.y - 10, 20, 20)


class GameManager:
    def __init__(self):
        self.catcher = Catcher()
        self.diamond = Diamond()
        self.score = 0
        self.speed = 100
        self.catcher_speed = 10
        self.paused = False
        self.over = False

    def reset(self):
        print("Restarting game...")
        self.__init__()

    def toggle_pause(self):
        self.paused = not self.paused
        print("Paused" if self.paused else "Resumed")

    #def update(self):
        #if self.paused or self.over:
            #return
        #self.diamond.update(self.speed)
        #if self.check_collision():
            #self.score += 1
            #print("Score:", self.score)
            #self.speed += 5
            #self.diamond = Diamond()
        #elif self.diamond.y < -WINDOW_HEIGHT // 2:
            #self.over = True
            #self.catcher.color = (1.0, 0.0, 0.0)
            #print("Game Over! Final Score:", self.score)

    def update(self):
        if self.paused or self.over:
           return

    # Smoothly increase fall speed
        self.speed += 5 * delta_time  # 5 pixels/sec per second

        self.diamond.update(self.speed)  # Make sure self.speed is in pixels/sec

        if self.check_collision():
           self.score += 1
           print("Score:", self.score)
           self.diamond = Diamond()
    
        elif self.diamond.y < -WINDOW_HEIGHT // 2:
           self.over = True
           self.catcher.color = (1.0, 0.0, 0.0)
           print("Game Over! Final Score:", self.score)


    def check_collision(self):
        cx, cy, cw, ch = self.catcher.get_box()
        dx, dy, dw, dh = self.diamond.get_box()
        return (cx < dx + dw and cx + cw > dx and
                cy < dy + dh and cy + ch > dy)

    def draw(self):
        self.catcher.draw()
        if not self.over:
            self.diamond.draw()

class Button:
    def __init__(self, x, y, width, height, action, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.color = color

    #def draw_arrow(self):  # Teal left-arrow for restart
        #glColor3f(*self.color)
        #glBegin(GL_POINTS)
        #cx = self.x
        #cy = self.y

        #shaft_length = 12
        #head_length = 6
        #head_height = 6

    
        #Utils.draw_line(cx - shaft_length // 2, cy, cx + shaft_length // 2, cy)

    
        #Utils.draw_line(cx - shaft_length // 2, cy, cx - shaft_length // 2 + head_length, cy + head_height)
        #Utils.draw_line(cx - shaft_length // 2, cy, cx - shaft_length // 2 + head_length, cy - head_height)
        #Utils.draw_line(cx - shaft_length // 2 + head_length, cy + head_height, cx - shaft_length // 2 + head_length, cy - head_height)

        #glEnd()

    def draw_arrow(self):  # Simple hollow left arrow (←)
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        cx = self.x
        cy = self.y

    
        left = (cx - 10, cy)
        right = (cx + 10, cy)
        head_top = (cx - 6, cy + 6)
        head_bottom = (cx - 6, cy - 6)

    
        Utils.draw_line(*left, *right)

    
        Utils.draw_line(*left, *head_top)
        Utils.draw_line(*left, *head_bottom)
        glEnd()




    def draw_pause(self):  # Amber pause icon
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        cx = self.x
        cy = self.y
        Utils.draw_line(cx - 5, cy + 10, cx - 5, cy - 10)
        Utils.draw_line(cx + 5, cy + 10, cx + 5, cy - 10)
        glEnd()

    #def draw_play(self):  # Amber play icon
        #glColor3f(*self.color)
        #glBegin(GL_POINTS)
        #cx = self.x
        #cy = self.y
        #Utils.draw_line(cx - 5, cy + 10, cx + 8, cy)
        #Utils.draw_line(cx - 5, cy - 10, cx + 8, cy)
        #glEnd()
    def draw_play(self):  # ▶ Hollow play icon
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        cx = self.x
        cy = self.y

    
        left_top = (cx - 6, cy + 10)
        left_bottom = (cx - 6, cy - 10)
        tip = (cx + 10, cy)

    
        Utils.draw_line(*left_top, *tip)
        Utils.draw_line(*tip, *left_bottom)
        Utils.draw_line(*left_bottom, *left_top)
        glEnd()

    def draw_cross(self):  # Red cross
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        cx = self.x
        cy = self.y
        Utils.draw_line(cx - 10, cy + 10, cx + 10, cy - 10)
        Utils.draw_line(cx - 10, cy - 10, cx + 10, cy + 10)
        glEnd()

    def contains(self, mx, my):
        return (self.x - self.width // 2 <= mx <= self.x + self.width // 2 and
                self.y - self.height // 2 <= my <= self.y + self.height // 2)



game = GameManager()

buttons = [
    Button(-WINDOW_WIDTH//2 + 40, WINDOW_HEIGHT//2 - 40, 40, 40, "restart", (0.25, 0.71, 0.71)),
    Button(0, WINDOW_HEIGHT//2 - 40, 40, 40, "pause", (0.95, 0.68, 0.05)),
    Button(WINDOW_WIDTH//2 - 40, WINDOW_HEIGHT//2 - 40, 40, 40, "exit", (1.0, 0.0, 0.0))
]

def draw_buttons():
    for btn in buttons:
        if btn.action == "restart":
            btn.draw_arrow()
        elif btn.action == "pause":
            if game.paused:
                btn.draw_play()
            else:
                btn.draw_pause()
        elif btn.action == "exit":
            btn.draw_cross()



def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    game.draw()
    draw_buttons()
    glutSwapBuffers()



#def update(value):
    #global delta_time, last_time
    #current_time = time.time()
    #delta_time = current_time - last_time
    #last_time = current_time
    #game.update()
    #glutPostRedisplay()
    #glutTimerFunc(REFRESH_RATE, update, 0)

def update(value):
    global delta_time, last_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    game.update()
    glutPostRedisplay()
    glutTimerFunc(REFRESH_RATE, update, 0)


def special_keys(key, x, y):
    if not game.paused and not game.over:
        if key == GLUT_KEY_LEFT:
            game.catcher.move("left", game.catcher_speed)
        elif key == GLUT_KEY_RIGHT:
            game.catcher.move("right", game.catcher_speed)

#def mouse_click_handler(button, state, x, y):
    #if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        #mx = x - WINDOW_WIDTH // 2
        #my = WINDOW_HEIGHT // 2 - y

        #for btn in buttons:
            #if btn.contains(mx, my):
                #if btn.action == "restart":
                    #game.reset()
                #elif btn.action == "pause":
                    #game.toggle_pause()
                #elif btn.action == "exit":
                    #print("Goodbye! Final Score:", game.score)
                    #glutLeaveMainLoop()

def mouse_click_handler(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Get current window size (in case resized)
        win_w = glutGet(GLUT_WINDOW_WIDTH)
        win_h = glutGet(GLUT_WINDOW_HEIGHT)

        # Convert screen (pixel) coords to OpenGL coords
        mx = (x / win_w) * WINDOW_WIDTH - WINDOW_WIDTH // 2
        my = (1 - y / win_h) * WINDOW_HEIGHT - WINDOW_HEIGHT // 2

        print(f"Mouse clicked at ({mx:.2f}, {my:.2f})")

        for btn in buttons:
            if btn.contains(mx, my):
                print(f"Button '{btn.action}' clicked")
                if btn.action == "restart":
                    print("Starting Over")
                    game.reset()
                elif btn.action == "pause":
                    game.toggle_pause()
                elif btn.action == "exit":
                    print("Goodbye! Final Score:", game.score)
                    glutLeaveMainLoop()


def init():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-WINDOW_WIDTH // 2, WINDOW_WIDTH // 2, -WINDOW_HEIGHT // 2, WINDOW_HEIGHT // 2, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPointSize(2)


# Setup and run
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow(b"Catch the Diamonds!")
init()

glutDisplayFunc(display)
glutSpecialFunc(special_keys)
#glutKeyboardFunc(keyboard)
glutTimerFunc(REFRESH_RATE, update, 0)
glutMouseFunc(mouse_click_handler)

glutMainLoop()

