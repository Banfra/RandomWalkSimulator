#Bastien Anfray 8INF802 – Simulation de systèmes
#Partie 3 - Utilisation du générateur

import randomGen
import pygame
import time
import sys
import math
import matplotlib.pyplot as plt

#variables initialization
steps = []
distArray = []
width = 700
height = 700
environment = []
arraytemp = []
userChoice = 0
userChoice2 = 0
i = 0
j = 0
first_i =0
first_j = 0
old_i = 0
old_j = 0
nbStep = 0
screen = 0
rect = 0
font = 0
pixel_size = 7
wait_time = 0.05
text = "Hello World"
test_number = 10000

array1 = []
array2 = []
array3 = []


#Just a random walk, the character go in a random direction at each step
def randomWalk():
    #variable initialization
    global i
    global j
    global old_i
    global old_j
    global nbStep
    global array1
    arraytemp = []
    # print("randomWalk")

    #for each number generated, we go on one of the four directions
    for step in steps:
        old_i = i
        old_j = j
        if step == 1:#North
            i = i-1
        elif step == 2:#East
            j = j+1
        elif step == 3:#South
            i = i+1
        elif step == 4:#West
            j = j-1
        
        #we increase the number of step
        nbStep += 1
        #we draw the new step we made
        if userChoice != 4:
            drawPixel(j,i)
        else:
            calculate_Distance(i,j, first_i, first_j, arraytemp)
    if arraytemp is not None:
        array1.append(arraytemp)


#Same as the random walk but the character can not come back on his last step
def nonReversingWalk():
    #variables initialization
    global i
    global j
    global old_i
    global old_j
    global nbStep
    global steps
    global environment
    global screen
    global array2
    global arraytemp
    oldStep = 0
    step_cancelled = 0
    environment[i][j] = 1

    # print("nonReversingWalk")
    
    #for each number generated, we go on one of the four directions. We verify that we do not come from this position
    for step in steps:
        #we put a 2 on the position of the step before now. It represents the position we can not go on
        environment[old_i][old_j] = 2
        if userChoice != 4:
            pygame.draw.rect(screen,(0,0,0),(old_j*pixel_size,old_i*pixel_size,pixel_size,pixel_size),1)
        
        if step == 1 and i-1 > -1 and environment[i-1][j] != 2:#North
            environment[old_i][old_j] = 1
            old_i = i
            old_j = j

            i = i-1
            environment[i][j] = 1
            calculate_Distance(i,j, first_i, first_j, arraytemp)
        elif step == 2 and j+1 < width/pixel_size and environment[i][j+1] != 2:#East
            environment[old_i][old_j] = 1
            old_i = i
            old_j = j

            j = j+1
            environment[i][j] = 1
            calculate_Distance(i,j, first_i, first_j, arraytemp)
        elif step == 3 and i+1 < height/pixel_size and environment[i+1][j] != 2:#South
            environment[old_i][old_j] = 1
            old_i = i
            old_j = j

            i = i+1
            environment[i][j] = 1
            calculate_Distance(i,j, first_i, first_j, arraytemp)
        elif step == 4 and j-1 > -1 and environment[i][j-1] != 2:#West
            environment[old_i][old_j] = 1
            old_i = i
            old_j = j

            j = j-1
            environment[i][j] = 1
            calculate_Distance(i,j, first_i, first_j, arraytemp)
        else: #if we come from this position (or we are in the limit of the array), we cancel the step and increase the number of cancelled steps
            step_cancelled += 1
            nbStep -= 1

        #we increase the number of step
        nbStep += 1
        #we draw the new step we made
        if userChoice != 4:
            drawPixel(j,i)
    
    if arraytemp is not None and nbStep == userChoice2:
        arr = []
        for a in range(0, len(arraytemp)):
            arr.append(arraytemp[a])
        array2.append(arr)
        

    #we regenerate random numbers because of the steps cancelled, we do not want to lose steps. Then we call the function nonReversingWalk again
    if step_cancelled > 0:
        steps = randomGen.generateSequence(1, 4, step_cancelled)
        nonReversingWalk()
    
    

