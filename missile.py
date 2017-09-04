import pygame
import random
import math

global alive, black, white, red, green, blue, populationSize, xPosition, yPosition
screen_width = 1200
screen_height = 600
fps=60

#Variables for test
xTarget = int(input("Enter the x-coordinates of the target (0-1200): "))
while xTarget <0 or xTarget > 1200:
    print("Enter a value between 0 & 1200")
    xTarget = int(input("Enter the x-coordinates of the target (0-1200): "))

populationSize = int(input("Enter the number of members of each population: "))
while populationSize < 1:
    print("Enter a number greater than 0")
    populationSize = ("Enter the number of members of each population: ")

mutation = int(input("Enter the % chance of an element's attribute mutating: "))
while mutation < 0 or mutation > 100:
    print("Enter a number between 0 and 100")
    mutation = int(input("Enter the % chance of an element's attribute mutating: "))

maxSpeed = 3000 #Can be changed, but needs to be significantly high to reach target

alive = 0 #How many missiles haven't landed
generations = 0 #How many generations have lived
population=[] #Stores score, speed & angle of all living missiles
best = [[9999,[0,0]], [9999,[0,0]]] #Two best scoring missiles

solved = False #Has a solution been found

#Used to trace tail
xPosition = 0
yPosition = 0

#Colours
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

class Block(pygame.sprite.Sprite): #Missile & target class

    #Used to move missile
    ySpeed = 0
    xSpeed = 0

    #Used to store in population[]
    speed = 0
    angle = 0

    #Used to make sure missile is stored in population[] only once
    stored = 0
        
    def __init__(self, color, width, height, speed, angle): #Initialisation function
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        pygame.draw.ellipse(self.image, color, [0,0,width, height])

        self.rect = self.image.get_rect()

        self.findSpeed(speed, angle) #Uses trig to find y & x speed

        #Saves variables to store later
        self.speed = speed
        self.angle = angle

    def update(self): #Move missile
        global alive
        
        self.rect.y -= self.ySpeed
        self.rect.x += self.xSpeed

        if self.rect.y >= screen_height-20: #If missile hits floor, stop
            self.ySpeed = 0
            self.xSpeed = 0
            if self.stored == 0:
                self.score()
                self.stored = 1
                alive -= 1
        else:  #Create parabolic arc
            self.ySpeed -= 9.8/fps

    def findSpeed(self, speed, angle): #Uses trig to find y & x speed
        radians = math.radians(angle)

        self.ySpeed = (speed * math.sin(radians))/fps
        self.xSpeed = (speed * math.cos(radians))/fps

    def score(self): #Scores the missile, score = distance from target, lower score = better
        details = [self.speed, self.angle]
        score = xTarget - self.rect.x
        if score < 0:
            score = score * -1
        population.append([score, details])

    def storePosition(self): #Saves score, speed & angle so can find best later
        global xPosition, yPosition
        xPosition = self.rect.x
        yPosition = self.rect.y

class Trail(pygame.sprite.Sprite): #Trail sprite. Smaller & static

    def __init__(self, color, y, x):
        super().__init__()

        self.image = pygame.Surface([5,5])
        self.image.fill(color)

        pygame.draw.ellipse(self.image, color, [0,0,5,5])
        self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x

def makeRandomRocket(): #Makes missiles for first round, completely random speed & angle
    speed = random.randrange(0, maxSpeed*100)
    speed = speed/100
    angle = random.randrange(0, 36000)
    angle = angle/100
    rocket = Block(black, 20, 20, speed, angle)
    rocket.rect.x = 0
    rocket.rect.y = screen_height-20

    all_sprites_list.add(rocket)
    rockets.add(rocket)

def findBest(): #Finds two best scoring missile
    global populationSize
    total = 0
    for k in range (populationSize):
        total += population[k][0]
        if population[k][0] < best[0][0]:
            best[0] = population[k]
        elif population[k][0] < best[1][0]:
            best[1] = population[k]

        if best[1][0] > best[0][0]: #Order scores so best[0] is less than best[1]
            store0 = best[0]
            store1 = best[1]

            best[0] = store1
            best[1] = store0
    average = total/populationSize
    return average

