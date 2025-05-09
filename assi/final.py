# task1
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *

# import random


# W_Width, W_Height = 1000,650

# rain_size=50
# rain_count=20
# rain_speed=15
# rain_direction=0.0
# background_color=0.0
# target_color=0.0

# blue_raindrop=[(random.uniform(-W_Width//2, W_Width//2), random.uniform(-W_Height, W_Height-50)) for _ in range(rain_count)]
# grey_raindrop=[(random.uniform(-W_Width//2, W_Width//2), random.uniform(-W_Height, W_Height-50)) for _ in range(rain_count)]

# def draw_raindrop():
#     global rain_size,rain_count,rain_speed,rain_direction,blue_raindrop,grey_raindrop

#     glBegin(GL_LINES)
#     i=0
#     while i<rain_count:
#         glColor3f (100/255, 149/255, 237/255)
    
#         x, y = blue_raindrop[i]
#         glVertex2f(x, y)
#         glVertex2f(x + rain_direction, y - rain_size)
#         glColor3f(169/255, 169/255, 169/255)
    
#         x, y = grey_raindrop[i]
#         glVertex2f(x, y)
#         glVertex2f(x + rain_direction, y - rain_size)
#         i+=1
#     glEnd()

# def draw_rainfall():
#     global rain_size,rain_count,rain_speed,rain_direction,blue_raindrop,grey_raindrop
    
#     i = 0
#     while i < rain_count:
#         x, y = blue_raindrop[i]
#         x += rain_direction  
#         y -= rain_speed  
            
#         if y < -(W_Height // 2): 
#             x = random.uniform(-W_Width // 2, W_Width // 2)  
#             y = random.uniform(-W_Height, W_Height // 2)  
#         blue_raindrop[i] = (x, y) 
#         i += 1
        
#     i = 0
#     while i < rain_count:
#         x, y = grey_raindrop[i]
#         x += rain_direction
#         y -= rain_speed
#         if y < -(W_Height // 2):
#             x = random.uniform(-W_Width // 2, W_Width // 2)
#             y = random.uniform(-W_Height, W_Height // 2)
#         grey_raindrop[i] = (x, y)
#         i += 1

# def rain_animation():
#     draw_rainfall()
#     glutPostRedisplay()

# def specialkeylistener(key, x, y):
#     global rain_size,rain_count,rain_speed,rain_direction,blue_raindrop,grey_raindrop
    
    
#     if key == GLUT_KEY_RIGHT:
#         rain_direction+=1.25
#         rain_speed+=1
#         print('Bending to the right')
#     elif key == GLUT_KEY_LEFT:
#         rain_direction-=1.25
#         rain_speed+=1
#         print('Bending to the left')


        
#     glutPostRedisplay()

# def day_night():
    
    
#     global background_color, target_color
#     if target_color==0.0:
#         if background_color<1:
#             background_color += 0.05
#         else:
#             background_color = 1
#     else:
#         if background_color >0:  
#             background_color -=0.05
#         else:
#             background_color=0

#     glutPostRedisplay()  
#     glutTimerFunc(60,lambda _: day_night(),0)

# def specialkey(key,x,y):
#     global target_color
    

#     if key == GLUT_KEY_F1:  
#         target_color = 1.0 
#     elif key== GLUT_KEY_F5:
#         target_color= 0.0
    
    
#     glutPostRedisplay()

# def draw_background():
#     #sky
#     glBegin(GL_TRIANGLES)
#     glColor3f(0, 0, 0)  

#     glVertex2f(-W_Width//2, W_Height)
#     glVertex2f(-W_Width//2, -W_Height)
#     glVertex2f(W_Width//2, -W_Height)
#     glEnd()

#     glBegin(GL_TRIANGLES)
#     glColor3f(0, 0, 0) 
#     glVertex2f(W_Width//2, -W_Height)
#     glVertex2f(W_Width//2, W_Height)
#     glVertex2f(-W_Width//2, W_Height)
#     glEnd()

#     #ground
#     glBegin(GL_TRIANGLES)
#     glColor3f(97/255,67/255,33/255)
#     glVertex2f(-W_Width//2, -W_Height)
#     glVertex2f(-W_Width//2, 150)  
#     glVertex2f(W_Width//2, 150)
#     glEnd()

