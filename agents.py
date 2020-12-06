from random import randint
from normal_dist import normal_int
from math import radians, cos, sin, atan2, degrees, sqrt
from csv import writer
from utils import convert

EAT_DIST = 2


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, x, y):
        self.x += x
        self.y += y

    def distance(self, pos):
        a = (pos.x - self.x) ** 2
        b = (pos.y - self.y) ** 2
        c = sqrt(a+b)
        return c

    def __str__(self):
        x = f"({self.x}, {self.y})"
        return x


def overlap(pos1, r1, pos2, r2):
    dist = pos1.distance(pos2)
    x = dist - r1 - r2
    if x <= 0:
        return True
    else:
        return False


# TODO Make Agent class inherit from 'Food'
class Agent:
    '''
    '''
    def __init__(self, id, model):
        self.id = id
        self.model = model
        self.pos = Pos(0, 0)
        self.path = [(self.pos.x, self.pos.y)]

        self.eaten = 0

        self.speed = randint(1, 2)
        self.sense = 5
        self.heading = randint(0, 360)

    def born(self):
        # TODO: Choose spot on grid that is not within anyone elses ranges.
        # TODO: Choose spot on outer edge (0,0), (1,0), (0,1), (1,1)
        pass

    def die(self):
        self.model.agents.remove(self)

    def closest_food(self):
        # Check for nearby food
        nearby_food = []
        food_dist = []
        for each_food in self.model.food:
            if overlap(self.pos, self.sense, each_food.pos, each_food.size):
                nearby_food.append(each_food)
                food_dist.append(self.pos.distance(each_food.pos))

        # Closest food
        if nearby_food:
            i = food_dist.index(min(food_dist))
            return nearby_food[i]
        else:
            return None

    def eat(self, food):
        self.eaten += 1
        food.die()

    def step(self):

        # Check Surroundings and Determine State #

        target_food = self.closest_food()

        if target_food is None:
            state = 'wander'
        elif self.pos.distance(target_food.pos) < EAT_DIST:
            self.eat(target_food)
            target_food = self.closest_food()
            state = 'chase'
            if target_food is None:
                state = 'wander'
        else:
            state = 'chase'

        # Get New Heading Based on State #
        # Follow Food
        if state == 'chase':
            dy = target_food.pos.y - self.pos.y
            dx = target_food.pos.x - self.pos.x
            tst = degrees(atan2(dy, dx))
            if tst < 0:
                tst += 360
            new_heading = tst

        # If wandering
        if state == 'wander':
            new_heading = convert(self.heading + normal_int(60))

        # Apply
        self.heading = new_heading
        add_x = self.speed * cos(radians(new_heading))
        add_y = self.speed * sin(radians(new_heading))
        self.pos.add(add_x, add_y)
        self.path.append((self.pos.x, self.pos.y))


class Food:
    def __init__(self, id, model):
        self.id = id
        self.model = model
        self.pos = Pos(randint(-10, 10), randint(-10, 10))
        self.size = 1
        self.eaten = False

    def die(self):
        self.model.food.remove(self)


class Model:
    '''
    '''
    def __init__(self, n_agents, n_food):
        self.n_agents = n_agents
        self.agents = []
        self.n_food = n_food
        self.food = []
        for i in range(n_agents):
            self.agents.append(Agent(i, self))
        for i in range(n_food):
            self.food.append(Food(i, self))

    def step(self):
        for agent in self.agents:
            agent.step()


if __name__ == '__main__':

    my_model = Model(2, 10)

    data = [['object', 'time', 'x', 'y']]

    for food in my_model.food:
        data.append([f"Food{food.id}", "0", food.pos.x, food.pos.y])

    for i in range(100):
        my_model.step()
        for agent in my_model.agents:
            data.append([f"Agent {agent.id}", i, agent.pos.x, agent.pos.y])

    with open("tst.csv", 'w', newline='') as f:
        r = writer(f)
        r.writerows(data)

    for agent in my_model.agents:
        print(f"Agent {agent.id} has eaten {agent.eaten}.")
