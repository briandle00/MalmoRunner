---
layout: default
title:  Status
---
<iframe width="560" height="315" src="https://www.youtube.com/embed/znTW1nh2T-8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Summary
Our agent's environment is set up as a survival course in Minecraft using the Malmo platform with a start point and end point. Agent learns how to navigate a maze which is covered with many magma tiles and food items. There are many food items distributed in the maze available for collection and consumption. Some our poisonous and some add health. We want our agent to be able to learn saturation values of various food items available to it. This is a hidden value that determines how long a food is able to keep a player full for, even beyond the regular displayed hunger bar. Our end goal for the agent is to be able to navigate the fastest path to the end in full health.


## Approach:
We are experimenting with two different Reinforcement algorithms. We have started with Proximal Policy Optimization(PPO) algorithm. PPO is an on-policy algorithm and is an easy method to implement and tune.

In our first method We are adding an immediate view of the grid and agent's health bar to the Observation space in our algorithm. This includes magma tiles, food items, start and end blocks if they are in the immediate view of the agent. Small Negative Rewards are given for every step the agent takes and the status of it's health bar being less than 100 percent. Big Positive rewards are given when reaching the end block. Currently we are training with the default parameters of the PPO function in Rllib library. We will be tuning the parameter after our first successful run.

<img width="741" alt="Returns_project" src="docs/returns_project.png">


## Evaluation
As we train we are using a log_returns function to log the reward progress of the agent with every step. We are hoping to see an upward graph as the agent trains.
As Qualitive Evaluation we are monitoring the Agent's progress on the screen hoping to see it successfully make the correct decisions.

Here is the result from the log:
<img width="741" alt="" src="https://user-images.githubusercontent.com/62405418/141696775-10b495b7-5775-4ac9-bf58-fd4caa95cdd0.png">


## Remaining Goals and Challenges:
One of our biggest challenges has been system incompatibility and slow running time on some of team memebers devices. This makes experimenting, training and building the enviroment more challenging.
Currently we are working with Discrete movement If successful at training we would love to work with Continuous Movement. At this moment we are using the default settings for the PPO function. We would love to experiment with a different learning rate and tuning other parameters as well. We are planning to also experiment with DQN which is based on Q network given we have extra time.

## Resources Used:
<strong> https://spinningup.openai.com/en/latest/algorithms/ppo.html</strong></a> 

<strong> https://medium.datadriveninvestor.com/which-reinforcement-learning-rl-algorithm-to-use-where-when-and-in-what-scenario-e3e7617fb0b1</strong></a> 

<strong> https://spinningup.openai.com/en/latest/algorithms/ppo.html</strong></a> 
