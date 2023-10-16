# remember to activate mario environment
# with: conda activate mario
# then: python3 main.py

# left node represents run
# right node represents run+jump
# the data is its state:
#   0 = died here
#   1 = run
#   2 = run+jump
#   


from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT, COMPLEX_MOVEMENT
import gym
import os
import random
env = gym.make("SuperMarioBros-v0", apply_api_compatibility=True, render_mode="human")
env = JoypadSpace(env, SIMPLE_MOVEMENT)
done = True
env.reset()
jsize = 1000
point = 0
height = 0
journey = []
if(os.path.isfile("printed_journey.txt")):
    with open("printed_journey.txt", "r") as f:
        journeyList = f.split(",")
    for i in journeyList:
        journey.append(int(i))
else:
    for i in range(jsize):
        journey.append(random.randint(0,1))
air_points = []
prev_stop = 0
stored_life = 3
completed = False
count = 0
while (not completed):
    print ("restarting")
    for step in range(50000):
        count = count+1
        if(count % 5000 ==0):
            print("Made it")
            journeyString = ""
            for action in journey:
                journeyString = journeyString + str(action) + ","
            with open('printed_journey.txt', 'w') as creating_new_csv_file: 
                pass
            with open('printed_journey.txt', 'w') as f:
                f.write(journeyString)
        if (point > 3150):
            completed == True
        action = (journey[step//10])%2+1
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        if (stored_life > info['life']):
            # detects if mario has died
            stored_life = info['life']
            if (point>50):
                print ("died")
                done = True
        if (point > 50):
            if (info['x_pos'] < point):
                print ("tp'd back")
                point = 0
                done = True
        if done:
            print ("break now!")
            if (journey[step//10] < 2):
                journey[step//10] += 2
            else:
                print("found block")
            env.reset()
            break
        point = info['x_pos']
        height = info['y_pos']
    try:
        death_move = jsize - min(journey[::-1].index(2), journey[::-1].index(3))-2
    except:
        try:
            death_move = jsize - journey[::-1].index(3)-2
        except:
            death_move = jsize - journey[::-1].index(2)-2
    if (journey[death_move] == 0):
        journey[death_move] = 3
    elif (journey[death_move] == 1):
        journey[death_move] = 2
    else:
        i = death_move-1
        while (journey[i] > 1):
            i -= 1
        for j in range(i, death_move):
            journey[j] = random.randint(2,3)
    journey[death_move+1] = random.randint(2,3) 
print (journey)
env.close()