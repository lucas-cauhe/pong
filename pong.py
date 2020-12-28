import pygame
from pygame.locals import *
import sys
from PIL import Image
import random
import math
import time

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480


def plot_countdown(screen):
	countdown = 3
	green = (0, 255, 0)
	blue = (0, 0, 128)
	font = pygame.font.Font('freesansbold.ttf', 64)
	for i in range(3):
		text = font.render(str(countdown), True, green, blue)
		screen.blit(text, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
		pygame.display.flip()
		time.sleep(1)
		countdown -= 1

def predict(ball_pos, angle, directiony, directionx): # predice la posición final de la pelota dependiendo de si va a rebotar o no

	ans = 0
	distance_to_bar = (SCREEN_WIDTH/2) -25
	x = distance_to_bar * math.tan(angle)
	if directiony < 0:
		ans = ball_pos + x
	else:
		ans = ball_pos - x

	if ans > 480 or ans < 0:  # Check whether it will bounce or not
		ans = get_bounce_prediction(ball_pos, angle, directionx, directiony)
		
	return ans

def get_bounce_prediction(ball_pos, angle, directionx, directiony):
	ans = 0
	if directiony < 0:
		x = (SCREEN_HEIGHT - ball_pos) * math.tan(angle)
		if directionx >= 0:
			res = (SCREEN_WIDTH-(SCREEN_WIDTH/2 + x)) * math.tan(angle)
			ans =  400 - res
		else:
			res = (SCREEN_WIDTH/2 - x) * math.tan(angle)
			ans =  400 - res
	else:
		x = ball_pos * math.tan(angle)
		if directionx >= 0:
			ans = (SCREEN_WIDTH-(SCREEN_WIDTH/2 + x)) * math.tan(angle)
			
		else:
			ans = (SCREEN_WIDTH/2 - x) * math.tan(angle)
			

	return ans

class Bar:

	def __init__(self, image, screen):
		self.image = image
		self.img_widht, self.img_height = Image.open(self.image).size
		self.screen = screen
		self.x = 0
		self.y = 0
		self.score = 0

	def plot_image(self, axis):
		self.x, self.y = axis
		image_to_plot = pygame.image.load(self.image).convert_alpha()

		self.screen.blit(image_to_plot, axis)
	
	def get_axis(self):
		return self.x, self.y
	def set_axis(self, axis):
		self.x, self.y = axis
	def get_size(self):
		return self.img_widht, self.img_height
	def get_score(self):
		return self.score

	def move_up(self):
		if self.y != 0:
			self.y -= 0.375
		else:
			self.y = 0

	def move_down(self):
		if self.y != SCREEN_HEIGHT-150:	
			self.y += 0.375
		else:
			self.y = SCREEN_HEIGHT-150

class Ball:

	def __init__(self, image, screen):
		self.image = image
		self.img_widht, self.img_height = Image.open(self.image).size
		self.screen = screen
		self.x = 0
		self.y = 0
		self.directionx = random.uniform(-1, 1)
		self.directiony = random.uniform(-1, 1) 
		self.z = random.uniform(0, 1)  
		self.collisiony = 0
		self.predictionr = 0
		self.predictionl = 0

 
	def plot_image(self, axis):
		self.x, self.y = axis
		image_to_plot = pygame.image.load(self.image).convert_alpha()

		self.screen.blit(image_to_plot, axis)
	
	def get_axis(self):
		return self.x, self.y

	def move(self):
		if self.x == SCREEN_WIDTH/2 and self.directionx >= 0:
			self.predictionr = predict(self.y, self.z, self.directiony, self.directionx)
			self.predictionl = 0
		elif self.x == SCREEN_WIDTH/2 and self.directionx < 0:
			self.predictionl = predict(self.y, self.z, self.directiony, self.directionx)
			self.predictionr = 0

		if self.directionx >= 0:
			self.x += 0.5 * math.cos(self.z) 
		else:
			self.x -= 0.5 * math.cos(self.z)
		if self.directiony>= 0:
			self.y -= 0.5 * math.sin(self.z)
		else:
			self.y += 0.5 * math.sin(self.z)
		

	def collision(self, left_bar, right_bar):
		if self.y <= 0:
			#print('has collided at: ', self.x)
			self.directiony = -1
		elif self.y >= SCREEN_HEIGHT-self.img_height:
			#print('has collided at: ', self.x)
			self.directiony = 1

		left_x, left_y = left_bar.get_axis()
		right_x, right_y = right_bar.get_axis()
		left_width, left_height = left_bar.get_size()
		right_width, right_height = right_bar.get_size()

		if self.x <= left_x+left_width and self.x >= 0 and self.y >= left_y and self.y <= left_y+5+left_height:
			self.directionx = 1
		elif self.x >= right_x-right_width and self.x <= SCREEN_WIDTH and self.y >= right_y and self.y <= right_y+right_height:
			self.collisiony = self.y
			self.directionx = -1

		if self.x < 0:
			right_bar.score += 1
			plot_countdown(self.screen)
			self.directionx = random.uniform(-1, 1)
			self.directiony = random.uniform(-1, 1)
			self.z = random.uniform(0, 1)
			self.plot_image((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
			right_bar.set_axis((SCREEN_WIDTH-25, SCREEN_HEIGHT/2 - 75))
			left_bar.set_axis((0, SCREEN_HEIGHT/2 - 75))
		elif self.x > SCREEN_WIDTH:
			left_bar.score += 1
			plot_countdown(self.screen)
			self.directionx = random.uniform(-1, 1)
			self.directiony = random.uniform(-1, 1)
			self.z = random.uniform(0, 1)
			self.plot_image((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
			right_bar.set_axis((SCREEN_WIDTH-25, SCREEN_HEIGHT/2 - 75))
			left_bar.set_axis((0, SCREEN_HEIGHT/2 - 75))





def main():
	pygame.init()

	count = 0
	screen = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption("Holi bros")
	
	plot_countdown(screen)

	background_image = 'images/background.png'
	bar_image = 'images/Bar.png'
	ball_image = 'images/ball.png'
	left_pong_bar = Bar(bar_image, screen)
	right_pong_bar = Bar(bar_image, screen) 

	background = pygame.image.load(background_image).convert_alpha()
	screen.blit(background, (0, 0))

	font = pygame.font.Font('freesansbold.ttf', 64)
	blue = (0, 0, 128)
	player1 = font.render(str(left_pong_bar.get_score()), True, blue)
	player2 = font.render(str(right_pong_bar.get_score()), True, blue)
	screen.blit(player1, (SCREEN_WIDTH/4, SCREEN_HEIGHT/5))
	screen.blit(player2, (SCREEN_WIDTH*3/4, SCREEN_HEIGHT/5))

	ball = Ball(ball_image, screen)
	ball.plot_image((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

	left_pong_bar.plot_image((0, SCREEN_HEIGHT/2 - 75))	
	right_pong_bar.plot_image((SCREEN_WIDTH-25, SCREEN_HEIGHT/2 - 75))

	pygame.display.update()
	while True:

		ball.move()
		ball.collision(left_pong_bar, right_pong_bar)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		if ball.predictionr == 0:
			if right_pong_bar.y < SCREEN_HEIGHT/2 - 75:
				right_pong_bar.move_down()
			else:
				right_pong_bar.move_up()

		if ball.predictionl == 0:
			if left_pong_bar.y < SCREEN_HEIGHT/2 - 75:
				left_pong_bar.move_down()
			else:
				left_pong_bar.move_up()
		if right_pong_bar.y != ball.predictionr and ball.predictionr != 0:
			if ball.predictionr < right_pong_bar.y:
				right_pong_bar.move_up()
			else:
				right_pong_bar.move_down()
		elif left_pong_bar.y != ball.predictionl and ball.predictionl != 0:
			if ball.predictionl < left_pong_bar.y:
				left_pong_bar.move_up()
			else:
				left_pong_bar.move_down()


		keys = pygame.key.get_pressed()
		if keys[K_UP]:
			right_pong_bar.move_up()
		elif keys[K_DOWN]:
			right_pong_bar.move_down()
		elif keys[K_w]:
			left_pong_bar.move_up()
		elif keys[K_s]:
			left_pong_bar.move_down()
				

		right_pong_bar_axis = right_pong_bar.get_axis()
		left_pong_bar_axis = left_pong_bar.get_axis()
		ball_axis = ball.get_axis()

		screen.blit(background, (0, 0))
		ball.plot_image(ball_axis)
		right_pong_bar.plot_image(right_pong_bar_axis)
		left_pong_bar.plot_image(left_pong_bar_axis)
		player1 = font.render(str(left_pong_bar.get_score()), True, blue)
		player2 = font.render(str(right_pong_bar.get_score()), True, blue)
		screen.blit(player1, (SCREEN_WIDTH/4, SCREEN_HEIGHT/5))
		screen.blit(player2, (SCREEN_WIDTH*3/4, SCREEN_HEIGHT/5))

		pygame.display.flip()


if __name__ == "__main__":
	main()
