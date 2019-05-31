from rule.hand_card import HandCard
from rule.player import Player
from rule.card_stack import CardStack
from rule.agent import Agent
from rule.point import Point
from rule.tenpai import *
import threading
import random
import time
import copy
from rule.log import Log

class Game:
    # 0 : wait for discard
    # 1 : wait for chi pon kan
    # 2 : wait for draw
    # 3 : wait for next kyouku
    waiting_state = 0
    game_round = 1

    #game infomation
    chan_fon = 30
    kyouku = 0
    honba = -1
    kyoutaku = 0
    oya = 1
    first_oya = 1
    remain_tile = 70
    first_oya = 0
    current_player = 0
    draw_rin_shan = False
    red_number = 0

    richi_list = [0, 0, 0 ,0]
    richi_number = 0

    winner = -1
    winner2 = -1
    loser = -1
    is_tsumo = False
    winning_tile = -1

    #game log
    discard_stack = [[], [], [], []]
    start_deal = [[], [], [], []]
    draw_stack = [[], [], [], []]
    final_card = [[], [], [], []]

    discard_tile = -1

    kyouku_over = True

    card_stack = CardStack()
    pl = []
    def __init__(self):
        #threading.Thread.__init__(self)
        self.card_stack.reset(self.red_number)
        self.game_log = Log()

        self.pl.append(Player())
        self.pl.append(Player())
        self.pl.append(Player())
        self.pl.append(Player())
        self.pl[0].id = 1
        self.pl[1].id = 2
        self.pl[2].id = 3
        self.pl[3].id = 4

        self.oya = random.randint(0, 3)
        self.first_oya = self.oya + 1
        if self.first_oya > 3:
            self.first_oya = 0

    def restart_game(self):
        self.reset()
        self.card_stack.reset(self.red_number)
        self.game_log = Log()

        self.pl.append(Player())
        self.pl.append(Player())
        self.pl.append(Player())
        self.pl.append(Player())
        self.pl[0].id = 1
        self.pl[1].id = 2
        self.pl[2].id = 3
        self.pl[3].id = 4

        self.oya = random.randint(0, 3)
        self.first_oya = self.oya + 1
        if self.first_oya > 3:
            self.first_oya = 0

        self.chan_fon = 30
        kyouku_over = True
        self.not_end = True

    
    def reset(self):
        self.card_stack.reset(self.red_number)
        self.game_round = 1
        self.winner = -1
        self.winner2 = -1
        self.loser = -1
        self.winning_tile = -1
        self.is_tsumo = False
        self.pl[0].reset()
        self.pl[1].reset()
        self.pl[2].reset()
        self.pl[3].reset()
        self.discard_stack = [[], [], [], []]
        self.draw_stack = [[], [], [], []]
        self.richi_list = [0, 0, 0 ,0]
        self.richi_number = 0


    def next_kyouku(self):
        switch_oya = True

        if self.winner != -1 or self.pl[self.oya].info.tenpai_list == []:
            self.kyouku += 1
            self.honba = 0
            if self.kyouku == 5:
                self.kyouku = 1
                if self.chan_fon == 30:
                    self.chan_fon = 31
                else :
                    # . . .
                    self.chan_fon = 32
        else :
            self.honba += 1
            switch_oya = False

        self.reset()
        pai = self.card_stack.deal()

        self.pl[0].card.deal(copy.deepcopy(pai[0]))
        self.pl[1].card.deal(copy.deepcopy(pai[1]))
        self.pl[2].card.deal(copy.deepcopy(pai[2]))
        self.pl[3].card.deal(copy.deepcopy(pai[3]))

        self.start_deal = pai

        
        self.pl[0].info.chan_fon = self.chan_fon
        self.pl[1].info.chan_fon = self.chan_fon
        self.pl[2].info.chan_fon = self.chan_fon
        self.pl[3].info.chan_fon = self.chan_fon

        if switch_oya:
            self.oya += 1
            if self.oya == 4:
                self.oya = 0
            
        self.current_player = self.oya
        self.pl[self.oya].info.men_fon = 30
        self.pl[self.find_next_player(1)].info.men_fon = 31
        self.pl[self.find_next_player(2)].info.men_fon = 32
        self.pl[self.find_next_player(3)].info.men_fon = 33
        self.current_player = self.oya
        self.waiting_state = 2
        if self.chan_fon == 32:
            self.not_end = False

        #print(self.chan_fon, " ", self.kyouku, " ", self.honba)



    def next_player(self):
        if self.current_player == 3:
            self.current_player = 0
        else :
            self.current_player += 1

    def find_next_player(self, i):
        num = i + self.current_player
        return num % 4

    def check_action(self, pai):
        # 0 : right
        # 1 : opposite
        # 2 : left
        result = [-1, -1, -1]

        result[0] = self.pl[self.find_next_player(1)].can_do_something(self.discard_tile, True, self.card_stack.get_dora())
        result[1] = self.pl[self.find_next_player(2)].can_do_something(self.discard_tile, False, self.card_stack.get_dora())
        result[2] = self.pl[self.find_next_player(3)].can_do_something(self.discard_tile, False, self.card_stack.get_dora())
        if result[0] or result[1] or result[2]:
            return True
        else :
            return False

    def reset_action_state(self):
        for i in self.pl:
            i.info.action_state = -1

    def record_game_log(self):
        self.final_card = [[], [], [], []]

        self.final_card[0] = [self.pl[0].card.card13]
        self.final_card[1] = [self.pl[1].card.card13]
        self.final_card[2] = [self.pl[2].card.card13]
        self.final_card[3] = [self.pl[3].card.card13]

        self.final_card[0].append(self.pl[0].card.chi_card)
        self.final_card[0].append(self.pl[0].card.pon_card)
        self.final_card[0].append(self.pl[0].card.kan_card)

        self.final_card[1].append(self.pl[1].card.chi_card)
        self.final_card[1].append(self.pl[1].card.pon_card)
        self.final_card[1].append(self.pl[1].card.kan_card)

        self.final_card[2].append(self.pl[2].card.chi_card)
        self.final_card[2].append(self.pl[2].card.pon_card)
        self.final_card[2].append(self.pl[2].card.kan_card)

        self.final_card[3].append(self.pl[3].card.chi_card)
        self.final_card[3].append(self.pl[3].card.pon_card)
        self.final_card[3].append(self.pl[3].card.kan_card)

        if self.winner != -1:
            self.final_card[self.winner].append([self.winning_tile])
            if self.winner2 != -1:
                self.final_card[self.winner2].append([self.winning_tile])


        self.game_log.append_game_log(self.chan_fon, self.oya, self.kyouku, self.honba, self.kyoutaku, self.card_stack.get_dora(), self.card_stack.get_uradora(), self.start_deal, self.draw_stack, self.discard_stack, self.final_card)


    end = True
    def run(self):
        self.not_end = True
        if True:
        #while end:
            if self.kyouku_over:
                self.kyouku_over = False
                self.next_kyouku()

            if self.game_round == 2:
                self.pl[0].first = False
                self.pl[1].first = False
                self.pl[2].first = False
                self.pl[3].first = False


            #
            #wait for discard
            #if haven't decide
            #retrun -1
            #else check if someone can do something
            if self.waiting_state == 0:
                has_kan = [0, 0]

                self.discard_tile = self.pl[self.current_player].discard(self.discard_stack[self.current_player])
                has_kan = self.pl[self.current_player].an_kan()
                self.is_tsumo = self.pl[self.current_player].tsumo()
                if self.is_tsumo:
                    self.winner = self.current_player
                    self.waiting_state = 3
                    self.winning_tile = self.pl[self.current_player.card.draw_tile]

                #print('player ', self.current_player, '\tdiscard\t', self.discard_tile)
                if has_kan[0] != 0:
                    self.discard_stack[self.current_player].append(60)
                    self.draw_rin_shan = True
                    self.pl[0].be_claimed()
                    self.pl[1].be_claimed()
                    self.pl[2].be_claimed()
                    self.pl[3].be_claimed()
                    has_chan_kan = False
                    if self.pl[self.find_next_player(1)].can_chan_kan(has_kan[1], has_kan[0]):
                        has_chan_kan = True
                    if self.pl[self.find_next_player(2)].can_chan_kan(has_kan[1], has_kan[0]):
                        has_chan_kan = True
                    if self.pl[self.find_next_player(3)].can_chan_kan(has_kan[1], has_kan[0]):
                        has_chan_kan = True
                    if has_chan_kan:
                        result1 = self.pl[self.find_next_player(1)].claim(has_kan[1]) == 6
                        result2 = self.pl[self.find_next_player(2)].claim(has_kan[1]) == 6
                        result3 = self.pl[self.find_next_player(3)].claim(has_kan[1]) == 6
                        if result1 or result2 or result3:
                            self.waiting_state = 3
                            if result1:
                                self.winner = self.find_next_player(1)
                            if result2 and self.winner == -1:
                                self.winner = self.find_next_player(2)
                            elif result2 and self.winner != -1:
                                self.winner2 = self.find_next_player(2)
                            if result3 and self.winner == -1:
                                self.winner = self.find_next_player(3)
                            elif result3 and self.winner != -1:
                                self.winner2 = self.find_next_player(3)
                            self.loser =  self.current_player
                    self.waiting_state = 2

                elif self.discard_tile != -1:
                    if self.pl[self.current_player].card.richi:
                        self.richi_list[self.current_player] = 1
                        if sum(self.richi_list > self.richi_number):
                            self.richi_number += 1
                            self.kyoutaku += 1000
                    self.discard_stack[self.current_player].append(self.discard_tile)
                    wait = self.check_action(self.discard_tile)
                    if wait:
                        self.waiting_state = 1
                        #return
                        #continue
                    else :
                        self.discard_tile = -1
                        self.next_player()
                        self.waiting_state = 2
            #wait for naki
            if self.waiting_state == 1:
                # 0 : right
                # 1 : opposite
                # 2 : left
                result = [-1, -1, -1]

                result[0] = self.pl[self.find_next_player(1)].claim(self.discard_tile)
                result[1] = self.pl[self.find_next_player(2)].claim(self.discard_tile)
                result[2] = self.pl[self.find_next_player(3)].claim(self.discard_tile)


                #print(result)

                if result[0] == -1 or result[1] == -1 or result[2] == -1:
                    return 0
                    #continue
                if result[0] == 0 and result[1] == 0 and result[2] == 0:
                    self.discard_tile = -1
                    self.reset_action_state()
                    self.next_player()
                    self.waiting_state = 2
                else :
                    self.waiting_state = 0
                    self.reset_action_state()
                    self.pl[0].be_claimed()
                    self.pl[1].be_claimed()
                    self.pl[2].be_claimed()
                    self.pl[3].be_claimed()
                    if result[0] == 6 or result[1] == 6 or result[2] == 6:                          #ron
                        self.waiting_state = 3
                        self.winning_tile = self.discard_tile
                        if result[0] == 6:
                            self.winner = self.find_next_player(1)
                        if result[1] == 6 and self.winner == -1:
                            self.winner = self.find_next_player(2)
                        elif result[1] == 6 and self.winner != -1:
                            self.winner2 = self.find_next_player(2)
                        if result[2] == 6 and self.winner == -1:
                            self.winner = self.find_next_player(3)
                        elif result[2] == 6 and self.winner != -1:
                            self.winner2 = self.find_next_player(3)
                        self.loser = self.current_player
                    elif result[0] == 1 or result[0] == 2:                                          #pon / kan
                        self.current_player = self.find_next_player(1)
                        #print('player ', self.current_player, '\tpon\t', self.discard_tile)
                        self.pl[self.current_player].info.time_to_discard = True
                        if result[0] == 1:
                            self.draw_stack[self.current_player].append(50)
                            self.pl[self.current_player].card.pon(self.discard_tile, 3)
                        else :
                            self.discard_stack[self.current_player].append(60)
                            self.pl[self.current_player].card.min_kan(self.discard_tile, 3)
                            self.waiting_state = 2
                    elif result[1] == 1 or result[1] == 2:                                          #pon / kan
                        self.current_player = self.find_next_player(2)
                        #print('player ', self.current_player, '\tpon\t', self.discard_tile)
                        self.pl[self.current_player].info.time_to_discard = True
                        if result[1] == 1:
                            self.draw_stack[self.current_player].append(50)
                            self.pl[self.current_player].card.pon(self.discard_tile, 2)
                        else :
                            self.discard_stack[self.current_player].append(60)
                            self.pl[self.current_player].card.min_kan(self.discard_tile, 2)
                            self.waiting_state = 2
                    elif result[2] == 1 or result[2] == 2:                                          #pon / kan
                        self.current_player = self.find_next_player(3)
                        #print('player ', self.current_player, '\tpon\t', self.discard_tile)
                        self.pl[self.current_player].info.time_to_discard = True
                        if result[2] == 1:
                            self.draw_stack[self.current_player].append(50)
                            self.pl[self.current_player].card.pon(self.discard_tile, 1)
                        else :
                            self.discard_stack[self.current_player].append(60)
                            self.pl[self.current_player].card.min_kan(self.discard_tile, 1)
                            self.waiting_state = 2
                    elif result[0] > 2 and result[1] == 0 and result[2] == 0:                       #chi
                        self.current_player = self.find_next_player(1)
                        #print('player ', self.current_player, '\tchi\t', self.discard_tile)
                        self.pl[self.current_player].info.time_to_discard = True
                        self.draw_stack[self.current_player].append(40)
                        no_aka = self.discard_tile
                        if no_aka % 10 == 0:
                            no_aka += 5
                        if result[0] == 3:
                            self.pl[self.current_player].card.chi(self.discard_tile, no_aka + 1, no_aka + 2)
                        elif result[0] == 4:
                            self.pl[self.current_player].card.chi(self.discard_tile, no_aka - 1, no_aka + 1)
                        elif result[0] == 5:
                            self.pl[self.current_player].card.chi(self.discard_tile, no_aka - 2, no_aka - 1)
                    else :
                        self.discard_tile = -1
                        self.reset_action_state()
                        self.next_player()
                        self.waiting_state = 2
                        #continue
                self.discard_tile = -1
                return 0
                #continue
            #wait for draw card
            if self.waiting_state == 2:
                new_pai = -1
                if self.draw_rin_shan:
                    new_pai = self.card_stack.draw_rin_shan()
                    self.pl[self.current_player].info.rin_shan = True
                else :
                    new_pai = self.card_stack.draw()
                

                self.remain_tile -= 1
                
                if new_pai == -1:
                    self.waiting_state = 3
                    return 0
                    #continue
                else :
                    #print('player ', self.current_player, '\tdraw\t', new_pai)
                    self.draw_stack[self.current_player].append(new_pai)
                    if self.card_stack.first_card == self.card_stack.hai_tei:
                        self.pl[0].info.last = True
                        self.pl[1].info.last = True
                        self.pl[2].info.last = True
                        self.pl[3].info.last = True
                    
                    self.pl[self.current_player].draw(new_pai)
                    self.pl[self.current_player].an_kan_tsumo_check()
                    if self.current_player == 0:
                        self.game_round += 1

                    self.waiting_state = 0
            if self.waiting_state == 3:
                # if some body win
                if self.winner != -1:
                    point = point_check(self.pl[self.winner].card, self.chan_fon, self.pl[self.winner].info.men_fon, self.pl[self.winner].info.last, self.pl[self.winner].info.first, self.pl[self.winner].info.rin_shan, self.pl[self.winner].info.chan_kan, self.pl[self.winner].info.i_ba_tsu, self.red_number, self.card_stack.get_dora, self.card_stack.get_uradora)
                    self.pl[self.winner].info.update_reward = True
                    self.pl[self.winner].info.reward = point.point
                    print(point.point)
                    if self.is_tsumo:
                        self.pl[self.winner].info.point += point.point + 300 * self.honba + 1000 * self.kyoutaku
                        for i in range(0, 3):
                            if self.pl[self.winner].info.men_fon == 30:
                                self.pl[self.find_next_player(i + 1)].info.point -= point.point / 3 + 100 * self.honba
                            else :
                                if self.pl[self.find_next_player(i + 1)].info.men_fon == 30:
                                    self.pl[self.find_next_player(i + 1)].info.point -= point.point / 2 + 100 * self.honba
                                else :
                                    self.pl[self.find_next_player(i + 1)].info.point -= point.point / 4 + 100 * self.honba
                    else :
                        self.pl[self.winner].info.point += point.point + 300 * self.honba + 1000 * self.kyoutaku
                        self.pl[self.loser].info.point -= point.point + 300 * self.honba
                    if self.winner2 != -1:
                        point = point_check(self.pl[self.winner2].card, self.chan_fon, self.pl[self.winner2].info.men_fon, self.pl[self.winner2].info.last, self.pl[self.winner2].info.first, self.pl[self.winner2].info.rin_shan, self.pl[self.winner2].info.chan_kan, self.pl[self.winner2].info.i_ba_tsu, self.red_number, self.card_stack.get_dora, self.card_stack.get_uradora)
                        self.pl[self.winner2].info.update_reward = True
                        self.pl[self.winner2].info.reward = point.point
                        if self.is_tsumo:
                            self.pl[self.winner2].info.point += point.point + 300 * self.honba + 1000 * self.kyoutaku
                            for i in range(0, 3):
                                if self.pl[self.winner2].info.men_fon == 30:
                                    self.pl[self.find_next_player(i + 1)].info.point -= point.point / 3 + 100 * self.honba
                                else :
                                    if self.pl[self.find_next_player(i + 1)].info.men_fon == 30:
                                        self.pl[self.find_next_player(i + 1)].info.point -= point.point / 2 + 100 * self.honba
                                    else :
                                        self.pl[self.find_next_player(i + 1)].info.point -= point.point / 4 + 100 * self.honba
                        else :
                            self.pl[self.winner2].info.point += point.point + 300 * self.honba + 1000 * self.kyoutaku
                            self.pl[self.loser].info.point -= point.point + 300 * self.honba
                    self.kyoutaku = 0

                else :
                    ten = [0, 0, 0, 0]
                    for i in range(0, 4):
                        if self.pl[i].info.tenpai_list == []:
                            ten[i] = 1
                    ten_num = sum(ten)
                    if ten_num == 1:
                        for i in range(0, 4):
                            if ten[i] == 1:
                                self.pl[i].info.point += 3000
                            else :
                                self.pl[i].info.point -= 1000
                    elif ten_num == 2:
                        for i in range(0, 4):
                            if ten[i] == 1:
                                self.pl[i].info.point += 1500
                            else :
                                self.pl[i].info.point -= 1500
                    elif ten_num == 3:
                        for i in range(0, 4):
                            if ten[i] == 1:
                                self.pl[i].info.point += 1000
                            else :
                                self.pl[i].info.point -= 3000


                self.record_game_log()
                self.next_kyouku()


                return 1

                #end game
                

                #for i in range(4):
                #    print('player id ', i)
                #    print(self.start_deal[i])
                #    print(self.draw_stack[i])
                #    print(self.discard_stack[i])
                #    print(self.final_card[i], '\t', self.pl[i].card.kan_card)
                #    print(' ')
                #self.end = False
                #for i in self.pl:
                #    i.info.end_game = True

            return 0

                    
                


            






if __name__ == '__main__':
    game = Game()

    for i in range(0, 4):
        game.pl[i].id = i
    
    agent = []
    for i in range(0, 4):
        agent.append(Agent(game.pl[i].card, game.pl[i].info, i + 1))



    start_time = time.time()

    #game.start()
    #for i in agent:
    #    i.start()

    round_count = 0
    while game.not_end:
        round_count += game.run()
        for i in range(0, 4):
            agent[i].run()


    game.game_log.write_log_file()

    #game.join()
    #for i in agent:
    #    i.join()

    end_time = time.time()
    update_table()

    print('elapse time ', end_time - start_time)
    print('total ', round_count)

    print(agent[0].card.card13)
    print(agent[1].card.card13)
    print(agent[2].card.card13)
    print(agent[3].card.card13)

