from rule.card_stack import CardStack
from rule.hand_card import HandCard
import copy
import time
import numpy as np
from functools import cmp_to_key

def old_card_encoding(pai, num = 13):
    card = []
    pai.red_trans()

    i = 0
    if num == 13:
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

        card.append([len(pai.check_card13) - i, 2])
    else :
        while i < len(pai.check_card14) - 1:
            if pai.check_card14[i] == pai.check_card14[i + 1]:
                if i >= len(pai.check_card14) - 2:
                    break
                if pai.check_card14[i] != pai.check_card14[i + 2]:
                    if pai.check_card14[i + 2] - pai.check_card14[i] == 1:
                        card.append([2, 0])
                    elif pai.check_card14[i + 2] - pai.check_card14[i] == 2 and pai.check_card14[i] / 10 == pai.check_card14[i + 2] / 10:
                        card.append([2, 1])
                    else :
                        card.append([2, 2])
                    i += 2
                else :
                    if i >= len(pai.check_card14) - 3:
                        break
                    if pai.check_card14[i] != pai.check_card14[i + 3]:
                        if pai.check_card14[i + 3] - pai.check_card14[i] == 1:
                            card.append([3, 0])
                        elif pai.check_card14[i + 3] - pai.check_card14[i] == 2 and pai.check_card14[i] / 10 == pai.check_card14[i + 3] / 10:
                            card.append([3, 1])
                        else :
                            card.append([3, 2])
                        i += 3
                    else :
                        if i >= len(pai.check_card14) - 4:
                            break
                        if pai.check_card14[i + 4] - pai.check_card14[i] == 1:
                            card.append([4, 0])
                        elif pai.check_card14[i + 4] - pai.check_card14[i] == 2 and pai.check_card14[i] / 10 == pai.check_card14[i + 4] / 10:
                            card.append([4, 1])
                        else :
                            card.append([4, 2])
                        i += 4
            else :
                if pai.check_card14[i + 1] - pai.check_card14[i] == 1:
                    card.append([1, 0])
                elif pai.check_card14[i - 1] - pai.check_card14[i] == 2 and pai.check_card14[i] / 10 == pai.check_card14[i + 1] / 10:
                    card.append([1, 1])
                else :
                    card.append([1, 2])
                i += 1

        card.append([len(pai.check_card14) - i, 2])
    
    return card

#
#must do red_trans outside this function
def card_encoding(pai, num = 13):
    card = []
    #pai.red_trans()

    pin = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    man = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    sou = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    other = [0, 0, 0, 0, 0, 0, 0]
    if num == 13:
        for i in pai.check_card13:
            if i >= 30:
                other[int(i) - 30] += 1
            elif i > 20:
                sou[int(i) - 21] += 1
            elif i > 10:
                man[int(i) - 11] += 1
            else :
                pin[int(i) - 1] += 1
    else :
        for i in pai.check_card14:
            if i >= 30:
                other[int(i) - 30] += 1
            elif i > 20:
                sou[int(i) - 21] += 1
            elif i > 10:
                man[int(i) - 11] += 1
            else :
                pin[int(i) - 1] += 1

    

    for i in range(0, 7):
        if pin[i] > 0:
            if pin[i + 1] > 0:
                card.append([pin[i], 0])
            elif pin[i + 2] > 0:
                card.append([pin[i], 1])
            else :
                card.append([pin[i], 2])
    if pin[7] > 0:
        if pin[8] > 0:
            card.append([pin[7], 0])
        else :
            card.append([pin[7], 2])
    if pin[8] > 0:
        card.append([pin[8], 2])

    for i in range(0, 7):
        if man[i] > 0:
            if man[i + 1] > 0:
                card.append([man[i], 0])
            elif man[i + 2] > 0:
                card.append([man[i], 1])
            else :
                card.append([man[i], 2])
    if man[7] > 0:
        if man[8] > 0:
            card.append([man[7], 0])
        else :
            card.append([man[7], 2])
    if man[8] > 0:
        card.append([man[8], 2])

    for i in range(0, 7):
        if sou[i] > 0:
            if sou[i + 1] > 0:
                card.append([sou[i], 0])
            elif sou[i + 2] > 0:
                card.append([sou[i], 1])
            else :
                card.append([sou[i], 2])
    if sou[7] > 0:
        if sou[8] > 0:
            card.append([sou[7], 0])
        else :
            card.append([sou[7], 2])
    if sou[8] > 0:
        card.append([sou[8], 2])

    for i in other:
        if i > 0:
            card.append([i, 2])

    return card


