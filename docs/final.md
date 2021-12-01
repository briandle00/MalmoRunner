---
layout: default
title: Final Report
---

## Video

## Project Summary

Our agent's environment is set up as a survival course in Minecraft using the Malmo platform with a start point and end point. The agent learns to navigate this maze filled with magma, a healing item (golden apples), and a poisonous item (spider eyes). These food items are distributed throughout the maze to be collected and consumed. Because the agent only takes damage-over-time from touching magma instead of dying and resetting instantly, we hoped that we could train the agent to both safely navigate the maze and heal itself after making mistakes, all while avoiding poisoning itself. Our end goal would be to have the agent navigate the maze to the end point with full health.

We believed this challenge would be interesting because the benefit from food is not directly attached to the goal of finishing a maze. These food items do not do anything to increase the speed of the agent or give it more time to find the end of the maze. Rather, more or less time is _indirectly_ given to the agent as its health can act as a resource while exploring. This delayed action and reward is able to really test the limits of the algorithmic approach that we decide on.

## Approaches

# Baseline

# Proposed Approach

## Evaluation

# Qualitative

Unfortunately, even after several hours of training, the agent never truly discerns the difference between the food items. They are eaten arbitrarily, but perhaps with more training time it could eventually learn to eat golden apples and to avoid spider eyes. There is more quantitative detail on this evaluation in the section below.

After a lot of training, the agent does seem to be more careful with its movement than at the start. When the agent is first launched and training begins, its movement is extremely erratic as it simply tries out all of its available inputs. However, as time goes on, it does seem to make less extraneous inputs if it sees a diamond block (end goal for the maze). This is likely a result of its light punishment for every input it makes. However, given a different punishment value for inputs, this movement could have been even more refined or perhaps just stuck in a loop. Early iterations of the agent, especially before a time limit was added, would sometimes get stuck in an infinite loop as it decides to never explore and simply stay alive in one place. We found that reducing the punishment for each step significantly increased the rate at which the agent was willing to explore.

# Quantitative

A bug in the current version of Malmo could have lead to the poor performance in food selection. We originally wanted to punish the agent only for dying, but not for touching magma blocks. This would mean that it is completely free to explore on top of magma blocks as long as it has the resources (golden apples) to do so. Unfortunately, rewards on death are currently not working, and thus we had to punish it only for timeouts and for touching magma. This further increases the gap between action and reward when the numerical reward value is coming from slightly inaccurate places.

## References
