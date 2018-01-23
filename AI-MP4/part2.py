import numpy as np
import random
import time

C = 100
gamma = 0.80
#all (state,action) pairs and q values
Q = {}
#number of occurrences of (state, action)
track_states = {}
#paddle parameters
paddle_moves = [0.0,0.04,-0.04]
height = 0.2

#sets Q and track_states to empty
def create_dicts():
    Q = {}
    track_states = {}

#discretizes a state according to assignment
def discretize_state((ball_x,ball_y,vel_x,vel_y,paddle)):
    disc_x = min(np.floor(10*ball_x),9)
    disc_y = min(np.floor(10*ball_y),9)
    if vel_x > 0:
        disc_velx = 1
    else:
        disc_velx = -1
    if abs(vel_y) < 0.015:
        disc_vely = 0
    elif vel_y >= 0.015:
        disc_vely = 1
    else:
        disc_vely = -1
    disc_paddle = min(np.floor(10*paddle)/(1-height),9)
    return (disc_x,disc_y,disc_velx,disc_vely,disc_paddle)

#get move for a state
def get_move(state):
    move = None
    q_val = -1000000
    for dir in paddle_moves:
        if (discretize_state(state),dir) not in track_states or (discretize_state(state),dir) not in Q:
            return dir
        if Q[(discretize_state(state),dir)] > q_val:
            move = dir
            q_val = Q[(discretize_state(state),dir)]
    return move

#get next state and reward if there was a bounce
def get_next_state(state, move):
    reward = 0.0
    (ball_x,ball_y,vel_x,vel_y,paddle) = state
    paddle += move
    #create_dicts stuff if out of grid
    if paddle >= 0.8:
        paddle = 0.8
    if paddle <= 0:
        paddle = 0.0
    ball_x += vel_x
    ball_y += vel_y
    if ball_x < 0:
        ball_x = -ball_x
        vel_x = -vel_x
    if ball_y > 1:
        ball_y = 2.0 - ball_y
        vel_y = -vel_y
    if ball_y < 0:
        ball_y = -ball_y
        vel_y = -vel_y
    #if ball to the right edge of grid
    if ball_x > 1.0:
        bounces = (state[1]-ball_y)/(state[0]-ball_x) * (1-state[0]) + state[1]
        #was successful bounces
        if bounces <= paddle+height and bounces >= paddle:
            reward = 1.0
            ball_x = 2.0 - ball_x
            stop = 0
            while stop == 0:
                u = random.uniform(-0.015, 0.015)
                new_vel_x = -vel_x + u
                v = random.uniform(-0.03, 0.03)
                new_vel_y = vel_y + v
                if abs(new_vel_x) > 0.03:
                    stop = 1
                else:
                    stop = 0
            vel_x = new_vel_x
            vel_y = new_vel_y
            return ((ball_x, ball_y, vel_x, vel_y, paddle), reward)
        else:
            #didn't bounces
            return (None, -1.0)

    return ((ball_x,ball_y,vel_x,vel_y,paddle), reward)

#gets best Q for a state
def find_qval(state):
    if state is None:
        return -1.0
    currq = -1000000
    for dir in paddle_moves:
        if (discretize_state(state),dir) in Q:
            tempq = Q[(discretize_state(state), dir)]
        else:
            tempq = 0.0
        currq = max(currq, tempq)
    return currq

#does the learning on set number of games
def train_q_learner(num_games):
    for i in range(num_games):
        bounces = 0
        if i % 1000 == 0:
            print i
        state = (0.5,0.5,0.03,0.01,0.5-height/2.0)
        keep_playing = 1
        while keep_playing==1:
            move = get_move(state)
            disc_state = (discretize_state(state), move)
            state, reward = get_next_state(state, move)
            if reward > 0:
                bounces += 1
            if state is None:
                keep_playing = 0
            if disc_state in track_states:
                track_states[disc_state] += 1
                alpha = (C*1.0)/(C+track_states[disc_state])
                Q[disc_state] = Q[disc_state]+(alpha*(reward+gamma*find_qval(state)-Q[disc_state]))
            else:
                track_states[disc_state] = 1
                alpha = 1.0
                Q[disc_state] = alpha*(reward+gamma*find_qval(state))
        if i % 1000 == 0:
            print bounces

#trains q learning and plays 1000 test games
def train_and_play():
    create_dicts()
    start = time.time()
    train_q_learner(20001)
    print((time.time()-start)/60.0)
    tot_bounces = 0
    for i in range(1000):
        state = (0.5,0.5,0.03,0.01,0.5-height/2.0)
        while state is not None:
            move = get_move(state)
            state, reward = get_next_state(state, move)
            if reward > 0:
                tot_bounces += 1
    return tot_bounces/1000.0

print("Average number of bounces: " + str(train_and_play()))