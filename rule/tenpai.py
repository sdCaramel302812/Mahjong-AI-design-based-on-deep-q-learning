import rule.define
import copy
import numpy as np
from rule.point import Point
from rule.card_stack import CardStack
from rule.hand_card import HandCard
import time
from rule.shan_ten_table import *

def chi_toi_check(pai):
    #pai.red_trans()
    if len(pai.check_card14) != 14:
        return False
    for i in range(0, 7):
        if pai.check_card14[i * 2] != pai.check_card14[i * 2 + 1]:
            return False
        if i <= 5 and pai.check_card14[i * 2] == pai.check_card14[i * 2] + 2:
            return False
    return True

def kokushi_check(pai):
    if len(pai.card14) != 14:
        return False
    p1 = False
    p9 = False
    m1 = False
    m9 = False
    s1 = False
    s9 = False
    t = False
    n = False
    s = False
    p = False
    h = False
    f = False
    c = False
    for p in pai.card14:
        if p == 1:
            p1 = True
        elif p == 9:
            p9 = True
        elif p == 11:
            m1 = True
        elif p == 19:
            m9 = True
        elif p == 21:
            s1 = True
        elif p == 29:
            s9 = True
        elif p == 30:
            t = True
        elif p == 31:
            n = True
        elif p == 32:
            s = True
        elif p == 33:
            p = True
        elif p == 34:
            h = True
        elif p == 35:
            f = True
        elif p == 36:
            c = True
        else :
            return False
    
    if p1 and p9 and m1 and m9 and s1 and s9 and t and n and s and p and h and f and c:
        return True
    else :
        return False

def old_win_check(pai):
    if len(pai.card14) % 3 != 2:
        return False
    if pai.draw_tile == -1 and pai.ron_tile == -1:
        return False
    #pai.red_trans()
    if chi_toi_check(pai):
        return True
    if kokushi_check(pai):
        return True

    if len(pai.check_card14) < 2:
        return False
    if len(pai.check_card14) == 2:
        if pai.check_card14[0] == pai.check_card14[1]:
            return True
        else :
            return False
    
    #
    #find pair
    for i in range(0, len(pai.check_card14) - 1):      
        remain = copy.copy(pai.check_card14)
        if pai.check_card14[i] == pai.check_card14[i + 1]:
            remain = np.delete(remain, [i, i + 1])

            #
            #check meld
            j = len(remain) - 1
            while True:
                if j <= 0:
                    return True

                if remain[j] >= 30:
                    if remain[j] == remain[j - 1] and remain[j] == remain[j - 2]:
                        # ton ton ton
                        remain = np.delete(remain, [j - 2, j - 1, j])
                        j = j - 3
                        continue
                    else :
                        break
                elif remain[j] >= 20:
                    if remain[j] == remain[j - 1] and remain[j] == remain[j - 2]:
                        # 1s 1s 1s
                        remain = np.delete(remain, [j - 2, j - 1, j])
                        j = j - 3
                        continue
                    elif remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 2] == 1:
                        # 1s 2s 3s
                        remain = np.delete(remain, [j - 2, j - 1, j])
                        j = j - 3
                        continue
                    elif j >= 3 and remain[j - 1] == remain[j - 2] and remain[j - 1] == remain[j - 3]:
                        # 1s 2s 2s 2s 2s 3s
                        remain = np.delete(remain, [j - 3, j - 2, j - 1])
                        j = j - 3
                        continue
                    elif j >= 3 and remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 3] == 1:
                        # 1s 2s 2s 3s 3s 4s
                        remain = np.delete(remain, [j - 3, j - 2, j])
                        j = j - 3
                        continue
                    elif j >= 5 and remain[j] - remain[j - 2 ] == 1 and remain[j - 2] - remain[j - 4] == 1 and remain[j - 2] == remain[j - 3]:
                        # 1s 1s 2s 2s 3s 3s
                        remain = np.delete(remain, [j - 4, j - 2, j])
                        j = j - 3
                        continue
                    else :
                        break
                elif remain[j] >= 10:
                    if remain[j] == remain[j - 1] and remain[j] == remain[j - 2]:
                        # 1s 1s 1s
                        remain = np.delete(remain, [j - 2, j - 1, j])
                        j = j - 3
                        continue
                    elif remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 2] == 1:
                        # 1s 2s 3s
                        remain = np.delete(remain, [j - 2, j - 1, j])
                        j = j - 3
                        continue
                    elif j >= 3 and remain[j - 1] == remain[j - 2] and remain[j - 1] == remain[j - 3]:
                        # 1s 2s 2s 2s 2s 3s
                        remain = np.delete(remain, [j - 3, j - 2, j - 1])
                        j = j - 3
                        continue
                    elif j >= 3 and remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 3] == 1:
                        # 1s 2s 2s 3s 3s 4s
                        remain = np.delete(remain, [j - 3, j - 2, j])
                        j = j - 3
                        continue
                    elif j >= 5 and remain[j] - remain[j - 2 ] == 1 and remain[j - 2] - remain[j - 4] == 1 and remain[j - 2] == remain[j - 3]:
                        # 1s 1s 2s 2s 3s 3s
                        remain = np.delete(remain, [j - 4, j - 2, j])
                        j = j - 3
                        continue
                    else :
                        break
                elif remain[j] >= 0:
                    if remain[j] == remain[j - 1] and remain[j] == remain[j - 2]:
                        # 1s 1s 1s
                        remain = np.delete(remain, [j - 2, j - 1, j])
                        j = j - 3
                        continue
                    elif remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 2] == 1:
                        # 1s 2s 3s
                        remain = np.delete(remain, [j - 2, j - 1, j])
                        j = j - 3
                        continue
                    elif j >= 3 and remain[j - 1] == remain[j - 2] and remain[j - 1] == remain[j - 3]:
                        # 1s 2s 2s 2s 2s 3s
                        remain = np.delete(remain, [j - 3, j - 2, j - 1])
                        j = j - 3
                        continue
                    elif j >= 3 and remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 3] == 1:
                        # 1s 2s 2s 3s 3s 4s
                        remain = np.delete(remain, [j - 3, j - 2, j])
                        j = j - 3
                        continue
                    elif j >= 5 and remain[j] - remain[j - 2 ] == 1 and remain[j - 2] - remain[j - 4] == 1 and remain[j - 2] == remain[j - 3]:
                        # 1s 1s 2s 2s 3s 3s
                        remain = np.delete(remain, [j - 4, j - 2, j])
                        j = j - 3
                        continue
                    else :
                        break

    return False


def win_check(pai):
    if (find_shan_ten_table(pai, 14)) == -1:
        return True
    else :
        return False

