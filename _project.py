# Rllib docs: https://docs.ray.io/en/latest/rllib.html
# Malmo python examples: https://canvas.eee.uci.edu/courses/34142/pages/python-examples-malmo-functionality
# Malmo XML docs:https://microsoft.github.io/malmo/0.30.0/Schemas/Mission.html
# Harvesting Food
try:
    from malmo import MalmoPython
except:
    import MalmoPython

import sys
import time
import json
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint
import random
import gym, ray
from gym.spaces import Discrete, Box
from ray.rllib.agents import ppo
from ray import tune


class DiamondCollector(gym.Env):

    def __init__(self, env_config):  
        # Static Parameters
        self.check_food = False
        self.size = 50
        self.reward_density = .2
        self.penalty_density = .7
        self.obs_size = 5
        self.max_episode_steps = 100
        self.log_frequency = 10
        self.life = 20
        self.action_dict = {
            0: 'move 1',  # Move one block forward
            1: 'turn 1',  # Turn 90 degrees to the right
            2: 'turn -1',  # Turn 90 degrees to the left
            3: 'use 1',  # eat fruit
            4: 'hotbar.1 1',
            5: 'hotbar.2 1'
        }

        # Rllib Parameters
        # self.action_space = Discrete(len(self.action_dict))
        self.action_space = Box(-1.0, 1.0, shape=(5,), dtype=np.float32)
        #self.action_space = Box(-1, 1, shape=(3,), dtype=np.float32)        
        self.observation_space = Box(0, 1, shape=(101, ), dtype=np.float32)

        # Malmo Parameters
        self.agent_host = MalmoPython.AgentHost()
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

        # DiamondCollector Parameters
        self.obs = None
        self.allow_break_action = False
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []

    def reset(self):
        """
        Resets the environment for the next episode.
        Returns
            observation: <np.array> flattened initial obseravtion
        """
        # Reset Malmo
        world_state = self.init_malmo()

        # Reset Variables
        self.check_food = False
        self.returns.append(self.episode_return)
        current_step = self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0

        # Log
        if len(self.returns) > self.log_frequency + 1 and \
            len(self.returns) % self.log_frequency == 0:
            self.log_returns()

        # Get Observation
        self.obs, self.w_break_action = self.get_observation(world_state)

        return self.obs

    def step(self, action):
        """
        Take an action in the environment and return the results.
        Args
            action: #<int> index of the action to take#
            new action: <Box> 
        Returns
            observation: <np.array> flattened array of obseravtion
            reward: <int> reward from taking action
            done: <bool> indicates terminal state
            info: <dict> dictionary of extra information
        """
        # Get Action

        if not self.check_food:
            self.agent_host.sendCommand('chat /difficulty normal')
            self.agent_host.sendCommand( "chat /effect @p minecraft:hunger 5 201");
            self.check_food = True


        move = action[0]
        turn = action[1]
        use = 1 if action[2] > 0 else 0
        hotbar1 = 1 if action[3] > 0 else 0
        hotbar2 = 1 if action[4] > 0 else 0
        
        # if command != 'use 1' or self.allow_break_action:
        self.agent_host.sendCommand('move ' + str(move))
        self.agent_host.sendCommand('turn ' + str(turn))
        self.agent_host.sendCommand('hotbar.1 ' + str(hotbar1))
        self.agent_host.sendCommand('hotbar.1 0')
        self.agent_host.sendCommand('hotbar.2 ' + str(hotbar2))
        self.agent_host.sendCommand('hotbar.2 0')
        if use == 1:
            self.agent_host.sendCommand('use ' + str(use))
            time.sleep(1.75)
            self.agent_host.sendCommand('use 0')
        # self.agent_host.sendCommand(command)
        # if action == 3:
        #     print('EATING')
        #     time.sleep(1.75)
        #     self.agent_host.sendCommand('use 0')
        # elif action == 4:
        #     self.agent_host.sendCommand('hotbar.1 0')
        # elif action == 5:
        #     self.agent_host.sendCommand('hotbar.2 0')
        time.sleep(.1)
        self.episode_step += 1
        
        # Get Observation
        world_state = self.agent_host.getWorldState()
        
        for error in world_state.errors:
            print("Error:", error.text)
        self.obs, self.allow_break_action = self.get_observation(world_state)
        # Life = self.obs[-1] * 20
        

        # if Life < 20:
        #     self.agent_host.sendCommand('use 1')
        # self.agent_host.sendCommand('use 1')

        # Get Done
        done = not world_state.is_mission_running 
        # Get Reward
        reward = 0
        for r in world_state.rewards:
            reward += r.getValue()
        #to acount for time
        reward -= 0.1
        self.episode_return += reward
    
        return self.obs, reward, done, dict()


    def get_mission_xml(self):
        healthyPool = ['golden_apple', 'golden_carrot', 'cooked_beef']
        poisonPool = ['spider_eye', 'poisonous_potato', 'chicken']

        num = int(10)
        x = randint(0,10,size=int(num))
        z = randint(0,10,size=int(num))
        addXml = ""
        for i in range(num):
            addXml +="<DrawItem x='{}' y='3' z='{}' type='golden_apple'/> ".format(x[i],z[i])
            addXml +="<DrawBlock x='{}' y='2' z='{}' type='glass'/> ".format(x[i],z[i])
        num = int(10)
        x = randint(0,10,size=int(num))
        z = randint(0,10,size=int(num))
        for i in range(num):
            addXml +="<DrawItem x='{}' y='3' z='{}' type='spider_eye'/> ".format(x[i],z[i])
            addXml +="<DrawBlock x='{}' y='2' z='{}' type='bedrock'/> ".format(x[i],z[i])
        x = randint(0,10)
        z = randint(0,10)
        addXml +="<DrawBlock x='{}' y='2' z='{}' type='diamond_block'/> ".format(x,z)

        
        
        return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <About>
                        <Summary>Malmo Runner</Summary>
                    </About>
                    <ModSettings>
                        <MsPerTick>50</MsPerTick>
                    </ModSettings>
                    <ServerSection>
                        <ServerInitialConditions>
                            <Time>
                                <StartTime>12000</StartTime>
                                <AllowPassageOfTime>false</AllowPassageOfTime>
                            </Time>
                            <Weather>clear</Weather>
                        </ServerInitialConditions>
                        <ServerHandlers>
                            <FlatWorldGenerator generatorString="2;4x7;1;"/>
                            <MazeDecorator>
                                <SizeAndPosition length="10" width="10" xOrigin="0" yOrigin="1" zOrigin="0" height="0"/>
                                <GapProbability variance="0.2">0.5</GapProbability>
                                <Seed>random</Seed>
                                <MaterialSeed>random</MaterialSeed>
                                <AllowDiagonalMovement>false</AllowDiagonalMovement>
                                <StartBlock fixedToEdge="true" type="redstone_block" height="1"/>
                                <EndBlock fixedToEdge="true" type="diamond_block" height="1"/>
                                <PathBlock type="stone" height="1"/>
                                <FloorBlock type="magma" height="1"/>
                                <GapBlock type="magma" height="1"/>
                                <AddNavigationObservations/>
                            </MazeDecorator>
                            <DrawingDecorator>
                                <DrawCuboid type="air" x1='0' y1='3' z1='0' x2='9' y2='3' z2='9' />''' + \
                                addXml +\
                                '''
                            </DrawingDecorator>
                            <ServerQuitFromTimeUp timeLimitMs="30000" description="out_of_time"/>
                            <ServerQuitWhenAnyAgentFinishes/>
                        </ServerHandlers>
                    </ServerSection>
                    <AgentSection mode="Survival">
                        <Name>Runner</Name>
                        <AgentStart>
                            <Placement x="0.5" y="2" z="0.5" pitch="45" yaw="0"/>
                            <Inventory>
                                <InventoryItem slot="0" type="golden_apple"/>
                                <InventoryItem slot="1" type="spider_eye"/>
                            </Inventory>
                        </AgentStart>
                        <AgentHandlers>
                            <InventoryCommands />
                            <ChatCommands />
                            <ObservationFromHotBar />
                            <RewardForTouchingBlockType>
                               <Block type="magma" reward="-5.0" />
                               <Block type="diamond_block" reward="500.0" />
                            </RewardForTouchingBlockType>
                            <RewardForSendingCommand reward="-0.1" />
                            <ContinuousMovementCommands/>
                            <ObservationFromFullStats/>
                            <ObservationFromRay/>
                            <ObservationFromNearbyEntities>
                                <Range name="Entities" xrange="10" yrange="1" zrange="10"/>
                            </ObservationFromNearbyEntities>
                            <ObservationFromGrid>
                                <Grid name="floorAll">
                                    <min x="-'''+str(int(self.obs_size/2))+'''" y="-1" z="-'''+str(int(self.obs_size/2))+'''"/>
                                    <max x="'''+str(int(self.obs_size/2))+'''" y="-1" z="'''+str(int(self.obs_size/2))+'''"/>
                                </Grid>
                            </ObservationFromGrid>
                            <AgentQuitFromTouchingBlockType>
                                <Block type="diamond_block" />
                            </AgentQuitFromTouchingBlockType>
                            <RewardForMissionEnd rewardForDeath="-25.0">
                                <Reward description="out_of_time" reward="-25.0"/>
                            </RewardForMissionEnd>
                        </AgentHandlers>
                    </AgentSection>
                </Mission>'''
    def init_malmo(self):
        """
        Initialize new malmo mission.
        """
        my_mission = MalmoPython.MissionSpec(self.get_mission_xml(), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(1)

        max_retries = 3
        my_clients = MalmoPython.ClientPool()
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

        for retry in range(max_retries):
            try:
                self.agent_host.startMission( my_mission, my_clients, my_mission_record, 0, 'DiamondCollector' )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)

        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print("\nError:", error.text)

        return world_state

    def get_observation(self, world_state):
        """
        Use the agent observation API to get a flattened 2 x 5 x 5 grid around the agent. 
        The agent is in the center square facing up.
        Args
            world_state: <object> current agent world state
        Returns
            observation: <np.array> the state observation
            allow_break_action: <bool> whether the agent is facing a diamond
        """
        obs = np.zeros((4 * self.obs_size * self.obs_size, ))
        allow_break_action = False

        while world_state.is_mission_running:
            time.sleep(0.5)
            world_state = self.agent_host.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid.')

            if world_state.number_of_observations_since_last_state > 0:
                # First we get the json from the observation API
                msg = world_state.observations[-1].text
                observations = json.loads(msg)

                # Get observation
                grid = observations['floorAll']
                items = observations['Entities']
                Life = observations['Life']


                #Normalize life score
                life_score = Life / 20

                #print("this is grid"+ str(grid))
                #print("This is life"+str(Life))

                #print("This is items:"+ str(items))

                i = 0

                for x in grid:
                    obs[i] = x == 'glass'
                    i+=1

                for x in grid:
                    obs[i] = x == 'magma'
                    i+=1

                for x in grid:
                    obs[i] = x == 'bedrock'
                    i+=1

                for x in grid:
                    obs[i] = x =='diamond_block'
                    i+=1
            
                
                # Rotate observation with orientation of agent
                obs = obs.reshape((4, self.obs_size, self.obs_size))
                yaw = observations['Yaw']
                if yaw >= 225 and yaw < 315:
                    obs = np.rot90(obs, k=1, axes=(1, 2))
                elif yaw >= 315 or yaw < 45:
                    obs = np.rot90(obs, k=2, axes=(1, 2))
                elif yaw >= 45 and yaw < 135:
                    obs = np.rot90(obs, k=3, axes=(1, 2))

                obs = obs.flatten()
                obs = np.append(obs, life_score)

                #allow_break_action = observations['LineOfSight']['type'] == 'golden_apple'
                #allow_break_action = observations['LineOfSight']['type'] == 'chicken'
                
                break
        if world_state.is_mission_running != True:
            obs = np.zeros((4 * self.obs_size * self.obs_size+1, ))

        return obs, allow_break_action
    
    def log_returns(self):
        """
        Log the current returns as a graph and text file
        Args:
            steps (list): list of global steps after each episode
            returns (list): list of ttal return of each episode
        """
        box = np.ones(self.log_frequency) / self.log_frequency
        returns_smooth = np.convolve(self.returns[1:], box, mode='same')
        plt.clf()
        plt.plot(self.steps[1:], returns_smooth)
        plt.title('MalmoRunner')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig('returns.png')

        with open('returns.txt', 'w') as f:
            for step, value in zip(self.steps[1:], self.returns[1:]):
                f.write("{}\t{}\n".format(step, value)) 


if __name__ == '__main__':
    ray.init()
    trainer = ppo.PPOTrainer(env=DiamondCollector, config={
        'env_config': {},
        'framework': 'torch',
        'num_gpus': 0,
        'num_workers': 0,
        'gamma': 0.9,
        'lr': 0.001
    })
    while True:
        print(trainer.train())
    # config = {
    # "env": DiamondCollector,
    # "lr": tune.grid_search([1e-3, 1e-4, 1e-5]),
    # "gamma": tune.grid_search([0.9, 0.99]),
    # 'framework': 'torch',       # Use pyotrch instead of tensorflow
    # 'num_gpus': 0,              # We aren't using GPUs
    # 'num_workers': 0            # We aren't using parallelism
    # }
    # tune.register_env("DiamondCollector",lambda env_ctx: DiamondCollector(**env_ctx))
    # tune.run(
    # 'PPO', 
    # stop={
    #     'timesteps_total': 1000000}, config=config)
    # print("best hyperparameters: ", analysis.best_config)

