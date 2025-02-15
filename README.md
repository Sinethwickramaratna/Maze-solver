# Maze-solver
Simple maze solving program for e-puck robot in Webots

**Overview**  
This code controls a robot within the Webots simulation environment. The robot is designed to perform two primary tasks:  

1. **Wall-following**: The robot uses its distance sensors to follow walls while avoiding obstacles in its path.  
2. **Object color recognition**: The robot employs a camera to recognize specific colored objects and react accordingly.  

**Key Components**  

**Robot Initialization**  
The robot is created using the `Robot()` class from the Webots controller. The timestep is retrieved to manage the timing of the simulation steps.  

**Motor Setup**  
Two motors (leftMotor and rightMotor) control the robot's movement. The motors are set to velocity control mode, which means their positions are set to "infinite," allowing the robot's speed to be adjusted by changing the velocity. The initial speed is set to 0, ensuring the robot remains stationary at the start.  

**Sensor Setup**  
- **Distance Sensors**: These sensors detect walls or obstacles in front, to the left, and to the right of the robot, as well as at the corners (left corner and right corner).  
- **Camera**: The camera recognizes objects based on their color. Object recognition is enabled in the simulation.  

**Wall-Following Logic (`wallFollowing()` Function)**  
This function dictates the robot's movement based on the readings from the distance sensors:  
- **Front Wall**: If a wall is detected directly in front, the robot adjusts its movement:  
  - If there is a wall on the left, it turns right.  
  - If there is no wall on the left, it turns left.  
- **Left or Right Wall**: If a wall is detected on the left or right but not in front, the robot follows the wall straight, based on which side is detected.  
- **Corner Detection**: If a corner is detected (either left or right), the robot reduces the speed on one side to make a more gradual turn.  

**Object Recognition Logic**  
In the main loop, the robot continuously checks for objects using the camera against predefined color patterns.  
- If the camera detects an object, it compares the color with the `color_pattern`.  
- If the recognized object matches the first color in the pattern, the robot reacts accordingly:  
  - **Position Adjustment**: If the object appears off-center (either left or right), the robot will turn to align with it.  
  - **Front Wall Detection**: If there is a wall directly in front, the robot stops focusing on the object and resumes wall-following.  
  - **Move Towards the Object**: If the object is centered in the camera's view, the robot moves straight toward it.  

**Main Loop**  
The main loop continuously runs as long as the simulation is active. Each cycle of the loop performs the following actions:  
- The robot checks for detected objects using the camera.  
- If no objects are detected, it continues wall-following.  
- If an object is detected, it checks the color and adjusts its movement accordingly.  
- If the color is recognized and the object is centered, the robot moves toward it; otherwise, it continues to follow the wall.  

**When the Simulation Ends**  
The code continues executing until the simulation is stopped, and there is no need for explicit cleanup code in this case.  

**Summary of Robot Behavior**  
- **Wall-following**: The robot utilizes its sensors to detect walls and obstacles, adjusting its movement to follow walls or avoid collisions.  
- **Object recognition**: The robot uses the camera to identify objects based on predefined color patterns, adjusting its movement to align with recognized objects or maintaining wall-following if no objects are found. 