def shan_ten_check_13(pai, size):
    card = pai
    back_up  = copy.deepcopy(card)


    # shan ten number
    min_s = 8
    s = 8
    #total mentsu number
    k = int((size - 1) / 3)
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
    '''    #check kokushi
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
        min_s = kokushi_s'''

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
            c_rem = size - 2

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
    c_rem = size

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

    return int(min_s)

def shan_ten_check_14(pai, size):
    card = pai
    back_up  = copy.deepcopy(card)

    # shan ten number
    min_s = 8
    s = 8
    #total mentsu number
    k = int((size - 2) / 3)
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
    '''    #check kokushi
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
        min_s = kokushi_s'''

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
            c_rem = size - 2

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
                elif j < len(card) - 1 and card[j][1] != 2 and card[j][0] > 0 and card[j + 1][0] > 0:
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
    c_rem = size

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
        elif j < len(card) - 1 and card[j][1] != 2 and card[j][0] > 0 and card[j + 1][0] > 0:
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

    return min_s


def kokushi_shan_ten_check(pai, num = 13):
    #check kokushi
    kokushi = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if num == 13:
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
    else :
        for i in pai.card14:
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
    return kokushi_s


def pattern_cmp(x, y):
    sum_x = 0
    sum_y = 0
    for i in range(0, len(x)):
        sum_x += x[i][0] * (i + 1)
    for i in range(0, len(y)):
        sum_y += y[i][0] * (i + 1)
    return sum_x - sum_y

def pattern_sort(pai):
    sum_list = []
    sub_list = []
    i = 0
    while i < len(pai):
        dist = 0
        for j in range(i, len(pai)):
            if pai[j][1] >= 2:
                dist = j - i
                break
        sum1 = 0
        sum2 = 0
        for j in range(0, int(dist) + 1):
            sum1 += (j + 1) * pai[j][0]
            sum2 += (dist - j + 1) * pai[j][0]
        if sum2 > sum1:
            for j in range(0, int((dist + 1) / 2)):
                tmp = pai[j + i][0]
                pai[j + i][0] = pai[int(dist) + i - j][0]
                pai[int(dist) + i - j][0] = tmp
            for j in range(0, int((dist) / 2)):
                tmp = pai[i + j][1]
                pai[i + j][1] = pai[int(dist) + i - 1 - j][1]
                pai[int(dist) + i - 1 - j][1] = tmp
        sum_list.append(max(sum1, sum2))
        sub_list.append(pai[i : i + dist + 1])
        i += dist + 1
    
    sub_list.sort(key = cmp_to_key(pattern_cmp))
    new_pai = sub_list[0]
    for i in range(1, len(sub_list)):
        new_pai = np.append(new_pai, sub_list[i], axis = 0).tolist()
    return new_pai
    

