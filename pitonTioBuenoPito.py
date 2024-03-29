import pygame
import socket
from threading import Thread

#Functions

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

#Pseudo-constants
pygame.init()
resInfo = pygame.display.Info()
resolution = [resInfo.current_w,  resInfo.current_h]
ballRadius = 40
gravity = 0.5
jumpForce = 15

host ="127.0.0.1"
port = 9090

#Colors
backgroundColor = (170, 170, 255)
floorColor = (30,200,30)
pColors = [(255,0,0),(0,0,255)]
ballColor = (255, 255, 255)

#Rects
screen = pygame.display.set_mode(resolution)

floorImg = pygame.Surface((resolution[0], resolution[1]/3))
floorm = pygame.mask.from_surface(floorImg)

pPos = [
[resolution[0]/4 - resolution[0]/20/2, resolution[1]/3],
    [resolution[0] - resolution[0]/4 - resolution[0]/20/2, resolution[1]/3]
]
floorPos = (0, 2*resolution[1]/3)

players = [pygame.mask.Mask, pygame.mask.Mask]

img1 = pygame.Surface((resolution[0]/20, resolution[1]/5)).convert_alpha()
img2 = pygame.Surface((resolution[0]/20, resolution[1]/5)).convert_alpha()

ballPos = (int(resolution[0]/2) - ballRadius/2, int(resolution[1]/2))
ballr1 = pygame.Rect((ballPos[0] - ballPos[0]/2, ballPos[1] - ballPos[1]/2), (ballRadius, ballRadius))
ballr2 = pygame.Rect((ballPos[0] - ballPos[0]/2, ballPos[1] - ballPos[1]/2), (ballRadius, ballRadius))

## GAME ##

running = True

speeds = [[0,0],[0,0]]
grounded = [False, False]
data = ""
alone = True
clock = pygame.time.Clock()

#Networking

def listen():
	global data
	while True:
		data = soc.recv(1024).decode()

soc = socket.socket()
soc.connect((host, port))
Thread(target=listen, daemon=True).start()

#Main bucle
while running:
       #Clock
       clock.tick(60)
       
       #Drawing
       screen.fill(backgroundColor)
       
       floorImg.fill(floorColor)
       screen.blit(floorImg, floorPos)
       
       pygame.draw.circle(screen, ballColor, ballPos, ballRadius)
       
       rotp1, rotr1 = rot_center(img1, 0, pPos[0][0], pPos[0][1])
       rotp2, rotr2 = rot_center(img2, 0, pPos[1][0], pPos[1][1])
       	
       players[0] = pygame.mask.from_surface(rotp1)
       players[1] = pygame.mask.from_surface(rotp2)
       
       screen.blit(rotp1, rotr1)
       if not alone:
       	screen.blit(rotp2, rotr2)
       
       pygame.display.flip()
       
       #Physics
       for s in speeds:
        s[1] += gravity

       for p in pPos:
        idx = pPos.index(p)
        
        p[0] += speeds[idx][0]
        p[1] += speeds[idx][1]
        
        grounded[0] = players[0].overlap(floorm, (int(-rotr1[0]), int(floorPos[1] - rotr1[1])))
        grounded[1] = players[1].overlap(floorm, (int(-rotr2[0]), int(floorPos[1] - rotr2[1])))
        
        for i in range(2):
         	if grounded[i]:
         		speeds[i][1] = -speeds[i][1]
         	
       if data == "a" and grounded[1]:
         	speeds[1][1] -= jumpForce
       elif data == "Disconnected":
        	alone = True
       elif data == "Connected":
        	alone = False
       data = ""

       #Events
       for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
        	soc.send("a".encode())
        	if grounded[0]:
        	 speeds[0][1] -= jumpForce		

pygame.quit()