#
# just do it when card number is 13 - 3n
def old_tenpai_check(pai):
    #pai.red_trans()

    waiting_tile = np.zeros((1, 0))

    #
    #check for kokushi
    p1 = 0
    p9 = 0
    m1 = 0
    m9 = 0
    s1 = 0
    s9 = 0
    t = 0
    n = 0
    s = 0
    pei = 0
    h = 0
    f = 0
    c = 0
    if len(pai.check_card13) == 13:
        num19 = 0
        for p in pai.card13:
            num19 = num19 + 1
            if p == 1:
                p1 = 1
            elif p == 9:
                p9 = 1
            elif p == 11:
                m1 = 1
            elif p == 19:
                m9 = 1
            elif p == 21:
                s1 = 1
            elif p == 29:
                s9 = 1
            elif p == 30:
                t = 1
            elif p == 31:
                n = 1
            elif p == 32:
                s = 1
            elif p == 33:
                pei = 1
            elif p == 34:
                h = 1
            elif p == 35:
                f = 1
            elif p == 36:
                c = 1
        num19 = p1 + p9 + m1 + m9 + s1 + s9 + t + n + s + pei + h + f + c
        if num19 == 13:
            waiting_tile = np.append(waiting_tile, [1, 9, 11, 19, 21, 29, 30, 31, 32, 33, 34, 35, 36])
            return waiting_tile
        if num19 == 12:
            if not p1:
                waiting_tile = np.append(waiting_tile, [1])
            elif not p9:
                waiting_tile = np.append(waiting_tile, [9])
            elif not m1:
                waiting_tile = np.append(waiting_tile, [11])
            elif not m9:
                waiting_tile = np.append(waiting_tile, [19])
            elif not s1:
                waiting_tile = np.append(waiting_tile, [21])
            elif not s9:
                waiting_tile = np.append(waiting_tile, [29])
            elif not t:
                waiting_tile = np.append(waiting_tile, [30])
            elif not n:
                waiting_tile = np.append(waiting_tile, [31])
            elif not s:
                waiting_tile = np.append(waiting_tile, [32])
            elif not p:
                waiting_tile = np.append(waiting_tile, [33])
            elif not h:
                waiting_tile = np.append(waiting_tile, [34])
            elif not f:
                waiting_tile = np.append(waiting_tile, [35])
            elif not c:
                waiting_tile = np.append(waiting_tile, [36])
            return waiting_tile

    #
    #check for normal case
    pin = np.zeros(9)
    man = np.zeros(9)
    sou = np.zeros(9)
    other = np.zeros(7)
    for i in range(0, len(pai.check_card13)):
        if pai.check_card13[i] >= 30:
            other[int(pai.check_card13[i]) - 30] = other[int(pai.check_card13[i]) - 30] + 1
        elif pai.check_card13[i] >= 20:
            sou[int(pai.check_card13[i]) - 21] = sou[int(pai.check_card13[i]) - 21] + 1
        elif pai.check_card13[i] >= 10:
            man[int(pai.check_card13[i]) - 11] = man[int(pai.check_card13[i]) - 11] + 1
        else :
            pin[int(pai.check_card13[i]) - 1] = pin[int(pai.check_card13[i]) - 1] + 1
    #
    #check single number
    single = 0
    for p in other:
        if p == 1:
            single = single + 1
    if pin[0] == 1 and pin[1] == 0 and pin[2] == 0:
        single = single + 1
    if man[0] == 1 and man[1] == 0 and man[2] == 0:
        single = single + 1
    if sou[0] == 1 and sou[1] == 0 and man[2] == 0:
        single = single + 1
    if pin[8] == 1 and pin[7] == 0 and pin[6] == 0:
        single = single + 1
    if man[8] == 1 and man[7] == 0 and man[6] == 0:
        single = single + 1
    if sou[8] == 1 and sou[7] == 0 and sou[6] == 0:
        single = single + 1
    if pin[0] == 0 and pin[1] == 1 and pin[2] == 0 and pin[3] == 0:
        single = single + 1
    if man[0] == 0 and man[1] == 1 and man[2] == 0 and man[3] == 0:
        single = single + 1
    if sou[0] == 0 and sou[1] == 1 and sou[2] == 0 and sou[3] == 0:
        single = single + 1
    if pin[8] == 0 and pin[7] == 1 and pin[6] == 0 and pin[5] == 0:
        single = single + 1
    if man[8] == 0 and man[7] == 1 and man[6] == 0 and man[5] == 0:
        single = single + 1
    if sou[8] == 0 and sou[7] == 1 and man[6] == 0 and man[5] == 0:
        single = single + 1
    for i in range(2,7):
        if pin[i] == 1 and pin[i - 1] == 0 and pin[i - 2] == 0 and pin[i + 1] == 0 and pin[i + 2] == 0:
            single = single + 1
        if man[i] == 1 and man[i - 1] == 0 and man[i - 2] == 0 and man[i + 1] == 0 and man[i + 2] == 0:
            single = single + 1
        if sou[i] == 1 and sou[i - 1] == 0 and sou[i - 2] == 0 and sou[i + 1] == 0 and sou[i + 2] == 0:
            single = single + 1

    if single > 1:
        return waiting_tile
    #
    #exculde continuous sequence
    #
    # 1 1 1 1 1 1 1 1 1
    if pin[0] == 1 and pin[1] == 1 and pin[2] == 1 and pin[3] == 1 and pin[4] == 1 and pin[5] == 1 and pin[6] == 1 and pin[7] == 1 and pin[8] == 1:
        for i in range(0, 9):
            pin[i] = 0
    if man[0] == 1 and man[1] == 1 and man[2] == 1 and man[3] == 1 and man[4] == 1 and man[5] == 1 and man[6] == 1 and man[7] == 1 and man[8] == 1:
        for i in range(0, 9):
            man[i] = 0
    if sou[0] == 1 and sou[1] == 1 and sou[2] == 1 and sou[3] == 1 and sou[4] == 1 and sou[5] == 1 and sou[6] == 1 and sou[7] == 1 and sou[8] == 1:
        for i in range(0, 9):
            sou[i] = 0
    #
    # 0 1 1 2 1 2 1 1 0
    if pin[0] == 1 and pin[1] == 1 and pin[2] == 2 and pin[3] == 1 and pin[4] == 2 and pin[5] == 1 and pin[6] == 1 and pin[7] == 0:
        for i in range(0, 8):
            pin[i] = 0
    if man[0] == 1 and man[1] == 1 and man[2] == 2 and man[3] == 1 and man[4] == 2 and man[5] == 1 and man[6] == 1 and man[7] == 0:
        for i in range(0, 8):
            man[i] = 0
    if sou[0] == 1 and sou[1] == 1 and sou[2] == 2 and sou[3] == 1 and sou[4] == 2 and sou[5] == 1 and sou[6] == 1 and sou[7] == 0:
        for i in range(0, 8):
            sou[i] = 0
    if pin[0] == 0 and pin[1] == 1 and pin[2] == 1 and pin[3] == 2 and pin[4] == 1 and pin[5] == 2 and pin[6] == 1 and pin[7] == 1 and pin[8] == 0:
        for i in range(0, 8):
            pin[i] = 0
    if man[0] == 0 and man[1] == 1 and man[2] == 1 and man[3] == 2 and man[4] == 1 and man[5] == 2 and man[6] == 1 and man[7] == 1 and man[8] == 0:
        for i in range(0, 8):
            man[i] = 0
    if sou[0] == 0 and sou[1] == 1 and sou[2] == 1 and sou[3] == 2 and sou[4] == 1 and sou[5] == 2 and sou[6] == 1 and sou[7] == 1 and sou[8] == 0:
        for i in range(0, 8):
            sou[i] = 0
    if pin[1] == 0 and pin[8] == 1 and pin[2] == 1 and pin[3] == 1 and pin[4] == 2 and pin[5] == 1 and pin[6] == 2 and pin[7] == 1:
        for i in range(0, 8):
            pin[i] = 0
    if man[1] == 0 and man[8] == 1 and man[2] == 1 and man[3] == 1 and man[4] == 2 and man[5] == 1 and man[6] == 2 and man[7] == 1:
        for i in range(0, 8):
            man[i] = 0
    if sou[1] == 0 and sou[8] == 1 and sou[2] == 1 and sou[3] == 1 and sou[4] == 2 and sou[5] == 1 and sou[6] == 2 and sou[7] == 1:
        for i in range(0, 8):
            sou[i] = 0
    #
    # 0 1 1 1 1 1 2 1 1 0
    if pin[0] == 1 and pin[1] == 1 and pin[2] == 1 and pin[3] == 1 and pin[4] == 1 and pin[5] == 2 and pin[6] == 1 and pin[7] == 1 and pin[8] == 0:
        for i in range(0, 8):
            pin[i] = 0
    if man[0] == 1 and man[1] == 1 and man[2] == 1 and man[3] == 1 and man[4] == 1 and man[5] == 2 and man[6] == 1 and man[7] == 1 and man[8] == 0:
        for i in range(0, 8):
            man[i] = 0
    if sou[0] == 1 and sou[1] == 1 and sou[2] == 1 and sou[3] == 1 and sou[4] == 1 and sou[5] == 2 and sou[6] == 1 and sou[7] == 1 and sou[8] == 0:
        for i in range(0, 8):
            sou[i] = 0
    if pin[0] == 0 and pin[1] == 1 and pin[2] == 1 and pin[3] == 1 and pin[4] == 1 and pin[5] == 1 and pin[6] == 2 and pin[7] == 1 and pin[8] == 1:
        for i in range(0, 8):
            pin[i] = 0
    if man[0] == 0 and man[1] == 1 and man[2] == 1 and man[3] == 1 and man[4] == 1 and man[5] == 1 and man[6] == 2 and man[7] == 1 and man[8] == 1:
        for i in range(0, 8):
            man[i] = 0
    if sou[0] == 0 and sou[1] == 1 and sou[2] == 1 and sou[3] == 1 and sou[4] == 1 and sou[5] == 1 and sou[6] == 2 and sou[7] == 1 and sou[8] == 1:
        for i in range(0, 8):
            sou[i] = 0
    #
    # 0 1 1 2 1 1 1 1 1 0
    if pin[0] == 1 and pin[1] == 1 and pin[2] == 2 and pin[3] == 1 and pin[4] == 1 and pin[5] == 1 and pin[6] == 1 and pin[7] == 1 and pin[8] == 0:
        for i in range(0, 8):
            pin[i] = 0
    if man[0] == 1 and man[1] == 1 and man[2] == 2 and man[3] == 1 and man[4] == 1 and man[5] == 1 and man[6] == 1 and man[7] == 1 and man[8] == 0:
        for i in range(0, 8):
            man[i] = 0
    if sou[0] == 1 and sou[1] == 1 and sou[2] == 2 and sou[3] == 1 and sou[4] == 1 and sou[5] == 1 and sou[6] == 1 and sou[7] == 1 and sou[8] == 0:
        for i in range(0, 8):
            sou[i] = 0
    if pin[0] == 0 and pin[1] == 1 and pin[2] == 1 and pin[3] == 2 and pin[4] == 1 and pin[5] == 1 and pin[6] == 1 and pin[7] == 1 and pin[8] == 1:
        for i in range(0, 8):
            pin[i] = 0
    if man[0] == 0 and man[1] == 1 and man[2] == 1 and man[3] == 2 and man[4] == 1 and man[5] == 1 and man[6] == 1 and man[7] == 1 and man[8] == 1:
        for i in range(0, 8):
            man[i] = 0
    if sou[0] == 0 and sou[1] == 1 and sou[2] == 1 and sou[3] == 2 and sou[4] == 1 and sou[5] == 1 and sou[6] == 1 and sou[7] == 1 and sou[8] == 1:
        for i in range(0, 8):
            sou[i] = 0
    #
    # 0 1 1 1 1 1 1 0
    for i in range(1, 3):
        if pin[i - 1] == 0 and pin[i] == 1 and pin[i + 1] == 1 and pin[i + 2] == 1 and pin[i + 3] == 1 and pin[i + 4] == 1 and pin[i + 5] == 1 and pin[i + 6] == 0:
            for j in range(i, i + 6):
                pin[j] = 0
        if man[i - 1] == 0 and man[i] == 1 and man[i + 1] == 1 and man[i + 2] == 1 and man[i + 3] == 1 and man[i + 4] == 1 and man[i + 5] == 1 and man[i + 6] == 0:
            for j in range(i, i + 6):
                man[j] = 0
        if sou[i - 1] == 0 and sou[i] == 1 and sou[i + 1] == 1 and sou[i + 2] == 1 and sou[i + 3] == 1 and sou[i + 4] == 1 and sou[i + 5] == 1 and sou[i + 6] == 0:
            for j in range(i, i + 6):
                sou[j] = 0
    if pin[0] == 1 and pin[1] == 1 and pin[2] == 1 and pin[3] == 1 and pin[4] == 1 and pin[5] == 1 and pin[6] == 0:
        for j in range(0, 6):
            pin[j] = 0
    if man[0] == 1 and man[1] == 1 and man[2] == 1 and man[3] == 1 and man[4] == 1 and man[5] == 1 and man[6] == 0:
        for j in range(0, 6):
            man[j] = 0
    if sou[0] == 1 and sou[1] == 1 and sou[2] == 1 and sou[3] == 1 and sou[4] == 1 and sou[5] == 1 and sou[6] == 0:
        for j in range(0, 6):
            sou[j] = 0
    if pin[8] == 1 and pin[7] == 1 and pin[6] == 1 and pin[5] == 1 and pin[4] == 1 and pin[3] == 1 and pin[2] == 0:
        for j in range(3, 9):
            pin[j] = 0
    if man[8] == 1 and man[7] == 1 and man[6] == 1 and man[5] == 1 and man[4] == 1 and man[3] == 1 and man[2] == 0:
        for j in range(3, 9):
            man[j] = 0
    if sou[8] == 1 and sou[7] == 1 and sou[6] == 1 and sou[5] == 1 and sou[4] == 1 and sou[3] == 1 and sou[2] == 0:
        for j in range(3, 9):
            sou[j] = 0
    #
    # 0 1 1 2 1 1 0
    for i in range(1, 4):
        if pin[i - 1] == 0 and pin[i] == 1 and pin[i + 1] == 1 and pin[i + 2] == 2 and pin[i + 3] == 1 and pin[i + 4] == 1 and pin[i + 5] == 0:
            for j in range(i, i + 5):
                pin[j] = 0
        if man[i - 1] == 0 and man[i] == 1 and man[i + 1] == 1 and man[i + 2] == 2 and man[i + 3] == 1 and man[i + 4] == 1 and man[i + 5] == 0:
            for j in range(i, i + 5):
                man[j] = 0
        if sou[i - 1] == 0 and sou[i] == 1 and sou[i + 1] == 1 and sou[i + 2] == 2 and sou[i + 3] == 1 and sou[i + 4] == 1 and sou[i + 5] == 0:
            for j in range(i, i + 5):
                sou[j] = 0
    if pin[0] == 1 and pin[1] == 1 and pin[2] == 2 and pin[3] == 1 and pin[4] == 1 and pin[5] == 0:
        for j in range(0, 5):
            pin[j] = 0
    if man[0] == 1 and man[1] == 1 and man[2] == 2 and man[3] == 1 and man[4] == 1 and man[5] == 0:
        for j in range(0, 5):
            man[j] = 0
    if sou[0] == 1 and sou[1] == 1 and sou[2] == 2 and sou[3] == 1 and sou[4] == 1 and sou[5] == 0:
        for j in range(0, 5):
            sou[j] = 0
    if pin[3] == 0 and pin[4] == 1 and pin[5] == 1 and pin[6] == 2 and pin[7] == 1 and pin[8] == 1:
        for j in range(4, 9):
            pin[j] = 0
    if man[3] == 0 and man[4] == 1 and man[5] == 1 and man[6] == 2 and man[7] == 1 and man[8] == 1:
        for j in range(4, 9):
            man[j] = 0
    if sou[3] == 0 and sou[4] == 1 and sou[5] == 1 and sou[6] == 2 and sou[7] == 1 and sou[8] == 1:
        for j in range(4, 9):
            sou[j] = 0
    #
    # 0 1 2 2 1 0
    for i in range(1, 5):
        if pin[i - 1] == 0 and pin[i] == 1 and pin[i + 1] == 2 and pin[i + 2] == 2 and pin[i + 3] == 1 and pin[i + 4] == 0:
            for j in range(i, i + 4):
                pin[j] = 0
        if man[i - 1] == 0 and man[i] == 1 and man[i + 1] == 2 and man[i + 2] == 2 and man[i + 3] == 1 and man[i + 4] == 0:
            for j in range(i, i + 4):
                man[j] = 0
        if sou[i - 1] == 0 and sou[i] == 1 and sou[i + 1] == 2 and sou[i + 2] == 2 and sou[i + 3] == 1 and sou[i + 4] == 0:
            for j in range(i, i + 4):
                sou[j] = 0
    if pin[0] == 1 and pin[1] == 2 and pin[2] == 2 and pin[3] == 1 and pin[4] == 0:
        for i in range(0, 4):
            pin[i] = 0
    if man[0] == 1 and man[1] == 2 and man[2] == 2 and man[3] == 1 and man[4] == 0:
        for i in range(0, 4):
            man[i] = 0
    if sou[0] == 1 and sou[1] == 2 and sou[2] == 2 and sou[3] == 1 and sou[4] == 0:
        for i in range(0, 4):
            sou[i] = 0
    if pin[0] == 1 and pin[1] == 2 and pin[2] == 2 and pin[3] == 1 and pin[4] == 0:
        for i in range(0, 4):
            pin[i] = 0
    if man[5] == 1 and man[6] == 2 and man[7] == 2 and man[8] == 1 and man[4] == 0:
        for i in range(5, 9):
            man[i] = 0
    if sou[5] == 1 and sou[6] == 2 and sou[7] == 2 and sou[8] == 1 and sou[4] == 0:
        for i in range(5, 9):
            sou[i] = 0
    #
    # 0 2 2 2 0
    for i in range(1, 6):
        if pin[i - 1] == 0 and pin[i] == 2 and pin[i + 1] == 2 and pin[i + 2] == 2 and pin[i + 3] == 0:
            for j in range(i, i + 3):
                pin[j] = 0
        if man[i - 1] == 0 and man[i] == 2 and man[i + 1] == 2 and man[i + 2] == 2 and man[i + 3] == 0:
            for j in range(i, i + 3):
                man[j] = 0
        if sou[i - 1] == 0 and sou[i] == 2 and sou[i + 1] == 2 and sou[i + 2] == 2 and sou[i + 3] == 0:
            for j in range(i, i + 3):
                sou[j] = 0
    if pin[0] == 2 and pin[1] == 2 and pin[2] == 2 and pin[3] == 0:
        for i in range(0, 3):
            pin[i] = 0
    if man[0] == 2 and man[1] == 2 and man[2] == 2 and man[3] == 0:
        for i in range(0, 3):
            man[i] = 0
    if sou[0] == 2 and sou[1] == 2 and sou[2] == 2 and sou[3] == 0:
        for i in range(0, 3):
            sou[i] = 0
    if pin[6] == 2 and pin[7] == 2 and pin[8] == 2 and pin[5] == 0:
        for i in range(6, 9):
            pin[i] = 0
    if man[6] == 2 and man[7] == 2 and man[8] == 2 and man[5] == 0:
        for i in range(6, 9):
            man[i] = 0
    if sou[6] == 2 and sou[7] == 2 and sou[8] == 2 and sou[5] == 0:
        for i in range(6, 9):
            sou[i] = 0
    #
    # 0 1 1 1 0
    for i in range(1, 6):
        if pin[i - 1] == 0 and pin[i] == 1 and pin[i + 1] == 1 and pin[i + 2] == 1 and pin[i + 3] == 0:
            for j in range(i, i + 3):
                pin[j] = 0
        if man[i - 1] == 0 and man[i] == 1 and man[i + 1] == 1 and man[i + 2] == 1 and man[i + 3] == 0:
            for j in range(i, i + 3):
                man[j] = 0
        if sou[i - 1] == 0 and sou[i] == 1 and sou[i + 1] == 1 and sou[i + 2] == 1 and sou[i + 3] == 0:
            for j in range(i, i + 3):
                sou[j] = 0
    if pin[0] == 1 and pin[1] == 1 and pin[2] == 1 and pin[3] == 0:
        for i in range(0, 3):
            pin[i] = 0
    if man[0] == 1 and man[1] == 1 and man[2] == 1 and man[3] == 0:
        for i in range(0, 3):
            man[i] = 0
    if sou[0] == 1 and sou[1] == 1 and sou[2] == 1 and sou[3] == 0:
        for i in range(0, 3):
            sou[i] = 0
    if pin[6] == 1 and pin[7] == 1 and pin[8] == 1 and pin[5] == 0:
        for i in range(6, 9):
            pin[i] = 0
    if man[6] == 1 and man[7] == 1 and man[8] == 1 and man[5] == 0:
        for i in range(6, 9):
            man[i] = 0
    if sou[6] == 1 and sou[7] == 1 and sou[8] == 1 and sou[5] == 0:
        for i in range(6, 9):
            sou[i] = 0
    #exclude continuous sequence
    #
    for i in range(1, 8):
        if pin[i - 1] > 0 or pin[i] > 0 or pin[i + 1] > 0:
            pai.ron(i + 1)
            if win_check(pai):
                waiting_tile = np.append(waiting_tile, [i + 1])
        if man[i - 1] > 0 or man[i] > 0 or man[i + 1] > 0:
            pai.ron(i + 11)
            if win_check(pai):
                waiting_tile = np.append(waiting_tile, [i + 11])
        if sou[i - 1] > 0 or sou[i] > 0 or sou[i + 1] > 0:
            pai.ron(i + 21)
            if win_check(pai):
                waiting_tile = np.append(waiting_tile, [i + 21])
    if pin[0] > 0 or pin[1] > 0:
        pai.ron(1)
        if win_check(pai):
            waiting_tile = np.append(waiting_tile, [1])
    if man[0] > 0 or man[1] > 0:
        pai.ron(11)
        if win_check(pai):
            waiting_tile = np.append(waiting_tile, [11])
    if sou[0] > 0 or sou[1] > 0:
        pai.ron(21)
        if win_check(pai):
            waiting_tile = np.append(waiting_tile, [21])
    if pin[7] > 0 or pin[8] > 0:
        pai.ron(9)
        if win_check(pai):
            waiting_tile = np.append(waiting_tile, [9])
    if man[7] > 0 or man[8] > 0:
        pai.ron(19)
        if win_check(pai):
            waiting_tile = np.append(waiting_tile, [19])
    if sou[7] > 0 or sou[8] > 0:
        pai.ron(29)
        if win_check(pai):
            waiting_tile = np.append(waiting_tile, [29])
    for i in range(0, 7):
        if other[i] > 0:
            pai.ron(i + 30)
            if win_check(pai):
                waiting_tile = np.append(waiting_tile, [i + 30])
    #check for normal case
    #

    #
    #check for chi toi
    if len(pai.check_card13) == 13:
        dan_ki = -1
        i = 0
        while i <= 12:
            if i == 12:
                dan_ki = pai.check_card13[12]
                break
            if pai.check_card13[i] == pai.check_card13[i + 1]:
                i = i + 2
            else :
                if dan_ki == -1:
                    dan_ki = pai.check_card13[i]
                    i = i + 1
                else :
                    dan_ki = -1
                    break
        if dan_ki != -1:
            waiting_tile = np.append(waiting_tile, [dan_ki])

    return waiting_tile


