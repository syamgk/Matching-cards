import random
from time import sleep
from subprocess import check_output
import thread
try:
	import pygame
	from pygame.locals import *
except ImportError:
	print "Needs pygame library:\nYou can install it by typing:\nsudo apt-get instal python-pygame"
	exit(0)
#----------------------------------------------------------------------------------------------------------------------
class Game(object):
	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		color = Green = 144, 238, 144
		self.get_resolution()
		self.screen = pygame.display.set_mode(self.screen_size)
		self.screen.fill(color)
		pygame.display.set_caption("Match Images")	
		pygame.event.set_allowed([QUIT,MOUSEBUTTONDOWN,MOUSEBUTTONUP])
		self.shuffle()
		self.score = 0
		self.scoreboard(0)
		self.corresponding_pos = []
		self.check = []
		self.matched = set()
		self.draw_cards()
	def get_resolution(self):
# get screen sizes w.r.t current disply resolution
		f = random.choice
		disply = check_output(["xrandr"]).split(", ")[1].split(" ")
		self.screen_size = screen_w, screen_h = int(disply[1]), int(disply[-1]) -60
		self.table_size = table_w, table_h = screen_w -80 ,screen_h -80
		self.card_size = self.WIDTH,self.HEIGHT = table_w/f([4,6]) ,table_h/f([4,6])
		self.card_pic_size = self.WIDTH -20 ,self.HEIGHT -20
		self.num = (table_w *table_h)/(self.WIDTH*self.HEIGHT)
		self.qm_size = self.i,self.j = self.WIDTH -40/2,self.HEIGHT -40/2
	def shuffle(self):
#load images and shuffle 
		self.card_list = check_output(["ls","images/card_pic"]).split("\n")[:-1]
		self.image_list = check_output(["ls","images/linux"]).split("\n")[:-1]
		random.shuffle(self.image_list)
		self.image_list = 2* self.image_list[:self.num/2]
		random.shuffle(self.image_list)
		print self.image_list
	def sound(self, effect):
#play corresponding sound files
		pygame.mixer.music.load('./sounds/'+effect)
		pygame.mixer.music.play()
	def image(self, name):
#load corresponding images
		img = pygame.image.load("./images/" +name)
		img =  pygame.transform.scale(img, self.card_pic_size)
		view_card=pygame.Surface(self.card_size)
		view_card.blit(img, (10,10))
		return view_card
	def draw_cards(self):
#draw the deck of cards
		self.blank_card = self.image("card_pic/"+random.choice(self.card_list))
		for x in range(40,self.screen_size[0]-40,self.WIDTH+1):
				for y in range (40,self.screen_size[1]-80,self.HEIGHT+1):
					self.screen.blit(self.blank_card ,(x,y))
		pygame.display.flip()
	def show_card(self,card_num,pos):
#show card
		self.view_card=self.image("linux/"+self.image_list[card_num])
		self.screen.blit(self.view_card,pos)
		self.sound("pop.mp3")
		pygame.display.flip()
		self.check.append(self.image_list[card_num])
		self.corresponding_pos.append((pos[0],pos[1]))
	def check_prev(self):
#check for matching
 		a = self.corresponding_pos[-1] == self.corresponding_pos[-2]
		if not self.check[1] == self.check[0] or a:
			sleep(.2)
			self.screen.blit(self.blank_card,self.corresponding_pos[-2])
			self.screen.blit(self.blank_card,self.corresponding_pos[-1])
			self.sound("bump.wav")
			if not self.score ==0 :self.scoreboard(-5)
			pygame.display.flip()
		elif not self.corresponding_pos[-1] == self.corresponding_pos[-2]:
			self.sound("coin.wav")
			self.scoreboard(10)
			self.matched.add(self.corresponding_pos[-1])
			self.matched.add(self.corresponding_pos[-2])
			if len(self.matched) == self.num: self.sound("stage_clear.wav")
		self.check = []
	def track_card(self ,event):
#track cards w.r.t position
		size, p, n = self.screen_size, event.pos, 0
		for x in range(40,size[0]-40,self.WIDTH+1):
			for y in range (40,size[1]-80,self.HEIGHT+1):
				if x<=p[0] and p[0]<=x+self.WIDTH and y<=p[1]and p[1]<=y+self.HEIGHT:
					if (x, y) in self.matched: return
					self.show_card(n,(x,y))
					if len(self.check) == 2:self.check_prev()
				n+=1
	def scoreboard(self,point):
		self.score += point
		bg = pygame.Surface((150,20))
		bg.fill((144, 238, 144))
		font = pygame.font.Font(None, 30)
		text = font.render("Score : "+str(self.score) , 1, (10, 10, 10))
		textpos = text.get_rect()
		textpos.centerx = bg.get_rect().centerx
		bg.blit(text, (0, 0))
		self.screen.blit(bg, (self.screen_size[0]-200, 10))
		pygame.display.flip()
	def handle_events(self):
#handle events w.r.t clicks
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				check_output(["python","puzzle.py"])
			elif event.type==pygame.MOUSEBUTTONDOWN:
				self.track_card(event)
				print event
G = Game()
while True:
	G.handle_events()