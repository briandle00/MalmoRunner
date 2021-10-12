---
layout: default
title: Proposal
---

## Summary
We want to create an obstacle course in Minecraft using the Malmo platform with a set start point and end point for the agent to learn how to navigate, with varying degrees of difficulty in the implemented obstacles. It is similar to a maze problem, but the addition of obstacles should allow for increased complexity. The agent will have the information of surrounding blocks as input, and navigate similarly to Assignment 1, and the path taken will be outputted. 

## AI/ML Algorithms
We plan to use reinforcement learning in combination with the Malmo platform to view blocks surrounding the agent, with rewards based on reaching the end goal and minimizing time.

## Evaluation Plan
For quantitative evaluation, we will focus on minimizing moves used, time spent, and minimizing the number of deaths of the agent. The baseline is for an agent to barely make it through the course without dying. We would like to improve on its efficiency as it is trained, using number of moves and real-life time spent as metrics to compare against. We hope to have the agent take something within 25% of the most efficient route in terms of moves spent, and only a few seconds per move.

For qualititave evaluation, the sanity cases would be to run it on mazes deemed to be more simple than the final maze, within a reasonable time frame. We will draw a a box chart of the internals of our reinforcement learning algorithm with the necessary layers. Our moonshot case would be that our agent is able to complete the obstacle course accurately and similarly to how a human would solve it in terms of time and move efficiency. We would also hope that any complex obstacles we introduce, even extremely complex ones involving target aiming or puzzles, could eventually be solved by the agent as well.
