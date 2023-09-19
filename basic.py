# remember to activate mario environment
# with: conda activate mario
# then: python3 main.py

# current issue: Mario can't get over high pipe

from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT, COMPLEX_MOVEMENT
import gym
env = gym.make("SuperMarioBros-v0", apply_api_compatibility=True, render_mode="human")
env = JoypadSpace(env, SIMPLE_MOVEMENT)
done = True
env.reset()
point = 0
height = 0
jump_points = []
air_points = []
prev_stop = 0
stored_life = 3
for step in range(50000):
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
                if (i not in air_points):
                    jump_points.append(i)
                # adds previous 50 points into the jump points array
    if (point > 50):
        if (info['x_pos'] == point and info['y_pos'] == height):
            for i in range(point-50, point):
                if (i not in air_points):
                    jump_points.append(i)
            if (prev_stop == info['x_pos']):
                for i in reversed(range(point-50, point)):
                    if (i in air_points):
                        jump_points.append(i)
                    elif (i > point - 10):
                        break
            state = env.reset()
            prev_stop = info['x_pos']

                # reset the environment if mario stops moving
    if (height != info['y_pos']):
        air_points.append(point)
    if done:
        state = env.reset()
    point = info['x_pos']
    height = info['y_pos']
env.close()