def comp(x, y):
    return (score[x] > score[y])

import gym
import random
from operator import itemgetter
mut = 500
pool_size = 400
new_pool = 1000
sharp = 1
sep = 10
cntr = 0
time_l = 100
survivors = 20
number = 2786
winners = [[[] for z in range(sep)] for y in range(new_pool)]
am_winners = [0 for x in range(sep)]
flag = 0
pt = [[[(random.randint(0,50)/25 - 1) for x in range(time_l)] for z in range(sep)] for y in range(pool_size)]
env = gym.make('MountainCarContinuous-v0')
env = gym.wrappers.Monitor(env, "./video", force=True, video_callable=lambda episode_id: True)
q = 1
file = open(str(number) + ".txt", "r")
s = file.readlines()
s = [x.strip().split(" ") for x in s]
tact = [list(map(float,x)) for x in s]
file.close()
kappa_d = -1
kappa_s = 0
observation = env.reset()
for t in range(time_l + 50):
        action = env.action_space.sample()
        env.render()
        if (t == 0):
            sp = int(4.99*sep*(observation[0] + 0.6))
        if (t < 100):
            observation, reward, done, info = env.step([tact[sp][t]])
        else:
            observation, reward, done, info = env.step([1.0])
        kappa_d = max(observation[0],kappa_d)
        kappa_s += reward
        if done:
            break
print(str(kappa_s))
