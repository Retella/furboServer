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
players = [
    pygame.Rect((resolution[0]/4 - resolution[0]/20/2, resolution[1]/3), (resolution[0]/20, resolution[1]/5)),
    pygame.Rect((resolution[0] - resolution[0]/4 - resolution[0]/20/2, resolution[1]/3), (resolution[0]/20, resolution[1]/5))
]
ballPos = (int(resolution[0]/2) - ballRadius/2, int(resolution[1]/2))

## GAME ##

screen = pygame.display.set_mode(resolution)
running = True

speeds = [[0,0],[0,0]]
grounded = [False, False]
data = ""
alone = True

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

       #Physics
       for s in speeds:
        s[1] += gravity

       for p in players:
        idx = players.index(p)
        
        p[0] += speeds[idx][0]
        p[1] += speeds[idx][1]

        if (p.colliderect(floor)):
            grounded[idx] = True
            speeds[idx][1] = -speeds[idx][1] * 0.5
        else:
         	grounded[idx] = False
         	
       if data == "a" and grounded[1]:
         	speeds[1][1] -= jumpForce
       elif data == "Disconnected":
        	alone = True
       elif data == "Connected":
        	alone = False
       data == ""
       #Drawing
       screen.fill(backgroundColor)
       pygame.draw.rect(screen, floorColor, floor)
       pygame.draw.circle(screen, ballColor, ballPos, ballRadius)

       
       pygame.draw.rect(screen, pColors[0], players[0])
       if not alone:
       	pygame.draw.rect(screen, pColors[1], players[1])

       pygame.display.flip()

       #Events
       for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
        	soc.send("a".encode())
        	if grounded[idx]:
        	 speeds[0][1] -= jumpForce
    

pygame.quit()