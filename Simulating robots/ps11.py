# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random
import ps11_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        # TODO: Your code goes here
        self.w = width
        self.h = height
        self.tile = {}
        for i in range(width):
            for j in range(height):
                self.tile[i,j] = 'dirty'
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        # TODO: Your code goes here
        i = math.floor(pos.getX())
        j = math.floor(pos.getY())
        self.tile[i,j] = 'clean'
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        # TODO: Your code goes here
        if self.tile[m,n] == 'clean':
            return True
        else:
            return False
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        # TODO: Your code goes here
        return len(self.tile)
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        # TODO: Your code goes here
        num = 0
        for i in range(self.w):
            for j in range(self.h):
                if self.tile[i,j] == 'clean':
                    num += 1
        return num
    
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        # TODO: Your code goes here
        x = self.w*random.random()
        y = self.h*random.random()
        return Position(x,y)
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        # TODO: Your code goes here
        if (0. <= pos.getX() <= self.w) and (0. <= pos.getY() <= self.h):
            return True
        else:
            return False


class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        # TODO: Your code goes here
        self.room = room
        self.speed = speed
        self.d = random.randint(0,360)
        self.p = self.room.getRandomPosition()
        
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        # TODO: Your code goes here
        return self.p
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        # TODO: Your code goes here
        return self.d
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        # TODO: Your code goes here
        self.p = position
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        # TODO: Your code goes here
        self.d = direction


class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # TODO: Your code goes here
        newPos = self.p.getNewPosition(self.d,self.speed)
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)
            self.room.cleanTileAtPosition(newPos)
        else:
            self.setRobotDirection(random.randint(0,360))
            
            


# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    # TODO: Your code goes here
    res = []
    for trial in range(num_trials):
        if visualize:
            anim = ps11_visualize.RobotVisualization(num_robots, width, height)
        rob = []
        res_trial = []
        room = RectangularRoom(width,height)
        for robot in range(num_robots):
            rob.append(robot_type(room, speed))
        cleaned = 0.
        while cleaned < min_coverage:
            for robot in range(num_robots):
                rob[robot].updatePositionAndClean()
            cleaned = room.getNumCleanedTiles()/room.getNumTiles()
            res_trial.append(cleaned)
            if visualize:
                anim.update(room, rob)
        if visualize:        
            anim.done()
        res.append(res_trial)
    return res
            
            
        
        

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means

def avgLen(trials):
    sumTrials = 0
    for i in range(len(trials)):
        sumTrials += len(trials[i])
    return sumTrials/len(trials)

# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    # TODO: Your code goes here
    x = []
    y= []
    for i in range(1,6):
        x.append(25*i*i)
        res = runSimulation(1, 1.0, 5*i, 5*i, 0.75, 100, Robot, False)
        y.append(avgLen(res))
    pylab.plot(x,y)
    pylab.title('Time to clean 75% of square room with 1 robot, for various room size')
    pylab.ylabel('Temesteps')
    pylab.xlabel('Room area')
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    # TODO: Your code goes here
    x = []
    y= []
    for i in range(1,11):
        x.append(i)
        res = runSimulation(i, 1.0, 25, 25, 0.75, 100, Robot, False)
        y.append(avgLen(res))
    pylab.plot(x,y)
    pylab.title('Time to clean 75% of square 25x25 room  for various robots number')
    pylab.ylabel('Temesteps')
    pylab.xlabel('Robot number')
    pylab.show()

def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    # TODO: Your code goes here
    x = []
    y= []
    roomX = [20,25,40,50,80,100]
    roomY = [20,16,10,8,5,4]
    for i in range(len(roomX)):
        x.append(roomX[i]/roomY[i])
        res = runSimulation(2, 1.0, roomX[i], roomY[i], 0.75, 100, Robot, False)
        y.append(avgLen(res))
    pylab.plot(x,y)
    pylab.title('Time to clean 75% of square room with 2 robot, for various room size')
    pylab.ylabel('Temesteps')
    pylab.xlabel('Width to height')
    pylab.show()

def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    # TODO: Your code goes here
    x = []
    y= []
    for i in range(1,6):  
        res = computeMeans(runSimulation(i, 1.0, 25, 25, 1.00, 10, Robot, False))
        y = range(len(res))
        x = res 
        pylab.plot(x,y, label=f"Num of robots: {i}")
        
    pylab.legend(loc='upper center') 
    pylab.ylabel('Temesteps')
    pylab.xlabel('Percentage cleaned')
    pylab.show()
    
# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    # TODO: Your code goes here
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # TODO: Your code goes here
        newPos = self.p.getNewPosition(self.d,self.speed)
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)
            self.room.cleanTileAtPosition(newPos)
            self.setRobotDirection(random.randint(0,360))
        else:
            self.setRobotDirection(random.randint(0,360))


# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    Robots are compered with timesteps for  clean room 10x10 vs  percentage cleaned
    """
    # TODO: Your code goes here
    x = []
    y= [] 
    res = computeMeans(runSimulation(1, 1.0, 10, 10, 1.0, 10, Robot, False))
    y = range(len(res))
    x = res 
    pylab.plot(x,y, label=f"Robot")
 
    res = computeMeans(runSimulation(1, 1.0, 10, 10, 1.0, 10, RandomWalkRobot, False))
    y = range(len(res))
    x = res 
    pylab.plot(x,y, label=f"RandomWalkRobot")
        
    pylab.legend(loc='upper center') 
    pylab.ylabel('Temesteps')
    pylab.xlabel('Percentage cleaned')
    pylab.show()
