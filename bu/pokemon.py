class Pokemon:
	def __init__(self, n):
		self.name = n
	
	def printname(self):
		print("You have chosen to start with " + self.name)

class Buddy(Pokemon):
	def __init__(self, n, num):
		super().__init__(self, n)
		self.numDays = num


starter = Pokemon("Charmander")
starter.printname()

