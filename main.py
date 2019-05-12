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
    args = parser.parse_args()

    game = Game()

    for i in range(0, 4):
        game.pl[i].id = i
    
    agent = []
    for i in range(0, 4):
        agent.append(Agent(game.pl[i].card, game.pl[i].info, i + 1))
        # name, new_model, epoch, batch_size, gamma, epsilon, in_dim = 1, middle_dim = 1, out_dim = 1, learning_rate = 0.001
        name = "AI" + str(i)
        agent[i].set_ai(name, False, 2, 32, 0.2, 0.8, 34, 32, 34, 0.01)



    start = time.time()


    round_count = 0
    for i in range(0, args.number):
        while game.end:
            round_count += game.run()
            for i in range(0, 4):
                agent[i].run()
        game.game_log.write_log_file("./log/")
        game.restart_game()

    
    update_table()

    for i in range(0, 4):
        agent[i].ai.train()
        agent[i].ai.save_training()


    end = time.time()
    update_table()

    print('elapse time ', end - start)
    print('total ', round_count)