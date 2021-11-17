---
layout: default
title:  Status
---
<iframe width="560" height="315" src="https://www.youtube.com/embed/znTW1nh2T-8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Summary
Our agent's environment is set up as a survival course in Minecraft using the Malmo platform with a start point and end point. Agent learns how to navigate a maze which is covered with many magma tiles and food items. There are many food items distributed in the maze available for collection and consumption. Some our poisonous and some add health. We want our agent to be able to learn saturation values of various food items available to it. This is a hidden value that determines how long a food is able to keep a player full for, even beyond the regular displayed hunger bar. Our end goal for the agent is to be able to navigate the fastest path to the end in full health.


## Approach:
We are experimenting with two different Reinforcement algorithms PPO and DQN. We have started with Proximal Policy Optimization(PPO) algorithm. PPO is an on-policy algorithm and is an easy method to implement and tune.

<img width="741" alt="Screenshot" src="https://user-images.githubusercontent.com/62405418/141696775-10b495b7-5775-4ac9-bf58-fd4caa95cdd0.png">

In our first method We are adding an immediate view of the grid and agent's health bar to the Observation space in our algorithm. This includes magma tiles, food items, start and end blocks if they are in the immediate view of the agent. Small Negative Rewards are given for every step the agent takes. Big Positive rewards are given when reaching the end block. This block is a diamond block. It's blue and initially out of agent's field of view. 
Our maze is located in a field of grass. Agent will recieve negative reward if it steps off the the maze. We are working to making the agent turn before he can take this move. We are assigning a negative reward in each step. This is to reward the agent solving the maze with the fewest steps possible.

Currently we are training with the default parameters of the PPO function in Rllib library. We will be tuning some parameter after our first successful run. We are planning to expermited with different gammas and learning rates. We will be expermineting with a deep learning model in the up comming weeks.


## Evaluation
As we train we are using a log_returns function to log the reward progress of the agent with every step. We are hoping to see an upward graph as the agent trains.
As Qualitive Evaluation we are monitoring the Agent's progress on the screen hoping to see it successfully make the correct decisions.

Here is the result from the log:<br />
![alt text](https://github.com/briandle00/MalmoRunner/blob/1b2b22cbbdf7db4d229b1aa46f6ee289a2e19d4e/docs/returns_project.png?raw=true)
<br />
As you can see from the log results, as the number of steps increase you can see a gradual increase in the reward. Although the log images shows that the rewards are a little irratic, the rewards still gradually move upwards in the log with the increase in number of steps. This result was achieved by running the Agent in minecraft for 2 hours. Running it for more time and consequently for more steps, we will see a gradual increase in the rewards as well. With the current results, I expect the rewards to steadily go above and venture into positive reward space after about 50000 steps. Currently, the reward system is such that the longer the agent stays in the maze the more negative reward it gets. Agent gets positive reward for reaching the end diamond block. Agent also gets negative reward for going out of the maze limits or touching the magma block. Since many aspects of the reward system are negative the overall reward is going to be negative for many steps at the beginning of the game. After a considerable amount of steps we will start seeing positive rewars when the agent starts reaching the end diamond block. Since the observation space is 101 for each obsrvation that is made, the run time is long for each step. But running it for longer time will provide promising results and hopefully the agent is able to complete the maze and also evealuate which food item is better for its health.

With future updates to the RL algorithm and continuous actions implemented in the game, I expect a much better log result. An additional change to the reward system focusing on more positive rewards rather than negatives. This way, we will say a positive log results and agent will be able to learn better and and solve the maze quicker.


## Remaining Goals and Challenges:
One of our biggest challenges has been system incompatibility and slow running time on some of team memebers devices. This makes experimenting, training and building the enviroment more challenging.
Currently we are working with Discrete movement If successful at training we would love to work with Continuous Movement. At this moment we are using the default settings for the PPO function. We would love to experiment with a different learning rate and tuning other parameters as well. We are planning to also experiment with DQN which is based on Q network given we have extra time.

## Resources Used:
<strong> https://spinningup.openai.com/en/latest/algorithms/ppo.html</strong>

<strong> https://medium.datadriveninvestor.com/which-reinforcement-learning-rl-algorithm-to-use-where-when-and-in-what-scenario-e3e7617fb0b1</strong></a> 

<strong> https://spinningup.openai.com/en/latest/algorithms/ppo.html</strong>
