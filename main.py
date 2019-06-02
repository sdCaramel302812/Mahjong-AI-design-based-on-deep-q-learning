from rule.agent import Agent
import threading
import random
import time
import copy
from rule.game import Game
from rule.tenpai import *

import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help="run how many time", type=int)
    parser.add_argument("-a", "--action", help="ai choosing action", type=int)
    args = parser.parse_args()

    game = Game()

    if args.action == None:
        ai_action = 0
    else :
        ai_action = args.action

    for i in range(0, 4):
        game.pl[i].id = i
    
    agent = []
    for i in range(0, 4):
        agent.append(Agent(game.pl[i].card, game.pl[i].info, i + 1))
        # name, new_model, epoch, batch_size, gamma, epsilon, in_dim = 1, middle_dim = 1, out_dim = 1, learning_rate = 0.001, training action
        name = "New_AI" + str(i)
        agent[i].set_ai(name, False, 2, 32, 0.2, 0.1, 10, 32, 5, 0.1, ai_action)



    start = time.time()

    if args.number == None:
        total_round = 1
    else :
        total_round = args.number
    

    round_count = 0
    for i in range(0, total_round):
        while game.not_end:
            round_count += game.run()
            for i in range(0, 4):
                agent[i].run()
        
        for i in range(0, 4):
            agent[i].ai.train()
            #agent[i].ai.save_training()
        if round_count / 20 > 1:
            round_count -= 20
            for i in range(0, 4):
                agent[i].ai.reset()
        if i == total_round - 1:
            game.game_log.write_log_file("./log/")
        game.restart_game()
        

    

    end = time.time()
    update_table()

    print('elapse time ', end - start)
    print('total ', round_count)