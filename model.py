from agents import Agent, Food
from random import shuffle


class Model:
    '''Initializes, Runs, and Captures the interactions between Agents and Food'''
    def __init__(self, params):
        self.params = params
        self.agents = []
        self.food = []
        self.current_day = 0
        self.remaining_steps = self.params["DAILY_STEPS"]

        # Data Capture Attributes
        self.pop_sum = [['day', 'agents']]
        self.attr_sum = [['day', 'avg_speed', 'avg_size', 'avg_sense']]
        self.agent_data = [['id', 'birthday', 'deathday', 'reproduced', 'food_eaten', 'agents_eaten']]
        self.food_data = [['id', 'birthday', 'deathday']]

        # Initialize original cohort of agents
        for i in range(self.params["N_AGENTS"]):
            self.agents.append(Agent(self, params['SPEED'], params['SIZE'], params['SENSE']))

        # Initialize original cohort of food
        self.restore_food()

    def restore_food(self):
        '''Determines how much food to add each day and adds it.'''
        remaining_food = 0

        # Count the number of living foods
        if self.food:
            for food in self.food:
                if food.alive:
                    remaining_food += 1

        # Add food up to N_FOOD amount
        for i in range(self.params["N_FOOD"] - remaining_food):
            new_food = Food(self)
            self.food.append(new_food)

    def step(self):
        '''Execute each living agents 'step' method'''
        for agent in self.agents:
            if agent.alive:
                agent.step()

    def day(self):
        '''Runs, resets, and captures the actions of each day'''
        # Let any applicable agents reproduce
        for agent in self.agents:
            if agent.reproduce:
                agent.birth()
                agent.reproduce = False

        # Reset remaining steps each day
        self.remaining_steps = self.params["DAILY_STEPS"]

        # Capture # of Alive Agents
        living_agents = 0
        speeds = []
        size = []
        sense = []
        for agent in self.agents:
            if agent.alive:
                living_agents += 1
                speeds.append(agent.speed)
                size.append(agent.size)
                sense.append(agent.sense)

        self.pop_sum.append([self.current_day, living_agents])

        # Average Speed, but return 0 if no agents (i.e., all are dead)
        avg_speed = sum(speeds) / len(speeds) if len(speeds) else 0
        avg_size = sum(size) / len(size) if len(size) else 0
        avg_sense = sum(sense) / len(sense) if len(sense) else 0
        self.attr_sum.append([self.current_day, avg_speed, avg_size, avg_sense])

        # Let agents move around and capture their movement
        for i in range(self.params["DAILY_STEPS"]):
            self.step()
            self.remaining_steps -= 1

        # After each agent has moved, let them reset
        for agent in self.agents:
            agent.end_day()

        # Reorder the Agents to reduce repeated bias
        shuffle(self.agents)

        # Restore the environments food to N_FOOD
        self.restore_food()

    def run(self):
        '''Runs the model for N_DAYS'''
        for day in range(self.params["N_DAYS"]):
            self.day()
            self.current_day += 1

