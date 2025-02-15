"""IESLRobot controller."""

# Importing necessary classes from the controller module
from controller import Robot
import math

# Create the Robot instance to interact with Webots environment
robot = Robot()

# Get the time step of the current simulation world (in milliseconds)
timestep = int(robot.getBasicTimeStep())

# Initialize the motors for the left and right wheels
leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")

# Set the motors to velocity control mode (infinite position)
leftMotor.setPosition(float("inf"))
rightMotor.setPosition(float("inf"))

# Set initial velocities of the motors to 0 (robot starts stationary)
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

# Define the speed the robot will move with
speed = 4

# Initialize the camera and enable object recognition
camera = robot.getDevice("camera1")
camera.enable(timestep)
camera.recognitionEnable(timestep)

# Initialize distance sensors for detecting walls and obstacles
front_ds = robot.getDevice("front_ds")
front_ds.enable(timestep)
left_ds = robot.getDevice("left_ds")
left_ds.enable(timestep)
right_ds = robot.getDevice("right_ds")
right_ds.enable(timestep)
leftcorner_ds = robot.getDevice("leftcorner_ds")
leftcorner_ds.enable(timestep)
rightcorner_ds = robot.getDevice("rightcorner_ds")
rightcorner_ds.enable(timestep)

# Variable to track the wall-following direction
wall = ""

# Function to implement wall-following behavior
def wallFollowing():
    global wall
    # Read the sensor values to determine proximity to obstacles
    left_wall = left_ds.getValue() < 700
    right_wall = right_ds.getValue() < 700
    left_corner = leftcorner_ds.getValue() < 700
    right_corner = rightcorner_ds.getValue() < 700
    front_wall = front_ds.getValue() < 700

    # Default speed values for both wheels
    leftspeed = speed
    rightspeed = speed

    # Logic to adjust robot's movement if there is a wall in front
    if front_wall:
        if left_wall:
            leftspeed = speed
            rightspeed = -speed  # Turn right if there's a wall on the left
        else:
            leftspeed = -speed  # Turn left if there's no wall on the left
            rightspeed = speed

    # If there's a wall on the left or right, but not in front, keep moving straight
    if left_wall or right_wall and not front_wall:
        leftspeed = speed
        rightspeed = speed
        if left_wall:
            wall = "left"  # Follow the left wall
        if right_wall:
            wall = "right"  # Follow the right wall
    
    # Adjust robot speed based on wall-following logic when there's no wall in front
    elif wall == "left" and not front_wall:
        leftspeed = speed / 2  # Move slower on the left side
        rightspeed = speed
    elif wall == "right" and not front_wall:
        leftspeed = speed
        rightspeed = speed / 2  # Move slower on the right side

    # Adjust robot speed when the robot detects a corner (left corner or right corner)
    if left_corner:
        leftspeed = speed
        rightspeed = speed / 16  # Move slower on the right side when near left corner
    if right_corner:
        leftspeed = speed / 16  # Move slower on the left side when near right corner
        rightspeed = speed

    # Set the velocities of both motors
    leftMotor.setVelocity(leftspeed)
    rightMotor.setVelocity(rightspeed)

# Predefined color patterns the robot is looking for
color_pattern = [(1, 0, 0), (1, 1, 0), (1, 0, 1), (0.647059, 0.411765, 0.117647), (0, 1, 0)]

# Position of an object in the image (unused in the code)
object_pos = [(0.7, 0.502, 0.05)]

# Main loop: runs until the simulation is stopped
while robot.step(timestep) != -1:
    
    # Get detected objects from the camera
    object = camera.getRecognitionObjects()
    
    # Read the current values from the distance sensors to detect walls
    front_wall = front_ds.getValue() < 350
    left_wall = left_ds.getValue() < 350
    right_wall = right_ds.getValue() < 350
    
    # If there are no color patterns left to search, stop the robot
    if len(color_pattern) == 0:
        robot.stepEnd()
        
    else:
        # If no objects detected by the camera, continue wall-following
        if len(object) == 0:
            wallFollowing()
        else:
            # Get the RGB color values of the recognized object
            color = object[0].getColors()
            recognized_color = (color[0], color[1], color[2])
            
            # If the recognized color matches the first color pattern in the list
            if recognized_color == color_pattern[0]:
                position = object[0].getPositionOnImage()
                
                # If there's a wall in front, pop the color pattern from the list
                if front_wall:
                    color_pattern.pop(0)
                    wallFollowing()  # Continue wall-following behavior
                else:
                    # Adjust the robot's movement based on the object's position in the camera's image
                    if position[0] > 40:
                        # Turn left if the object is to the right
                        leftMotor.setVelocity(speed)
                        rightMotor.setVelocity(-speed)
                    elif position[0] < 10:
                        # Turn right if the object is to the left
                        leftMotor.setVelocity(-speed)
                        rightMotor.setVelocity(speed)
                    else:
                        # Move straight if the object is in the center
                        leftMotor.setVelocity(speed)
                        rightMotor.setVelocity(speed)
            else:
                # If the color doesn't match, continue with wall-following behavior
                wallFollowing()
    
    # Read sensor data (distance sensors and camera) here as needed

    # Send actuator commands (set motor speeds) here as needed

# Exit cleanup code (not required in this example, but could be added here)
