# 2048.py 
# Aug 22, 2015
# Written in python / pygame by DavidSousaRJ - david.sousarj@gmail.com
# License: Creative Commons
# Sorry about some comments in portuguese!
#
# CHANGES:
# Aug 24 - fixed colors /fonts
# BUG: game ending not working
# BUG: when a play is not possible it keeps adding a random tile
# TODO: include score, button undo and new game
import os
import sys
import pygame
from pygame.locals import *
from random import randint

TABLE=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

def isgameover(TABLE):
	status=0
	zerocount=0
	for LINE in TABLE:
		if 2048 in LINE:
			status=1
			return status
		elif 0 not in LINE:
			zerocount+=1
	if zerocount==4:
		#condicoes de gameover: nao ter zero e nao ter consecutivo igual
		#procura consecutivos horizontal
		for i in range(4):
			for j in range(3):
				if TABLE[i][j]==TABLE[i][j+1]: return status
		#procura consecutivos na vertical
		for j in range(4):
			for i in range(3):
				if TABLE[i][j]==TABLE[i+1][j]: return status
		status=2
	return status

#regras do 2048
# define a direcaoo jogada, p.ex. : cima
# para cada coluna, de cima pra baixo
#	   move o numero para o zero-consecutivo-mais-longe 
#	   se o nao-zero-mais-perto e igual ao numero, combina

def moveup(pi,pj,T):
	justcomb=False
	while pi > 0 and (T[pi-1][pj] == 0 or (T[pi-1][pj] == T[pi][pj] and not justcomb)):
		if T[pi-1][pj] == 0:
			T[pi-1][pj] = T[pi][pj]
			T[pi][pj]=0
			pi-=1
		elif T[pi-1][pj]==T[pi][pj]:
			T[pi-1][pj] += T[pi][pj]
			T[pi][pj] = 0
			pi-=1
			justcomb=True
	return T

def movedown(pi,pj,T):
	justcomb=False
	while pi < 3 and (T[pi+1][pj] == 0 or (T[pi+1][pj] == T[pi][pj] and not justcomb)):
		if T[pi+1][pj] == 0:
			T[pi+1][pj] = T[pi][pj]
			T[pi][pj]=0
			pi+=1
		elif T[pi+1][pj]==T[pi][pj]:
			T[pi+1][pj] += T[pi][pj]
			T[pi][pj] = 0
			pi+=1
			justcomb=True
	return T

def moveleft(pi,pj,T):
	justcomb=False
	while pj > 0 and (T[pi][pj-1] == 0 or (T[pi][pj-1] == T[pi][pj] and not justcomb)):
		if T[pi][pj-1] == 0:
			T[pi][pj-1] = T[pi][pj]
			T[pi][pj]=0
			pj-=1
		elif T[pi][pj-1]==T[pi][pj]:
			T[pi][pj-1] += T[pi][pj]
			T[pi][pj] = 0
			pj-=1
			justcomb=True
	return T

def moveright(pi,pj,T):
	justcomb=False
	while pj < 3 and (T[pi][pj+1] == 0 or (T[pi][pj+1] == T[pi][pj] and not justcomb)):
		if T[pi][pj+1] == 0:
			T[pi][pj+1] = T[pi][pj]
			T[pi][pj]=0
			pj+=1
		elif T[pi][pj+1]==T[pi][pj]:
			T[pi][pj+1] += T[pi][pj]
			T[pi][pj] = 0
			pj+=1
			justcomb=True
	return T

