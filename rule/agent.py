import threading
import time
from rule.hand_card import HandCard
from rule.player import Player
from rule.player_info import PlayerInfo

class Agent:#(threading.Thread):

    id = 0
    def __init__(self, pai, info, id):
        #threading.Thread.__init__(self)

        self.card = pai
        self.info = info
        self.id = id

    # return 0 or chi case
    def want_to_chi(self):
        # . . .
        return self.info.chi_able_list[0][2]
        #return 0

    def want_to_pon(self):
        # . . .
        return True

    def want_to_kan(self):
        # . . .
        return False

    def want_to_ron(self):
        # . . .
        return False

    # return an kan case
    def want_to_ankan(self):
        # . . .
        return -1

    def want_to_tsumo(self):
        # . . .
        return True

    def which_to_discard(self):
        # . . .
        return self.card.card13[0]

    def run(self):
        if True:
        #while not self.info.end_game:
            if self.info.time_to_discard:
                if self.info.can_tsumo:
                    self.info.can_tsumo = False
                    if self.want_to_tsumo():
                        self.info.want_to_tsumo = True
                        return
                if self.info.can_ankan:
                    self.info.can_ankan = False
                    self.info.an_kan_case = self.want_to_ankan()
                    if self.info.an_kan_case != -1:
                        self.info.action_state = 2
                        return
                self.info.discard_tile = self.which_to_discard()
            else :
                if self.info.can_ron:
                    if self.want_to_ron():
                        self.info.action_state = 6
                    else :
                        self.info.action_state = 0
                    self.info.can_ron = False
                if self.info.can_kan:
                    if self.want_to_kan():
                        self.info.can_pon = False
                        self.info.can_kan = False
                        self.info.action_state = 2
                        return
                    else :
                        self.info.action_state = 0
                    self.info.can_kan = False
                if self.info.can_pon:
                    if self.want_to_pon():
                        self.info.action_state = 1
                    else :
                        self.info.action_state = 0
                    self.info.can_pon = False
                if self.info.can_chi:
                    self.info.action_state = self.want_to_chi()
                    self.info.can_chi = False



if __name__ == '__main__':
    pl = Player()
    test = Agent(pl.card, pl.info)
    print("test ", test.card.card14)
    print("pl   ", pl.card.card14)
    pl.draw(19)
    print("test ", test.card.card14)
    print("pl   ", pl.card.card14)