#Same as the random walk but the character can not go somewhere he has been before
def selfAvoidingWalk():
    #variables initialization
    global i
    global j
    global old_i
    global old_j
    global nbStep
    global steps
    global environment
    global screen
    global array3
    global arraytemp
    oldStep = 0
    step_cancelled = 0
    environment[i][j] = 1
    blocked = 0

    # print("selfAvoidingWalk")
    
    #for each number generated, we go on one of the four directions. We verify that we have never been on one of the positions
    for step in steps:
        
        if step == 1 and i-1 > -1 and environment[i-1][j] != 1:#North
            old_i = i
            old_j = j

            i = i-1
            environment[i][j] = 1
            calculate_Distance(i,j, first_i, first_j, arraytemp)
        elif step == 2 and j+1 < width/pixel_size and environment[i][j+1] != 1:#East
            old_i = i
            old_j = j

            j = j+1
            environment[i][j] = 1
            calculate_Distance(i,j, first_i, first_j, arraytemp)
        elif step == 3 and i+1 < height/pixel_size and environment[i+1][j] != 1:#South
            old_i = i
            old_j = j

            i = i+1
            environment[i][j] = 1
            calculate_Distance(i,j, first_i, first_j, arraytemp)
        elif step == 4 and j-1 > -1 and environment[i][j-1] != 1:#West
            old_i = i
            old_j = j

            j = j-1
            environment[i][j] = 1
            calculate_Distance(i,j, first_i, first_j, arraytemp)
        #if we have ever been on the four directions, we are blocked and we stop the simulation
        elif(i-1 == -1 or i+1 == height/pixel_size or j-1 == -1 or j+1 == width/pixel_size):
            if userChoice != 4:
                print("BLOCKED at ", nbStep)
            elif userChoice == 4:
                if arraytemp is not None and nbStep < userChoice2:
                    arr = []
                    for a in range(0, len(arraytemp)):
                        arr.append(arraytemp[a])
                    array3.append(arr)
                    blocked = 1
            break
        elif (environment[i-1][j] == 1) and (environment[i+1][j] == 1) and (environment[i][j-1] == 1) and (environment[i][j+1] == 1):
            if userChoice != 4:
                print("BLOCKED at ", nbStep)
            elif userChoice == 4:
                if arraytemp is not None and nbStep < userChoice2:
                    arr = []
                    for a in range(0, len(arraytemp)):
                        arr.append(arraytemp[a])
                    array3.append(arr)
                    blocked = 1
            break
        else: #if we have ever been on the direction of the step (or we are in the limit of the array), we cancel the step and increase the number of cancelled steps
            step_cancelled += 1
            nbStep -= 1

        #we increase the number of step
        nbStep += 1
        #we draw the new step we made
        if userChoice != 4:
            drawPixel(j,i)
    
    if arraytemp is not None and nbStep == userChoice2 and blocked != 1:
        arr = []
        for a in range(0, len(arraytemp)):
            arr.append(arraytemp[a])
        array3.append(arr)

    #we regenerate random numbers because of the steps cancelled, we do not want to lose steps. Then we call the function selfAvoidingWalk again
    if step_cancelled > 0 and blocked != 1:
        steps = randomGen.generateSequence(1, 4, step_cancelled)
        selfAvoidingWalk()

#Choice selection function
def choiceSelection():
    #variables initialization
    global environment
    global steps
    global i
    global j
    global first_i
    global first_j
    global userChoice
    global userChoice2

    #Mode choosing. We can only choose 1, 2 or 3
    while userChoice not in [1, 2, 3, 4]:
        print("Welcome in the random Walk Program, please make your choice :\n1 - Random Walk\n2 - Non Reversing Walk\n3 - Self Avoiding Walk\n4 - All + see graph")
        userInput = input("Choose your walk : ")
        try:
            userChoice = int(userInput)
        except ValueError:
            print("That's not an int!")

    #Step number choosing (positive number only)
    while True:
        userInput2 = input("Put the number of steps you want (positive number) : ")
        try:
            userChoice2 = int(userInput2)
            if(userChoice2 > 0):
                break
        except ValueError:
            print("That's not an int!")

    #Generation of the steps (1 to 4 are directions North, East, South, West).
    steps = randomGen.generateSequence(1, 4, userChoice2)

    #the environment is an array of 0. His size is the height and width divided by the ratio of the 2D graphics (pixel_size)
    environment = [[0 for i in range(int(height/pixel_size))] for j in range(int(width/pixel_size))]

    #we start at the middle of the environment
    i = int(len(environment)/2)
    j = int(len(environment)/2)
    first_i = i
    first_j = j
    old_i = i
    old_j = j

    if userChoice != 4:
        pygameInit() #initialization of the pygame environment
    #the user choice call one of the 3 functions
    if userChoice == 1:
        randomWalk()
    elif userChoice == 2:
        nonReversingWalk()
    elif userChoice == 3:
        selfAvoidingWalk()
    elif userChoice == 4:
        runAll()
    
