import pygame
import random
import math

global alive, black, white, red, populationSize
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

maxSpeed = 2000

alive = 0
generations = 0
population=[]
best = [[999,[0,0]], [999,[0,0]]]

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

class Block(pygame.sprite.Sprite):

    ySpeed = 0
    xSpeed = 0

    speed = 0
    angle = 0

    stored = 0
        
    def __init__(self, color, width, height, speed, angle):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        pygame.draw.ellipse(self.image, color, [0,0,width, height])

        self.rect = self.image.get_rect()

        self.findSpeed(speed, angle)

        self.speed = speed
        self.angle = angle

    def update(self):
        global alive
        
        self.rect.y -= self.ySpeed
        self.rect.x += self.xSpeed
        self.ySpeed -= 9.8/fps

        if self.rect.y >= screen_height-20:
            self.ySpeed = 0
            self.xSpeed = 0
            if self.stored == 0:
                self.score()
                self.stored = 1
                alive -= 1
        else:
            self.ySpeed -= 9.8/fps

    def findSpeed(self, speed, angle):
        radians = math.radians(angle)

        self.ySpeed = (speed * math.sin(radians))/fps
        self.xSpeed = (speed * math.cos(radians))/fps

    def score(self):
        details = [self.speed, self.angle]
        score = xTarget - self.rect.x
        if score < 0:
            score = score * -1
        population.append([score, details])

def makeRandomRocket():
    speed = random.randrange(0, maxSpeed*5)
    speed = speed/5
    angle = random.randrange(0, 3600)
    angle = angle/10
    rocket = Block(black, 20, 20, speed, angle)
    rocket.rect.x = 0
    rocket.rect.y = screen_height-20

    all_sprites_list.add(rocket)
    rockets.add(rocket)

def findBest():
    global populationSize
    total = 0
    for k in range (populationSize):
        total += population[k][0]
        if population[k][0] < best[0][0]:
            best[0] = population[k]
        elif population[k][0] < best[1][0]:
            best[1] = population[k]

        if best[1][0] > best[0][0]:
            store0 = best[0]
            store1 = best[1]

            best[0] = store1
            best[1] = store0
    average = total/populationSize
    return average

def newPopulation():
    speedMutate = random.randrange(0,100)
    angleMutate = random.randrange(0,100)

    if speedMutate <= mutation:
        speed = random.randrange(0, maxSpeed * 5)
        speed = speed/5
    else:
        speedParent = random.randrange(0,1)
        if speedParent == 0:
            speed = best[0][1][0]
        else:
            speed = best[1][1][0]

    if angleMutate <= mutation:
        angle = random.randrange(0, 3600)
        angle = angle/10
    else:
        angleParent = random.randrange(0,1)
        if angleParent == 0:
            angle = best[0][1][1]
        else:
            angle = best[1][1][1]

    rocket = Block(black, 20, 20, speed, angle)
    rocket.rect.x = 0
    rocket.rect.y = screen_height-20

    all_sprites_list.add(rocket)
    rockets.add(rocket)
    

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

rockets = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

for k in range(populationSize):
    makeRandomRocket()
    alive += 1

target = Block(red, 20, 20, 0, 0)
target.rect.x = xTarget
target.rect.y = screen_height-20

all_sprites_list.add(target)

done = False

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(white)

    all_sprites_list.draw(screen)

    clock.tick(fps)

    pygame.display.flip()

    rockets.update()

    if alive == 0:
        generations += 1
        average = findBest()
        print(generations, "Average: ", average, best)

        if best[1][0] == 0:
            print("Found Solution: Speed = ",best[1][1][0],"; Angle = ",best[1][1][1]," Degrees.")
            print("This took ",generations," Generations")
            done = True
        else:
            population = []
            for k in range (populationSize):
                newPopulation()
                alive += 1

pygame.quit()

    
