
import time, sys, os, pygame
from pygame.locals import *                #Allows easier use of pygame functions
#from tkinter import *
#from PIL import Image, ImageTk
pygame.init() #Initializes pyGame
clock = pygame.time.Clock()         #Limits FPS to 60

ScreenSizeObj = pygame.display.Info()
worldx, worldy = ScreenSizeObj.current_w,ScreenSizeObj.current_h
screen = pygame.display.set_mode([worldx, worldy])
ty = 64
tx = 64
level = 1
running = True


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.alive = True
        self.movey = 0
        self.aniCounter = 0
        self.vertSpeed = 0
        self.curFrame = 0
        self.accRem = 0
        self.images = []

        self.aniCycles = 2


        self.jumpForce = 1
        self.gravStrength = 1
        self.moveSpeed = 5
        self.accSpeed = 20
        
        
        self.isFlipped = False
        for i in range(1,self.aniCycles + 1): #Loads the two frames of animation
            img = pygame.image.load(os.path.join("pyGame_Image_Folder","Animation","Platformer","Knight","KnightWalk" + str(i) + ".png"))
            #an easier way to add more frames of the animation - just add 1 more number to the next file
            img.convert_alpha()
            self.images.append(img)
            self.image = self.images[self.curFrame]
            self.rect = self.image.get_rect()
            print(self.images)

    def gravity(self):
        if self.rect.y <= worldy-ty-ty:        #If character position above world bottom(in the air):
            self.accRem -= self.gravStrength         #Acceleration decreases by grav strength
                                        #FOUND ISSUE: NOT REGISTERING AS 'ON GROUND'
        else:                                        #else
            if self.accRem < 0:                               #if accelleration is negative and on the ground::
                self.vertSpeed = 0                                #Stop falling
                self.accRem = 0                                   #and kill all momentum
                
                      
            
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_SPACE]:
            if self.rect.y >= worldy -ty -ty:       #If not in the air(on the ground) and space pressed:
                self.accRem += self.jumpForce               #Accelleration increases by jump force
                print(self.accRem)                      

                  
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-self.moveSpeed, 0)
                  self.isFlipped = True
        if self.rect.right < worldx:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(self.moveSpeed, 0)
                  self.isFlipped = False
        if pressed_keys[K_ESCAPE]:
            running = False

        if self.aniCounter >= 10:                                    #Reduces the speeed of the animation 10x
            if self.curFrame >= self.aniCycles:                        #Resets the frame whenever it loops
                self.curFrame = 0
            self.image = self.images[self.curFrame]
            self.curFrame += 1
            self.aniCounter = 0

        self.vertSpeed += self.accRem


        
        self.aniCounter += 1
      #  if self.rect.y > worldy -ty -ty:# or self.accRem > 0:                           #if player height greater/equal to (lowest screen height - sprite height)
        self.rect.move_ip(0, -self.vertSpeed)                           #move vertically according to their speed                           
    def death(self):
        self.alive = False

    
    def draw(self, surface):
        if self.alive == True:
            if self.isFlipped == True:
                screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
            else:
                screen.blit(self.image, self.rect)