def newPopulation(): #Creates future generations
    speedMutate = random.randrange(0,100)
    angleMutate = random.randrange(0,100)

    if speedMutate <= mutation: #Mutate, completely rando speed
        speed = random.randrange(0, maxSpeed * 100)
        speed = speed/100
    else: #Don't mutate, take one of parents' values
        speedParent = random.randrange(0,1)
        if speedParent == 0:
            speed = best[0][1][0]
        else:
            speed = best[1][1][0]

    if angleMutate <= mutation: #Mutate, completely random angle
        angle = random.randrange(0, 36000)
        angle = angle/100
    else: #Don't mutate, take one of parents' values
        angleParent = random.randrange(0,1)
        if angleParent == 0:
            angle = best[0][1][1]
        else:
            angle = best[1][1][1]

    rocket = Block(black, 20, 20, speed, angle) #create new rocket

    #Place rocket at origin
    rocket.rect.x = 0
    rocket.rect.y = screen_height-20

    #Add to lists
    all_sprites_list.add(rocket)
    rockets.add(rocket)
    
def newPopulationBetter(): #Creates future generations
    speedParent = random.randrange(0,1)
    angleParent = random.randrange(0,1)

    #Take one of parents' speed values
    if speedParent == 0:
        speed = best[0][1][0]
    else:
        speed = best[1][1][0]

    #Take one of parent's angle values
    if angleParent == 0:
        angle = best[0][1][1]
    else:
        angle = best[1][1][1]

    speedMutate = random.randrange(0,100)
    angleMutate = random.randrange(0,100)

    #Mutate speed, change by 1% of max (+ or -)
    if speedMutate <= mutation:
        speed = speed + (random.randrange(-maxSpeed, maxSpeed))/100

    #Mutate angle, change by up to 3.6% (+ or -)
    if angleMutate <= mutation:
        angle = angle + (random.randrange(-3600, 3600))/1000

    rocket = Block(black, 20, 20, speed, angle) #Create new rocket

    #Place rocket at origin
    rocket.rect.x = 0
    rocket.rect.y = screen_height - 20

    #Add to lists
    all_sprites_list.add(rocket)
    rockets.add(rocket)
    
    
pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

#Define groups
rockets = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
trail_list = pygame.sprite.Group()

#Make first generation of missiles
for k in range(populationSize):
    makeRandomRocket()
    alive += 1

#Create + place target mark
target = Block(red, 20, 20, 0, 0)
target.rect.x = xTarget
target.rect.y = screen_height-20

trail_list.add(target)

done = False

clock = pygame.time.Clock()

while not done:
    if solved == False: #While trying to find solution
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(white)#Clear screen

        #Add sprites to screen
        all_sprites_list.draw(screen)
        trail_list.draw(screen)

        clock.tick(fps)

        pygame.display.flip()

        rockets.update()

        if alive == 0: #When all missiles have landed
            generations += 1 #Increment generation count
            average = findBest() #Find best scores & average distance from target
            print(generations, "Average: ", average, best)#Output information on generation

            if best[1][0] == 0: #If target has been hit
                print("Found Solution: Speed = ",best[1][1][0],"; Angle = ",best[1][1][1]," Degrees.")#Output solution details
                print("This took ",generations," Generations")#Output test information
                solved = True #Mark problem as solved

                #Start trail
                speed = best[1][1][0]
                angle = best[1][1][1]
                trailLeader = Block(green, 20, 20, speed, angle)
                trailLeader.rect.x = 0
                trailLeader.rect.y = screen_height-20
                trail_list.add(trailLeader)

            else: #Move + draw missiles
                all_sprites_list.empty()
                population = []
                for k in range (populationSize):
                    newPopulationBetter()
                    alive += 1
    else: #Draw trail
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        clock.tick(fps)
        pygame.display.flip()

        screen.fill(white)
        trailLeader.update()

        trailLeader.storePosition()

        point = Trail(blue, yPosition, xPosition)
        trail_list.add(point)

        trail_list.draw(screen)

pygame.quit()

    
