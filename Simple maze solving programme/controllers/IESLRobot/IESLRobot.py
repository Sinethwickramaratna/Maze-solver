"""IESLRobot controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import math
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

leftMotor=robot.getDevice("left wheel motor")
rightMotor=robot.getDevice("right wheel motor")

leftMotor.setPosition(float("inf"))
rightMotor.setPosition(float("inf"))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)
speed=4

camera=robot.getDevice("camera1")
camera.enable(timestep)
camera.recognitionEnable(timestep)

front_ds=robot.getDevice("front_ds")
front_ds.enable(timestep)
left_ds=robot.getDevice("left_ds")
left_ds.enable(timestep)
right_ds=robot.getDevice("right_ds")
right_ds.enable(timestep)
leftcorner_ds=robot.getDevice("leftcorner_ds")
leftcorner_ds.enable(timestep)
rightcorner_ds=robot.getDevice("rightcorner_ds")
rightcorner_ds.enable(timestep)


wall=""
def wallFollowing():
    global wall
    left_wall=left_ds.getValue()<700
    right_wall=right_ds.getValue()<700
    left_corner=leftcorner_ds.getValue()<700
    right_corner=rightcorner_ds.getValue()<700
    front_wall=front_ds.getValue()<700
    leftspeed=speed
    rightspeed=speed
    if front_wall:
        if left_wall:
            leftspeed=speed
            rightspeed=-speed
        else:
            leftspeed=-speed
            rightspeed=speed
    if left_wall or right_wall and not front_wall:
        leftspeed=speed
        rightspeed=speed
        if left_wall:
            wall="left"
        if right_wall:
            wall="right"
    
    elif wall=="left" and not front_wall:
        leftspeed=speed/2
        rightspeed=speed
    elif wall=="right" and not front_wall:
        leftspeed=speed
        rightspeed=speed/2
    if left_corner:
        leftspeed=speed
        rightspeed=speed/16
    if right_corner:
        leftspeed=speed/16
        rightspeed=speed
    leftMotor.setVelocity(leftspeed)
    rightMotor.setVelocity(rightspeed)

color_pattern=[(1,0,0),(1,1,0),(1,0,1),(0.647059,0.411765,0.117647),(0,1,0)]
object_pos=[(0.7,0.502,0.05)]

while robot.step(timestep) != -1:

    object=camera.getRecognitionObjects()
    front_wall=front_ds.getValue()<350
    left_wall=left_ds.getValue()<350
    right_wall=right_ds.getValue()<350
    if len(color_pattern)==0:
        robot.stepEnd()
        
    else:
         if len(object)==0:
             wallFollowing()
         else:
             color=object[0].getColors()
             recognized_color=(color[0],color[1],color[2])
             if (recognized_color)==color_pattern[0]:
                 position=object[0].getPositionOnImage()
                 if front_wall: 
                     color_pattern.pop(0)
                     wallFollowing()      
                 else:
                     if position[0]>40:
                         leftMotor.setVelocity(speed)
                         rightMotor.setVelocity(-speed)
                     elif position[0]<10:
                         leftMotor.setVelocity(-speed)
                         rightMotor.setVelocity(speed)
                     else:
                       leftMotor.setVelocity(speed)
                       rightMotor.setVelocity(speed) 
                      
             else:
                 wallFollowing()
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
