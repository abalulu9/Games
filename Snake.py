from tkinter import *
from random import randint
from numpy import * 

class Controls():

	def setDirection(self, key):

		self.direction = key.keysym

	def move(self, direction = None):

		if direction is not None:
			self.direction = direction

		if not self.AI:

			self.canvas.delete('snake')

		if self.direction == "Left":
			self.moveLeft()
		elif self.direction == "Right":
			self.moveRight()
		elif self.direction == "Up":
			self.moveUp()
		elif self.direction == "Down":
			self.moveDown()

		if self.alive and not self.AI:
			self.drawSnake()

	def moveLeft(self):
		if self.travelling != 'Right':
			if self.snake[0][0] != 0:
				self.snake.insert(0, (self.snake[0][0] - self.cellwidth, self.snake[0][1]))
				self.travelling = "Left"
			else:
				self.gameOver()
		else:
			self.moveRight()

	def moveRight(self):
		if self.travelling != 'Left':
			if self.snake[0][0] != self.cellwidth * (self.columns - 1):
				self.snake.insert(0, (self.snake[0][0] + self.cellwidth, self.snake[0][1]))
				self.travelling = "Right"
			else:
				self.gameOver()
		else:
			self.moveLeft()

	def moveUp(self):
		if self.travelling != 'Down':
			if self.snake[0][1] != 0:
				self.snake.insert(0, (self.snake[0][0], self.snake[0][1] - self.cellheight))
				self.travelling = "Up"
			else:
				self.gameOver()
		else:
			self.moveDown()

	def moveDown(self):
		if self.travelling != 'Up':
			if self.snake[0][1] != self.cellheight * (self.rows - 1):
				self.snake.insert(0, (self.snake[0][0], self.snake[0][1] + self.cellheight))
				self.travelling = "Down"
			else:
				self.gameOver()
		else:
			self.moveUp()

class Snake(Tk, Controls):

	def __init__(self, AI = False):

		self.AI = AI
		self.rows = 20
		self.columns = 20
		self.width = 500
		self.height = 500
		self.cellwidth = int(self.width / self.columns)
		self.cellheight = int(self.height / self.rows)

		if not AI:

			Tk.__init__(self)

			self.winfo_toplevel().title("Snake")

			self.canvas = Canvas(self, width = self.width, height = self.height + 20)
			self.canvas.pack(side = 'top', fill = 'both')
			self.bind('<KeyPress>', self.setDirection)
			self.highScore = 0



	def drawScore(self):

		self.canvas.delete('score')
		self.canvas.create_text(self.cellwidth, self.height + self.cellheight/2 - 2, anchor = 'w', text = f"Score: {self.score} \t Highscore: {self.highScore}", tags = 'score', font = "Times 12")


	def refresh(self):

		if self.alive:

			self.iterate()

			self.after(int(self.timePerFrame), self.refresh)

	def iterate(self, direction = None):

		self.move(direction)
		self.assessFood()
		self.assessCollision()

	def spawnFood(self):

		self.food = self.randomLocation()

		while self.food in self.snake:
			self.food = self.randomLocation()

	def drawFood(self):

		self.canvas.create_rectangle(self.food[0] + 2, self.food[1] + 2, self.food[0] + self.cellwidth - 2, self.food[1] + self.cellheight - 2, tags = 'food', fill = 'red')

	def randomLocation(self):

		return self.cellwidth * randint(0, self.rows - 2), self.cellheight * randint(0, self.columns - 1)

	def assessFood(self):

		if self.snake[0] == self.food:

			self.increaseLength = True
			self.score += 1
			self.spawnFood()

			if not self.AI:

				self.canvas.delete('food')
				self.drawFood()
				self.highScore = max(self.score, self.highScore)
				self.drawScore()

		if self.increaseLength == False:
			self.snake.pop()
		else:
			self.increaseLength = False

	def assessCollision(self):

		if self.snake[0] in self.snake[1:]:
			self.gameOver()

	def createSnake(self):

		self.snake = [(150 + self.cellwidth * i, self.cellheight * self.columns / 2) for i in range(5, 0, -1)]
		self.increaseLength = False

	def drawSnake(self):

		self.canvas.create_rectangle(self.snake[0][0] + 2, self.snake[0][1] + 2, self.snake[0][0] + self.cellwidth - 2, self.snake[0][1] + self.cellheight - 2, fill = 'gold', tags = 'snake')

		for snakeBit in self.snake[1:]:

			self.canvas.create_rectangle(snakeBit[0] + 2, snakeBit[1] + 2, snakeBit[0] + self.cellwidth - 2, snakeBit[1] + self.cellheight - 2, fill = 'black', tags = 'snake')

	def gameOver(self):

		self.alive = False

		if not self.AI:

			self.canvas.delete('all')
			self.canvas.create_text(250, 250, font = "Times 30", text = f"Game Over -- Score: {self.score}")
			button = Button(text = "Play Again?", font = "Times 20", command = self.start)
			button.configure(width = 10)
			self.canvas.create_window(250, 350, window = button)		

		else:

			return self.score 

	def start(self):

		self.direction = 'Right'
		self.travelling = 'Right'
		self.score = 0
		self.alive = True
		self.createSnake()
		self.spawnFood()


		if not self.AI:

			self.canvas.delete('all')
			self.drawSnake()
			self.canvas.create_rectangle(2, 500, 501, 521)
			self.drawScore()
			self.drawFood()
			self.refresh()

		else:

			self.outputState()



	def outputState(self):
		return self.foodState + [self.directionState] + self.snakeState

	@property 
	def snakeState(self):
		return [int(i/25) for snakeBit in self.snake for i in snakeBit]

	@property
	def foodState(self):
		return [int(food/25) for food in self.food]
	
	@property 
	def directionState(self):

		directionState = 0

		for direction in ['L', 'R', 'U', 'D']:
			if self.direction[0] == direction:
				break
			directionState += 1

		return directionState

	@property 
	def outputGrid(self):

		grid = [[[0, 0, 0] for i in range(self.columns)] for i in range(self.rows)]

		for snakeBit in self.snake:
			grid[int(snakeBit[0]/25)][int(snakeBit[1]/25)][0] = 1

		grid[int(self.food[0]/25)][int(self.food[1]/25)][1] = 1

		return grid

	@property
	def timePerFrame(self):
		return max((4900 - 80 * self.score) / 18, 100)
	
if __name__ == '__main__':
	
	snake = Snake(0)
	snake.start()
	# print(snake.outputState())
	# for i in range(5):
	# 	snake.iterate('Down')
	# 	print(snake.outputState())
	# for i in range(5):
	# 	snake.iterate('Left')
	# 	print(snake.outputState())
	# print(snake.outputGrid())

	snake.mainloop()