def tenpai_check(pai):
    if find_shan_ten_table(pai, 13) > 0:
        return []

    waiting_tile = []
    #pai.red_trans()
    pin = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    man = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    sou = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    other = [0, 0, 0, 0, 0, 0, 0]
    for i in pai.check_card13:
        if i >= 30:
            other[int(i) - 30] += 1
        elif i > 20:
            sou[int(i) - 21] += 1
        elif i > 10:
            man[int(i) - 11] += 1
        else :
            pin[int(i) - 1] += 1
    for i in range(1, 8):
        if pin[i - 1] > 0 or pin[i] > 0 or pin[i + 1] > 0:
            pai.ron(i + 1)
            if win_check(pai):
                waiting_tile.append(i + 1)
        if man[i - 1] > 0 or man[i] > 0 or man[i + 1] > 0:
            pai.ron(i + 11)
            if win_check(pai):
                waiting_tile.append(i + 11)
        if sou[i - 1] > 0 or sou[i] > 0 or sou[i + 1] > 0:
            pai.ron(i + 21)
            if win_check(pai):
                waiting_tile.append(i + 21)
    if pin[0] > 0 or pin[1] > 0:
        pai.ron(1)
        if win_check(pai):
            waiting_tile.append(1)
    if man[0] > 0 or man[1] > 0:
        pai.ron(11)
        if win_check(pai):
            waiting_tile.append(11)
    if sou[0] > 0 or sou[1] > 0:
        pai.ron(21)
        if win_check(pai):
            waiting_tile.append(21)
    if pin[7] > 0 or pin[8] > 0:
        pai.ron(9)
        if win_check(pai):
            waiting_tile.append(9)
    if man[7] > 0 or man[8] > 0:
        pai.ron(19)
        if win_check(pai):
            waiting_tile.append(19)
    if sou[7] > 0 or sou[8] > 0:
        pai.ron(29)
        if win_check(pai):
            waiting_tile.append(29)
    for i in range(0, 7):
        if other[i] > 0:
            pai.ron(30 + i)
            if win_check(pai):
                waiting_tile.append(i + 30)
    #check for normal case
    #

    #
    #check for chi toi
    if len(pai.check_card13) == 13:
        dan_ki = -1
        i = 0
        while i <= 12:
            if i == 12:
                dan_ki = pai.check_card13[12]
                break
            if pai.check_card13[i] == pai.check_card13[i + 1]:
                i = i + 2
            else :
                if dan_ki == -1:
                    dan_ki = pai.check_card13[i]
                    i = i + 1
                else :
                    dan_ki = -1
                    break
        if dan_ki != -1:
            waiting_tile = np.append(waiting_tile, [dan_ki])

    return waiting_tile


