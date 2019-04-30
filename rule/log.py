import datetime

class Log:
    def __init__(self, p1 = None, p2 = None, p3 = None, p4 = None):
        self.game_log = []
        self.set_name(p1, p2, p3, p4)
        
        
    def set_name(self, p1, p2, p3, p4):
        if p1 == None:
            p1 = "player 1"
        if p2 == None:
            p2 = "player 2"
        if p3 == None:
            p3 = "player 3"
        if p4 == None:
            p4 = "player 4"
        self.pl1_name = p1
        self.pl2_name = p2
        self.pl3_name = p3
        self.pl4_name = p4
        if len(self.pl1_name) < 8:
            self.pl1_name += "\t"
        if len(self.pl2_name) < 8:
            self.pl2_name += "\t"
        if len(self.pl3_name) < 8:
            self.pl3_name += "\t"
        if len(self.pl4_name) < 8:
            self.pl4_name += "\t"
        if len(self.pl1_name) < 4:
            self.pl1_name += "\t"
        if len(self.pl2_name) < 4:
            self.pl2_name += "\t"
        if len(self.pl3_name) < 4:
            self.pl3_name += "\t"
        if len(self.pl4_name) < 4:
            self.pl4_name += "\t"


    def append_game_log(self, chanfon, oya, kyouku, honba, kyoutaku, dora, uradora, start_deal, draw_stack, discard_stack, final_card):
        self.game_log.append([chanfon, oya, kyouku, honba, kyoutaku, dora, uradora, start_deal, draw_stack, discard_stack, final_card])

    def check_men_fon(self, oya, pl):
        where = (pl - oya) % 4
        if where == 0:
            return "East \t"
        if where == 1:
            return "South\t"
        if where == 2:
            return "West \t"
        if where == 3:
            return "North\t"

    # log for each game
    def write_log_file(self, path):
        file_name = path + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".log"
        f = open(file_name, 'w')

        f.write("+----------------------------+\n")
        f.write("| 1 ~  9 : pin               |\n")
        f.write("|11 ~ 19 : man               |\n")
        f.write("|21 ~ 29 : sou               |\n")
        f.write("|30 ~ 33 : wind              |\n")
        f.write("|     34 : bai               |\n")
        f.write("|     35 : fa                |\n")
        f.write("|     36 : chun              |\n")
        f.write("|     40 : chi               |\n")
        f.write("|     50 : pon               |\n")
        f.write("|     60 : kan               |\n")
        f.write("+----------------------------+\n\n")
        for log in self.game_log:
            f.write("===========================================================================\n")
            if log[0] == 30:
                f.write("East  ")
            else :
                f.write("South ")
            f.write(str(log[2]) + " - " + str(log[3]) + "\t\tdora : " + str(log[5]) + "\t\turaodra : " + str(log[6]) + "\n")
            f.write("===========================================================================\n")
            oya = log[1]
            f.write(self.check_men_fon(oya, 0) + "\tstart   : " + str(log[7][0]) + "\n")
            f.write(self.pl1_name + "\tdraw    : " + str(log[8][0]) + "\n")
            f.write("\t\t\tdiscard : " + str(log[9][0]) + "\n")
            f.write("\t\t\tfinal   : " + str(log[10][0]) + "\n")
            f.write("---------------------------------------------------------------------------\n")
            f.write(self.check_men_fon(oya, 1) + "\tstart   : " + str(log[7][1]) + "\n")
            f.write(self.pl2_name + "\tdraw    : " + str(log[8][1]) + "\n")
            f.write("\t\t\tdiscard : " + str(log[9][1]) + "\n")
            f.write("\t\t\tfinal   : " + str(log[10][1]) + "\n")
            f.write("---------------------------------------------------------------------------\n")
            f.write(self.check_men_fon(oya, 2) + "\tstart   : " + str(log[7][2]) + "\n")
            f.write(self.pl3_name + "\tdraw    : " + str(log[8][2]) + "\n")
            f.write("\t\t\tdiscard : " + str(log[9][2]) + "\n")
            f.write("\t\t\tfinal   : " + str(log[10][2]) + "\n")
            f.write("---------------------------------------------------------------------------\n")
            f.write(self.check_men_fon(oya, 3) + "\tstart   : " + str(log[7][3]) + "\n")
            f.write(self.pl4_name + "\tdraw    : " + str(log[8][3]) + "\n")
            f.write("\t\t\tdiscard : " + str(log[9][3]) + "\n")
            f.write("\t\t\tfinal   : " + str(log[10][3]) + "\n")
            f.write("\n")


        f.close()


    # statistic for game history
    def write_stat_file(self):
        # . . .
        test = 0






if __name__ == '__main__':
    #f = open(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".log", 'w')

    #f.close()

    #print(datetime.datetime.now())

    test = [[1,2,3], [4,5,6]]
    test1 = test + [14]
    #test = []
    test1[0] = 4
    print(test)

    #log = Log()
    #log.append_game_log(30, 1, 1, 0, 0, [1], [],
    # [[1,1,1], [2,2,2], [3,3,3], [4,4,4]],
    #  [[5,5,5], [6,6,6], [7,7,7], [8,8,8]],
    #   [[9,9,9], [8,8,8], [7,7,7], [6,6,6]],
    #    [[5,5,5], [4,4,4], [3,3,3], [2,2,2]])
    #log.write_log_file()

