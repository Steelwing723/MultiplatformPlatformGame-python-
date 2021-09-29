# Name: Joshua Davis
# UAID: 010946462
# Date: 12/04/2020
# Assignment 8	[game.py]
# Description: An implementation of assignment 5 in Python.
# -------------------------------------------------------------------------------------------------

import pygame
import time
import random

from pygame.locals import*
from time import sleep

#Global Variables
GROUND_LEVEL = 480
GRAVITY = 9.8
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1000
RIGHT = True
LEFT = False
MARIO_SPEED = 25
JUMP_HEIGHT = -90
JUMP_LIMIT = 8
LOOP = -1
NOLOOP = 0
Scroll_Position = 0


class Sprite():
	def __init__(self, xPos, yPos, im):
		self.x = xPos
		self.y = yPos
		self.image = pygame.image.load(im)

	def spriteCollision(self, s):
		if isinstance(self, Mario):
			myRight = self.xPos + self.w
			myLeft = self.xPos
		else:
			myRight = self.x + self.w
			myLeft = self.x

		myBottom = self.y + self.h
		myTop = self.y
		theirRight = s.x + s.w
		theirLeft = s.x
		theirBottom = s.y + s.h
		theirTop = s.y

		if myRight < theirLeft:
			return False;

		if myLeft > theirRight:
			return False;

		if myBottom <= theirTop:
			return False;

		if myTop > theirBottom:
			return False;

		return True;

class Mario(Sprite):
	def __init__(self, xPos, yPos):
		super(Mario, self).__init__(xPos, yPos, "images/marioR1.png")
		self.v_velocity = 0.0
		self.w = 60
		self.h = 95
		self.xPos = self.x
		self.yShadow = self.y
		self.collisionDif = 0
		self.onObject = False
		self.rightFacing = True
		self.jumpTimer = JUMP_LIMIT
		self.imageCycle = 0
		self.Jump_Sound = Sound("sound/smw_jump.wav", 2, NOLOOP, 0.05)
		self.Fizzle_Sound = Sound("sound/smw_shell_ricochet.wav", 3, NOLOOP, 0.05)

	def update(self):
		self.v_velocity += GRAVITY
		self.y += self.v_velocity
		if self.y >= GROUND_LEVEL - self.h:
			self.v_velocity = 0.0
			self.y = GROUND_LEVEL - self.h

		if self.y < 0:
			self.y = 0

		if self.jumpTimer <= JUMP_LIMIT:
			self.jumpTimer += 1

		self.xPos = self.x + Scroll_Position

	def move(self, direction):
		global Scroll_Position
		if direction == RIGHT:
			self.rightFacing = True
			Scroll_Position += MARIO_SPEED
			if self.imageCycle < 4:
				self.imageCycle += 1
			else:
				self.imageCycle = 0

		if direction == LEFT:
			self.rightFacing = False
			Scroll_Position -= MARIO_SPEED
			if self.imageCycle > 0:
				self.imageCycle -= 1
			else:
				self.imageCycle = 4

	def jump(self):
		self.v_velocity = JUMP_HEIGHT
		self.onObject = False
		self.Jump_Sound.play()

	def stopJump(self):
		if self.v_velocity < 0.0:
			self.v_velocity = 0.0

	def onSurface(self):
		if self.y + self.h >= GROUND_LEVEL:
			return True
		elif self.onObject:
			self.jumpTimer = 0
			return True
		else:
			return False


class Tube(Sprite):
	def __init__(self, xPos, yPos):
		super(Tube, self).__init__(xPos, yPos, "images/tubeBottom.png")
		self.w = 55
		self.h = 400

	def update(self):
		self.x = self.x

class Goomba(Sprite):
	def __init__(self, xPos, yPos):
		super(Goomba, self).__init__(xPos, yPos, "images/goomba.png")
		self.w = 40
		self.h = 47
		self.v_velocity = 0.0
		self.direction = self.randomDirection()
		self.onFire = False
		self.isDead = False
		self.framesOnFire = 40
		self.speed = 5
		self.Ignite_Sound = Sound("sound/smw_bowser_fire.wav", 3, NOLOOP, 0.05)

	def update(self):
		self.v_velocity += GRAVITY
		self.y += self.v_velocity
		if self.y >= GROUND_LEVEL - self.h:
			self.v_velocity = 0.0
			self.y = GROUND_LEVEL - self.h

		self.roam()

		if(self.framesOnFire < 40):
			self.framesOnFire += 1
			self.speed = 0

	def roam(self):
		if self.direction:
			self.x -= self.speed
		else:
			self.x += self.speed

	def burn(self):
		self.framesOnFire = 0
		self.onFire = True
		self.Ignite_Sound.play()

	def randomDirection(self):
		num = random.randrange(0, 1)
		if num == 0:
			return LEFT
		if num == 1:
			return RIGHT

	def tubeCollision(self, t):
		if self.y + self.h > t.y and self.y < t.y + t.h:
			self.direction = not self.direction

