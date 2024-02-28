import pygame
import socket
from threading import Thread

#Pseudo-constants
pygame.init()
resInfo = pygame.display.Info()
resolution = [resInfo.current_w,  resInfo.current_h]
ballRadius = 40
gravity = 0.2
jumpForce = 8

host ="127.0.0.1"
port = 9090

#Colors
backgroundColor = (170, 170, 255)
floorColor = (30,200,30)
pColors = [(255,0,0),(0,0,255)]
ballColor = (255, 255, 255)

#Rects

floor = pygame.Rect((0,resolution[1]*2/3),(resolution[0], resolution[1]/3))

pPos = [
[resolution[0]/4 - resolution[0]/20/2, resolution[1]/3],
    [resolution[0] - resolution[0]/4 - resolution[0]/20/2, resolution[1]/3]
]

players = [pygame.Rect((0,0),(0,0)), pygame.Rect((0,0),(0,0))]


rotp1 = pygame.Surface((resolution[0]/20, resolution[1]/5 ))
rotp2 = pygame.Surface((resolution[0]/20, resolution[1]/5) )

ballPos = (int(resolution[0]/2) - ballRadius/2, int(resolution[1]/2))
ballr1 = pygame.Rect((ballPos[0] - ballPos[0]/2, ballPos[1] - ballPos[1]/2), (ballRadius, ballRadius))
ballr2 = pygame.Rect((ballPos[0] - ballPos[0]/2, ballPos[1] - ballPos[1]/2), (ballRadius, ballRadius))

## GAME ##

screen = pygame.display.set_mode(resolution)
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
       pygame.draw.rect(screen, floorColor, floor)
       
       pygame.draw.circle(screen, ballColor, ballPos, ballRadius)

       rotp1.fill(pColors[0])
       rotp2.fill(pColors[1])

       screen.blit(rotp1, pPos[0])
       if not alone:
       	screen.blit(rotp2, pPos[1])
       	
       players[0] = rotp1.get_rect()
       players[0].topleft = pPos[0]
       players[1] = rotp2.get_rect()
       players[1].topleft = pPos[1]
       
       pygame.display.flip()
       
       #Physics
       for s in speeds:
        s[1] += gravity

       for p in pPos:
        idx = pPos.index(p)
        
        p[0] += speeds[idx][0]
        p[1] += speeds[idx][1]

        if (players[idx].colliderect(floor)):
            grounded[idx] = True
            speeds[idx][1] = -speeds[idx][1] * 0.0
        else:
         	grounded[idx] = False
         	
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