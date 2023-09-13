# remember to activate mario environment
# with: conda activate mario
# then: python3 main.py

# current issue: Mario will attempt to jump when in the air
#               & jumping while in the air cancels the jump

from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT, COMPLEX_MOVEMENT
import gym
env = gym.make("SuperMarioBros-v0", apply_api_compatibility=True, render_mode="human")
env = JoypadSpace(env, SIMPLE_MOVEMENT)
done = True
env.reset()
point = 0
jump_points = []
stored_life = 3
stored_loc = 0
for step in range(5000):
    #action = env.action_space.sample()
    if (point in jump_points):
        action = 2
        #jump if this area previously caused mario to die
    else:
        action = 1
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    if (stored_life > info['life']):
        # detects if mario has died
        stored_life = info['life']
        if (point>50):
            for i in range(point-50, point):
                jump_points.append(i)
                # adds previous 20 points into the jump points array
    if (step % 20 == 0):
        # every 20 steps, check if mario has changed position
        if (point > 50):
            if (info['x_pos'] == stored_loc):
                for i in range(point-50, point):
                    jump_points.append(i)
                state = env.reset()
                # reset the environment if mario stops moving
        stored_loc = info['x_pos']
    if done:
        state = env.reset()
    point = info['x_pos']
env.close()