import pygame

pygame.init()

win = pygame.display.set_mode((500,480))
pygame.display.set_caption('First Game')
clock = pygame.time.Clock()
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
screenwidth = 500
score = 0
bulletSound = pygame.mixer.Sound('bullet_fire.wav')
hitSound = pygame.mixer.Sound('bullet_hit.wav')
music = pygame.mixer.music.load('music.ogg')
pygame.mixer.music.play(-1)


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 5 
        self.isJump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y +11, 30, 51)  # rectangle  x,y,width,height
    
    def draw(self,win):
    
        if self.walkCount + 1 >= 27: # 9 images for left & right both and moving 3 frames for each count . ie 27 fps
            self.walkCount =0 
        if not(self.standing):
            
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount+= 1
            elif self.right :
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount+= 1
        else :
            if self.right:
                win.blit(walkRight[0],(self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 30, 51)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpcount = 10

        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text1 = font1.render(' - 5 ',1 , (255,0,0))
        win.blit(text1, (250 - (text1.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


         
        

class enemy(object):

    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self, x, y, width, height, end ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 6
        self.hitbox = (self.x + 22, self.y, 28 , 60)
        self.health = 10
        self.visible = True

    
    def draw(self, win):
        self.move()
        if self.visible: 
                
            if self.walkCount >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1 
            self.hitbox = (self.x + 22, self.y, 28, 60)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1]-25, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1]-25, 50 - (5 * (10 - self.health)), 10))
             

    
    def move(self):
        if self.vel > 0: # enemy moving right
            if self.x + self.vel < self.path[1]: # we will allow the enemy to move 
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    
    def hit(self):
        if self.health > 0:
            self.health-=1
        else:
            self.visible = False
             

        print('GOBLIN IS HIT.')


        

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 14  * facing

    def draw(self, win):
        pygame.draw.circle(win , self.color, (self.x , self.y), self.radius)







def redrawGameWindow():
    win.blit(bg,(0,0))
    man.draw(win)
    text = font.render('SCORE : '+ str(score), 1, (0,0,0))
    win.blit(text, (320, 20)) 
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


man = player(300, 400 , 64, 64)
goblin = enemy(100, 400, 64, 64, 460) 
bullets = []
font = pygame.font.SysFont('comicsans', 40, True, True)

run = True
# main loop to work
while run:
    clock.tick(27)
    if goblin.visible == True:

        if man.hitbox[1]  < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:   # first checks if we are above the bottom of rect and second checks if we are below the top of the rect
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score-=5
            
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:

        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:   # first checks if we are above the bottom of rect and second checks if we are below the top of the rect
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                hitSound.play()
                score+=1
                bullets.remove(bullet)
        if bullet.x < 500 and bullet.x >0:
            bullet.x+= bullet.vel
        else:
            bullets.remove(bullet)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets)<5:
            bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0,0,255),facing))
    
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -=man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screenwidth - man.width - man.vel:
        man.x+=man.vel
        man.left = False
        man.right = True
        man.standing = False
    else :
        man.standing = True
        man.walkCount = 0

    if not(man.isJump):
        # if keys[pygame.K_UP] and y > vel:
        #     y-=vel
        # if keys[pygame.K_DOWN] and y < screenwidth - height -vel:
        #     y+=vel
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = False
    else:
        if man.jumpcount >= -10:
            neg = 1
            if man.jumpcount < 0:
                neg = -1
            man.y -= (man.jumpcount ** 2) * (0.5) * neg  
            man.jumpcount-=1
        else:
            man.isJump = False
            man.jumpcount = 10

    redrawGameWindow()

pygame.quit()
