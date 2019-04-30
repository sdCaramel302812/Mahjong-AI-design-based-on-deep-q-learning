from rule.agent import Agent
import threading
import random
import time
import copy
from rule.game import Game
from rule.tenpai import *


if __name__ == '__main__':
    game = Game()

    for i in range(0, 4):
        game.pl[i].id = i
    
    agent = []
    for i in range(0, 4):
        agent.append(Agent(game.pl[i].card, game.pl[i].info, i + 1))



    start = time.time()


    round_count = 0
    while game.end:
        round_count += game.run()
        for i in range(0, 4):
            agent[i].run()


    game.game_log.write_log_file("./log/")
    update_table()


    end = time.time()
    update_table()

    print('elapse time ', end - start)
    print('total ', round_count)