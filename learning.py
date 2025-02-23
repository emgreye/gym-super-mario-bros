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
world = "3"
level = "1"
name = "SuperMarioBros-"+world+"-"+level+"-v0"
env = gym.make(name, apply_api_compatibility=True, render_mode="human")
env = JoypadSpace(env, SIMPLE_MOVEMENT)
done = True
env.reset()
jsize = 1000
point = 0
height = 0
journey = []
filename = world+level+'printed_journey.txt'
if(os.path.isfile(filename)):
    with open(filename, "r") as f:
        journeyString = f.readlines()
    f.close()
    journeyList = journeyString[0].split(",")
    for i in journeyList[0:len(journeyList)-1]:
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
        # save the current journey to the a file every 5000 steps
        if(count % 5000 ==0):
            print("Made it")
            journeyString = ""
            for action in journey:
                journeyString = journeyString + str(action) + ","
            filename = world+level+'printed_journey.txt'
            with open(filename, 'w') as creating_new_csv_file: 
                pass
            with open(filename, 'w') as f:
                f.write(journeyString)
        if (point > 3150):
            completed == True
        action = (journey[step//10])%2+1
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        # detects if mario has died
        if (stored_life > info['life']):
            stored_life = info['life']
            if (point>50):
                print ("died")
                done = True
        # detects if Mario has been sent back to the start of the level
        if (point > 50):
            if (info['x_pos'] < point):
                print ("tp'd back")
                point = info['x_pos'] - 1
                # done = True
        # if any 'done' state has occured (such as teleporting back or losing a life)
        # then restart the journey
        if done:
            print ("break now!")
            # add 2 to the move that killed mario
            if (journey[step//10] < 2):
                journey[step//10] += 2
            else:
                print("found block")
            env.reset()
            break
        point = info['x_pos']
        height = info['y_pos']
    # find the move that killed mario
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