class BatVert(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        self.curFrame = 0
        self.aniCycles = 2
        self.aniCounter = 0
        self.upSwing = False
        for i in range(1,self.aniCycles + 1):
            img = pygame.image.load(os.path.join("pyGame_Image_Folder","Animation","Platformer","Bat","BatFly", "BatFly"+ str(i) + ".png"))
            self.images.append(img)
            self.image = self.images[self.curFrame]
            self.rect = self.image.get_rect()
        self.rect.move_ip(worldx // 2, 0)
    def update(self):
        if self.rect.y >= worldy - (2 * ty):
            self.upSwing = True
        if self.rect.y <= worldy // 2 :
            self.upSwing = False
            
        if self.upSwing == True:
            self.rect.move_ip(0, -3)
        if self.upSwing == False:
            self.rect.move_ip(0, 3)


        if self.aniCounter >= 10:                                    #Reduces the speeed of the animation 15x
            if self.curFrame >= self.aniCycles:                        #Resets the frame whenever it loops
                self.curFrame = 0
            self.image = self.images[self.curFrame]
            self.curFrame += 1
            self.aniCounter = 0
        self.aniCounter += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Platform(pygame.sprite.Sprite):
    def __init__(self,xloc, yloc, imgw, imgh, img):
        super().__init__()
        self.image = pygame.image.load("pyGame_Image_Folder/Terrain/Platformer/FloatingIsland/Floating_Island_1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc
        imgw = 128
        imgh = 64
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
class Spike(pygame.sprite.Sprite):
    def __init__(self,xloc, yloc, imgw, imgh, img):
        super().__init__()
        self.image = pygame.image.load("pyGame_Image_Folder/Animation/Platformer/Obstacles/Spike/Spike1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc
        imgw = 128
        imgh = 128
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Level:                                             
    def ground(level,gloc,tx,ty):
        ground_list = pygame.sprite.Group()
        i = 0
        if level == 1:
            tileGround = pygame.image.load("pyGame_Image_Folder/Terrain/Platformer/Floor/Ground1.png")
            while i < len(gloc):
                ground = Platform(gloc[i], worldy - ty, tx, ty, tileGround)
                ground_list.add(ground)
                i += 1
                
    def spike(level, tx, ty):
        spike_list = pygame.sprite.Group()
        sploc = []                                       #sploc is a list which determines the location of the spikes e.g. [0, 642,screenY,256]. it may be more efficient to add locs here
        i = 0
        if level == 1:
             #Place spike locations for stage 1 here
             sploc.append((worldy, worldx // 2))
             sploc.append((worldy // 2, worldx // 2))
             sploc.append((0, 0))
             while i < len(sploc):                                    
                j = 0
                while j <= sploc[i][2]:
                    spike = Spike((sploc[i][0] + (j * tx)), sploc[i][1], tx, ty, pygame.image.load("pyGame_Image_Folder/Animation/Platformer/Obstacles/Spike/Spike1.png"))
                    spike_list.add(spike)
                    j = j + 1
                i = i + 1
        if level == 2:
            print("not yet complete")
        return spike_list                  
                
    #add enemy spawn loc here

    def platform(level, tx, ty):
        plat_list =pygame.sprite.Group()
        ploc = []                                       #ploc is a list which determines the location of the platforms e.g. [0, 642,screenY,256]
        i = 0
        if level == 1:
            #Place platform locations for stage 1 here
            ploc.append((worldx // 2, worldy - ty - ty, 3))
            ploc.append((worldx-768, worldy - ty - 392, 3))
            ploc.append((worldx-1024, worldy - ty - 392, 3))
            while i < len(ploc):
                j = 0
                while j <= ploc[i][2]:
                    plat = Platform((ploc[i][0] + (j * tx)), ploc[i][1], tx, ty, pygame.image.load("pyGame_Image_Folder/Terrain/Platformer/FloatingIsland/Floating_Island_1.png"))
                    plat_list.add(plat)
                    j = j + 1
                i = i + 1
        if level == 2:
            print("not yet complete")
        return plat_list
    
class Updraft(pygame.sprite.Sprite):
        print("asdf")
            

    
gloc = [0,worldy,128,worldy,256,worldy,384,worldy,512,worldy,640,worldy]
i = 0

while i <= (worldx / tx) + tx:
    gloc.append(i * tx)
    i = i + 1
    
ground_list = Level.ground(1, gloc, tx, ty)
plat_list = Level.platform(1, tx, ty)
#spike_list = Level.spike(1, tx, ty)


player = Player() #spawn the player char
batvert = BatVert()   #spawn the enemy bat
player.rect.y = worldy - ty - ty        #Places player on ground





#Loop for the majority of the actual game
while running == True:
    clock.tick(60)
    #Allows quitting the game without Task Manager
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.gravity()

    player.update()
    batvert.update()


    player.draw(screen)
    batvert.draw(screen)
 #   ground_list.draw(screen)
    plat_list.draw(screen)
 #   spike_list.draw(screen)
#    if pygame.Rect.colliderect(spike1.rect,player.rect):
 #       player.death()
        

    pygame.display.update()
    screen.fill("blue")
