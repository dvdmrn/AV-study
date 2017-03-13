import pygame
import time
import collections
import csv

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

car_width = 73

keylogData = collections.OrderedDict()


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('schwa.png')

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    # time.sleep(2)

    game_loop()
    
    

def crash():
    message_display('You Crashed')
    
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    gameExit = False

    initTime = time.time()

    pressVal = 0

    while not gameExit:
        # update time stamp
        currentTime = time.time()
        currentTime = currentTime - initTime 
        keylogData[currentTime] = pressVal

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pressVal = 1
                if event.key == pygame.K_RIGHT:
                    print keylogData
                if event.key == pygame.K_e:
                    exportVals(keylogData)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key==pygame.K_SPACE:
                    pressVal = 0

        x += x_change

        gameDisplay.fill(white)
        car(x,y)
        pygame.display.set_caption(str(time.time()))

        if x > display_width - car_width or x < 0:
            crash()
            
        
        pygame.display.update()
        clock.tick(60)

def exportVals(klData):
    with open('keylog_data.csv', 'w') as csvfile:
        fieldnames = ['time', 'keypress']
        writer = csv.writer(csvfile)
        # writer.writeheader()
        keylogData = klData.items()
        print "writing keylog_data.csv"
        for e in keylogData:
            writer.writerow(e)
        print "finished writing file"


game_loop()
pygame.quit()
quit()