def effective_card(pai, third = False):
    card = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in pai.check_card13:
        card[int(i)] += 1
    back_up = copy.copy(card)
    effective_list = []

    for i in range(1, 37):
        #find pair
        card = copy.copy(back_up)
        if card[i] >= 2:
            card[i] -= 2

            j = 0
            while j < 37:
                if card[j] >= 3:
                    card[j] -= 3
                elif j < 28 and card[j] > 0 and card[j + 1] > 0 and card[j + 2] > 0:
                    card[j] -= 1
                    card[j + 1] -= 1
                    card[j + 2] -= 1
                else :
                    j += 1

            j = 0
            while j < 37:
                if card[j] >= 2:
                    card[j] -= 2
                    effective_list.append(j)
                elif j < 29 and card[j] > 0 and card[j + 1] > 0:
                    card[j] -= 1
                    card[j + 1] -= 1
                    effective_list.append(j)
                    effective_list.append(j + 1)
                    if (j - 1) % 10 != 0:
                        effective_list.append(j - 1)
                    if (j + 2) % 10 != 0:
                        effective_list.append(j + 2)
                elif j < 28 and card[j] > 0 and card[j + 1] == 0 and card[j + 2] > 0 and j % 10 != 9:
                    card[j] -= 1
                    card[j + 2] -= 1
                    effective_list.append(j + 1)
                else :
                    j += 1

            j = 0
            while j < 37:
                if card[j] > 0:
                    effective_list.append(j)
                    if third:
                        if (j - 1) % 10 != 0:
                            effective_list.append(j - 1)
                        if (j + 1) % 10 != 0:
                            effective_list.append(j + 1)
                j += 1


            card = copy.copy(back_up)
            card[i] -= 2

            j = 0
            while j < 37:
                if card[j] >= 2:
                    card[j] -= 2
                    effective_list.append(j)
                elif j < 29 and card[j] > 0 and card[j + 1] > 0:
                    card[j] -= 1
                    card[j + 1] -= 1
                    effective_list.append(j)
                    effective_list.append(j + 1)
                    if (j - 1) % 10 != 0:
                        effective_list.append(j - 1)
                    if (j + 2) % 10 != 0:
                        effective_list.append(j + 2)
                elif j < 28 and card[j] > 0 and card[j + 1] == 0 and card[j + 2] > 0 and j % 10 != 9:
                    card[j] -= 1
                    card[j + 2] -= 1
                    effective_list.append(j + 1)
                else :
                    j += 1

            j = 0
            while j < 37:
                if card[j] >= 3:
                    card[j] -= 3
                elif j < 28 and card[j] > 0 and card[j + 1] > 0 and card[j + 2] > 0:
                    card[j] -= 1
                    card[j + 1] -= 1
                    card[j + 2] -= 1
                else :
                    j += 1

            j = 0
            while j < 37:
                if card[j] > 0:
                    effective_list.append(j)
                    if third:
                        if (j - 1) % 10 != 0:
                            effective_list.append(j - 1)
                        if (j + 1) % 10 != 0:
                            effective_list.append(j + 1)
                j += 1

    card = copy.copy(back_up)

    j = 0
    while j < 37:
        if card[j] >= 3:
            card[j] -= 3
        elif j < 28 and card[j] > 0 and card[j + 1] > 0 and card[j + 2] > 0:
            card[j] -= 1
            card[j + 1] -= 1
            card[j + 2] -= 1
        else :
            j += 1

    j = 0
    while j < 37:
        if card[j] >= 2:
            card[j] -= 2
            effective_list.append(j)
        elif j < 29 and card[j] > 0 and card[j + 1] > 0:
            card[j] -= 1
            card[j + 1] -= 1
            effective_list.append(j)
            effective_list.append(j + 1)
            if (j - 1) % 10 != 0:
                effective_list.append(j - 1)
            if (j + 2) % 10 != 0:
                effective_list.append(j + 2)
        elif j < 28 and card[j] > 0 and card[j + 1] == 0 and card[j + 2] > 0 and j % 10 != 9:
            card[j] -= 1
            card[j + 2] -= 1
            effective_list.append(j + 1)
        else :
            j += 1

    j = 0
    while j < 37:
        if card[j] > 0:
            effective_list.append(j)
            if third:
                if (j - 1) % 10 != 0:
                    effective_list.append(j - 1)
                if (j + 1) % 10 != 0:
                    effective_list.append(j + 1)
        j += 1

    card = copy.copy(back_up)

    j = 0
    while j < 37:
        if card[j] >= 2:
            card[j] -= 2
            effective_list.append(j)
        elif j < 29 and card[j] > 0 and card[j + 1] > 0:
            card[j] -= 1
            card[j + 1] -= 1
            effective_list.append(j)
            effective_list.append(j + 1)
            if (j - 1) % 10 != 0:
                effective_list.append(j - 1)
            if (j + 2) % 10 != 0:
                effective_list.append(j + 2)
        elif j < 28 and card[j] > 0 and card[j + 1] == 0 and card[j + 2] > 0 and j % 10 != 9:
            card[j] -= 1
            card[j + 2] -= 1
            effective_list.append(j + 1)
        else :
            j += 1

    j = 0
    while j < 37:
        if card[j] >= 3:
            card[j] -= 3
        elif j < 28 and card[j] > 0 and card[j + 1] > 0 and card[j + 2] > 0:
            card[j] -= 1
            card[j + 1] -= 1
            card[j + 2] -= 1
        else :
            j += 1

    j = 0
    while j < 37:
        if card[j] > 0:
            effective_list.append(j)
            if third:
                if (j - 1) % 10 != 0:
                    effective_list.append(j - 1)
                if (j + 1) % 10 != 0:
                    effective_list.append(j + 1)
        j += 1


    effective_list.sort()
    # element of effective list would be repeat
    current = 0
    effective_number = 0
    for i in effective_list:
        if current != i:
            effective_number += 4 - back_up[i]
            current = i

    return effective_number

            



def file_encoder(file_name, table, start_point = None):
    if start_point == None:
        start_point = 0
    i = 0
    f = open(file_name, 'ab')
    for key, value in table.items():
        if i >= start_point:
            f.write(int(key).to_bytes(8, 'big'))
            if value == -1:
                f.write(int(8).to_bytes(1, 'big'))
            else :
                f.write(int(value).to_bytes(1, 'big'))
        i += 1
    f.close()
    


def file_decoder(file_name, table):
    f = open(file_name, 'rb')
    while True:
        i_1 = int.from_bytes(f.read(8), 'big')
        i_2 = int.from_bytes(f.read(1), 'big')
        if i_1 is 0 and i_2 is 0:
            break
        table[i_1] = i_2
        if i_2 == 8:
            table[i_1] = -1
    f.close()