class Fireball(Sprite):
	def __init__(self, xPos, yPos):
		super(Fireball, self).__init__(xPos, yPos, "images/fireball.png")
		self.w = 47
		self.h = 47
		self.extinguished = False
		self.burnTime = 50
		self.h_velocity = 0
		self.v_velocity = 0.0
		self.Fireball_Sound = Sound("sound/smw_fireball.wav", 3, NOLOOP, 0.05)
		self.Fizzle_Sound = Sound("sound/smw_shell_ricochet.wav", 3, NOLOOP, 0.05)

	def update(self):
		self.v_velocity += GRAVITY
		self.y += self.v_velocity

		if self.y >= GROUND_LEVEL - self.h:
			self.y = GROUND_LEVEL - self.h
			self.v_velocity = -50.0

		self.x += self.h_velocity

	def setHorizontalVelocity(self, direction):
		self.Fireball_Sound.play()
		if direction == RIGHT:
			self.h_velocity = 50
		else:
			self.h_velocity = -50

class Model():
	def __init__(self):
		self.sprites = []
		self.mario = Mario(SCREEN_WIDTH/2 -60, 100)
		self.sprites.append(self.mario)
		self.generateLevel()
		self.collision = False

	def update(self):
		self.removeFireballs()
		self.removeGoombas()

#Collision Handling
		if not self.collision:
			self.mario.onObject = False

		for sprite in self.sprites:
			sprite.update()

			if isinstance (sprite, Goomba):
				if sprite.framesOnFire < 40 and sprite.framesOnFire > 20:
					sprite.isDead = True
				for s in self.sprites:
					if isinstance (s, Tube):
						self.collision = sprite.spriteCollision(s)
						if self.collision:
							sprite.tubeCollision(s)

			if isinstance (sprite, Fireball):
				sprite.burnTime -= 1
				if sprite.burnTime <= 0:
					sprite.extinguished = True
				for s in self.sprites:
					if isinstance (s, Tube):
						self.collision = sprite.spriteCollision(s)
						if self.collision:
							sprite.extinguished = True
							sprite.Fizzle_Sound.play()
					if isinstance (s, Goomba):
						self.collision = sprite.spriteCollision(s)
						if self.collision:
							sprite.extinguished = True
							s.burn()

			if isinstance (sprite, Tube):
				self.collision = self.mario.spriteCollision(sprite)
				if self.collision:
					self.tubeCollision(sprite)

	def removeGoombas(self):
		for sprite in self.sprites:
			if isinstance (sprite, Goomba):
				if sprite.isDead:
					self.sprites.remove(sprite)

	def removeFireballs(self):
		for sprite in self.sprites:
			if isinstance (sprite, Fireball):
				if sprite.extinguished:
					self.sprites.remove(sprite)

	def addFireball(self):
		self.fireball = Fireball(self.mario.xPos, self.mario.y)
		self.fireball.setHorizontalVelocity(self.mario.rightFacing)
		self.sprites.append(self.fireball)

	def tubeCollision(self, t):
		global Scroll_Position
		m = self.mario

		if (m.xPos <= t.x + t.w and m.xPos >= t.x) or (m.xPos + m.w >= t.x and m.xPos + m.w <= t.x + t.w):	#if mario is above/below the tube
			if m.yShadow + m.h <= t.y or m.y + m.h <= t.y:	#if mario is above the tube
				m.onObject = True
				m.v_velocity = 0.0
				m.y = t.y - m.h
				m.yShadow = m.y

			if m.yShadow >= t.y + t.h:						#if mario is below the tube
				m.v_velocity = 0
				m.y = t.y + t.h
				m.Fizzle_Sound.play()

		if m.y + m.h > t.y and m.y < t.y + t.h:				#if mario is left or right of the tube
			if m.rightFacing:								#if mario is left of the tube
				m.collisionDiff = abs(m.xPos + m.w - t.x)	#find how far mario entered tube
				Scroll_Position -= m.collisionDiff - 5		#push mario out of tube to the left

			if not m.rightFacing:							#if mario is right of the tube
				m.collisionDif = abs(m.xPos - t.x - m.w)	#find how far mario entered tube
				Scroll_Position += m.collisionDif - 4		#push mario out of tube to the right

	def generateLevel(self):
		self.sprites.append(Tube(-1655, 150))
		self.sprites.append(Tube(-1655, -250))
		self.sprites.append(Tube(-1600, 150))
		self.sprites.append(Goomba(-700, 300))
		self.sprites.append(Goomba(-600, 300))
		self.sprites.append(Goomba(-500, 300))
		self.sprites.append(Tube(-335, 340))
		self.sprites.append(Goomba(-150, 300))
		self.sprites.append(Tube(120, 400))
		self.sprites.append(Tube(200, 300))
		self.sprites.append(Tube(200, -300))
		self.sprites.append(Tube(255, -350))
		self.sprites.append(Goomba(600, 300))
		self.sprites.append(Tube(645, -350))
		self.sprites.append(Tube(700, -300))
		self.sprites.append(Tube(700, 300))
		self.sprites.append(Tube(780, 400))
		self.sprites.append(Goomba(900, 100))
		self.sprites.append(Tube(1000, 200))
		self.sprites.append(Tube(1055, 200))
		self.sprites.append(Tube(1110, 250))
		self.sprites.append(Goomba(1300, 100))
		self.sprites.append(Goomba(1400, 100))
		self.sprites.append(Tube(1600, 150))
		self.sprites.append(Tube(1655, -250))
		self.sprites.append(Tube(1655, 150))

