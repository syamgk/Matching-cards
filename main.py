import random
from time import sleep
from subprocess import check_output
import puzzle
try:
	import pygame
	from pygame.locals import *
except ImportError:
	print "Needs pygame library:\nYou can install it by typing:\nsudo apt-get install python-pygame"
	exit(0)
#-----------------------------------------------------------------------------------------
class Menu:
	def __init__(self):
		pygame.init()
		self.get_resolution()
		self.color = Green = 144, 238, 144
		self.screen = pygame.display.set_mode(self.screen_size)
		self.screen.fill(self.color)
		pygame.display.set_caption("Match Images")	
		pygame.event.set_allowed([QUIT,MOUSEBUTTONDOWN,MOUSEBUTTONUP])
		self.load_img("start.png",self.start_pos)
		self.load_img("quit.gif",self.quit_pos)
		self.load_img("sound.png",self.sound_pos,self.aud_size)
		self.load_img("help.png",self.help_pos,self.aud_size)
		font = pygame.font.Font(None, 30)
		pygame.display.flip()
		self.sound("bg.mp3",-1)
		pygame.mixer.music.set_volume(1)
		n = 1
		while n:
			sleep(.01)
			for event in pygame.event.get():
				print event
				if event.type==pygame.MOUSEBUTTONDOWN:
					p = event.pos
					if self.fun(self.start_pos,p,(165,85)):
						n=0
						self.sound("click.mp3")
						sleep(.5)
					elif self.fun(self.sound_pos,p,self.aud_size):#audio
						s =pygame.mixer.music.get_volume()
						s-=0.05
						if s< .1: s=0
						bg = pygame.Surface((150,20))
						bg.fill((144, 238, 144))
						text = font.render("Vol : "+str(int(s*100)) , 1, (10, 10, 10))
						textpos = text.get_rect()
						textpos.centerx = bg.get_rect().centerx
						bg.blit(text, (0, 0))
						self.screen.blit(bg, (self.screen_size[0]-100, self.screen_size[1]-20))
						pygame.display.flip()
						pygame.mixer.music.set_volume(s)
					elif self.fun(self.help_pos,p,self.aud_size):#help
						self.sound("help.mp3")
						bg = pygame.Surface((250,40))
						bg.fill((144, 238, 144))
						text = font.render("Click to open cards", 1, (10, 10, 10))
						text2 = font.render("then match same cards", 1, (10, 10, 10))
						textpos = text.get_rect()
						textpos.centerx = bg.get_rect().centerx
						bg.blit(text, (0, 0))
						bg.blit(text2, (0, 20))
						self.screen.blit(bg, (0, self.screen_size[1]-200))
						pygame.display.flip()
					elif self.fun(self.quit_pos,p,(234,74)):#quit
						self.sound("help.mp3")
						sleep(.3)
						exit(0)		
		self.screen.fill(self.color)
	def fun(self,pos,p,size):
#position(blit pos) ,{p}event.pos,[size] of img
		if pos[0]<=p[0] and p[0]<=pos[0]+size[0] and pos[1]<=p[1]and p[1]<=pos[1]+size[1]:
			return True
		return False
	def get_resolution(self):
# get screen sizes w.r.t current disply resolution
		disply = check_output(["xrandr"]).split(", ")[1].split(" ")
		self.screen_size = screen_w, screen_h = int(disply[1]), int(disply[-1]) -60

		self.aud_size=(screen_w/15,screen_w/15)
 		self.start_pos = tuple(map(lambda x,y: (x-y)/2, self.screen_size,(165,85)))
		self.quit_pos = ((screen_w-234)/2 ,screen_h-74)
 		self.sound_pos = tuple(map(lambda x,y: x-y, self.screen_size,self.aud_size))
 		self.help_pos = ((screen_w-self.aud_size[1])/2 , self.start_pos[1]+85)
	def load_img(self, name,position=0,resize=0):
#load corresponding images{names, trans size,blit pos}
		img = pygame.image.load("./images/" +name)
		if resize: img =  pygame.transform.scale(img, self.aud_size)
		if position: self.screen.blit(img,position )
	def sound(self, effect,repeat=0):
#play corresponding sound files
		pygame.mixer.music.load('./sounds/'+effect)
		pygame.mixer.music.play(repeat)
Menu()
G = puzzle.Game()
while 1:
	G.start_puzzle()