def file_combiner(file1, file2, output):
    if file1 == output or file2 == output or file1 == file2 :
        print("parameter can't be same")
        return
    table1 = {}
    table2 = {}
    file_decoder(file1, table1)
    file_decoder(file2, table2)
    file_encoder(output, table1, 0)
    file_encoder(output, table2, 0)


def array_encoder(arr):
    result = 0
    for i in arr:
        result <<= 2
        result |= i[0]
        result <<= 2
        result |= i[1]
    return result
    
def effective_encoder(arr):
    result = 0
    for i in arr:
        result <<= 3
        result |= i

def effective_file_encoder(file_name, table, start_point = None):
    if start_point == None:
        start_point = 0
    i = 0
    f = open(file_name, 'ab')
    for key, value in table.items():
        if i >= start_point:
            f.write(int(key).to_bytes(14, 'big'))
            f.write(int(value).to_bytes(2, 'big'))
        i += 1
    f.close()

def effective_file_decoder(file_name, table):
    f = open(file_name, 'rb')
    while True:
        i_1 = int.from_bytes(f.read(14), 'big')
        i_2 = int.from_bytes(f.read(2), 'big')
        if i_1 is 0 and i_2 is 0:
            break
        table[i_1] = i_2
    f.close()

def create_table_13(iter_time, n):
    yama = CardStack()
    card = HandCard()

    table = {}
    file_decoder('lookup_table_13.DAT', table)
    size = len(table)

    for i in range(0, iter_time):
        yama.reset(0)
        card_list = yama.deal_with_n(n)
        for j in range(0, 4):
            pai = card_list[j]
            card.deal(pai)

            old_pattern = card_encoding(card)
            pattern = pattern_sort(old_pattern)
            result = array_encoder(pattern)

            if table.get(result) == None:
                s = shan_ten_check_13(card_encoding(card), len(card.card13))
                kokushi_s = kokushi_shan_ten_check(card, 13)
                if kokushi_s > s:
                    table[result] = s
                else :
                    table[result] = kokushi_s

    file_encoder('lookup_table_13.DAT', table, size)
    print(len(table))

def create_table_14(iter_time, n):
    yama = CardStack()
    card = HandCard()

    table = {}
    file_decoder('lookup_table_14.DAT', table)
    size = len(table)

    for i in range(0, iter_time):
        yama.reset(0)
        card_list = yama.deal_with_n(n)
        for j in range(0, 4):
            pai = card_list[j]
            card.deal(pai[0 : 13])
            card.draw(pai[13])

            old_pattern = card_encoding(card, 14)
            pattern = pattern_sort(old_pattern)
            result = array_encoder(pattern)

            if table.get(result) == None:
                s = shan_ten_check_14(card_encoding(card, 14), len(card.card14))
                kokushi_s = kokushi_shan_ten_check(card, 14)
                if kokushi_s > s:
                    table[result] = s
                else :
                    table[result] = kokushi_s

    file_encoder('lookup_table_14.DAT', table, size)
    print(len(table))


def test_func():
    test = HandCard()

    test.check_card13 = [1,3,3,4,15,19,22,24,26,30,30,31,33]
    print(effective_card(test, True))


if __name__ == '__main__':
    #yama = CardStack()
    test = HandCard()

    test.check_card13 = [1,3,3,4,15,19,22,24,26,30,30,31,33]
    print(effective_card(test))

    #table = {}

    #yama.reset(0)
    #test.deal([1,2,3,4,5,6,7,18,9,12,12,13,21])
    #test.deal(yama.deal()[0])
    #test.deal([3,3,3,4,5,15,16,17,18,18,35,35,35])
    #test.draw(18)

    #print(shan_ten_check_14(test))


    #ddd = [[4, 1], [4, 0], [3, 1], [2, 1], [1, 2], [1, 2], [1, 0], [2, 1], [3, 2]]
    #print(ddd)
    #new_ddd = pattern_sort(ddd)
    #print(new_ddd)
    
    #shan_ten = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    #start = time.time()

    #create_table_13(100, 13)
    #create_table_14(100, 14)
    #print(shan_ten_check_13(test))
    #for i in range(0, 1000):
    #    yama.reset(0)
    #    test.deal(yama.deal()[0])
    #    shan_ten[int(shan_ten_check_13(card_encoding(test), len(test.card13)))] += 1
    #    shan_ten_check_13(test)

    #for i in range(1000):
    #    card = card_encoding(test)
    #    pattern_sort(card)

    #end = time.time()

    #print(end - start)


    #print(shan_ten)
    #f = open('test.txt', 'rb')
    #num = 1000
    #i_byte = num.to_bytes(52, 'big')
    #print(int.from_bytes( f.read(52), 'big'))
    #print(bin(10))

