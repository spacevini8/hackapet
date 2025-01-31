class Potato:
    def __init__(self, maxWater, maxFood, maxBugs, maxHealth):
        self.maxWater = maxWater
        self.maxFood = maxFood
        self.maxBugs = maxBugs
        self.maxHealth = maxHealth

        self.water = self.maxWater//4
        self.food = self.maxFood//4
        self.bugs = 0
        self.health = maxHealth

        self.alive = True