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
winners = [[[] for z in range(sep)] for y in range(new_pool)]
am_winners = [0 for x in range(sep)]
flag = 0
pt = [[[(random.randint(0,50)/25 - 1) for x in range(time_l)] for z in range(sep)] for y in range(pool_size)]
env = gym.make('MountainCarContinuous-v0')
q = 1
while (flag == 0):
    score = [[] for x in range(sep)]
    rew = []
    ms = []
    for i_episode in range(pool_size):
        t_score = -1
        mrew = 0
        mk = 0
        sp = 0
        observation = env.reset()
        for t in range(time_l):
            action = env.action_space.sample()
            if (t == 0):
                sp = int(4.99*sep*(observation[0] + 0.6))
            observation, reward, done, info = env.step([pt[i_episode][sp][t]])
            t_score = max(observation[0],t_score)
            mrew += reward
            mk += 1
            if done:
                if (am_winners[sp] < new_pool):
                    winners[am_winners[sp]][sp] = pt[i_episode][sp]
                    am_winners[sp] += 1
                break
        score[sp].append(t_score)
        for i in range(sep):
            if (i != sp):
                score[i].append(-1)
    print(str(q) + " Genration")
    ts = [[[] for z in range(sep)] for y in range(pool_size)]
    stats = []
    stats.append(q)
    for j in range(sep):
        g = []
        for x in range(pool_size):
            mg = []
            mg.append(score[j][x])
            mg.append(x)
            g.append(mg)
        g.sort(key=itemgetter(0), reverse=True)
        for i in range(pool_size):
            ts[i][j] = pt[g[i][1]][j]
        print(g[0][0])
        stats.append(g[0][0])
    pt = ts[:survivors]
    observation = env.reset()
    kappa_d = -0.6
    kappa_s = 0
    for t in range(time_l):
        action = env.action_space.sample()
        if (t == 0):
            sp = int(4.99*sep*(observation[0] + 0.6))
        observation, reward, done, info = env.step([pt[0][sp][t]])
        kappa_d = max(observation[0],kappa_d)
        kappa_s += reward
        if done:
            break
    print("Distance = ",kappa_d)
    stats.append(kappa_s)
    """   Save data  
    file = open("Stats1.txt", "a+")
    file.write("\n" + " ".join(map(str,stats)))
    file.close()
      Next generation   """
    mys = 0
    for i in range(pool_size - survivors):
        a = random.randint(0,survivors - 1)
        b = random.randint(0,survivors - 1)
        new = [[] for x in range(sep)]
        for j in range(time_l):
            for k in range(sep):
                d = random.randint(0, 1)
                if mut == 0:
                    m = 1
                else:
                    m = random.randint(0, mut)
                if m == mut:
                    new[k].append(random.randint(0, 50)/25 - 1)
                else:
                    new[k].append(pt[a][k][j]*d + pt[b][k][j]*(1-d))
        pt.append(new)
    q += 1
    ttt = 0
    for i in range(sep):
        if am_winners[i] < new_pool:
            ttt = 1
    if ttt == 0:
        flag = 1
    print(" ".join(map(str, am_winners)))
pt = winners
print("Starting second phase...")
survivors = 300
pool_size = new_pool
while q < 3000:
    score = [[] for i in range(sep)]
    rew = []
    ms = []
    for i_episode in range(pool_size):
        t_score = 0
        mrew = 0
        mk = 0
        sp = 0
        observation = env.reset()
        for t in range(time_l):
            action = env.action_space.sample()
            if t == 0:
                sp = int(4.99*sep*(observation[0] + 0.6))
            observation, reward, done, info = env.step([pt[i_episode][sp][t]])
            t_score  += reward
            mrew += reward
            mk += 1
            if done:
                break
        score[sp].append(t_score)
        for i in range(sep):
            if i != sp:
                score[i].append(0)
    print(str(q) + " Genration")
    ts = [[[] for z in range(sep)] for y in range(pool_size)]
    ststs = []
    stats.append(q)
    for j in range(sep):
        g = []
        for x in range(pool_size):
            mg = []
            mg.append(score[j][x])
            mg.append(x)
            g.append(mg)
        g.sort(key=itemgetter(0), reverse=True)
        for i in range(pool_size):
            ts[i][j] = pt[g[i][1]][j]
        print(g[0][0])
        stats.append(g[0][0])
    pt = ts[:survivors]
    observation = env.reset()
    kappa = 0
    for t in range(time_l + 40):
        action = env.action_space.sample()
        if (t == 0):
            sp = int(4.99*sep*(observation[0] + 0.6))
        observation, reward, done, info = env.step([pt[0][sp][min(t,99)]])
        kappa += reward
        if done:
            break
    print("Reward = ",kappa)
    stats.append(kappa)
    """   Save data   
    file = open("Stats2.txt", "a+")
    file.write("\n" + " ".join(map(str,stats)))
    file.close()
       Next generation   
    file = open(str(cntr) + ".txt","a+")
    for i in range(sep):
        file.write("\n" + " ".join(map(str,pt[0][i])))
    file.close()"""
    cntr += 1
    mys = 0
    for i in range(pool_size - survivors):
        a = random.randint(0,survivors - 1)
        b = random.randint(0,survivors - 1)
        new = [[] for x in range(sep)]
        for j in range(time_l):
            for k in range(sep):
                d = random.randint(0,1)
                if (mut == 0):
                    m = 1
                else:
                    m = random.randint(0,mut)
                if m == mut:
                    new[k].append(random.randint(0,50)/25 - 1)
                else:
                    new[k].append(pt[a][k][j]*d + pt[b][k][j]*(1-d))
        pt.append(new)
    q += 1
"""  End goal  """
final_tactic = pt[0]
observation = env.reset()
kappa = 0
for t in range(time_l + 40):
    action = env.action_space.sample()
    if t == 0:
        sp = int(4.99*sep*(observation[0] + 0.6))
    observation, reward, done, info = env.step([final_tactic[sp][min(t,99)]])
    kappa += reward
    if done:
        break