class View():
	def __init__(self, model):
		screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.ground_image = pygame.image.load("images/ground.png")
		self.goomba_on_fire = pygame.image.load("images/goomba_on_fire.png")
		self.tubeTop = pygame.image.load("images/tubeTop.png")
		self.model = model
		self.mario_images_R = []
		self.mario_images_L = []
		self.loadImageArray()

	def update(self):
		global Scroll_Position
		self.screen.fill([100,200,255])
		self.screen.blit(self.ground_image, (-100, GROUND_LEVEL))

		for sprite in self.model.sprites:
			if isinstance(sprite, Mario):
				if self.model.mario.rightFacing:
					self.screen.blit(self.mario_images_R[self.model.mario.imageCycle], (sprite.x, sprite.y))
				else:
					self.screen.blit(self.mario_images_L[self.model.mario.imageCycle], (sprite.x, sprite.y))
			elif isinstance(sprite, Goomba):
				if sprite.onFire:
					self.screen.blit(self.goomba_on_fire, (sprite.x - Scroll_Position, sprite.y))
				else:
					self.screen.blit(sprite.image, (sprite.x - Scroll_Position, sprite.y))
			elif isinstance(sprite, Tube):
				self.screen.blit(sprite.image, (sprite.x - Scroll_Position, sprite.y))
				if sprite.y < 0:
					self.screen.blit(self.tubeTop, (sprite.x - Scroll_Position, sprite.y))
				else:
					self.screen.blit(sprite.image, (sprite.x - Scroll_Position, sprite.y))
			else:
				self.screen.blit(sprite.image, (sprite.x - Scroll_Position, sprite.y))

		pygame.display.flip()

	def loadImageArray(self):
		self.mario_images_R.append(pygame.image.load("images/marioR1.png"))
		self.mario_images_R.append(pygame.image.load("images/marioR2.png"))
		self.mario_images_R.append(pygame.image.load("images/marioR3.png"))
		self.mario_images_R.append(pygame.image.load("images/marioR4.png"))
		self.mario_images_R.append(pygame.image.load("images/marioR5.png"))
		self.mario_images_L.append(pygame.image.load("images/marioL1.png"))
		self.mario_images_L.append(pygame.image.load("images/marioL2.png"))
		self.mario_images_L.append(pygame.image.load("images/marioL3.png"))
		self.mario_images_L.append(pygame.image.load("images/marioL4.png"))
		self.mario_images_L.append(pygame.image.load("images/marioL5.png"))

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True
		self.key_right = False
		self.key_left = False
		self.key_up = False
		self.key_space = False
		self.key_ctrl = False

	def update(self):
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
				if event.key == K_LEFT or event.key == K_a:
					self.key_left = True
				if event.key == K_RIGHT or event.key == K_d:
					self.key_right = True
				if event.key == K_UP or event.key == K_SPACE or event.key == K_w:
					self.key_up = True
				if event.key == K_LCTRL:
					self.key_ctrl = True
			elif event.type == KEYUP:
				if event.key == K_LEFT or event.key == K_a:
					self.key_left = False
				if event.key == K_RIGHT or event.key == K_d:
					self.key_right = False
				if event.key == K_UP or event.key == K_SPACE or event.key == K_w:
					self.key_up = False
				if event.key == K_LCTRL:
					self.key_ctrl = False

		m = self.model.mario
		m.yShadow = m.y						#store mario's previous y-position
		if self.key_left:
			m.move(LEFT)
		if self.key_right:
			m.move(RIGHT)
		if self.key_up:
			if m.jumpTimer >= JUMP_LIMIT:
				if m.onSurface():
					m.jump()
		else:
			m.stopJump()
		if self.key_ctrl:
			self.model.addFireball()
			self.key_ctrl = False

class Sound():
	def __init__(self, src, ch, l, vol):
		self.sound = pygame.mixer.Sound(src)
		self.sound.set_volume(vol)
		self.channel = ch
		self.loop = l

	def play(self):
		pygame.mixer.Channel(self.channel).play(self.sound, loops = self.loop)

print("Use the arrow keys or 'WASD' to move. Spacebar or up arrow to jump. Left ctrl to shoot fireballs. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)

BGM = Sound("sound/smw_ovr1.wav", 1, LOOP, 0.05)
BGM.play()

while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")