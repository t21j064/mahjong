import sys
import math
from Agari import Agari  # Agari をインポート

class PointCalculation:
    def __init__(self, tile):
        self.tile = tile
        self.point = 0
        self.hu = 20
        self.titoi = 0
        self.pinfu = 0
        
    def check_tile_count(self):
        """ 枚数のエラー確認 """
        All = 0
        for count in self.tile:
            if count > 4:
                print("一つの牌が5枚以上あります")
                sys.exit()
            else:
                All += count
        print(All)
    
    def check_agari(self):
        """ あがりかくにん """
        agari = Agari(self.tile)
        if agari.check_agari():
            print("あがり")
        else:
            #七対子確認
            pair = 0
            for count in self.tile:
                if count == 2:  # 2枚で雀頭とみなす
                    pair += 1
            #国士無双
            required_tile = [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]
            counts = [self.tile[i] for i in required_tile]# 必要な牌の枚数を取得
            # 必要牌が全て1枚以上存在するかチェック
            if all(count >= 1 for count in counts):
                # 必要牌の中にちょうど1種類だけ2枚（雀頭）があるかチェック
                if sum(count == 2 for count in counts) == 1:
                    self.point = self.point +13
                    print("国士無双")
                    sys.exit()
                else:
                    sys.exit()
            elif pair == 7:
                return 
            else:
                print("あがってません")
                sys.exit()
    
    def check_yaku(self):
        """ 面前確認 """
        print("鳴いている（y）鳴いていない（n）入力してください")
        naki = input()

        if naki =="y":
            print("yを入力しました")
            print("ツモっている（y）ツモっていない（n）入力してください")
            tumo = input()
            if tumo =="y":
                self.hu = self.hu + 2
        elif naki =="n":
            print("nを入力しました")
            print("リーチしている（y）していない（n）入力してください")
            riti = input()
            print("ツモっている（y）ツモっていない（n）入力してください")
            tumo = input()
            if tumo =="y":
                self.point += 1
                self.hu = self.hu + 2
                print("門前自摸")
            elif tumo =="n":
                self.hu = self.hu + 10
                print("ツモってない")
            else:
                print("yかnを入力してください")
                sys.exit()
            if riti =="y":
                self.point += 1
                print("リーチ")
            elif riti =="n":
                print("リーチしてない")
            else:
                print("yかnを入力してください")
                sys.exit()
                
        else:
            print("yかnを入力してください")
            sys.exit()

        """役確認"""
        melds = 0 # 暗刻
        pair = 0  # 雀頭
        for count in self.tile:
            if count >= 3:  # 3枚以上で暗刻とみなす
                melds += 1
            elif count == 2:  # 2枚で雀頭とみなす
                pair += 1

        # タンヤオ
        if all(self.tile[i] == 0 for i in [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]):
            self.point += 1
            print("タンヤオ")

        # 平和
        honor_tiles = [27, 28, 29, 30, 31, 32, 33]  # 東南西北白發中
        if naki == "n" and melds == 0 and pair == 1:
            if all(self.tile[i] == 0 for i in honor_tiles):
                if all(self.tile[i] <= 2 for i in range(34)):
                    self.point += 1
                    self.pinfu += 1
                    print("平和")

        # 一盃口
        peiko = 0
        if naki == "n":
            for i in range(0, 27, 9):
                for j in range(0, 7):
                    if self.tile[i+j] >= 2 and self.tile[i+j+1] >= 2 and self.tile[i+j+2] >= 2:
                        peiko = peiko + 1
                        if peiko == 2:
                            self.point +=2
                            print("二盃口")
                        else:
                            self.point += 1
                            print("一盃口")
                        break

        # 役牌
        yakuhai_tiles = [27, 28, 29, 30, 31, 32, 33]
        for yakuhai in yakuhai_tiles:
            if self.tile[yakuhai] >= 3:
                self.point += 1
                print("役牌")

        # 七対子
        if pair == 7:
            self.point += 2
            self.titoi += 1
            print("七対子")

        # 対々和
        if melds == 4:
            self.point += 2
            print("対々和")

        # 三色同刻
        for i in range(9):
            if self.tile[i] >= 3 and self.tile[i+9] >= 3 and self.tile[i+18] >= 3:
                self.point += 2
                print("三色同刻")

        # 三色同順
        for i in range(7):
            if all(self.tile[i+j] >= 1 and self.tile[i+9+j] >= 1 and self.tile[i+18+j] >= 1 for j in range(3)):
                self.point += 2
                print("三色同順")

        # 混老頭
        if all(self.tile[i] == 0 for i in range(1, 8)) and \
           all(self.tile[i] == 0 for i in range(10, 17)) and \
           all(self.tile[i] == 0 for i in range(19, 26)):
            self.point += 2
            print("混老頭")

        # 一気通貫
        for i in range(0, 27, 9):
            if all(self.tile[i+j] >= 1 for j in range(9)):
                if naki == "n":
                    self.point += 2
                else:
                    self.point += 1
                print("一気通貫")

        # 小三元
        sangen_count = 0
        for tile_index in [31, 32, 33]:
            if self.tile[tile_index] >= 3:
                sangen_count += 1
        if sangen_count == 2 and pair == 1:
            self.point += 2
            print("小三元")

        # 混一色
        if any(self.tile[i] > 0 for i in range(0, 9)) and \
           all(self.tile[i] == 0 for i in range(9, 27)) and \
           any(self.tile[i] > 0 for i in range(27, 34)):
            if naki == "n":
                self.point += 3
            else:
                self.point += 2
            print("混一色")

        if any(self.tile[i] > 0 for i in range(9, 18)) and \
           all(self.tile[i] == 0 for i in range(0, 9)) and \
           all(self.tile[i] == 0 for i in range(18, 27)) and \
           any(self.tile[i] > 0 for i in range(27, 34)):
            if naki == "n":
                self.point += 3
            else:
                self.point += 2
            print("混一色")

        if any(self.tile[i] > 0 for i in range(18, 27)) and \
           all(self.tile[i] == 0 for i in range(0, 18)) and \
           any(self.tile[i] > 0 for i in range(27, 34)):
            if naki == "n":
                self.point += 3
            else:
                self.point += 2
            print("混一色")

        # 清一色
        if any(self.tile[i] > 0 for i in range(0, 9)) and \
           all(self.tile[i] == 0 for i in range(9, 34)):
            if naki == "n":
                self.point += 6
            else:
                self.point += 5
            print("清一色")

        if any(self.tile[i] > 0 for i in range(9, 18)) and \
           all(self.tile[i] == 0 for i in range(0, 9)) and \
           all(self.tile[i] == 0 for i in range(18, 34)):
            if naki == "n":
                self.point += 6
            else:
                self.point += 5
            print("清一色")

        if any(self.tile[i] > 0 for i in range(18, 27)) and \
           all(self.tile[i] == 0 for i in range(0, 18)) and \
           all(self.tile[i] == 0 for i in range(27, 34)):
            if naki == "n":
                self.point += 6
            else:
                self.point += 5
            print("清一色")

        # 緑一色
        ryu_tiles = [19, 20, 21, 23, 25, 32]
        if any(self.tile[i] > 0 for i in ryu_tiles) and all(self.tile[i] == 0 for i in range(34) if i not in ryu_tiles):
            self.point += 13
            print("緑一色")

        # 字一色
        if any(self.tile[i] > 0 for i in range(27, 34)) and all(self.tile[i] == 0 for i in range(27)):
            self.point += 13
            print("字一色")
            
        #大三元
        required_tile = [31,32,33]
        sangen_count = 0
        for tile_index in required_tile:
            if self.tile[tile_index] >= 3:  # 3枚以上で刻子または槓子とみなす
                sangen_count += 1
        if sangen_count == 3:  # 大三元の条件
                self.point = self.point +13
                print("大三元")


        #四暗刻
        if melds == 4 and pair == 1 and naki == "n":  # 四暗刻の条件
            self.point = self.point +13
            print("四暗刻")
        
        """符計算 """
        if melds > 0 and melds <5:
            print("数牌2～8暗刻の数は？")
            anko = int(input())
            self.hu = self.hu + anko*4
            print("字牌と数牌1・9暗刻の数は？")
            anko1 = int(input())
            self.hu = self.hu + anko1*8
            print("数牌2～8明刻の数は？")
            minko = int(input())
            self.hu = self.hu + minko*2
            print("字牌と数牌1・9明刻の数は？")
            minko1 = int(input())
            self.hu = self.hu + minko1*4
        for yakuhai in yakuhai_tiles:
            if self.tile[yakuhai] == 2:
               self.hu = self.hu + 2   
        
        return self.point
    
    def check_point(self):
        """符計算に必要な情報取得 """
        sum = 0 #合計点数
        
        #親か子を確認
        print("親（y）子（n）入力してください")
        oya = input()
        if oya =="y":
            print("親です")
        elif oya =="n":
            print("子です")
        else:
            print("yかnを入力してください")
            sys.exit()
        
        #待ち方を確認
        print("待ち牌が一種類ですか（y）二種類以上ですか（n）入力してください")
        mati = input()
        if mati =="y":
            print("一種類")
            self.hu = self.hu + 2
        elif mati =="n":
            print("二種類以上")
        else:
            print("yかnを入力してください")
            sys.exit()
        
        """点数計算"""
        #符を10単位で繰り上げ
        fu1 = math.ceil(self.hu / 10) * 10
        if self.titoi > 0:
            fu1 = 25
            self.hu =25
        elif self.pinfu >0:
            print("平和ツモです(y)違う(n)")
            pinfu1 = input()
            if pinfu1 =="y":
                print("平和ツモ")
                fu1 = 20
                self.hu =20
            elif pinfu1 =="n":
                print("平和ロン")
            else:
                print("yかnを入力してください")
                sys.exit()
        print(f"総飜数: {self.point}")
        print(f"総符数: {self.hu}")
        
        #飜数が５以上の場合
        if oya =="y": #親の場合
            if self.point == 5:
                sum = 12000
            elif self.point == 6 or self.point == 7:
                sum = 18000
            elif self.point == 8 or self.point == 9 or self.point == 10:
                sum = 24000
            elif self.point == 11 or self.point == 12:
                sum = 36000
            elif self.point >= 13:
                sum = 48000
        else: #子の場合
            if self.point == 5:
                sum = 8000
            elif self.point == 6 or self.point == 7:
                sum = 12000
            elif self.point == 8 or self.point == 9 or self.point == 10:
                sum = 16000
            elif self.point == 11 or self.point == 12:
                sum = 24000
            elif self.point >= 13:
                sum = 32000
                
        #飜数が4以下の場合
        if oya =="y": #親の場合
            if self.point == 1:
                if fu1 ==20:
                    print("エラー")
                    sys.exit()
                elif fu1 ==25:
                    print("エラー")
                    sys.exit()
                elif fu1 ==30:
                    sum = 1500
                elif fu1 ==40:
                    sum = 2000
                elif fu1 ==50:
                    sum = 2400
                elif fu1 ==60:
                    sum = 2900
                elif fu1 ==70:
                    sum = 3400
            if self.point == 2:
                if fu1 ==20:
                    sum = 2000
                elif fu1 ==25:
                    sum = 2400
                elif fu1 ==30:
                    sum = 2900
                elif fu1 ==40:
                    sum = 3900
                elif fu1 ==50:
                    sum = 4800
                elif fu1 ==60:
                    sum = 5800
                elif fu1 ==70:
                    sum = 6800
            if self.point == 3:
                if fu1 ==20:
                    sum = 3900
                elif fu1 ==25:
                    sum = 4800
                elif fu1 ==30:
                    sum = 5800
                elif fu1 ==40:
                    sum = 7700
                elif fu1 ==50:
                    sum = 9600
                elif fu1 ==60:
                    sum = 11600
                elif fu1 ==70:
                    sum = 12000
            if self.point == 4:
                if fu1 ==20:
                    sum = 7700
                elif fu1 ==25:
                    sum = 9600
                elif fu1 ==30:
                    sum = 11600
                elif fu1 ==40:
                    sum = 12000
                elif fu1 ==50:
                    sum = 12000
                elif fu1 ==60:
                    sum = 12000
                elif fu1 ==70:
                    sum = 12000
        else: #子の場合
            if self.point == 1:
                if fu1 ==20:
                    print("エラー")
                    sys.exit()
                elif fu1 ==25:
                    print("エラー")
                    sys.exit()
                elif fu1 ==30:
                    sum = 1000
                elif fu1 ==40:
                    sum = 1300
                elif fu1 ==50:
                    sum = 1600
                elif fu1 ==60:
                    sum = 2000
                elif fu1 ==70:
                    sum = 2300
            if self.point == 2:
                if fu1 ==20:
                    sum = 1300
                elif fu1 ==25:
                    sum = 1600
                elif fu1 ==30:
                    sum = 2000
                elif fu1 ==40:
                    sum = 2600
                elif fu1 ==50:
                    sum = 3200
                elif fu1 ==60:
                    sum = 3900
                elif fu1 ==70:
                    sum = 4500
            if self.point == 3:
                if fu1 ==20:
                    sum = 2600
                elif fu1 ==25:
                    sum = 3200
                elif fu1 ==30:
                    sum = 3900
                elif fu1 ==40:
                    sum = 5200
                elif fu1 ==50:
                    sum = 6400
                elif fu1 ==60:
                    sum = 7700
                elif fu1 ==70:
                    sum = 8000
            if self.point == 4:
                if fu1 ==20:
                    sum = 5200
                elif fu1 ==25:
                    sum = 6400
                elif fu1 ==30:
                    sum = 7700
                elif fu1 ==40:
                    sum = 8000
                elif fu1 ==50:
                    sum = 8000
                elif fu1 ==60:
                    sum = 8000
                elif fu1 ==70:
                    sum = 8000
            
        return sum
        
        