import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, xPos, yPos, im):
		self.x = xPos
		self.y = yPos
		self.image = pygame.image.load(im)

class Turtle(Sprite):
	def __init__(self, xPos, yPos):
		super(Turtle, self).__init__(xPos, yPos, "images/turtle.png")
		# self.x = xPos
		# self.y = yPos
		# self.turtle_image = pygame.image.load("turtle.png")

class Lettuce(Sprite):
	def __init__(self, xPos, yPos):
		super(Lettuce, self).__init__(xPos, yPos, "images/lettuce.png")
		# self.x = xPos
		# self.y = yPos
		# self.lettuce_image = pygame.image.load("lettuce.png")

class Model():
	def __init__(self):
		self.dest_x = 0
		self.dest_y = 0
		self.turtle = Turtle(0, 0)
		# self.lettuce = Lettuce(200, 200)
		self.sprites = []
		self.sprites.append(self.turtle)
		self.sprites.append(Lettuce(500, 400))
		
	def deleteLettuce(self):
		for sprite in self.sprites:
			if isinstance(sprite, Lettuce):
				self.sprites.remove(sprite)

	def update(self):
		if self.turtle.x < self.dest_x:
			self.turtle.x += 1
		if self.turtle.x > self.dest_x:
			self.turtle.x -= 1
		if self.turtle.y < self.dest_y:
			self.turtle.y += 1
		if self.turtle.y > self.dest_y:
			self.turtle.y -= 1

	def set_dest(self, pos):
		self.dest_x = pos[0]
		self.dest_y = pos[1] 

class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		#self.turtle_image = pygame.image.load("images/turtle.png")
		self.model = model
		#self.model.rect = self.turtle_image.get_rect()

	def update(self):	
		self.screen.fill([0,200,100])
		# self.screen.blit(self.model.turtle.image, (self.model.turtle.x, self.model.turtle.y))
		#self.screen.blit(self.model.lettuce.image, (self.model.dest_x, self.model.dest_y))
		pygame.display.flip()
#one option for loops:
		for sprite in self.model.sprites:
			# print(isinstance(sprite, Lettuce))
			# if isinstance(sprite, Mario)
				# Do the thing
			self.screen.blit(sprite.image, (sprite.x, sprite.y))
#another option:
		# for i in range(len(self.model.sprites)):
			# self.screen.blit(self.model.sprites[i].image, (self.model.sprites[i].x, self.model.sprites[i].y))

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
			elif event.type == pygame.MOUSEBUTTONUP:
				self.model.set_dest(pygame.mouse.get_pos())
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.dest_x -= 1
		if keys[K_RIGHT]:
			self.model.dest_x += 1
		if keys[K_UP]:
			self.model.dest_y -= 1
		if keys[K_DOWN]:
			self.model.dest_y += 1
		

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")