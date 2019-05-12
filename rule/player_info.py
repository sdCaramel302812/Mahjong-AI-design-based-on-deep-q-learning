import numpy as np

class PlayerInfo:
    want_to_richi = 0
    want_to_tsumo = False

    update_reward = False
    reward = 0

    end_game = False

    can_do_something = False
    can_pon = False
    can_chi = False
    can_kan = False
    can_ron = False
    can_tsumo = False
    can_ankan = False
    can_richi = False

    has_tenpai = False

    just_naki = False

    discard_tile = -1

    time_to_discard = False
    chan_fon = -1
    men_fon = -1
    i_ba_tsu = False
    fu_ri_ten = False
    first = False
    last = False
    rin_shan = False
    chan_kan = 0
    point = 25000
    # -1 : undetermined
    #  0 : don't do anything
    #  1 : pon
    #  2 : kan
    #  3 : chi, order : 1 2 3
    #  4 : chi, order : 2 1 3
    #  5 : chi, order : 3 1 2
    #  6 : ron
    #  7 : tsumo
    action_state = -1

    pon_able_tile = -1
    an_kan_case = -1
    def __init__(self):
        # (tile, ankan : -1 / kakan : 1)
        self.kan_able_list = []
        # (tile, tile, action)
        self.chi_able_list = []
        self.what_to_tenpai = []
        self.tenpai_list = []



if __name__ == '__main__':
    info = PlayerInfo()
    info.kan_able_list.append((10, 20))
    print(info.kan_able_list)
    #info.kan_able_list = np.append(info.kan_able_list, [(20, 30)], axis = 0)
    info.kan_able_list.append([20, 30])
    print(info.kan_able_list[0][1])