#     glBegin(GL_TRIANGLES)
#     glColor3f(97/255,67/255,33/255)
#     glVertex2f(W_Width//2, 150)
#     glVertex2f(W_Width//2, -W_Height)
#     glVertex2f(-W_Width//2, -W_Height)
#     glEnd()

#     #hills
#     glBegin(GL_TRIANGLES)
    
#     glColor3f(34/255, 139/255, 34/255)  

#     x = -W_Width // 2  
#     while x < W_Width // 2:
#         glVertex2f(x + 25, 100)  
#         glVertex2f(x, 45) 
#         glVertex2f(x + 50, 45)  
#         x += 50  
#     glEnd()

# def draw_house():
#     # Roof (Lavender)
#     glBegin(GL_TRIANGLES)
#     glColor3f(186/255, 22/255, 63/255)  
#     glVertex2f(0, 225)    
#     glVertex2f(-150, 50)  
#     glVertex2f(150, 50)   
#     glEnd()

#     # House Body (White)
#     glBegin(GL_TRIANGLES)
#     glColor3f(240/255,232/255,205/255)
#     glVertex2f(-100, -100)  
#     glVertex2f(-100, 50)    
#     glVertex2f(100, 50)     
#     glEnd()

#     glBegin(GL_TRIANGLES)
#     glColor3f(240/255,232/255,205/255)  
#     glVertex2f(100, 50)   
#     glVertex2f(100, -100) 
#     glVertex2f(-100, -100) 
#     glEnd()

#     # Door (Dark Blue)
#     glBegin(GL_TRIANGLES)
#     glColor3f(191/255, 213/255, 232/255)  
#     glVertex2f(-30, -100)  
#     glVertex2f(-30, 30)    
#     glVertex2f(30, 30)     
#     glEnd()

#     glBegin(GL_TRIANGLES)
#     glColor3f( 191/255, 213/255, 232/255) 
#     glVertex2f(30, 30)   
#     glVertex2f(30, -100) 
#     glVertex2f(-30, -100) 
#     glEnd()

#     # Windows (White)
#     glBegin(GL_TRIANGLES)
#     glColor3f ( 191/255, 213/255, 232/255)  
#     glVertex2f(-80, -20) 
#     glVertex2f(-80, 30)  
#     glVertex2f(-40, 30)  
#     glEnd()

#     glBegin(GL_TRIANGLES)
#     glColor3f(191/255, 213/255, 232/255)  
#     glVertex2f(-40, -20) 
#     glVertex2f(-40, 30)  
#     glVertex2f(-80, -20) 
#     glEnd()

#     glBegin(GL_TRIANGLES)
#     glColor3f(191/255, 213/255, 232/255)  
#     glVertex2f(40, -20)   
#     glVertex2f(40, 30)    
#     glVertex2f(80, 30)    
#     glEnd()

#     glBegin(GL_TRIANGLES)
#     glColor3f(191/255, 213/255, 232/255)  
#     glVertex2f(80, 30)   
#     glVertex2f(80, -20)  
#     glVertex2f(40, -20)  
#     glEnd()

#     # Window Grills (Black)
#     glLineWidth(5)
#     glBegin(GL_LINES)
#     glColor3f(0, 0, 0)  
#     glVertex2f(-80, 5)    
#     glVertex2f(-40, 5)    
#     glVertex2f(-60, 30)   
#     glVertex2f(-60, -20)  
#     glVertex2f(40, 5)     
#     glVertex2f(80, 5)     
#     glVertex2f(60, 30)    
#     glVertex2f(60, -20)   
#     glEnd()

#     # Door Knob (Black)
#     glPointSize(10)
#     glBegin(GL_POINTS)
#     glColor3f(0, 0, 0)  
#     glVertex2f(20, -35)  
#     glEnd()



# def display():
    
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glClearColor(0,0,0,0)
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
#     gluLookAt(0,0,200,	0,0,0,	0,1,0)
#     glMatrixMode(GL_MODELVIEW)

#     draw_background()
#     draw_house()
#     draw_raindrop()
#     glutSwapBuffers()

# def init():
    
#     glClearColor(0,0,0,0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(104,	1,	1,	1000.0)