def randomfill(TABLE):
	# search for zero in the game table
	flatTABLE = sum(TABLE,[])
	if 0 not in flatTABLE:
		return TABLE
	empty=False
	w=0
	while not empty:
		w=randint(0,15)
		if TABLE[w//4][w%4] == 0:
			empty=True
	z=randint(1,5)
	if z==5:
		TABLE[w//4][w%4] = 4
	else:
		TABLE[w//4][w%4] = 2
	return TABLE

def key(DIRECTION,TABLE):
	if   DIRECTION =='w':
		for pi in range(1,4):
			for pj in range(4):
				if TABLE[pi][pj] !=0: TABLE=moveup(pi,pj,TABLE)
	elif DIRECTION =='s':
		for pi in range(2,-1,-1):
			for pj in range(4):
				if TABLE[pi][pj] !=0: TABLE=movedown(pi,pj,TABLE)
	elif DIRECTION =='a':
		for pj in range(1,4):
			for pi in range(4):
				if TABLE[pi][pj] !=0: TABLE=moveleft(pi,pj,TABLE)
	elif DIRECTION =='d':
		for pj in range(2,-1,-1):
			for pi in range(4):
				if TABLE[pi][pj] !=0: TABLE=moveright(pi,pj,TABLE)
	return TABLE

def showtext(TABLE):
    os.system('clear')
    for LINE in TABLE:
        for N in LINE:
            print "%4s" %N,
        print ""

########################################################################
# Parte Grafica
width=400
height=400
boxsize = min(width,height)//4;
margin = 5
thickness = 0
STATUS=0

colorback=(189,174,158)
colorblank=(205,193,180)
colorlight=(249,246,242)
colordark=(119,110,101)

dictcolor1={
0:colorblank,
2:(238,228,218),
4:(237,224,200),
8:(242,177,121),
16:(245,149,99),
32:(246,124,95),
64:(246,95,59),
128:(237,207,114),
256:(237,204,97),
512:(237,200,80),
1024:(237,197,63),
2048:(237,194,46) }

dictcolor2={
2:colordark,
4:colordark,
8:colorlight,
16:colorlight,
32:colorlight,
64:colorlight,
128:colorlight,
256:colorlight,
512:colorlight,
1024:colorlight,
2048:colorlight }

# Init screen
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption( 'Python 2048 by DavidSousaRJ' )
myfont = pygame.font.SysFont("Arial", 30, bold=True)

def gameover(STATUS):
	if STATUS == 1:
		label = myfont.render("You win! :)", 1, (255,255,255))
		screen.blit(label, (100, 100))
	elif STATUS == 2:
		label = myfont.render("Game over! :(", 1, (255,255,255))
		screen.blit(label, (100, 100))
	pygame.display.update()

def show(TABLE):
	screen.fill(colorback)
	for i in range(4):
		for j in range(4):
			pygame.draw.rect(screen, dictcolor1[TABLE[i][j]], (j*boxsize+margin,
											  i*boxsize+margin,
											  boxsize-2*margin,
											  boxsize-2*margin),
											  thickness)
			if TABLE[i][j] != 0:
				label = myfont.render("%4s" %(TABLE[i][j]), 1, dictcolor2[TABLE[i][j]] )
				screen.blit(label, (j*boxsize+4*margin, i*boxsize+5*margin))
	pygame.display.update()


#paintCanvas
TABLE=randomfill(TABLE)
TABLE=randomfill(TABLE)
show(TABLE)
showtext(TABLE)
running=True

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			print "quit"
			pygame.quit(); sys.exit()
		if event.type == pygame.KEYDOWN:
			if running:
				if event.key == pygame.K_UP:
					TABLE=key('w',TABLE)
					TABLE=randomfill(TABLE)
					show(TABLE)
					showtext(TABLE)
					STATUS=isgameover(TABLE)
					if STATUS<0:
						running=False
						gameover(STATUS)
				if event.key == pygame.K_DOWN:
					TABLE=key('s',TABLE)
					TABLE=randomfill(TABLE)
					show(TABLE)
					showtext(TABLE)
					STATUS=isgameover(TABLE)
					if STATUS<0:
						running=False
						gameover(STATUS)
				if event.key == pygame.K_LEFT:
					TABLE=key('a',TABLE)
					TABLE=randomfill(TABLE)
					show(TABLE)
					showtext(TABLE)
					STATUS=isgameover(TABLE)
					if STATUS<0:
						running=False
						gameover(STATUS)
				if event.key == pygame.K_RIGHT:
					TABLE=key('d',TABLE)
					TABLE=randomfill(TABLE)
					show(TABLE)
					showtext(TABLE)
					STATUS=isgameover(TABLE)
					if STATUS<0:
						running=False
						gameover(STATUS)
#end
