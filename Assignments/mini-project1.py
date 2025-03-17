import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width, height = 800, 600                                                    # width and height of the screen created
rotation_angle = 0                                                          # rotation angle  (global variable)
arm_angle = 0                                                               # arm angle (global variable)
arm_direction = 1                                                           # arm direction (global variable)
leg_angle = 0                                                               # leg angle (global variable)
leg_direction = 1                                                           # leg direction (global variable)
arms_enabled = True                                                         # enable arms (global variable)
legs_enabled = True                                                         # enable legs (global variable)

def drawAxes():                                                             # draw x-axis and y-axis
    glLineWidth(3.0)                                                        # specify line size (1.0 default)
    glBegin(GL_LINES)                                                       # replace GL_LINES with GL_LINE_STRIP or GL_LINE_LOOP
    glColor3f(1.0, 0.0, 0.0)                                                # x-axis: red
    glVertex3f(0.0, 0.0, 0.0)                                               # v0
    glVertex3f(100.0, 0.0, 0.0)                                             # v1
    glColor3f(0.0, 1.0, 0.0)                                                # y-axis: green
    glVertex3f(0.0, 0.0, 0.0)                                               # v0
    glVertex3f(0.0, 100.0, 0.0)                                             # v1
    glColor3f(0.0, 0.0, 1.0)                                                # z-axis: blue
    glVertex3f(0.0, 0.0, 0.0)                                               # v0
    glVertex3f(0.0, 0.0, 100.0)                                             # v1
    glEnd()

# For Mini-project 1:
# TODO: 1) Create a scarecrow as instructed and 2) Constantly rotate head and nose ONLY
def draw_Scarecrow():                                                  # This is the drawing function drawing all graphics (defined by you)
    glClearColor(0, 0, 0, 1)                                                # set background RGBA color 
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)                        # clear the buffers initialized in the display mode

    # configure quatratic drawing
    quadratic = gluNewQuadric()
    gluQuadricDrawStyle(quadratic, GLU_FILL)  

    # TODO: Head (sphere: radius=2.5) 
    glPushMatrix()
    glTranslatef(0.0, 12.5, 0.0)
    glRotatef(rotation_angle, 0, 1, 0)
    glColor3f(0.0, 1.0, 0.0)
    gluSphere(quadratic, 2.5, 32, 32)
    glPopMatrix()

    # TODO: Nose (cylinder: base-radius=0.3, top-radius=0, length=2)
    glPushMatrix()
    glTranslatef(0.0, 12.5, 0.0)
    glRotatef(rotation_angle, 0, 1, 0)
    glTranslatef(0.0, 0.0, 2.5)
    glColor3f(1.0, 0.0, 0.0)
    gluCylinder(quadratic, 0.3, 0.0, 1.8, 32, 32)  
    glPopMatrix()

    # TODO: Torso (cylinder: radius=2.5, length=10)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glColor3f(1.0, 1.0, 0.0)
    gluCylinder(quadratic, 2.5, 2.5, 10.0, 32, 32)
    glPopMatrix()

    # TODO: Left Leg (cylinders: radius=1.0, length=12)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glTranslatef(-1.2, 0.0, 0.0)
    glRotatef(-leg_angle, 1, 0, 0)
    glColor3f(1.0, 0.0, 0.0)
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # TODO: Right Leg (cylinders: radius=1.0, length=12)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glTranslatef(1.2, 0.0, 0.0)
    glRotatef(leg_angle, 1, 0, 0)
    glColor3f(1.0, 0.0, 0.0)
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # TODO: Left Arm (cylinders: radius=1.0, length=10)
    glPushMatrix()
    glRotatef(-90, 0, 1, 0)
    glTranslatef(0.0, 9.0, 2.5)
    glRotatef(arm_angle, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # TODO: Right Arm (cylinders: radius=1.0, length=10)
    glPushMatrix()
    glRotatef(90, 0,1, 0)
    glTranslatef(0.0, 9.0, 2.5)
    glRotatef(arm_angle, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

def main():
    global rotation_angle
    global arm_angle
    global arm_direction
    global leg_angle
    global leg_direction
    global arms_enabled
    global legs_enabled

    pygame.init()                                                           # initialize a pygame program
    glutInit()                                                              # initialize glut library 

    screen = (width, height)                                                # specify the screen size of the new program window
    display_surface = pygame.display.set_mode(screen, DOUBLEBUF | OPENGL)   # create a display of size 'screen', use double-buffers and OpenGL
    pygame.display.set_caption('CPSC 360 - Alyssa Perry')                   # set title of the program window

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)                                             # set mode to projection transformation
    glLoadIdentity()                                                        # reset transf matrix to an identity
    gluPerspective(45, (width / height), 0.1, 100.0)                        # specify perspective projection view volume

    glMatrixMode(GL_MODELVIEW)                                              # set mode to modelview (geometric + view transf)
    initmodelMatrix = glGetFloat(GL_MODELVIEW_MATRIX)                       # backup the current modelview matrix before any transfs
    modelMatrix = glGetFloat(GL_MODELVIEW_MATRIX)

    while True:
        bResetModelMatrix = False
        glPushMatrix()
        glLoadIdentity()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    glRotatef(event.rel[1], 1, 0, 0)
                    glRotatef(event.rel[0], 0, 1, 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    bResetModelMatrix = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    arms_enabled = not arms_enabled

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    legs_enabled = not legs_enabled
        
        # reset the current model-view back to the initial matrix
        if (bResetModelMatrix):
            glLoadIdentity()
            modelMatrix = initmodelMatrix
        
        glMultMatrixf(modelMatrix)
        modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        glLoadIdentity()
        gluLookAt(0, 0, 50, 0, 0, -1, 0, 1, 0)
        glMultMatrixf(modelMatrix)

        rotation_angle += 1                                                 # increment the rotation angle by 1 degree
        if rotation_angle >= 360:
            rotation_angle -= 360                                           # reset the rotation angle back to 0 degree to keep between 0 and 360

        if arms_enabled:
            arm_angle += arm_direction * 1                          # increment the wave angle by 1 degree
            if arm_angle >= 45 or arm_angle <= -45:
                arm_direction *= -1                                     # reverse the wave direction when the wave angle reaches 45 or -45 degrees

        if legs_enabled:
            leg_angle += leg_direction * 1                          # increment the wave angle by 1 degree
            if leg_angle >= 45 or leg_angle <= -45:
                leg_direction *= -1                                     # reverse the wave direction when the wave angle reaches 45 or -45 degrees

        # ONLY write your code inside the function below 
        #   You don't need to modify any other code in this file,
        #    except for using a global variable to store and update 
        #       the rotation angle.
        draw_Scarecrow()

        # draw x, y, z axes
        drawAxes()
        
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

main()