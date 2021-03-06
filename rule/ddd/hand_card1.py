import numpy as np
from rule.card_stack import CardStack
import copy

class HandCard:
    def __init__(self):
        self.card13 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.card14 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.check_card13 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.check_card14 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.draw_tile = -1
        self.ron_tile = -1
        self.chi_card = []
        self.pon_card = []
        self.kan_card = []
        self.old_s = -1
    
    richi = False
    def red_trans(self):
        red_num = 0
        self.check_card13 = copy.copy(self.card13)
        self.check_card14 = copy.copy(self.card14)
        for p in self.check_card13:
            if p == 0 or p == 10 or p == 20:
                p = p + 5
        for p in self.check_card14:
            if p == 0 or p == 10 or p == 20:
                p = p + 5
                red_num = red_num + 1
        self.check_card13.sort()
        self.check_card14.sort()
        return red_num

    def reset(self):
        self.chi_card = []
        self.pon_card = []
        self.kan_card = []
        self.old_s = -1

    def deal(self, card):
        self.card13 = copy.copy(card)
        self.card13.sort()
        self.card14 = copy.copy(self.card13)

    def draw(self, card):
        self.draw_tile = card
        self.ron_tile = -1
        self.card14 = self.card13 + [card]
        self.card14.sort()
        self.red_trans()

    def discard(self, card):
        self.draw_tile = -1

        self.card14.remove(card)
        #self.card14.pop()
        self.card13 = copy.copy(self.card14)
        self.red_trans()
        return True

    def ron(self, card):
        self.ron_tile = card
        self.card14 = self.card13 + [card]
        self.card14.sort()

    #
    #p1 : which pai you eat
    def chi(self, p1, p2, p3):
        i = 0
        p2red = False
        p3red = False
        index1 = -1
        index2 = -1
        for p in self.card13:
            if p != 0 and p != 10 and p != 20:
                if p == p2 and index1 == -1:
                    index1 = i
                elif p == p3 and index2 == -1:
                    index2 = i
            else :
                if p + 5 == p2 and index1 == -1:
                    index1 = i
                    p2red = True
                elif p + 5 == p3 and index2 == -1:
                    index2 = i
                    p3red = True
            i = i + 1
        if index1 == -1 or index2 == -1:
            return False
        
        del self.card13[index1]
        del self.card13[index2 - 1]
        self.chi_card.append([p1, p2, p3])
        self.card14 = copy.copy(self.card13)
        if p2red:
            self.chi_card[-1][1] -= 5
        if p3red:
            self.chi_card[-1][2] -= 5
        return True

    #
    #dir :
    # 1  : right hand side
    # 2  : opposite
    # 3  : left  hand side
    def pon(self, pai, dir):

        i = 0
        index1 = -1
        index2 = -1
        pai_no_red = pai
        red = 0
        if pai == 0 or pai == 10 or pai == 20:
            pai_no_red = pai + 5
            red = red + 1
        for p in self.card13:
            if p != 0 and p != 10 and p != 20:
                if p == pai_no_red and index1 == -1:
                    index1 = i
                elif p == pai_no_red and index2 == -1:
                    index2 = i
            else :
                if p == pai and index == -1:
                    index1 = i
                    red = red + 1
                elif p == pai and index2 == -1:
                    index2 = i
                    red = red + 1
            i = i + 1
        if index1 == -1 or index2 == -1:
            return False

        del self.card13[index1]
        del self.card13[index2 - 1]
        self.card14 = copy.copy(self.card13)
        if red == 0:
            self.pon_card.append([pai, pai, pai, dir])
        elif red == 1:
            self.pon_card.append([pai_no_red - 5, pai_no_red, pai_no_red, dir])
        elif red == 2:
            self.pon_card.append([pai_no_red - 5, pai_no_red - 5, pai_no_red, dir])
        return True

    #
    #dir :
    # 0  : self
    # 1  : right hand side
    # 2  : opposite
    # 3  : left  hand side
    def min_kan(self, pai, dir):
        i = 0
        index1 = -1
        index2 = -1
        index3 = -1
        pai_no_red = pai
        if pai == 0 or pai == 10 or pai == 20:
            pai_no_red = pai + 5
        for p in self.card13:
            if p != 0 and p != 10 and p != 20:
                if p == pai_no_red and index1 == -1:
                    index1 = i
                elif p == pai_no_red and index2 == -1:
                    index2 = i
                elif p == pai_no_red and index3 == -1:
                    index3 = i
            else :
                if p == pai and index == -1:
                    index1 = i
                elif p == pai and index2 == -1:
                    index2 = i
                elif p == pai and index3 == -1:
                    index3 = i
            i = i + 1
        if index1 == -1 or index2 == -1 or index3 == -1:
            return False

        del self.card13[index1]
        del self.card13[index2 - 1]
        del self.card13[index3 - 2]
        self.kan_card.append([pai_no_red, dir])
        self.card14 = copy.copy(self.card13)
        return True

    def an_kan(self, pai):
        i = 0
        index1 = -1
        index2 = -1
        index3 = -1
        index4 = -1
        pai_no_red = pai
        if pai == 0 or pai == 10 or pai == 20:
            pai_no_red = pai + 5
        for p in self.card14:
            if p != 0 and p != 10 and p != 20:
                if p == pai_no_red and index1 == -1:
                    index1 = i
                elif p == pai_no_red and index2 == -1:
                    index2 = i
                elif p == pai_no_red and index3 == -1:
                    index3 = i
                elif p == pai_no_red and index4 == -1:
                    index4 = i
            else :
                if p == pai and index1 == -1:
                    index1 = i
                elif p == pai and index2 == -1:
                    index2 = i
                elif p == pai and index3 == -1:
                    index3 = i
                elif p == pai and index4 == -1:
                    index4 = i
            i = i + 1
        if index4 == -1:
            return False

        del self.card14[index1]
        del self.card14[index2 - 1]
        del self.card14[index3 - 2]
        del self.card14[index4 - 3]
        self.kan_card.append([pai_no_red, 0])
        self.card13 = copy.copy(self.card14)
        return True

    def ka_kan(self, pai):
        i = 0
        index = -1
        pai_no_red = pai
        if pai == 0 or pai == 10 or pai == 20:
            pai_no_red = pai + 5
        for p in self.card14:
            if p != 0 and p != 10 and p != 20:
                if p == pai_no_red:
                    index = i
                    break
            else :
                if p == pai:
                    index = i
                    break
            i = i + 1
        if index == -1:
            return False
        
        i = 0
        for my_pon in self.pon_card:
            if my_pon[2] == pai_no_red:
                self.kan_card.append([pai_no_red, my_pon[3]])
                del self.pon_card[i]
                del self.card14[index]
                self.card13 = copy.copy(self.card14)
                return True
            i = i + 1

        return False


    
if __name__ == '__main__':
    yama = CardStack()
    test = HandCard()
    test.deal(yama.special_deal(0)[0])
    print(test.card13)
    test.pon(1, 2)
    test.discard(2)
    print(test.card14)
    print(test.pon_card)
    print(test.kan_card)
    test.draw(6)
    test.ka_kan(1)
#    print(test.kan_card)
    print(test.card14)
    print(test.pon_card)
    print(test.kan_card)
