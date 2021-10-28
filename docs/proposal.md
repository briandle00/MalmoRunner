---
layout: default
title: Proposal
---

## Summary
We want to create an obstacle course in Minecraft using the Malmo platform with a set start point and end point for the agent to learn how to navigate, with varying degrees of difficulty in the implemented obstacles. It is similar to a maze problem, but the addition of obstacles should allow for increased complexity. The agent will have the information of surrounding blocks as input, and navigate similarly to Assignment 1, and the path taken will be outputted. 

We want to create an agent in Minecraft that is able to learn and rank saturation values of various food items. This is a hidden value that determines how long a food is able to keep a player full for, even beyond the regular displayed hunger bar.

## AI/ML Algorithms
We plan to use q-learning, a tabular reinforcement learning algorithm. This is because the action space is discrete and relatively small.

## Evaluation Plan
For quantitative evaluation, we will focus on time spent alive after eating the food item. To measure this time quickly, we will apply a damage over time effect to the agent. After making the agent walk, we can provide rewards for distance travelled, which will end up with the agent travelling further as long as it lives longer (the damage over time is constant). We can take note of the accuracy of its choices to plot or view later as well if tweaking needs to be done. The baseline would be to surpass a 50% success rate when picking between every pair of given food items. We hope to have the agent choose the right food item about 75% of the time by the end of the training.

For qualitative evaluation, the sanity cases would be to give the agent a healing item and a poisonous item. It should quickly learn to choose the healing item. We will draw a box chart of the internals of our reinforcement learning algorithm with the necessary layers. Our moonshot case would be that our agent is able to pick the food items accurately every single time, and if we add a layer of complexity in which the agent must navigate a simple course while choosing the correct item, we would hope that the agent would stay on the path and not fall off in that case as well. Eventually we could increase the number of available food items to have the agent rank, which would increase the training time and the complexity of the problem greatly.
