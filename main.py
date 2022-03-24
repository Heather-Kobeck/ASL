
############
##imports###
############
import mediapipe
import py
import pygame
import cv2
import time
from HandDetector import HandDetector


######################
####PYGAME SETUP######
######################
pygame.init()

#### setup up fonts ####
font = pygame.font.Font('freesansbold.ttf', 32)


# Define the size of the game window
WIDTH = 1200
HEIGHT = 800
# make the game window object
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# name the game window
pygame.display.set_caption("ASL Learning Game")



# Image Loading 
homeImgPre = pygame.image.load("Assets/StartScreen.png")
homeImg = pygame.transform.scale(homeImgPre, (WIDTH, HEIGHT))

TanImgPre = pygame.image.load("Assets\TanDemo.png")
TanImg = pygame.transform.scale(TanImgPre, (800, 800))

BlueImgPre = pygame.image.load("Assets\BlueDemo.png")
BlueImg = pygame.transform.scale(BlueImgPre,(450,450))

RedImgPre = pygame.image.load("Assets\RedDemo.png")
RedImg = pygame.transform.scale(RedImgPre,(350,350))

correctImgPre = pygame.image.load("Assets\Correct.png")
correctImg = pygame.transform.scale(correctImgPre, (800, 850))

######################
###HELPER FUNCTIONS##
#####################

def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)

    