# glutInit()
# glutInitWindowSize(W_Width, W_Height)
# glutInitWindowPosition(0, 0)
# glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 


# wind = glutCreateWindow(b"A house in Rainfall")
# init()

# glutDisplayFunc(display)	
# glutIdleFunc(rain_animation)	

# glutSpecialFunc(specialkey)
# glutSpecialFunc(specialkeylistener)
# day_night()
# glutMainLoop() 


#task2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


window_width, window_height = 800, 600
sphere_list = []

is_frozen = False
movement_speed = 5
ball_size = 5
blink_interval = 500  
is_blinking = False   

class Sphere:
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        
        self.velocity = random.choice([(-1, 1), (-1, -1), (1, 1), (1, -1)])
       
        self.original_color = [random.random(), random.random(), random.random()]
        self.color = self.original_color.copy()

    def update_position(self):
        global is_frozen, movement_speed, window_width, window_height
        if not is_frozen:
            dx, dy = self.velocity
            self.x += dx * movement_speed
            self.y += dy * movement_speed

        
        if self.x <= 0:
            self.x = 0
            dx = abs(self.velocity[0])
            self.velocity = (dx, self.velocity[1])
        elif self.x >= window_width:
            self.x = window_width
            dx = -abs(self.velocity[0])
            self.velocity = (dx, self.velocity[1])
        
        if self.y <= 0:
            self.y = 0
            dy = abs(self.velocity[1])
            self.velocity = (self.velocity[0], dy)
        elif self.y >= window_height:
            self.y = window_height
            dy = -abs(self.velocity[1])
            self.velocity = (self.velocity[0], dy)

def window_resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glPointSize(ball_size)
    glBegin(GL_POINTS)
    for sphere in sphere_list:
        glColor3fv(sphere.color)
        glVertex2f(sphere.x, sphere.y)
    glEnd()
    glutSwapBuffers()

def process_mouse_input(button, state, xpos, ypos):
    global is_blinking
    if state == GLUT_DOWN:
        if button == GLUT_RIGHT_BUTTON:
            
            sphere_list.append(Sphere(xpos, window_height - ypos))
            print("Sphere added at:", xpos, window_height - ypos)
        elif button == GLUT_LEFT_BUTTON:
            
            if is_blinking:
                is_blinking = False
                
                for sphere in sphere_list:
                    sphere.color = sphere.original_color.copy()
                print("Blinking stopped.")
            else:
                is_blinking = True
                print("Blinking started.")
    glutPostRedisplay()

def adjust_properties(key, x, y):
    global is_frozen, movement_speed, ball_size
    if key == b' ':
        is_frozen = not is_frozen
    elif key == b's':
        movement_speed = max(0.5, movement_speed - 0.5)
        print("Speed decreased to", movement_speed)
    elif key == b'd':
        movement_speed += 0.5
        print("Speed increased to", movement_speed)
    glutPostRedisplay()

def modify_speed(key, x, y):
    global movement_speed
    if key == GLUT_KEY_UP:
        movement_speed += 0.5
        print("Speed increased to", movement_speed)
    elif key == GLUT_KEY_DOWN:
        movement_speed = max(0.5, movement_speed - 0.5)
        print("Speed decreased to", movement_speed)
    glutPostRedisplay()

def timer_update(value):
    if not is_frozen:
        for sphere in sphere_list:
            sphere.update_position()
    glutPostRedisplay()
    glutTimerFunc(16, timer_update, 0)

def blinking_timer(value):  
    if is_blinking:
        
        for sphere in sphere_list:
            if sphere.color != [0.0, 0.0, 0.0]:
                sphere.color = [0.0, 0.0, 0.0]
            else:
                sphere.color = sphere.original_color.copy()
    glutPostRedisplay()
    glutTimerFunc(blink_interval, blinking_timer, 0)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"Colorful Blinking Spheres")
glClearColor(0, 0, 0, 1)
glPointSize(ball_size)

glutDisplayFunc(render_scene)
glutReshapeFunc(window_resize)
glutMouseFunc(process_mouse_input)
glutKeyboardFunc(adjust_properties)
glutSpecialFunc(modify_speed)
glutTimerFunc(16, timer_update, 0)
glutTimerFunc(blink_interval, blinking_timer, 0)
glutMainLoop()

