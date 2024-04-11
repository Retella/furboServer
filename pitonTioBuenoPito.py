import pygame
import socket
import traceback
import math
import ast

#Functions

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect
    
def rotate(surface, angle, pivot, offset):
   
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.
    
def circleSurface(color, radius):
    shape_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    return shape_surf
    
def reflect(vector, inNormal):
	dot = vector[0]*inNormal[0] + vector[1]*inNormal[1]
	
	return [vector[0] - 2*dot * inNormal[0], 
	             vector[1] - 2*dot * inNormal[1]]
	             
def jump(num):
	jCos = math.cos(math.radians(angles[num]))
	jSin = math.sin(math.radians(angles[num])) 
	
	speeds[num][0] += jCos*jumpForce
	speeds[num][1] -= jSin*jumpForce
	
def goal(num):
	global ballPos
	global pPos
	global angles
	global ballSpeed
	global speeds
	
	ballPos = [int(resolution[0]/2 - ballRadius*2), int(resolution[1]/4)]
	ballSpeed = [0,0]
	pPos = [
[resolution[0]/4 - resolution[0]/40, resolution[1]/3],
    [resolution[0] - resolution[0]/4 - resolution[0]/40, resolution[1]/3]
]
	angles = [90,90]
	speeds = [[0,0],[0,0]]
	
	score[1 - num] += 1

def incredibleFunc(tOmeger, times):
	return 90 + (-tOmeger*500/math.sqrt(times)) * math.sin(times/15)

#Pseudo-constants
pygame.init()
resolution = [0,0]
resInfo = pygame.display.Info()
if resInfo.current_w < resInfo.current_h:
	resolution[0] = resInfo.current_w
	resolution[1] = int(resolution[0]*(800/360))
else:
	resolution[1] = resInfo.current_h
	resolution[0] = int(resolution[1]/(800/360))
ballRadius = resolution[0]/27
gravity = resolution[0]/2160
jumpForce = resolution[0]/54
bounciness = resolution[0]/5400
ballBounciness = resolution[0]/1350
maxSpeed = resolution[0]/36
porterHeight = resolution[1]/6
fps = 60

host ="127.0.0.1"
port = 9090

#Colors
backgroundColor = (170, 170, 255)
floorColor = (30,200,30)
pColors = [(255,0,0),(0,0,255)]
ballColor = (255, 255, 255)
porterColor = (255, 255, 255)

#Rects
screen = pygame.display.set_mode(resolution)

floorImg = pygame.Surface((resolution[0], resolution[1]/3))
floorm = pygame.mask.from_surface(floorImg)

pPos = [
[resolution[0]/4 - resolution[0]/40, resolution[1]/3],
    [resolution[0] - resolution[0]/4 - resolution[0]/40, resolution[1]/3]
]

floorPos = (0, int(2*resolution[1]/3))
porterPos = [(0, floorPos[1] - porterHeight), (resolution[0] - resolution[0]/40, floorPos[1] - porterHeight)]
scorePos = [(resolution[0]/10, resolution[0]/ 10), (resolution[0] - resolution[0]/10 - resolution[0]/5, resolution[0]/10)]

players = [pygame.mask.Mask((0,0),(0,0)), pygame.mask.Mask((0,0),(0,0))]

imgs = [pygame.Surface((resolution[0]/20, resolution[1]/5)).convert_alpha(), pygame.Surface((resolution[0]/20, resolution[1]/5)).convert_alpha()]
porterImg = pygame.Surface((resolution[0]/40, porterHeight))

scoreSquareImg = pygame.Surface((resolution[0]/5, resolution[0]/5))
scoreFont = pygame.font.SysFont(None, int(resolution[0]/3.6))

ballPos = [int(resolution[0]/2 - ballRadius*2), int(resolution[1]/4)]
ballSpeed = [0, 0]
ballImg = circleSurface(ballColor, ballRadius)
ballm = pygame.mask.from_surface(ballImg)

## GAME ##

running = True
isHost = False
bucles = 0

speeds = [[0,0],[0,0]]
grounded = [False, False]
jumpable = [False, False]
angles = [90, 90]
omega = [0, 0]
tOmega = [0, 0]
offsets = [0, 0]
t = [0, 0]
gotT = [0, 0]
lastAngle = [0, 0]
score = [0, 0]

data = ""
alone = True
clock = pygame.time.Clock()

#Networking

soc = socket.socket()
soc.connect((host, port))
soc.setblocking(0)