def calculate_Distance(x,y,xx,yy, array):
    dist = math.dist([x,y],[xx,yy])
    array.append(dist)


#initialization of the 2D environment
def pygameInit():
    #variables initialization
    global screen
    global text
    global nbStep
    global font
    global rect
    pygame.init()

    #we set the window size and fill it with white
    screen = pygame.display.set_mode((width, height))
    screen.fill((255,255,255))

    #we display the number of steps in the up left corner
    font = pygame.font.SysFont(None, 20)
    img = font.render(str(nbStep), True, (0,0,0))
    rect = img.get_rect()
    rect.topleft = (20, 20)

    pygame.display.update()

#this function draw on the 2d environment
def drawPixel(x, y):
    #variables initialization
    global old_i
    global old_j
    global rect
    global userChoice

    #we update the display of the environment and think about quitting the simulation
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()

    #we create a pixel and fill it with blue
    pixel = pygame.Surface((pixel_size, pixel_size))
    pixel.fill((0,0,255))
    #we draw the pixel on the screen
    screen.blit(pixel,(x*pixel_size,y*pixel_size))
    #We draw a red rectangle on the current pixel
    pygame.draw.rect(screen,(255,0,0),(x*pixel_size,y*pixel_size,pixel_size,pixel_size),1)
    #if we are on a non reversing walk, we draw a green rectangle on the pixel of the step before now
    if userChoice == 2:
        pygame.draw.rect(screen,(0,255,0),(old_j*pixel_size,old_i*pixel_size,pixel_size,pixel_size),1)
    #else we draw a black rectangle on it
    else:
        pygame.draw.rect(screen,(0,0,0),(old_j*pixel_size,old_i*pixel_size,pixel_size,pixel_size),1)

    #displaying the number of steps
    text = nbStep
    img = font.render(str(nbStep), True, (0,0,0))
    rect = img.get_rect()
    rect.topleft = (20, 20)
    #we clear the old text with a rectangle
    pygame.draw.rect(screen, (255,255,255),rect,0)
    #we draw the text on the rectangle
    screen.blit(img, rect)
    #we update the display
    pygame.display.update()
    #we wait to have the time to see the simulation

    time.sleep(wait_time)

def calculateMean(array):
    arraymean = [0 for a in range(userChoice2)]
    mean = 0
    val = 0
    nb_val = [0 for a in range(userChoice2)]
    for a in range(0, len(array)):
        for step_number in range(1, userChoice2):
            if len(array[a]) >= step_number:
                val = array[a][step_number-1]
                arraymean[step_number-1] += val
                nb_val[step_number - 1] += 1

    for a in range(0, len(arraymean)):
        if nb_val[a] != 0:
            arraymean[a] = pow(arraymean[a]/nb_val[a],2)

        if arraymean[a] == 0 and a > 0 :
            arraymean[a] = arraymean[a-1]
    return arraymean


def runAll():
    global wait_time
    wait_time = 0
    for a in range(0,test_number):
        reset()
        randomWalk()
        reset()
        nonReversingWalk()
        reset()
        selfAvoidingWalk()
    drawAllPlots()

def drawAllPlots():
    print(len(array1))
    print(len(array2))
    print(len(array3))

    array1mean = calculateMean(array1)
    array2mean = calculateMean(array2)
    array3mean = calculateMean(array3)


    l1 = plt.plot(array1mean, label = 'randomWalk')
    l2 = plt.plot(array2mean, label = 'nonReversingWalk')
    l3 = plt.plot(array3mean, label = 'selfAvoidingWalk')
    plt.legend()
    plt.ylabel("Distance de l'origine")
    plt.xlabel("Nombre de pas")
    plt.show()

def reset():
    global nbStep
    global i
    global j
    global old_i
    global old_j
    global steps
    global environment

    environment = [[0 for i in range(int(height/pixel_size))] for j in range(int(width/pixel_size))]
    nbStep = 0
    i = int(len(environment)/2)
    j = int(len(environment)/2)
    old_i = i
    old_j = j
    steps = randomGen.generateSequence(1, 4, userChoice2)
    arraytemp.clear()

#Main
choiceSelection() #choice selection, environment creation and generation of the steps
if userChoice != 4:    
    while(True):
        #we wait for an event to happen
        event = pygame.event.wait()
        #we think about quitting the simulation
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
