from random import randint, choice, uniform
from math import radians, cos, sin, atan2, degrees, sqrt


class Pos:
    '''Represents current coordinates of objects on a 2-D plane'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, x, y):
        '''Adds to the current coordinates.'''
        self.x += x
        self.y += y

    def distance(self, pos):
        '''Calculate distance from/to another Pos'''
        a = (pos.x - self.x) ** 2
        b = (pos.y - self.y) ** 2
        c = sqrt(a+b)
        return c

    def oob(self, width, height):
        '''Determines if position is Out of Bounds, given known width/height dimensions'''
        if self.x < 0 or self.y < 0 or self.x > width or self.y > height:
            return True
        else:
            return False

    def edge(self, w, h):
        '''Determines which edge, if any, given known width/height dimensions, the current position is on'''
        if self.x == 0:
            return 'l'
        elif self.x == w:
            return 'r'
        elif self.y == 0:
            return 'b'
        elif self.y == h:
            return 't'
        else:
            return None

    def nearest_edge(self, w, h):
        '''Returns the Pos of the nearest edge'''
        border_distances = {"dt": h - self.y,
                            "dr": w - self.x,
                            "db": self.y,
                            "dl": self.x}

        target_border = min(border_distances, key=border_distances.get)

        if target_border == "dt":
            x, y = self.x, h
        elif target_border == "dr":
            x, y = w, self.y
        elif target_border == "db":
            x, y = self.x, 0
        else:
            x, y = 0, self.y

        return Pos(x, y)

    def __str__(self):
        x = f"({self.x}, {self.y})"
        return x


def convert(x):
    '''Used to keep degrees within 0 and 360'''
    if x < 0:
        num = 360 + x
    elif x > 360:
        num = x - 360
    else:
        num = x

    return num


# This could be modified to be a method in Pos class
def overlap(pos1, r1, pos2, r2):
    '''Determines overlap between two objects, using their position and size (radius)'''
    dist = pos1.distance(pos2)
    x = dist - r1 - r2
    if x <= 0:
        return True
    else:
        return False


class Food:
    '''Generic food that can be eaten by Agents'''
    def __init__(self, model):
        self.model = model
        self.birthday = self.model.current_day
        self.id = str(self.birthday) + str(len(self.model.agents))
        self.pos = Pos(uniform(0, self.model.params["WIDTH"]), randint(0, self.model.params["HEIGHT"]))
        self.size = self.model.params["FOOD_SIZE"]
        self.value = self.model.params["FOOD_VALUE"]
        self.alive = True

    def die(self):
        '''Sets alive attribute to False'''
        self.alive = False
        self.model.food_data.append([self.id, self.birthday, self.model.current_day])
        self.model.food.remove(self)


class Agent:
    '''A being with a speed, size, sense, position, and heading'''
    def __init__(self, model, speed, size, sense):
        self.model = model
        self.birthday = self.model.current_day
        self.id = str(self.birthday) + str(len(self.model.agents))
        self.pos = None
        self.heading = None
        self.speed = speed
        self.size = size
        self.sense = sense
        self.born()
        self.eaten = 0
        self.energy_per_step = (self.size**3) * (self.speed**2) + self.sense
        self.value = self.energy_per_step * self.model.params["DAILY_STEPS"]
        self.reproduce = False
        self.alive = True
        self.home = False
        self.data = {"days_survived": 0, "reproduced": 0, "food_eaten": 0, "agents_eaten": 0}

    def born(self):
        '''Randomly chooses a place to live, provided it is away from other predators / prey'''
        h, w = self.model.params["HEIGHT"], self.model.params["WIDTH"]

        safe = False
        while not safe:

            side = choice(['t', 'r', 'b', 'l'])
            if side == 't':
                x, y = uniform(0, w), h
                heading = uniform(180, 360)
            elif side == 'r':
                x, y = w, uniform(0, h)
                heading = uniform(90, 270)
            elif side == 'b':
                x, y = uniform(0, w), 0
                heading = uniform(0, 180)
            else:
                x, y = 0, uniform(0, h)
                heading = choice([uniform(0, 90), uniform(270, 360)])

            safe = True
            for agent in self.model.agents:
                if agent.pos.distance(Pos(x, y)) < self.model.params["EAT_DIST"]:
                    if agent.size > self.size * (1 + self.model.params["PREDATOR_RATIO"]):
                        safe = False
                        break
                    elif agent.size < self.size * (1-self.model.params["PREDATOR_RATIO"]):
                        safe = False
                        break

            self.pos = Pos(x, y)
            self.heading = heading

    def die(self):
        '''Sets alive status to False'''
        self.alive = False
        self.model.agent_data.append([self.id, self.birthday, self.model.current_day,
                                      self.speed, self.size, self.sense,
                                      self.data['reproduced'], self.data['food_eaten'], self.data['agents_eaten']])
        self.model.agents.remove(self)

    def closest_food(self):
        '''Returns the closest food / edible Agent'''
        # Check for nearby food
        nearby_food = []
        food_dist = []
        for each_food in self.model.food:
            if each_food.alive and overlap(self.pos, self.sense, each_food.pos, each_food.size):
                nearby_food.append(each_food)
                food_dist.append(self.pos.distance(each_food.pos))

        # Check for nearby prey
        for prey in self.model.agents:
            if prey.alive and not prey.home and prey.size <= self.size * (1 - self.model.params["PREDATOR_RATIO"]):
                if overlap(self.pos, self.sense, prey.pos, prey.size):
                    nearby_food.append(prey)
                    food_dist.append(self.pos.distance(prey.pos))

        # Get closest food or prey
        if nearby_food:
            i = food_dist.index(min(food_dist))
            return nearby_food[i]
        else:
            return None

    def predators(self):
        '''Returns the closest predator, if any'''
        # Check for nearby predators
        predators_detected = []
        predator_dist = []
        for predator in self.model.agents:
            if predator.alive and not predator.home and predator.size >= self.size * (1 + self.model.params["PREDATOR_RATIO"]):
                if overlap(self.pos, self.sense, predator.pos, predator.size):
                    predators_detected.append(predator)
                    predator_dist.append(self.pos.distance(predator.pos))

        # Get nearest predator
        if predators_detected:
            i = predator_dist.index(min(predator_dist))
            return predators_detected[i]
        else:
            return None

    def eat(self, food):
        '''Takes another Agents / Foods energy and kills it.'''
        self.eaten += food.value
        if isinstance(food, Agent):
            self.data["agents_eaten"] += 1
        else:
            self.data["food_eaten"] += 1
        food.die()

    def target(self, pos):
        '''Returns the appropriate heading given a target pos'''
        dy = pos.y - self.pos.y
        dx = pos.x - self.pos.x
        direction = degrees(atan2(dy, dx))
        if direction < 0:
            direction += 360

        return direction

    def step(self):
        '''Uses the environment to determine heading and move Agent.'''

        state = "assessing"

        if self.home or not self.alive:
            # Do nothing
            return

        # Determine whether they could make it home before the day ends
        steps_left = self.model.remaining_steps
        nearest_edge = self.pos.nearest_edge(self.model.params["WIDTH"], self.model.params["HEIGHT"])
        distance_home = self.pos.distance(nearest_edge)

        # Must have eaten at least your value in order to head home
        if self.eaten >= self.value:
            if (distance_home / self.speed) + self.model.params["STEP_BUFFER"] >= steps_left:
                state = 'sprint_home'

        # Get closest predator
        predators = self.predators()

        # If headed home, bypass
        if state == 'sprint_home':
            state = 'home'
        elif predators:
            state = 'run'
        elif self.eaten >= self.value * (1 + self.model.params["REPRODUCTION_MOD"]):
            state = 'home'
        else:
            target_food = self.closest_food()

            if target_food is None:
                state = 'wander'
            elif self.pos.distance(target_food.pos) < self.model.params["EAT_DIST"]:
                self.eat(target_food)
                target_food = self.closest_food()
                state = 'chase'
                if target_food is None:
                    state = 'wander'
            else:
                state = 'chase'

        # Run from Predator
        if state == 'run':
            # Get direction of predator
            direction = self.target(predators.pos)

            # Flip a 180 and run!
            new_heading = convert(direction + 180)

        # Go home
        if state == 'home':
            direction = self.target(nearest_edge)
            new_heading = direction

        # Follow Food
        if state == 'chase':
            direction = self.target(target_food.pos)
            new_heading = direction

        # If wandering
        if state == 'wander':
            new_heading = convert(self.heading + uniform(-self.model.params["HEADING_MOD"],
                                                         self.model.params["HEADING_MOD"]))

        # SET NEW HEADING
        self.heading = new_heading
        dir_x = cos(radians(new_heading))
        dir_y = sin(radians(new_heading))

        # ADD SPEED MODIFIER
        add_x = dir_x * self.speed
        add_y = dir_y * self.speed

        # TODO: NEEDS A MORE REALISTIC SOLUTION TO BOUNDARY CHECK
        new_pos = Pos(self.pos.x + self.speed*dir_x, self.pos.y + self.speed*dir_y)
        if new_pos.oob(self.model.params["WIDTH"], self.model.params["HEIGHT"]):
            # If home and oob, stick to the edge
            if state == 'home':
                self.home = True
                dx, dy = nearest_edge.x, nearest_edge.y
                if dy == self.model.params["HEIGHT"]:
                    add_x = 0
                    add_y = self.model.params["HEIGHT"] - self.pos.y
                elif dx == self.model.params["WIDTH"]:
                    add_x = self.model.params["WIDTH"] - self.pos.x
                    add_y = 0
                elif dy == 0:
                    add_x = 0
                    add_y = -self.pos.y
                elif dx == 0:
                    add_x = -self.pos.x
                    add_y = 0

            else:
                new_heading = convert(self.heading + 180)
                self.heading = new_heading
                dir_x = cos(radians(new_heading))
                dir_y = sin(radians(new_heading))
                add_x = dir_x * self.speed
                add_y = dir_y * self.speed

        # Apply
        self.pos.add(add_x, add_y)

    def end_day(self):
        '''Resets (or kills) the Agent for a new day'''
        if self.alive and self.home and self.eaten >= self.value:
            if self.eaten >= self.value * (1 + self.model.params["REPRODUCTION_MOD"]):
                self.reproduce = True
            self.eaten = 0
            self.home = False

            # Determine new heading:
            side = self.pos.edge(self.model.params["WIDTH"], self.model.params["HEIGHT"])
            if side == 't':
                self.heading = uniform(180, 360)
            elif side == 'r':
                self.heading = uniform(90, 270)
            elif side == 'b':
                self.heading = uniform(0, 180)
            elif side == 'l':
                self.heading = choice([uniform(0, 90), uniform(270, 360)])

            self.data["days_survived"] += 1

        else:
            self.die()

    def birth(self):
        '''Creates a mutated Agent and adds it to the model'''
        mutate = True if uniform(0, 1) <= self.model.params["MUTATION_RATE"] else False

        speed = self.speed
        size = self.size
        sense = self.sense

        if mutate:
            if self.model.params["SPEED_ALLOW"]:
                speed *= 1 + (choice([-1, 1]) * self.model.params["SPEED_MOD"])
                speed = round(speed, 4)

            if self.model.params["SIZE_ALLOW"]:
                size *= 1 + (choice([-1, 1]) * self.model.params["SIZE_MOD"])
                size = round(size, 4)

            if self.model.params["SENSE_ALLOW"]:
                sense *= 1 + (choice([-1, 1]) * self.model.params["SENSE_MOD"])
                sense = round(sense, 4)

        # Right now, the offspring is technically born at a random location
        offspring = Agent(self.model, speed, size, sense)

        self.model.agents.append(offspring)

        self.data["reproduced"] += 1

