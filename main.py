
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



######################
###HELPER FUNCTIONS##
#####################

def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)

def handleMouse ():
    left, middle, right = pygame.mouse.get_pressed()
 
    if left:
        print("Left Mouse Key is being pressed")
    


def main():
    gameStages = ["home", "demo", "challenge", "instructions"]
    curStage = gameStages[0]

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

            lettersList = ["a","b","c","d"]
            curletter = lettersList[0]

            ### HAND DETECTION ###
            # update the webcam feed and hand tracker calculations
            handDetector.update()

            # if there is at least one hand seen, then
            # print out the landmark positions
            if len(handDetector.landmarkDictionary) > 0:
                print(handDetector.landmarkDictionary[0][0][0])

            
            if curletter == lettersList[0]:
               x = handDetector.landmarkDictionary[0][0][1]
               print(x)
               
           
        
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
