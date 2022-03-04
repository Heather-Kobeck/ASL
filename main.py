
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


######################
###HELPER FUNCTIONS##
#####################

def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)


def main ():
    # make a hand detector
    handDetector = HandDetector()

    # make a clock object that will be used
    # to make the game run at a consistent framerate
    clock = pygame.time.Clock()

  # make a boolean that represents whether the game should continue to run or not
    running = True

    # loop through every frame of the video and show it (stops when you reach the end of the video)
    #this while loops through the game and the video feed
    while running == True:

        ### HAND DETECTION ###
        # update the webcam feed and hand tracker calculations
        handDetector.update()

        # if there is at least one hand seen, then
        # print out the landmark positions
        if len(handDetector.landmarkDictionary) > 0: 
            print(handDetector.landmarkDictionary[0])

        ###EVENT HANDLER #####
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


         #### GAME UPDATES #####   
         # put code here that should be run every frame
         # of your game             
        pygame.display.update()
    
    #at the end of the code this will help ensure that there are no more random windows 
    cv2.destroyAllWindows()




###### CALLING DA FUNCTIONS ######
main()
