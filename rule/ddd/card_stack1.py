import numpy as np
import random
import time
import copy

class CardStack:
    rin_shan = 135
    hai_tei = 121
    first_card = 52
    def __init__(self):
        random.seed(time.time())
        self.card_wall = [0] * 136
        self.reset(0)
    
    def reset(self, red):
        self.first_card = 52
        self.rin_shan = 135
        self.hai_tei = 121
        for i in range(0, 136):
            self.card_wall[i] = int(i / 4) + 1
            if self.card_wall[i] == 10:
                self.card_wall[i] = 35
            if self.card_wall[i] == 20:
                self.card_wall[i] = 36
        if red >= 3:
            self.card_wall[16] = 0
            self.card_wall[56] = 10
            self.card_wall[96] = 20
            if red == 4:
                self.card_wall[17] = 0
        for i in range(0, 136):
            target = random.randint(0, 135)
            tmp = self.card_wall[i]
            self.card_wall[i] = self.card_wall[target]
            self.card_wall[target] = tmp
            
    def deal(self):
        self.first_card = 52
        p = []
        p.append(self.card_wall[0 : 13])
        p.append(self.card_wall[13 : 26])
        p.append(self.card_wall[26 : 39])
        p.append(self.card_wall[39 : 52])
        return p

    def deal_with_n(self, n):
        p = []
        p.append(self.card_wall[0 : n])
        p.append(self.card_wall[n : n * 2])
        p.append(self.card_wall[n * 2 : n * 3])
        p.append(self.card_wall[n * 3 : n * 4])
        return p

    def special_deal(self, red):
        self.first_card = 52
        self.rin_shan = 135
        self.hai_tei = 121
        for i in range(0, 136):
            self.card_wall[i] = int(i / 4) + 1
            if self.card_wall[i] == 10:
                self.card_wall[i] = 35
            if self.card_wall[i] == 20:
                self.card_wall[i] = 36
        if red >= 3:
            self.card_wall[16] = 0
            self.card_wall[56] = 10
            self.card_wall[96] = 20
            if red == 4:
                self.card_wall[17] = 0
        p = []
        p.append(self.card_wall[0 : 13])
        p.append(self.card_wall[13 : 26])
        p.append(self.card_wall[26 : 39])
        p.append(self.card_wall[39 : 52])
        return p
    
    def draw(self):
        if self.first_card <= self.hai_tei:
            self.first_card += 1
            return self.card_wall[self.first_card - 1]
        else :
            return -1

    def draw_rin_shan(self):
        if self.rin_shan > 132:
            self.rin_shan -= 1
            self.hai_tei -= 1
            return card_wall[self.rin_shan]
        else :
            return -1

    def get_dora(self):
        dora = []
        i = 135
        p = 131
        while self.rin_shan <= i:
            d = self.card_wall[p] + 1
            if d == 37:
                d = 30
            elif d == 30:
                d = 21
            elif d == 20:
                d = 11
            elif d == 10:
                d = 1
            dora.append(d)
            i -= 1
            p -= 2
        return dora

    def get_uradora(self):
        dora = []
        i = 135
        p = 130
        while self.rin_shan <= i:
            d = self.card_wall[p] + 1
            if d == 37:
                d = 30
            elif d == 30:
                d = 21
            elif d == 20:
                d = 11
            elif d == 10:
                d = 1
            dora.append(d)
            i -= 1
            p -= 2
        return dora

        
if __name__ == "__main__":
    test = CardStack()
    test.reset(0)
    print(test.card_wall)
    print(test.deal())
    print(test.draw())