#
#not only for richi but also check discard which to tenpai
#return value will be [int list int list ...]
def richi_check(pai):
    tenpai_list = []
    #pai.red_trans()

    if find_shan_ten_table(pai, 14) > 0:
        return tenpai_list


    for i in range(0, len(pai.check_card14)):
        copy_obj = copy.deepcopy(pai)
        p = copy_obj.check_card14[i]
        copy_obj.discard(p)
        tenpai = tenpai_check(copy_obj)
        if tenpai != []:
            tenpai_list.append([p, tenpai])

    return tenpai_list

#
#last for haitei, houtei
#first for w richi, tenho, chiho
#aka_n for aka number
def point_check(pai, chanfon, menfon, last, first, rinshan, chankan, ibatsu, aka_n, dora, uradora):
    if win_check(pai):
        yaku = Point()
        yaku.agari = True
        yaku.oya = True if (menfon == 30) else False

        copy_pai = copy.deepcopy(pai)

        min_ko_19 = 0
        an_ko_19 = 0
        min_ko_28 = 0
        an_ko_28 = 0
        min_kan_19 = 0
        an_kan_19 = 0
        min_kan_28 = 0
        an_kan_28 = 0
        pair = -1
        men_zen = True
        tan_yao = True
        pin_hu = True
        yaku_nashi = True
        ten_pai_fu = True
        chi_toi = False
        kokushi = False
        pei_ko = 0
        #
        #avoid card like 2 2 3 3 4 4 5 5
        # 0 : none
        # 1 : pin
        # 2 : man
        # 3 : sou
        i_pei_ko_with_pair = 0
        #whitch card to win
        last_pai = -1
        if pai.ron_tile != -1:
            last_pai = pai.ron_tile
        else :
            last_pai = pai.draw_tile
        if last_pai == 0 or last_pai == 10 or last_pai == 20:
            last_pai = last_pai + 5

        mentsu = np.zeros((0, 3))

        #
        #change red card into normal card
        yaku.akadora = yaku.akadora + copy_pai.red_trans()
        for p in copy_pai.chi_card:
            for i in range(0, 3):
                if p[i] == 0 or p[i] == 10 or p[i] == 20:
                    p[i] = p[i] + 5
                    yaku.akadora = yaku.akadora + 1
        for p in copy_pai.pon_card:
            for i in range(0, 3):
                if p[i] == 0 or p[i] == 10 or p[i] == 20:
                    p[i] = p[i] + 5
                    yaku.akadora = yaku.akadora + 1
        for p in copy_pai.kan_card:
            if aka_n >= 3 and (p[0] == 5 or p[0] == 15 or p[0] == 25):
                yaku.akadora = yaku.akadora + 1
                if aka_n == 4 and p[0] == 5:
                    yaku.akadora = yaku.akadora + 1
        
        if len(copy_pai.chi_card) != 0 or len(copy_pai.pon_card) != 0:
            men_zen = False

        for i in range(0, len(copy_pai.pon_card)):
            if copy_pai.pon_card[i][0] == 1 or copy_pai.pon_card[i][0] == 9 or copy_pai.pon_card[i][0] == 11 or copy_pai.pon_card[i][0] == 19 or copy_pai.pon_card[i][0] == 21 or copy_pai.pon_card[i][0] == 29:
                min_ko_19 = min_ko_19 + 1
                if copy_pai.pon_card[i][0] == chanfon:
                    yaku.chan_fon = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                if copy_pai.pon_card[i][0] == menfon:
                    yaku.men_fon = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                if copy_pai.pon_card[i][0] == 34:
                    yaku.haku = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                if copy_pai.pon_card[i][0] == 35:
                    yaku.fa = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                if copy_pai.pon_card[i][0] == 36:
                    yaku.chun = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
            else :
                min_ko_28 = min_ko_28 + 1
        for i in range(0, len(copy_pai.kan_card)):
            if copy_pai.kan_card[i][1] != 0:
                men_zen = False
            if copy_pai.kan_card[i][0] == 1 or copy_pai.kan_card[i][0] == 9 or copy_pai.kan_card[i][0] == 11 or copy_pai.kan_card[i][0] == 19 or copy_pai.kan_card[i][0] == 21 or copy_pai.kan_card[i][0] == 29:
                if copy_pai.kan_card[i][1] != 0:
                    min_kan_19 = min_kan_19 + 1
                else :
                    an_kan_19 = an_kan_19 + 1
                if copy_pai.kan_card[i][0] == chanfon:
                    yaku.chan_fon = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                if copy_pai.kan_card[i][0] == menfon:
                    yaku.men_fon = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                if copy_pai.kan_card[i][0] == 34:
                    yaku.haku = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                if copy_pai.kan_card[i][0] == 35:
                    yaku.fa = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                if copy_pai.kan_card[i][0] == 36:
                    yaku.chun = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
            else :
                if copy_pai.kan_card[i][1] != 0:
                    min_kan_28 = min_kan_28 + 1
                else :
                    an_kan_28 = an_kan_28 + 1

        #
        #check mentsu
        kokushi = kokushi_check(copy_pai)
        if not kokushi and chankan == -1:
            return yaku

        
        if len(copy_pai.card14) == 2:
            pair = copy_pai.card14[0]
            ten_pai_fu = True
            pin_hu = True
        elif not kokushi and len(copy_pai.card14) > 2:
            done = False

            for i in range(0, len(copy_pai.card14) - 1):
                if done:
                    break
                
                #fine pair
                remain = copy_pai.card14
                if copy_pai.card14[i] == copy_pai.card14[i + 1]:
                    pair = copy_pai.card14[i]
                    if pair == chanfon or pair == menfon or pair >= 34:
                        pin_hu = False
                    else :
                        pin_hu = True
                    remain = np.delete(remain, [i, i + 1])
                    mentsu = np.zeros((0, 3))
                    pei_ko = 0
                    i_pei_ko_with_pair = 0

                    #check meld
                    j = len(remain) - 1
                    while True:
                        if j <= 0:
                            done = True
                            break
                        
                        if remain[j] >= 30:
                            if remain[j] == remain[j - 1] and remain[j] == remain[j - 2]:
                                # ton ton ton
                                mentsu = np.append(mentsu, [[remain[j], remain[j], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 2, j - 1, j])
                                j = j - 3
                                continue
                            else :
                                break
                        elif remain[j] >= 20:
                            if remain[j] == remain[j - 1] and remain[j] == remain[j - 2]:
                                # 1s 1s 1s
                                mentsu = np.append(mentsu, [[remain[j], remain[j], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 2, j - 1, j])
                                j = j - 3
                                continue
                            elif remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 2] == 1:
                                # 1s 2s 3s
                                mentsu = np.append(mentsu, [[remain[j - 2], remain[j - 1], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 2, j - 1, j])
                                j = j - 3
                                continue
                            elif j >= 3 and remain[j - 1] == remain[j - 2] and remain[j - 1] == remain[j - 3]:
                                # 1s 2s 2s 2s 2s 3s
                                mentsu = np.append(mentsu, [[remain[j - 3], remain[j - 2], remain[j - 1]]], axis = 0)
                                remain = np.delete(remain, [j - 3, j - 2, j - 1])
                                j = j - 3
                                continue
                            elif j >= 3 and remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 3] == 1:
                                # 1s 2s 2s 3s 3s 4s
                                mentsu = np.append(mentsu, [[remain[j - 3], remain[j - 2], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 3, j - 2, j])
                                j = j - 3
                                continue
                            elif j >= 5 and remain[j] - remain[j - 2 ] == 1 and remain[j - 2] - remain[j - 4] == 1 and remain[j - 2] == remain[j - 3]:
                                # 1s 1s 2s 2s 3s 3s
                                if j > 10 and remain[j] - remain[j - 2] == 1 and remain[j - 2] - remain[j - 4] == 1 and remain[j - 4] - remain[j - 6] == 1 and remain[j - 6] - remain[j - 8] == 1 and remain[j - 8] - remain[j - 10] == 1 and pair == remain[j - 10] - 1:
                                    ten_pai_fu = False
                                pei_ko = pei_ko + 1
                                if pair == remain[j - 2] - 2:
                                    i_pei_ko_with_pair = 3
                                    if pair == last_pai or remain[j - 2] == last_pai:
                                        ten_pai_fu = False

                                mentsu = np.append(mentsu, [[remain[j - 4], remain[j - 2], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 4, j - 2, j])
                                j = j - 3
                                continue
                            else :
                                break
                        elif remain[j] >= 10:
                            if remain[j] == remain[j - 1] and remain[j] == remain[j - 2]:
                                # 1s 1s 1s
                                mentsu = np.append(mentsu, [[remain[j - 2], remain[j - 1], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 2, j - 1, j])
                                j = j - 3
                                continue
                            elif remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 2] == 1:
                                # 1s 2s 3s
                                mentsu = np.append(mentsu, [[remain[j - 2], remain[j - 1], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 2, j - 1, j])
                                j = j - 3
                                continue
                            elif j >= 3 and remain[j - 1] == remain[j - 2] and remain[j - 1] == remain[j - 3]:
                                # 1s 2s 2s 2s 2s 3s
                                mentsu = np.append(mentsu, [[remain[j - 3], remain[j - 2], remain[j - 1]]], axis = 0)
                                remain = np.delete(remain, [j - 3, j - 2, j - 1])
                                j = j - 3
                                continue
                            elif j >= 3 and remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 3] == 1:
                                # 1s 2s 2s 3s 3s 4s
                                mentsu = np.append(mentsu, [[remain[j - 3], remain[j - 2], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 3, j - 2, j])
                                j = j - 3
                                continue
                            elif j >= 5 and remain[j] - remain[j - 2 ] == 1 and remain[j - 2] - remain[j - 4] == 1 and remain[j - 2] == remain[j - 3]:
                                # 1s 1s 2s 2s 3s 3s
                                if j > 10 and remain[j] - remain[j - 2] == 1 and remain[j - 2] - remain[j - 4] == 1 and remain[j - 4] - remain[j - 6] == 1 and remain[j - 6] - remain[j - 8] == 1 and remain[j - 8] - remain[j - 10] == 1 and pair == remain[j - 10] - 1:
                                    ten_pai_fu = False
                                pei_ko = pei_ko + 1
                                if pair == remain[j - 2] - 2:
                                    i_pei_ko_with_pair = 2
                                    if pair == last_pai or remain[j - 2] == last_pai:
                                        ten_pai_fu = False

                                mentsu = np.append(mentsu, [[remain[j - 4], remain[j - 2], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 4, j - 2, j])
                                j = j - 3
                                continue
                            else :
                                break
                        elif remain[j] >= 0:
                            if remain[j] == remain[j - 1] and remain[j] == remain[j - 2]:
                                # 1s 1s 1s
                                mentsu = np.append(mentsu, [[remain[j - 2], remain[j - 1], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 2, j - 1, j])
                                j = j - 3
                                continue
                            elif remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 2] == 1:
                                # 1s 2s 3s
                                mentsu = np.append(mentsu, [[remain[j - 2], remain[j - 1], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 2, j - 1, j])
                                j = j - 3
                                continue
                            elif j >= 3 and remain[j - 1] == remain[j - 2] and remain[j - 1] == remain[j - 3]:
                                # 1s 2s 2s 2s 2s 3s
                                mentsu = np.append(mentsu, [[remain[j - 3], remain[j - 2], remain[j - 1]]], axis = 0)
                                remain = np.delete(remain, [j - 3, j - 2, j - 1])
                                j = j - 3
                                continue
                            elif j >= 3 and remain[j] - remain[j - 1] == 1 and remain[j - 1] - remain[j - 3] == 1:
                                # 1s 2s 2s 3s 3s 4s
                                mentsu = np.append(mentsu, [[remain[j - 3], remain[j - 2], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 3, j - 2, j])
                                j = j - 3
                                continue
                            elif j >= 5 and remain[j] - remain[j - 2 ] == 1 and remain[j - 2] - remain[j - 4] == 1 and remain[j - 2] == remain[j - 3]:
                                # 1s 1s 2s 2s 3s 3s
                                if j > 10 and remain[j] - remain[j - 2] == 1 and remain[j - 2] - remain[j - 4] == 1 and remain[j - 4] - remain[j - 6] == 1 and remain[j - 6] - remain[j - 8] == 1 and remain[j - 8] - remain[j - 10] == 1 and pair == remain[j - 10] - 1:
                                    ten_pai_fu = False
                                pei_ko = pei_ko + 1
                                if pair == remain[j - 2] - 2:
                                    i_pei_ko_with_pair = 1
                                    if pair == last_pai or remain[j - 2] == last_pai:
                                        ten_pai_fu = False

                                mentsu = np.append(mentsu, [[remain[j - 4], remain[j - 2], remain[j]]], axis = 0)
                                remain = np.delete(remain, [j - 4, j - 2, j])
                                j = j - 3
                                continue
                            else :
                                break

        if chi_toi_check(copy_pai):
            chi_toi = True
            yaku.chi_toi = True

        for i in range(0, len(mentsu)):
            if mentsu[i][0] == mentsu[i][1]:
                an_ko = True
                if mentsu[i][0] == copy_pai.ron_tile:
                    an_ko = False
                
                if mentsu[i][0] == 34:
                    yaku.haku = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                    if an_ko:
                        an_ko_19 = an_ko_19 + 1
                    else :
                        min_ko_19 = min_ko_19 + 1
                    tan_yao = False
                elif mentsu[i][0] == 35:
                    yaku.fa = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                    if an_ko:
                        an_ko_19 = an_ko_19 + 1
                    else :
                        min_ko_19 = min_ko_19 + 1
                    tan_yao = False
                elif mentsu[i][0] == 36:
                    yaku.chun = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                    if an_ko:
                        an_ko_19 = an_ko_19 + 1
                    else :
                        min_ko_19 = min_ko_19 + 1
                    tan_yao = False
                elif mentsu[i][0] == chanfon:
                    yaku.chan_fon = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                    if mentsu[i][0] == menfon:
                        yaku.men_fon = True
                        yaku.han = yaku.han + 1
                    if an_ko:
                        an_ko_19 = an_ko_19 + 1
                    else :
                        min_ko_19 = min_ko_19 + 1
                    tan_yao = False
                elif mentsu[i][0] == menfon:
                    yaku.men_fon = True
                    yaku.yaku_nashi = False
                    yaku.han = yaku.han + 1
                    if an_ko:
                        an_ko_19 = an_ko_19 + 1
                    else :
                        min_ko_19 = min_ko_19 + 1
                    tan_yao = False
                elif mentsu[i][0] == 1 or mentsu[i][0] == 9 or mentsu[i][0] == 11 or mentsu[i][0] == 19 or mentsu[i][0] == 21 or mentsu[i][0] == 29:
                    if an_ko:
                        an_ko_19 = an_ko_19 + 1
                    else :
                        min_ko_19 = min_ko_19 + 1
                    tan_yao = False
                else :
                    if an_ko:
                        an_ko_28 = an_ko_28 + 1
                    else :
                        min_ko_28 = min_ko_28 + 1
            else :
                if not pin_hu:
                    continue
                if not men_zen:
                    pin_hu = False
                    continue
                if an_kan_19 != 0 or an_kan_28 != 0 or an_ko_19 != 0 or an_ko_28 != 0:
                    pin_hu = False
                    continue
                if (mentsu[i][0] == last_pai and mentsu[i][2] != 9 and mentsu[i][2] != 19 and mentsu[i][2] != 29) or (mentsu[i][2] == last_pai and mentsu[i][0] != 1 and mentsu[i][0] != 11 and mentsu[i][0] != 21):
                    ten_pai_fu = False

        #check mentsu
        #

        #count fu
        fu = 20
        fu += min_ko_28 * 2
        fu += an_ko_28 * 4
        fu += min_ko_19 * 4
        fu += an_ko_19 * 8
        fu += min_kan_28 * 8
        fu += an_kan_28 * 16
        fu += min_kan_19 * 16
        fu += an_kan_19 * 32
        if pair == chanfon:
            fu += 2
        if pair == menfon:
            fu += 2
        if pair >= 34:
            fu += 2
        if copy_pai.draw_tile != -1:
            fu += 2
        if men_zen and copy_pai.ron_tile != -1:
            fu += 10
        fu += ten_pai_fu * 2
        if pin_hu and copy_pai.draw_tile != -1:
            fu = 20
        elif pin_hu and copy_pai.ron_tile != -1:
            fu = 30
        elif fu <= 100:
            fu = fu % 10 * 10
        else :
            fu = 110
        if chi_toi:
            fu = 25
        yaku.fu = fu

        #
        #check yaku
        if yaku.akadora > 0:
            yaku.han += yaku.akadora
        #dora
        for d in dora:
            for i in copy_pai.card14:
                if i == d:
                    yaku.dora += 1
                    yaku.han += 1
            for i in copy_pai.pon_card:
                if i[0] == d:
                    yaku.dora += 3
                    yaku.han += 3
            for i in copy_pai.kan_card:
                if i[0] == d:
                    yaku.dora += 4
                    yaku.han += 4
            for i in copy_pai.chi_card:
                for j in range(0, 3):
                    if i[j] == d:
                        yaku.dora += 1
                        yaku.han += 1
        #uradora
        for d in uradora:
            for i in copy_pai.card14:
                if i == d:
                    yaku.dora += 1
                    yaku.han += 1
            for i in copy_pai.pon_card:
                if i[0] == d:
                    yaku.dora += 3
                    yaku.han += 3
            for i in copy_pai.kan_card:
                if i[0] == d:
                    yaku.dora += 4
                    yaku.han += 4
            for i in copy_pai.chi_card:
                for j in range(0, 3):
                    if i[j] == d:
                        yaku.dora += 1
                        yaku.han += 1
        #pinhu
        if pei_ko == 2:
            chi_toi = False
        if pin_hu and not ten_pai_fu and not chi_toi:
            yaku.pin_hu = True
            yaku.han += 1
            yaku.yaku_nashi = False
        #tanyao
        for p in copy_pai.card14:
            if p == 1 or p == 9 or p == 11 or p == 19 or p == 21 or p >= 29:
                tan_yao = False
        for i in range(0, len(copy_pai.chi_card)):
            for j in range(0, 3):
                if copy_pai.chi_card[i][j] == 1 or copy_pai.chi_card[i][j] == 9 or copy_pai.chi_card[i][j] == 11 or copy_pai.chi_card[i][j] == 19 or copy_pai.chi_card[i][j] == 21 or copy_pai.chi_card[i][j] >= 29:
                    tan_yao = False
        if tan_yao:
            yaku.tan_yao = True
            yaku.han += 1
            yaku.yaku_nashi = False
        #tsumo
        if men_zen and copy_pai.draw_tile != -1:
            yaku.men_zen_tsusmo = True
            yaku.han += 1
            yaku.yaku_nashi = False
        #rinshan
        if rinshan:
            yaku.rin_shan = True
            yaku.han += 1
            yaku.yaku_nashi = False
        #chankan
        if chankan != 0:
            yaku.chan_kan = True
            yaku.han += 1
            yaku.yaku_nashi = False
        #haitei
        if last and copy_pai.draw_tile != -1:
            yaku.hai_tei = True
            yaku.han += 1
            yaku.yaku_nashi = False
        #hotei
        if last and copy_pai.ron_tile != -1:
            yaku.houtei = True
            yaku.han += 1
            yaku.yaku_nashi = False
        #w richi
        if first and copy_pai.richi:
            yaku.w_richi = True
            yaku.han += 2
            yaku.yaku_nashi = False
        #richi
        if copy_pai.richi and not yaku.w_richi:
            yaku.richi = True
            yaku.han += 1
            yaku.yaku_nashi = False
        #ibatsu
        if ibatsu:
            yaku.i_ba_tsu = True
            yaku.han += 1
            yaku.yaku_nashi = False
        #toitoi
        if min_kan_19 + min_kan_28 + min_ko_19 + min_ko_28 + an_kan_19 + an_kan_28 + an_ko_19 + an_ko_28 == 4:
            yaku.toi_toi = True
            yaku.han += 2
            yaku.yaku_nashi = False
        #sanshukuJ
        pin = np.zeros(7)
        man = np.zeros(7)
        sou = np.zeros(7)
        for i in range(0, len(copy_pai.chi_card)):
            min_num = 50
            for j in range(0, 3):
                if copy_pai.chi_card[i][j] < min_num:
                    min_num = copy_pai.chi_card[i][j]
            if min_num > 20:
                sou[int(min_num) - 21] += 1
            elif min_num > 10:
                man[int(min_num) - 11] += 1
            else :
                pin[int(min_num) - 1] += 1
        for i in range(0, len(mentsu)):
            if mentsu[i][0] == mentsu[i][1]:
                continue
            if mentsu[i][0] > 20:
                sou[int(mentsu[i][0]) - 21] += 1
            elif mentsu[i][0] > 10:
                man[int(mentsu[i][0]) - 11] += 1
            else :
                pin[int(mentsu[i][0]) - 1] += 1
        if i_pei_ko_with_pair != 0:
            if i_pei_ko_with_pair == 1:
                for i in range(0, 7):
                    if pin[i] > 0:
                        pin[i - 1] += 1
                        break
            if i_pei_ko_with_pair == 2:
                for i in range(0, 7):
                    if man[i] > 0:
                        man[i - 1] += 1
                        break
            if i_pei_ko_with_pair == 3:
                for i in range(0, 7):
                    if sou[i] > 0:
                        sou[i - 1] += 1
                        break
        for i in range(0, 7):
            if pin[i] > 0 and man[i] > 0 and sou[i] > 0:
                yaku.san_shuku_j = True
                yaku.yaku_nashi = False
                if men_zen:
                    yaku.han += 2
                else :
                    yaku.han += 1
                break
        #sanshukuK
        pin = np.zeros(9)
        man = np.zeros(9)
        sou = np.zeros(9)
        for i in copy_pai.pon_card:
            if i[0] >= 30:
                continue
            elif i[0] > 20:
                sou[int(i[0]) - 21] += 1
            elif i[0] > 10:
                man[int(i[0]) - 11] += 1
            else :
                pin[int(i[0]) - 1] += 1
        for i in copy_pai.kan_card:
            if i[0] >= 30:
                continue
            elif i[0] > 20:
                sou[int(i[0]) - 21] += 1
            elif i[0] > 10:
                man[int(i[0]) - 11] += 1
            else :
                pin[int(i[0]) - 1] += 1
        for i in mentsu:
            if i[0] != i[1]:
                continue
            if i[0] >= 30:
                continue
            elif i[0] > 20:
                sou[int(i[0] - 21)] += 1
            elif i[0] > 10:
                man[int(i[0] - 11)] += 1
            else :
                pin[int(i[0] - 1)] += 1
        for i in range(0, 9):
            if pin[i] > 0 and man[i] > 0 and sou[i] > 0:
                yaku.san_shuku_k = True
                yaku.yaku_nashi = False
                yaku.han += 2
                break 
        #ikki
        pin = np.zeros(3)
        man = np.zeros(3)
        sou = np.zeros(3)
        for i in copy_pai.chi_card:
            min_num = 50
            for j in range(0, 3):
                if min_num > i[j]:
                    min_num = i[j]
            if min_num == 1:
                pin[0] += 1
            elif min_num == 4:
                pin[1] += 1
            elif min_num == 7:
                pin[2] += 1
            elif min_num == 11:
                man[0] += 1
            elif min_num == 14:
                man[1] += 1
            elif min_num == 17:
                man[2] += 1
            elif min_num == 21:
                sou[0] += 1
            elif min_num == 24:
                sou[1] += 1
            elif min_num == 27:
                sou[2] += 1
        for i in mentsu:
            min_num = i[0]
            if min_num == 1:
                pin[0] += 1
            elif min_num == 4:
                pin[1] += 1
            elif min_num == 7:
                pin[2] += 1
            elif min_num == 11:
                man[0] += 1
            elif min_num == 14:
                man[1] += 1
            elif min_num == 17:
                man[2] += 1
            elif min_num == 21:
                sou[0] += 1
            elif min_num == 24:
                sou[1] += 1
            elif min_num == 27:
                sou[2] += 1
        if (pin[0] > 0 and pin[1] > 0 and pin[2] > 0) or (man[0] > 0 and man[1] > 0 and man[2] > 0) or (sou[0] > 0 and sou[1] > 0 and sou[2] > 0):
            yaku.ikki = True
            yaku.yaku_nashi = False
            if men_zen:
                yaku.han += 2
            else :
                yaku.han += 1
        #sananko
        if an_kan_19 + an_kan_28 + an_ko_19 + an_ko_28 == 3:
            yaku.san_an_ko = True
            yaku.yaku_nashi = False
            yaku.han += 2
        #sankantsu
        if min_kan_19 + an_kan_19 + min_kan_28 + an_kan_28 == 3:
            yaku.san_kan_tsu = True
            yaku.yaku_nashi = False
            yaku.han += 2
        #ryanpeiko
        if pei_ko == 2 and men_zen:
            yaku.ryan_pei_ko = True
            yaku.yaku_nashi = False
            yaku.han += 3
        #ipeiko
        if pei_ko == 1 and not chi_toi and men_zen:
            yaku.i_pei_ko = True
            yaku.yaku_nashi = False
            yaku.han += 1
        #chitoi
        if chi_toi and pei_ko != 2:
            yaku.chi_toi = True
            yaku.yaku_nashi = False
            yaku.han += 2
        if True:
            #chiitsu
            chin = True
            hon = True
            color = []
            for i in copy_pai.card14:
                color.append(i / 10)
            for i in copy_pai.chi_card:
                color.append(i[0] / 10) 
                color.append(i[0] / 10) 
                color.append(i[0] / 10) 
            for i in copy_pai.pon_card:
                color.append(i[0] / 10)
                color.append(i[0] / 10) 
                color.append(i[0] / 10) 
            for i in copy_pai.kan_card:
                color.append(i[0] / 10) 
                color.append(i[0] / 10) 
                color.append(i[0] / 10) 
            for i in range(1, len(color)):
                if color[i] != color[0] or color[0] == 3:
                    chin = False
                    break
            if chin:
                yaku.chin_i_tsu = True
                yaku.yaku_nashi = False
                if men_zen:
                    yaku.han += 6
                else :
                    yaku.han += 5
            #honitsu
            honiro = np.zeros(4)
            for i in range(0, 14):
                honiro[int(color[i])] += 1
            if (honiro[0] > 0 and honiro[1] > 0) or (honiro[0] > 0 and honiro[2] > 0) or (honiro[1] > 0 and honiro[2] > 0):
                hon = False
            if hon and not chin:
                yaku.hon_i_tsu = True
                yaku.yaku_nashi = False
                if men_zen:
                    yaku.han += 3
                else :
                    yaku.han += 2
        #junchan
        junchan = True
        if yaku.chi_toi:
            junchan = False
        for i in copy_pai.chi_card:
            min_num = 50
            for j in range(0, 3):
                if i[j] < min_num:
                    min_num = i[j]
            if not (min_num % 10 == 1 or min_num % 10 == 7):
                junchan = False
                break
        for i in copy_pai.pon_card:
            if i[0] >= 30 or not (i[0] % 10 == 1 or i[0] % 10 == 9):
                junchan = False
                break
        for i in copy_pai.kan_card:
            if i[0] >= 30 or not (i[0] % 10 == 1 or i[0] % 10 == 9):
                junchan = False
                break
        for i in mentsu:
            if i[0] == i[1]:
                if i[0] >= 30 or not (i[0] % 10 == 1 or i[0] % 10 == 9):
                    junchan = False
                    break
            else :
                if not (i[0] % 10 == 1 or i[0] % 10 == 7):
                    junchan = False
                    break
        if junchan:
            yaku.jun_chan = True
            yaku.yaku_nashi = False
            if men_zen:
                yaku.han += 3
            else :
                yaku.han += 2
        #honroto
        if min_kan_19 + min_ko_19 + an_kan_19 + an_ko_19 == 4 and (pair == 1 or pair == 9 or pair == 11 or pair == 19 or pair == 21 or pair == 29):
            yaku.hon_ro_tou = True
            yaku.yaku_nashi = False
            yaku.han += 2
        if chi_toi:
            honroto = True
            for i in copy_pai.card14:
                if not (i == 1 or i == 0 or i == 11 or i == 19 or i == 21 or i >= 29):
                    honroto = False
                    break
            if honroto:
                yaku.hon_ro_tou = True
                yaku.yaku_nashi = False
                yaku.han += 2
        #chanta
        chanta = True
        if yaku.chi_toi:
            chanta = False
        if not (pair % 10 == 1 or pair % 10 == 9 or pair >= 30):
            chanta = False
        for i in copy_pai.chi_card:
            min_num = 50
            for j in range(0, 3):
                if i[j] < min_num:
                    min_num = i[j]
            if not (min_num % 10 == 1 or min_num % 10 == 7):
                chanta = False
                break
        for i in copy_pai.pon_card:
            if not (i[0] % 10 == 1 or i[0] % 10 == 9 or i[0] >= 30):
                chanta = False
                break
        for i in copy_pai.kan_card:
            if not (i[0] % 10 == 1 or i[0] % 10 == 9 or i[0] >= 30):
                chanta = False
                break
        for i in mentsu:
            if i[0] == i[1]:
                if not (i[0] % 10 == 1 or i[0] % 10 == 9 or i[0] >= 30):
                    chanta = False
                    break
            else :
                if not (i[0] % 10 == 1 or i[0] % 10 == 7):
                    chanta = False
                    break
        if chanta and not yaku.hon_ro_tou:
            yaku.chan_ta = True
            yaku.yaku_nashi = False
            if men_zen:
                yaku.han += 2
            else :
                yaku.han += 1
        #shosangen
        sangen = 0
        if yaku.haku:
            sangen += 1
        if yaku.fa:
            sangen += 1
        if yaku.chun:
            sangen += 1
        if sangen == 2 and pair >= 34:
            yaku.shou_san_gen = True
            yaku.yaku_nashi = False
            yaku.han += 2
        if True:
            #daisushi
            wind = np.zeros(4)
            wind_num = 0
            for i in copy_pai.pon_card:
                if i[0] == 30:
                    wind[0] = 1
                elif i[0] == 31:
                    wind[1] = 1
                elif i[0] == 32:
                    wind[2] = 1
                elif i[0] == 33:
                    wind[3] = 1
            for i in copy_pai.kan_card:
                if i[0] == 30:
                    wind[0] = 1
                elif i[0] == 31:
                    wind[1] = 1
                elif i[0] == 32:
                    wind[2] = 1
                elif i[0] == 33:
                    wind[3] = 1
            for i in mentsu:
                if i[0] == 30:
                    wind[0] = 1
                elif i[0] == 31:
                    wind[1] = 1
                elif i[0] == 32:
                    wind[2] = 1
                elif i[0] == 33:
                    wind[3] = 1
            for i in wind:
                wind_num += i
            if wind_num == 4:
                yaku.dai_su_shi = True
                yaku.han = 13
                yaku.yaku_nashi = False
            #shosushi
            if wind_num == 3 and pair >= 30 and pair <= 33:
                yaku.shou_su_shi = True
                yaku.han = 13
                yaku.yaku_nashi = False
        #chinroto
        if len(copy_pai.chi_card) == 0:
            chinroto = True
            if yaku.chi_toi:
                chinroto = False
            if len(copy_pai.chi_card) != 0:
                chinroto = False
            for i in copy_pai.pon_card:
                if i[0] >= 30 or not (i[0] % 10 == 1 or i[0] % 10 == 9):
                    chinroto = False
                    break
            for i in copy_pai.kan_card:
                if i[0] >= 30 or not (i[0] % 10 == 1 or i[0] % 10 == 9):
                    chinroto = False
                    break
            for i in mentsu:
                if i[0] == i[1]:
                    if i[0] >= 30 or not (i[0] % 10 == 1 or i[0] % 10 == 9):
                        chinroto = False
                        break
                else :
                    chinroto = False
                    break
            if chinroto:
                yaku.chin_ro_tou = True
                yaku.han = 13
                yaku.yaku_nashi = False
        #sukantsu
        if min_kan_19 + min_kan_28 + an_kan_19 + an_kan_28 == 4:
            yaku.su_kan_tsu = True
            yaku.han = 13
            yaku.yaku_nashi = False
        #daisangen
        if sangen == 3:
            yaku.dai_san_gen = True
            yaku.han = 13
            yaku.yaku_nashi = False
        #tsuiso
        if len(copy_pai.chi_card) == 0:
            tsuiso = True
            if yaku.chi_toi:
                tsuiso = False
            for i in copy_pai.pon_card:
                if i[0] < 30:
                    tsuiso = False
                    break
            for i in copy_pai.kan_card:
                if i[0] < 30:
                    tsuiso = False
                    break
            for i in mentsu:
                if i[0] < 30:
                    tsuiso = False
                    break
            if tsuiso:
                yaku.tsu_i_so = True
                yaku.han = 13
                yaku.yaku_nashi = False
        #ryuiro
        ryuiro = True
        if yaku.chi_toi:
            ryuiro = False
        for i in copy_pai.pon_card:
            if not (i[0] == 22 or i[0] == 23 or i[0] == 24 or i[0] == 26 or i[0] == 28 or i[0] == 35):
                ryuiro = False
                break
        for i in copy_pai.kan_card:
            if not (i[0] == 22 or i[0] == 23 or i[0] == 24 or i[0] == 26 or i[0] == 28 or i[0] == 35):
                ryuiro = False
                break
        for i in copy_pai.chi_card:
            for j in range(0, 3):
                if not (i[j] == 22 or i[j] == 23 or i[j] == 24 or i[j] == 26 or i[j] == 28 or i[j] == 35):
                    ryuiro = False
                    break
        for i in mentsu:
            for j in range(0, 3):
                if not (i[j] == 22 or i[j] == 23 or i[j] == 24 or i[j] == 26 or i[j] == 28 or i[j] == 35):
                    ryuiro = False
                    break
        if ryuiro:
            yaku.ryu_i_so = True
            yaku.han = 13
            yaku.yaku_nashi = False
        #tenho
        if first and menfon == 30:
            yaku.ten_ho = True
            yaku.han = 13
            yaku.yaku_nashi = False
        #chiho
        if first and menfon != 30:
            yaku.chi_ho = True
            yaku.han = 13
            yaku.yaku_nashi = False
        #suanko
        if an_kan_19 + an_kan_28 + an_ko_19 + an_ko_28 == 4:
            yaku.su_an_ko = True
            yaku.han = 13
            yaku.yaku_nashi = False
        #suankodanki
        if yaku.su_an_ko and pair == last_pai:
            yaku.su_an_ko_dan_ki = True
            yaku.han = 13
            yaku.yaku_nashi = False
        #kokushi
        if kokushi:
            yaku.kokushi = True
            yaku.han = 13
            yaku.yaku_nashi = False
            #kokushi13
            for i in range(len(copy_pai.card14) - 1):
                if copy_pai.card14[i] == copy_pai.card14[i + 1]:
                    if copy_pai.card14[i] == pair:
                        yaku.kokushi_13 = True
        if True:
            #juseikyuren
            kyu = True
            jusei = False
            k = np.zeros(9)
            if men_zen and yaku.chin_i_tsu:
                for i in copy_pai.card14:
                    k[i % 10 - 1] += 1
                for i in range(0, 9):
                    if i == 0 or i == 8:
                        if k[i] < 3:
                            kyu = False
                    else :
                        if k[i] < 1:
                            kyu = False
            else :
                kyu = False
            if kyu:
                if last_pai % 10 == 1 or last_pai % 10 == 9:
                    if (last_pai % 10 == 1 and k[0] == 4) or (last_pai % 10 == 9 and k[8] == 4):
                        jusei = True
                else :
                    if k[int(last_pai) % 10 - 1] == 2:
                        jusei = True
            if jusei and kyu:
                yaku.jun_sei_kyu_ren = True
                yaku.han = 13
                yaku.yaku_nashi = False
            if not jusei and kyu:
                yaku.kyu_ren = True
                yaku.han = 13
                yaku.yaku_nashi = False

        return yaku

'''
def card_encoding(pai):
    card = []
    pai.red_trans()

    i = 0
    while i < len(pai.check_card13) - 1:
        if pai.check_card13[i] == pai.check_card13[i + 1]:
            if i >= len(pai.check_card13) - 2:
                break
            if pai.check_card13[i] != pai.check_card13[i + 2]:
                if pai.check_card13[i + 2] - pai.check_card13[i] == 1:
                    card.append([2, 0])
                elif pai.check_card13[i + 2] - pai.check_card13[i] == 2 and pai.check_card13[i] / 10 == pai.check_card13[i + 2] / 10:
                    card.append([2, 1])
                else :
                    card.append([2, 2])
                i += 2
            else :
                if i >= len(pai.check_card13) - 3:
                    break
                if pai.check_card13[i] != pai.check_card13[i + 3]:
                    if pai.check_card13[i + 3] - pai.check_card13[i] == 1:
                        card.append([3, 0])
                    elif pai.check_card13[i + 3] - pai.check_card13[i] == 2 and pai.check_card13[i] / 10 == pai.check_card13[i + 3] / 10:
                        card.append([3, 1])
                    else :
                        card.append([3, 2])
                    i += 3
                else :
                    if i >= len(pai.check_card13) - 4:
                        break
                    if pai.check_card13[i + 4] - pai.check_card13[i] == 1:
                        card.append([4, 0])
                    elif pai.check_card13[i + 4] - pai.check_card13[i] == 2 and pai.check_card13[i] / 10 == pai.check_card13[i + 4] / 10:
                        card.append([4, 1])
                    else :
                        card.append([4, 2])
                    i += 4
        else :
            if pai.check_card13[i + 1] - pai.check_card13[i] == 1:
                card.append([1, 0])
            elif pai.check_card13[i - 1] - pai.check_card13[i] == 2 and pai.check_card13[i] / 10 == pai.check_card13[i + 1] / 10:
                card.append([1, 1])
            else :
                card.append([1, 2])
            i += 1

    card.append([len(pai.check_card13) - i, 3])
    
    return card


def shan_ten_check_13(pai):
    card = copy.deepcopy(card_encoding(pai))
    back_up  = copy.deepcopy(card)

    # shan ten number
    min_s = 8
    s = 8
    #total mentsu number
    k = (len(pai.check_card13) - 1) / 3
    #pair
    p = 0
    #mentsu
    g = 0
    #datsu
    g1 = 0

    #check chitoi
    pair_num = 0
    for i in card:
        if i[0] >= 2:
            pair_num += 1
    min_s = 6 - pair_num
    #check kokushi
    kokushi = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in pai.card13:
        if i == 1:
            kokushi[0] += 1
        elif i == 9:
            kokushi[1] += 1
        elif i == 11:
            kokushi[2] += 1
        elif i == 19:
            kokushi[3] += 1
        elif i == 21:
            kokushi[4] += 1
        elif i >= 29:
            kokushi[int(i) - 24] += 1
    kokushi_pair = False
    kokushi_s = 0
    for i in kokushi:
        if i > 1:
            kokushi_pair = True
        if i == 0:
            kokushi_s += 1
    if kokushi_pair:
        kokushi_s -= 1
    if min_s > kokushi_s:
        min_s = kokushi_s
       

    for i in range(len(card)):
        #find pair
        card = copy.deepcopy(back_up)
        if card[i][0] >= 2:
            card[i][0] -= 2
            p = 1
            g = 0
            g1 = 0
            s = 2 * (k - g) - g1 - p
            c = 3 * g + 2 * g1 + 2 * p
            c_rem = len(pai.check_card13) - 2

            j = 0
            while j < len(card):
                if card[j][0] >= 3:
                    card[j][0] -= 3
                    g += 1
                    c_rem -= 3
                    s = 2 * (k - g) - g1 - p
                    c = 3 * g + 2 * g1 + 2 * p
                    if g + g1 > k or c_rem < s - c:
                        break
                elif j < len(card) - 2 and card[j][1] == 0 and card[j + 1][1] == 0 and card[j][0] > 0 and card[j + 1][0] > 0 and card[j + 2][0] > 0:
                    card[j][0] -= 1
                    card[j + 1][0] -= 1
                    card[j + 2][0] -= 1
                    g += 1
                    c_rem -= 3
                    s = 2 * (k - g) - g1 - p
                    c = 3 * g + 2 * g1 + 2 * p
                    if g + g1 > k or c_rem < s - c:
                        break
                else :
                    j += 1

            j = 0
            while j < len(card):
                if card[j][0] >= 2:
                    card[j][0] -= 2
                    g1 += 1
                    c_rem -= 2
                    s = 2 * (k - g) - g1 - p
                    c = 3 * g + 2 * g1 + 2 * p
                    if g + g1 > k or c_rem < s - c:
                        break
                elif j < len(card) - 1 and card[j][1] == 0 and card[j][0] > 0 and card[j + 1][0] > 0:
                    card[j][0] -= 1
                    card[j + 1][0] -= 1
                    g1 += 1
                    c_rem -= 2
                    s = 2 * (k - g) - g1 - p
                    c = 3 * g + 2 * g1 + 2 * p
                    if g + g1 > k or c_rem < s - c:
                        break
                else :
                    j += 1

            if min_s > s:
                min_s = s

    p = 0
    g = 0
    g1 = 0
    s = 2 * (k - g) - g1 - p
    c = 3 * g + 2 * g1 + 2 * p
    c_rem = len(pai.check_card13)

    card = copy.deepcopy(back_up)
    j = 0
    while j < len(card):
        if card[j][0] >= 3:
            card[j][0] -= 3
            g += 1
            c_rem -= 3
            s = 2 * (k - g) - g1 - p
            c = 3 * g + 2 * g1 + 2 * p
            if g + g1 > k or c_rem < s - c:
                break
        elif j < len(card) - 2 and card[j][1] == 0 and card[j + 1][1] == 0 and card[j][0] > 0 and card[j + 1][0] > 0 and card[j + 2][0] > 0:
            card[j][0] -= 1
            card[j + 1][0] -= 1
            card[j + 2][0] -= 1
            g += 1
            c_rem -= 3
            s = 2 * (k - g) - g1 - p
            c = 3 * g + 2 * g1 + 2 * p
            if g + g1 > k or c_rem < s - c:
                break
        else :
            j += 1

    j = 0
    while j < len(card):
        if card[j][0] >= 2:
            card[j][0] -= 2
            g1 += 1
            c_rem -= 2
            s = 2 * (k - g) - g1 - p
            c = 3 * g + 2 * g1 + 2 * p
            if g + g1 > k or c_rem < s - c:
                break
        elif j < len(card) - 1 and card[j][1] == 0 and card[j][0] > 0 and card[j + 1][0] > 0:
            card[j][0] -= 1
            card[j + 1][0] -= 1
            g1 += 1
            c_rem -= 2
            s = 2 * (k - g) - g1 - p
            c = 3 * g + 2 * g1 + 2 * p
            if g + g1 > k or c_rem < s - c:
                break
        else :
            j += 1

    if min_s > s:
        min_s = s

    return min_s'''

table_13 = {}
f = open('lookup_table_13.DAT', 'rb')
while True:
    i_1 = int.from_bytes(f.read(8), 'big')
    i_2 = int.from_bytes(f.read(1), 'big')
    if i_1 is 0 and i_2 is 0:
        break
    table_13[i_1] = i_2
    if i_2 == 8:
        table_13[i_1] = -1
f.close()
old_table_13_size = len(table_13)

table_14 = {}
f = open('lookup_table_14.DAT', 'rb')
while True:
    i_1 = int.from_bytes(f.read(8), 'big')
    i_2 = int.from_bytes(f.read(1), 'big')
    if i_1 is 0 and i_2 is 0:
        break
    table_14[i_1] = i_2
    if i_2 == 8:
        table_14[i_1] = -1
f.close()
old_table_14_size = len(table_14)

effective_table = {}
effective_file_decoder('effective_table.DAT', effective_table)
old_effective_table_size = len(effective_table)


#
#must do red_trans outside this function
def find_shan_ten_table(pai, num = 13):
    if num == 13:
        old_pattern = card_encoding(pai)
        pattern = pattern_sort(old_pattern)
        result = array_encoder(pattern)
        
        s = table_13.get(result)
        if s == None:
            s = shan_ten_check_13(card_encoding(pai), len(pai.card13))
            kokushi_s = kokushi_shan_ten_check(pai, 13)
            if kokushi_s > s:
                table_13[result] = s
            else :
                table_13[result] = kokushi_s

        return s
    else :
        old_pattern = card_encoding(pai, 14)
        pattern = pattern_sort(old_pattern)
        result = array_encoder(pattern)

        s = 6
        s = table_14.get(result)
        if s == None:
            s = shan_ten_check_14(card_encoding(pai, 14), len(pai.card14))
            kokushi_s = kokushi_shan_ten_check(pai, 14)
            if kokushi_s > s:
                table_14[result] = s
            else :
                table_14[result] = kokushi_s

        return s

def find_effective_table(arr):
    result = effective_encoder(arr)

    eff = effective_table.get(result)
    if eff == None:
        eff = effective_card(arr)
        effective_table[result] = eff
    
    return eff

def update_table():
    file_encoder('lookup_table_13.DAT', table_13, old_table_13_size)
    file_encoder('lookup_table_14.DAT', table_14, old_table_14_size)
    effective_file_encoder('effective_table.DAT', effective_table, old_effective_table_size)
    





def foo(i):
    test = 0
            




if __name__ == '__main__':
    yama = CardStack()
    test = HandCard()
    #test.deal(yama.deal()[0])
    test.deal([3,3,3,4,5,15,16,17,18,18,35,35,35])
    #test.min_kan(35, 1)
    test.draw(18)
    #print(test.card14)
    #print(test.kan_card)
    #print(win_check(test))

    #print(tenpai_check(test))
    #richi_check(test)
    #point_check(test, 30, 30, False, False, False, False, False, 0, [], [])

    #find_shan_ten_table(test)


    start = time.time()

    shan_ten = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    #print(tenpai_check(test))
    
    for i in range(0, 10000):
    #    win_check(test)
        yama.reset(0)
        test.deal(yama.deal()[0])#[1,2,3,5,6,7,11,12,13,15,16,17,30])
        test.draw(yama.draw())
        #test.deal([1,2,3,5,6,7,11,12,11,15,16,17,30])
        #test.draw(7)
        richi_check(test)
    #    foo(test)
    #    shan_ten[int(shan_ten_check_13(card_encoding(test), len(test.card13)))] += 1

    update_table()

    end = time.time()

    print(end - start)
    print(shan_ten)




    fuck = {'123':123,'456':345,(3,2,1):321}

    #try :
    #    print(fuck[5])
    #except :
    #    print("fuck")


