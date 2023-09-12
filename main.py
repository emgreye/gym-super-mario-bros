# remember to activate mario environment
# with: conda activate mario
# then: python3 main.py

from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT, COMPLEX_MOVEMENT
import gym
env = gym.make("SuperMarioBros-v0", apply_api_compatibility=True, render_mode="human")
env = JoypadSpace(env, SIMPLE_MOVEMENT)
done = True
env.reset()
point = 0
death_points = []
stored_life = 3
for step in range(5000):
    #action = env.action_space.sample()
    if (point in death_points):
        action = 2
    else:
        action = 1
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    if (stored_life > info['life']):
        stored_life = info['life']
        if (point>20):
            for i in range(point-20, point):
                death_points.append(i)
        point = 0
    if done:
        state = env.reset()
    point += 1
env.close()