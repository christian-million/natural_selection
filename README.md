# Disclaimer

I am trying to replicate the simulation model presented in the following youtube video using python: https://www.youtube.com/watch?v=0ZGbIKd0XrM&vl=en

The thoughts and ideas presented in that video are not my own and all credit should go to the owner of that channel / video / content. I am using the thoughts and ideas in that video educationally - as a prompt to improve my skills in python.

# Overview

Ultimately, my goal is to create a GUI from which the user can set parameters on a headless (custom) version of [this
natural selection simulation](https://www.youtube.com/watch?v=0ZGbIKd0XrM&vl=en). A summary of the simulation results will be sent to a Discord server using their
API.

If time allows, I’d love to be able to set parameters and execute the model with Discord commands, but I
am nervous that building the headless simulator will take up most of my time.

# Implementation

- A tkinter application
    - with text entry fields and drop down menus accompanied by some descriptive text that details how it might impact the simulation
- An Agent class representing the creatures in the model
    - Attributes like speed, size, sense, and alive
    - Methods like move, eat, replicate, and die
- A Model class that manages execution and data collection.
    - Attributes like n_agents and n_food
    - (Considering a Parameters class to pass to model. . . )
    - Methods like get_data and run
- A Food class for the creatures to eat.
    - Maybe creatures should inherit from food class for when I implement eating other creatures?
- Pushing to discord using a webhook
    - Maybe a discord bot if time allows

# Simulation Considerations

## Forward Facing Attributes

- `speed`: How far a creature can travel in a single step. (Faster creatures get food faster but spend more
energy)
- `size`: How big a creature is. (Can eat creatures 20% smaller than it, but uses more energy)
- `sense`: How far away a creature can detect food. (Can find food more efficiently, but costs energy).

# Other

- `eat_distance`: How far away do creatures need to be in order to eat the food. Does the probability
of a successful ‘eat’ increase as distance closes after a certain point?
- `heading`: Which direction is a creature headed. (Depends on state)
- `state`: A creatures goals / motivation?
    - `wandering`: Walking around looking for food
    - `chasing`: Detected food / smaller creature and is headed straight for it
    - `fleeing`: Detected larger creature and is headed away
    - `home`: Found food and is headed home
    - `Combos`?: fleeing + home found food but also being chased?

# Parameters

- prob_mutation: Probability that a mutation will happen on reproduction
- mutation_modifier: How much does each attribute change on mutation (speed, size,sense)
- n_agent: How many creatures to start with
- n_food: How much food appears each day?
- days: How many days to run the simulation
- steps: How many steps does each creature get per day?
- food_value: How nutritious is food?
- environment: How large is the environment?