def main():
    gameStages = ["home", "demo", "challenge", "instructions"]
    curStage = gameStages[0]
    correctGesture = False 
    updateTime = True

    # make a hand detector
    handDetector = HandDetector()

    # make a clock object that will be used
    # to make the game run at a consistent framerate
    clock = pygame.time.Clock()

  # make a boolean that represents whether the game should continue to run or not
    running = True

    # loop through every frame of the video and show it (stops when you reach the end of the video)
    # this while loops through the game and the video feed
    colorsList = ["Tan","Blue","Red","Purple","Green"]
    curColor = colorsList[0]

    while running == True:
        clock.tick(60)

        ########HOME SCREEN########

        if curStage == "home":
            WINDOW.fill((0,0,0))
            WINDOW.blit(homeImg,(0,0))

            ### mouse detection for start button ##
            if pygame.mouse.get_pos()[0] > 343 and pygame.mouse.get_pos()[1] > 480 and pygame.mouse.get_pos()[0] < 670 and  pygame.mouse.get_pos()[1] < 600:
                    left, middle, right = pygame.mouse.get_pressed()
                    if left:
                        curStage = gameStages[1]

            ## mouse detection for instruct button ##
            if pygame.mouse.get_pos()[0] > 343 and pygame.mouse.get_pos()[1] > 650 and pygame.mouse.get_pos()[0] < 670 and  pygame.mouse.get_pos()[1] < 850:
                    left, middle, right = pygame.mouse.get_pressed()
                    if left:
                        curStage = gameStages[3]

        
        ########DEMO MODE##########
        if curStage == "demo":
            WINDOW.fill((0,0,0))

           

            ### HAND DETECTION ###
            # update the webcam feed and hand tracker calculations
            handDetector.update()


            ########### HANDLES COLOR TAN #############
            # 8 12 16 20 are below 9
            if curColor == colorsList[0]:
                WINDOW.blit(TanImg, (-225, -225))
                text = "Use Your Left Hand to Sign the Color " + curColor
                displayText = font.render(text, True, (255,0,255))
                WINDOW.blit(displayText, (310, 50))
                joints = [8, 12, 16, 20]
                numJointsDown = 0
                
                # if there is at least one hand seen, then
                # print out the landmark positions
                if len(handDetector.landmarkDictionary) > 0:
                    # print(handDetector.landmarkDictionary[0][0][0])
                    for i in joints:
                        if handDetector.landmarkDictionary[0][i][1] > handDetector.landmarkDictionary[0][9][1] and handDetector.landmarkDictionary[0][i - 2][1] > handDetector.landmarkDictionary[0][4][1]  :
                            numJointsDown += 1
                        else:
                            numJointsDown -= 1

                    if numJointsDown == len(joints) and handDetector.landmarkDictionary[0][4][0] <= handDetector.landmarkDictionary[0][7][0]:
                        correctGesture = True
                        if(updateTime):
                            startTime = time.time()
                            updateTime = False
                    else: 
                        correctGesture = False
                        updateTime = True
                

                    if correctGesture:
                        inc = 2
                        curTime = time.time()
                        WINDOW.fill((210,180,140))
                        WINDOW.blit(correctImg, (195, -25))

                        ## forces the program to wait for a solid 2 seconds before allowing next stage ##
                        if(curTime - startTime > inc):
                            curColor = colorsList[1]
                            updateTime = True
                        


            ##########HANDLES COLOR BLUE ################
            if curColor == colorsList[1]:
                ## setup from previous stage ##
                correctGesture = False 
                WINDOW.fill((0,0,0))
                WINDOW.blit(BlueImg, (-175, -90))
                text = "Use Your Left Hand to Sign the Color " + curColor
                displayText = font.render(text, True, (255,0,255))
                WINDOW.blit(displayText, (310, 50))

                joints = [8, 12, 16, 20]
                numJointsUp = 0

                if len(handDetector.landmarkDictionary) > 0:
                    j = 1
                    for i in joints:
                        if handDetector.landmarkDictionary[0][i][1] < handDetector.landmarkDictionary[0][9][1] and handDetector.landmarkDictionary[0][i - 2][1] < handDetector.landmarkDictionary[0][4][1]:

                            if abs(handDetector.landmarkDictionary[0][8][2] - handDetector.landmarkDictionary[0][8][2]) < 2 :
                                 numJointsUp += 1
                            else:
                                 numJointsUp -= 1

                    if numJointsUp == len(joints) and handDetector.landmarkDictionary[0][4][0] <= handDetector.landmarkDictionary[0][7][0] and handDetector.landmarkDictionary[0][5][2] - handDetector.landmarkDictionary[0][17][2] > 8 :
                        correctGesture = True
                        if(updateTime):
                            startTime = time.time()
                            updateTime = False
                    else: 
                        correctGesture = False
                

                    if correctGesture:
                        inc = 2
                        curTime = time.time()
                        WINDOW.fill((10,50,150))
                        WINDOW.blit(correctImg, (195, -25))

                        ## forces the program to wait for a solid 2 seconds before allowing next stage ##
                        if(curTime - startTime > inc):
                            curColor = colorsList[2]
                            updateTime = True

        ########### HANDLES COLOR RED #############
            if(curColor == colorsList[2]):
                ## setup from previous stage ##
                correctGesture = False 
                WINDOW.fill((0,0,0))
                WINDOW.blit(RedImg, (-50, -25))
                text = "Use Your Left Hand to Sign the Color " + curColor
                displayText = font.render(text, True, (255,0,255))
                WINDOW.blit(displayText, (310, 50))

                 # if there is at least one hand seen, then
                # print out the landmark positions

                joints = [12, 16, 20]
                numJointsDown = 0

                if len(handDetector.landmarkDictionary) > 0:
                    # print(handDetector.landmarkDictionary[0][0][0])
                    for i in joints:
                        if handDetector.landmarkDictionary[0][i][1] > handDetector.landmarkDictionary[0][i -2][1]:
                            numJointsDown += 1
                        else:
                            numJointsDown -= 1

                    if numJointsDown == len(joints) and handDetector.landmarkDictionary[0][8][1] <= handDetector.landmarkDictionary[0][6][1]:
                        if  abs(handDetector.landmarkDictionary[0][3][0] - handDetector.landmarkDictionary[0][5][0]) < 15:
                            correctGesture = True
                            if(updateTime):
                                startTime = time.time()
                                updateTime = False
                    else: 
                        correctGesture = False
                        updateTime = True
                

                    if correctGesture:
                        inc = 2
                        curTime = time.time()
                        WINDOW.fill((255,40,40))
                        WINDOW.blit(correctImg, (195, -25))

                        ## forces the program to wait for a solid 2 seconds before allowing next stage ##
                        if(curTime - startTime > inc):
                            
                            curColor = colorsList[3]
                            updateTime = True
                        



                    

        
        ########CHALLENGE MODE########
        if curStage == "challenge":
            WINDOW.fill((0,0,0))
            WINDOW.blit(homeImg,(0,0))

        ######## INSTRUCTIONS SCREEN #########

        if curStage == "instructions":
            WINDOW.fill((0,0,0))
            


        ####### THINGS THAT SHOULD WORK IN ALL STAGES ##########        

        ###EVENT HANDLER #####
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #### GAME UPDATES #####
        # put code here that should be run every frame
        # of your game
        pygame.display.update()

    # at the end of the code this will help ensure that there are no more random windows
    cv2.destroyAllWindows()


###### CALLING DA FUNCTIONS ######
main()
