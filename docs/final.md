---
layout: default
title: Final Report
---

## Video

## Project Summary

Our agent's environment is set up as a survival course in Minecraft using the Malmo platform with a start point and end point. The agent learns to navigate this maze filled with magma, a healing item (golden apples), and a poisonous item (spider eyes). These food items are distributed throughout the maze to be collected and consumed. Because the agent only takes damage-over-time from touching magma instead of dying and resetting instantly, we hoped that we could train the agent to both safely navigate the maze and heal itself after making mistakes, all while avoiding poisoning itself. Our end goal would be to have the agent navigate the maze to the end point with full health.

We believed this challenge would be interesting because the benefit from food is not directly attached to the goal of finishing a maze. These food items do not do anything to increase the speed of the agent or give it more time to find the end of the maze. Rather, more or less time is _indirectly_ given to the agent as its health can act as a resource while exploring. This delayed action and reward is able to really test the limits of the algorithmic approach that we decide on.

## Approaches

### Baseline

As a sanity check, we started the agent off with just discrete actions, no food, and just a plain with an end block. We slowly added in items to its environment, eventually leading to magma blocks as "walls", stone for the ground, and glass and bedrock for item spawning.

We used the maze decorator included in Malmo in order to generate mazes. The maze was also sunken into the ground by one block; because the agent does not having jumping in his action space, this prevents it from going out of bounds. To generate the randomly placed items, pseudocode follows.

```
x = array of random int between 0 and length of maze
z = array of random int between 0 and width of maze
for i in range(chosen number of golden apples):
  add golden apple to field at x[i], z[i], and y=one block above surface
  add glass block to field at x[i], z[i], and y=surface level
  
x = array of random int between 0 and length of maze
z = array of random int between 0 and width of maze
for i in range(chosen number of spider eyes):
  add spider eye to field at x[i], z[i], and y=one block above surface
  add bedrock to field at x[i], z[i], and y=surface level
```

The final step was to move to a continous action space in order to enable the agent to eat the food that it is picking up. Eating food does not work with discrete actions in Malmo.

### Proposed Approach

We decided to initially tune our rewards to satisfactory performance while using unchanged default parameters for the PPO algorithm. The Proximal Policy Optimization (PPO) algorithm is described below.

![image](https://user-images.githubusercontent.com/50087239/144312978-29d792f6-f82e-4b00-968a-05257fa069bc.png)

PPO is an on-policy algorithm and is an easy method to implement and tune.

Xiao-Yang Liu, Leader of the deep learning library ElegantRL, describes PPO as follows:

![image](https://user-images.githubusercontent.com/50087239/144314449-9b43e3db-ebf1-4044-9c5f-abc850f6eb33.png)
```
(PPO) follows a classic Actor-Critic framework with four components:
Initialization: initializes the related attributes and networks.
Exploring: explores transitions through the interaction between the Actor-network and the environment.
Computing: computes the related variables, such as the ratio term, exact reward, and estimate advantage.
Updating: updates the Actor and Critic networks based on the loss function and objective function.
```

We will be tuning the following parameters:
- Learning Rate: Self explanatory. This controls how fast the agent will learn during each episode.
- Gamma: A constant known as a discount factor. This allows us to tune how much future states are weighed while the agent is learning. Reaching the end block in the future should be _discounted_ compared to reaching the end block immediately.

We are added immediate view of the grid and agent's health bar to the observation space in our algorithm. This includes magma tiles, food items, and start and end blocks (if they are in the immediate view of the agent). Small negative rewards are given for every step the agent takes. Big positive rewards are given when reaching the end block (a diamond block). Our maze is located in a plain of stone. We tuned the rewards in order to encourage exploration while still encouraging the agent to take more efficient paths towards its destinations, and additionally we wanted to allow it to take some damage to create even shorter paths, but it must heal using golden apples in order to do so effectively.

## Evaluation

### Qualitative

Unfortunately, even after several hours of training, the agent never truly discerns the difference between the food items. They are eaten arbitrarily, but perhaps with more training time it could eventually learn to eat golden apples and to avoid spider eyes. A bug in the current version of Malmo could have lead to the poor performance in food selection. We originally wanted to punish the agent only for dying, but not for touching magma blocks. This would mean that it is completely free to explore on top of magma blocks as long as it has the resources (golden apples) to do so. Unfortunately, rewards on death are currently not working, and thus we had to punish it only for timeouts and for touching magma. This further increases the gap between action and reward when the numerical reward value is coming from slightly inaccurate places.

After a lot of training, the agent does seem to be more careful with its movement than at the start. When the agent is first launched and training begins, its movement is extremely erratic as it simply tries out all of its available inputs. However, as time goes on, it does seem to make less extraneous inputs if it sees a diamond block (end goal for the maze). This is likely a result of its light punishment for every input it makes. However, given a different punishment value for inputs, this movement could have been even more refined or perhaps just stuck in a loop. Early iterations of the agent, especially before a time limit was added, would sometimes get stuck in an infinite loop as it decides to never explore and simply stay alive in one place. We found that reducing the punishment for each step significantly increased the rate at which the agent was willing to explore.

### Quantitative

## References
https://towardsdatascience.com/elegantrl-mastering-the-ppo-algorithm-part-i-9f36bc47b791
https://towardsdatascience.com/proximal-policy-optimization-tutorial-part-2-2-gae-and-ppo-loss-fe1b3c5549e8
- We used these blog posts to learn about the higher level concepts of PPO and about the parameters we would eventually be tuning for it (gamma and learning rate).
