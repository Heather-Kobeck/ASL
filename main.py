
############
##imports###
############
import mediapipe
import pygame
import cv2
from HandDetector import HandDetector


######################
####PYGAME SETUP######
######################

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
TanImg = pygame.transform.scale(TanImgPre, (WIDTH/2, HEIGHT/2))


######################
###HELPER FUNCTIONS##
#####################

def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)

    


def main():
    gameStages = ["home", "demo", "challenge", "instructions"]
    curStage = gameStages[1]
    correctGesture = False 

    # make a hand detector
    handDetector = HandDetector()

    # make a clock object that will be used
    # to make the game run at a consistent framerate
    clock = pygame.time.Clock()

  # make a boolean that represents whether the game should continue to run or not
    running = True

    # loop through every frame of the video and show it (stops when you reach the end of the video)
    # this while loops through the game and the video feed
    while running == True:

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

            colorsList = ["tan","blue","red","purple","green"]
            curColor = colorsList[0]
            

            ### HAND DETECTION ###
            # update the webcam feed and hand tracker calculations
            handDetector.update()


            #HANDLES COLOR TAN
            # 8 12 16 20 are below 9
            if curColor == colorsList[0]:
                WINDOW.blit(TanImg, (-125, -75))
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
                    else: 
                        correctGesture = False
                

                    if correctGesture:
                        WINDOW.fill((210,180,140))

            #HANDLES COLOR BLUE
                



                        
           
        
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