#Main bucle
while running:
    
    #Clock
    dt = clock.tick(fps) / 15
    if dt > 100: dt = 0
    
    try:
    	data = soc.recv(1024).decode()
    	print(data)
    except: pass
    
    if data == "Disconnected": 
    	alone = True
    try:
    	if data == "Connected" or data[0] == "[": 
    		alone = False
    except: pass
    if bucles < 100: 
    		bucles += 1
    		continue
        	
    if alone: isHost = True
    
    if isHost:
       #Drawing
       screen.fill(backgroundColor)
       
       floorImg.fill(floorColor)
       screen.blit(floorImg, floorPos)
       
       screen.blit(ballImg, ballPos)
       
       porterImg.fill(porterColor)
       for i in range(2):
       	screen.blit(porterImg, porterPos[i])
       	
       	scoreSquareImg.fill(pColors[i])
       	screen.blit(scoreSquareImg, scorePos[i])
       	
       	scoreText = scoreFont.render(str(score[i]), True, (255,255,255))
       	screen.blit(scoreText, (scorePos[i][0] - resolution[0]/216, scorePos[i][1]))
       
       rotr = [pygame.Rect, pygame.Rect]
       rotp = [pygame.Surface, pygame.Surface]
       
       for i in range(2 - int(alone)):
       	rotp[i], rotr[i] = rotate(imgs[i],-angles[i] - 90, pPos[i], pygame.math.Vector2(0, imgs[i].get_rect().h/2))
       	
       	players[i] = pygame.mask.from_surface(rotp[i])
       	
       	screen.blit(rotp[i], rotr[i])
       
       pygame.display.flip()
       
       #Physics
       maMasks = [floorm, players[0], players[1]]
       maPos = [floorPos, rotr[0], rotr[1]]
        #BALL
       ballSpeed[1] += gravity * dt
        
       for m in range(len(maMasks) - int(alone)):

         masker = maMasks[m]
         poser = maPos[m]
         
         bCol = ballm.overlap(masker, (int(poser[0] - ballPos[0]), int(poser[1] - ballPos[1])))
         if bCol:
           if m == 0:
            ballSpeed = reflect(ballSpeed, (0,1))
            for i in range(2):
            	ballSpeed[i] *= ballBounciness
           else:
              normalRaw = (ballRadius - bCol[0] - 10, ballRadius - bCol[1])
              normalMagnitude = math.sqrt(pow(normalRaw[0], 2) + pow(normalRaw[1], 2))
              normal = (normalRaw[0] / normalMagnitude, normalRaw[1] / normalMagnitude)
              area = ballm.overlap_area(masker, (int(poser[0] - ballPos[0]), int(poser[1] - ballPos[1])))
              absPoint = (ballPos[0] + bCol[0] + 0, ballPos[1] + bCol[1])
              if area > ballRadius/3:
              	ballPos = [(absPoint[0] + normal[0] * ballRadius * 2) - ballRadius, (absPoint[1] + normal[1] * ballRadius * 2) - ballRadius]
              	
              reflected = reflect(ballSpeed, normal)
              ballSpeed[0] = reflected[0]
              ballSpeed[1] = reflected[1]
              
              ballSpeed[0] += speeds[m - 1][0]
              ballSpeed[1] += speeds[m - 1][1]
              
              radiusVec = [absPoint[0] - poser.center[0], absPoint[1] - poser.bottom]
              absRadius = math.sqrt(pow(radiusVec[0], 2) + pow(radiusVec[1], 2))
              linearForce = abs(omega[maPos.index(poser)-1]) * absRadius / 20
              
              ballSpeed[0] += normal[0] * linearForce
              ballSpeed[1] += normal[1] * linearForce
              for i in range(2):
              	ballSpeed[i] *= ballBounciness
         	
       bRect = ballImg.get_rect(topleft= ballPos)
       if bRect.bottom > floorPos[1]:
         	ballPos[1] = floorPos[1] - ballRadius*2
       if bRect.left < 0:
       	if bRect.top < resolution[1] - porterHeight - floorImg.get_rect().h or alone:
       		ballPos[0] = ballRadius
       		ballSpeed[0] *= -ballBounciness
       	else:
       		goal(0)
       elif bRect.right > resolution[0]:
       	if bRect.top < resolution[1] - porterHeight - floorImg.get_rect().h or alone:
       		ballPos[0] = resolution[0] - ballRadius * 2
       		ballSpeed[0] *= -ballBounciness
       	else:
       		goal(1)
       
       for b in range(2):
         	if ballSpeed[b] > maxSpeed:
         		ballSpeed[b] = maxSpeed
         	elif ballSpeed[b] < -maxSpeed:
         		ballSpeed[b] = -maxSpeed
         		
         	ballPos[b] += ballSpeed[b] * dt
         	
        #PLAYERS.
       for p in range(2 - int(alone)):
        speeds[p][1] += gravity * dt
        
        for k in range(2):
        	pPos[p][k] += speeds[p][k] * dt
        	
        grounded[p] = rotr[p].bottom > floorPos[1]
        
        jumpable[p] = pPos[p][1] > floorPos[1] - 50 and math.sin(math.radians(angles[p])) > 0
        
        if grounded[p]: 
        	speeds[p][1] *= -bounciness
        	
        if rotr[p].bottom > floorPos[1] - 10:
        	t[p] += 1 *dt
        	angles[p] = incredibleFunc(tOmega[p], t[p])
        	
        omega[p] = angles[p] - lastAngle[p]
        
        if grounded[p]:
        	gotT[p] = False
        	speeds[p][0] = 0
        	pSine = math.sin(math.radians(angles[p]))
        	pCos = math.cos(math.radians(angles[p]))
        	
        	if pSine < 0:
        		pPos[p][1] = floorPos[1] - imgs[p].get_rect().h * (-pSine) - 1
        	else:
        		pPos[p][1] = floorPos[1] - imgs[p].get_rect().w/2 * abs(pCos) - 1
        
        if pPos[p][1] < floorPos[1] - 100 and pPos[p][1] > floorPos[1] - 170 and speeds[p][1] > 0 and not gotT[p]:
         	tOmega[p] = min(speeds[p][1]*30, 0.8)
         	
         	maT = 1
         	while angles[p] != 0:
         		maFunc = incredibleFunc(tOmega[p], maT)
         		if maFunc > angles[p] - 10 and maFunc < angles[p] + 10:
         			t[p] = maT
         			gotT[p] = True
         			break
         		if maT > 100:
         			tOmega[p] += 0.5
         			maT = 0
         		maT += 5
       
        if pPos[p][0] > resolution[0]:
         	speeds[p][0] *= -bounciness
         	pPos[p][0] = resolution[0]
        elif pPos[p][0] < 0:
         	speeds[p][0] *= -bounciness
         	pPos[p][0] = 0
       
        op = 1 - p
        
        pCol = 0
        try:
        	pCol = players[p].overlap(players[op], (rotr[op][0] - rotr[p][0], rotr[op][1] - rotr[p][1]))
        except: pass
        if pCol:
        	pVec = [pPos[p][0] - pPos[op][0], pPos[p][1] - pPos[op][1]]
        	pVecMag = math.sqrt(pow(pVec[0], 2) + pow(pVec[1], 2))
        	pVecUnit = [pVec[0]/ pVecMag, pVec[1] / pVecMag]
        	
        	for i in range(2):
        		pPos[p][i] += pVecUnit[i] * 15
        		pPos[op][i] -= pVecUnit[i] * 15
                	
        lastAngle[p] = angles[p]
         	
       if data == "a" and jumpable[1]:
         	jump(1)

       #Events
       for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
        	soc.send("a".encode())
        	if jumpable[0]:
        	 jump(0)

       infoList = [ballPos, pPos, angles, resolution[0], score]
       
       soc.send(str(infoList).encode())
        	 
    else:
      try:
       #Networking
       rotp = [0,0]
       rotr = [0,0]
       
       fixedBall = [0,0]
       fixedPos = [[0,0],[0,0]]
       
       if not data: continue
       
       if data[0] == "[":
       	infoList = ast.literal_eval(data)
       	
       	ballPos = infoList[0]
       	pPos = infoList[1]
       	angles = infoList[2]
       	otherRes = infoList[3]
       	score = infoList[4]
       	
       	resRatio = otherRes / resolution[0]
       	
       	for i in range(2):
       		fixedBall[i] = ballPos[i] / resRatio
       		for j in range(2):
       			fixedPos[i][j] = pPos[i][j] / resRatio
       		
       	for i in range(2):
       		rotp[i], rotr[i] = rotate(imgs[i],-angles[i] - 90, fixedPos[i], pygame.math.Vector2(0, imgs[i].get_rect().h/2))
       
       #Drawing
       screen.fill(backgroundColor)
       
       floorImg.fill(floorColor)
       screen.blit(floorImg, floorPos)
       
       screen.blit(ballImg, fixedBall)
       
       porterImg.fill(porterColor)
       for i in range(2):
       	screen.blit(porterImg, porterPos[i])
       	
       	scoreSquareImg.fill(pColors[i])
       	screen.blit(scoreSquareImg, scorePos[i])
       	
       	scoreText = scoreFont.render(str(score[i]), True, (255,255,255))
       	screen.blit(scoreText, (scorePos[i][0] - 5, scorePos[i][1]))
       	
       	screen.blit(rotp[i], rotr[i])
       
       pygame.display.flip()
       
       for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
        	soc.send("a".encode())
       
      except Exception as e: print(traceback.format_exc())
        	 	
    bucles += 1
    data = ""

pygame.quit()