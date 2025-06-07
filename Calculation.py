import numpy as np
import matplotlib.pyplot as plt
import sys
from Agari import Agari  # Agari をインポート

tile = [0,1,1,1,0,0,0,0,0, #萬子
        0,0,3,0,3,0,0,0,0, #筒子
        0,0,2,0,1,1,1,0,0, #索子
        0,0,0,0, #東南西北
        0,0,0,]#白發中
All = 0
point = 0 #飜数
melds = 0  # 暗刻の数
pair = 0   # 雀頭の数

""" 枚数のエラー確認 """
for i in range(0,34):
    if tile[i] > 4:
        print("一つの牌が5枚以上あります")
        sys.exit()
    else:
        All = All + tile[i]
print(All)
"""あがりかくにん"""
agari = Agari(tile)
if agari.check_agari():
    print("あがり")
else:
    #国士無双
    required_tile = [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]
    counts = [tile[i] for i in required_tile]# 必要な牌の枚数を取得
    # 必要牌が全て1枚以上存在するかチェック
    if all(count >= 1 for count in counts):
        # 必要牌の中にちょうど1種類だけ2枚（雀頭）があるかチェック
        if sum(count == 2 for count in counts) == 1:
            point = point +13
            print("国士無双")
            sys.exit()
        else:
            sys.exit()
    else:
        print("あがってません")
        sys.exit()

""" 面前確認 """
print("鳴いている（y）鳴いていない（n）入力してください")
naki = input()

if naki =="y":
    print("yを入力しました")
elif naki =="n":
    print("nを入力しました")
    print("リーチしている（y）していない（n）入力してください")
    riti = input()
    print("ツモっている（y）ツモっていない（n）入力してください")
    tumo = input()
    if tumo =="y":
        point += 1
        print("門前自摸")
    elif tumo =="n":
        print("ツモってない")
    else:
        print("yかnを入力してください")
        sys.exit()
    if riti =="y":
        point += 1
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

for count in tile:
    if count >= 3:  # 3枚以上で暗刻とみなす
        melds += 1
    elif count == 2:  # 2枚で雀頭とみなす
        pair += 1

# タンヤオ
if all(tile[i] == 0 for i in [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]):
    point += 1
    print("タンヤオ")

# 平和
honor_tiles = [27, 28, 29, 30, 31, 32, 33]  # 東南西北白發中
if naki == "n" and melds == 0 and pair == 1:
    if all(tile[i] == 0 for i in honor_tiles):
        if all(tile[i] <= 2 for i in range(34)):
            point += 1
            print("平和")

# 一盃口
peiko = 0
if naki == "n":
    for i in range(0, 27, 9):
        for j in range(0, 7):
            if tile[i+j] >= 2 and tile[i+j+1] >= 2 and tile[i+j+2] >= 2:
                peiko = peiko + 1
                if peiko == 2:
                    point +=2
                    print("二盃口")
                else:
                    point += 1
                    print("一盃口")
                break

# 役牌
yakuhai_tiles = [27, 28, 29, 30, 31, 32, 33]
for yakuhai in yakuhai_tiles:
    if tile[yakuhai] >= 3:
        point += 1
        print("役牌")

# 七対子
if pair == 7:
    point += 2
    print("七対子")

# 対々和
if melds == 4:
    point += 2
    print("対々和")

# 三色同刻
for i in range(9):
    if tile[i] >= 3 and tile[i+9] >= 3 and tile[i+18] >= 3:
        point += 2
        print("三色同刻")

# 三色同順
for i in range(7):
    if all(tile[i+j] >= 1 and tile[i+9+j] >= 1 and tile[i+18+j] >= 1 for j in range(3)):
        point += 2
        print("三色同順")

# 混老頭
if all(tile[i] == 0 for i in range(1, 8)) and \
   all(tile[i] == 0 for i in range(10, 17)) and \
   all(tile[i] == 0 for i in range(19, 26)):
    point += 2
    print("混老頭")

# 一気通貫
for i in range(0, 27, 9):
    if all(tile[i+j] >= 1 for j in range(9)):
        if naki == "n":
            point += 2
        else:
            point += 1
        print("一気通貫")

# 小三元
sangen_count = 0
for tile_index in [31, 32, 33]:
    if tile[tile_index] >= 3:
        sangen_count += 1
if sangen_count == 2 and pair == 1:
    point += 2
    print("小三元")

# 混一色
if any(tile[i] > 0 for i in range(0, 9)) and \
   all(tile[i] == 0 for i in range(9, 27)) and \
   any(tile[i] > 0 for i in range(27, 34)):
    if naki == "n":
        point += 3
    else:
        point += 2
    print("混一色")

if any(tile[i] > 0 for i in range(9, 18)) and \
   all(tile[i] == 0 for i in range(0, 9)) and \
   all(tile[i] == 0 for i in range(18, 27)) and \
   any(tile[i] > 0 for i in range(27, 34)):
    if naki == "n":
        point += 3
    else:
        point += 2
    print("混一色")

if any(tile[i] > 0 for i in range(18, 27)) and \
   all(tile[i] == 0 for i in range(0, 18)) and \
   any(tile[i] > 0 for i in range(27, 34)):
    if naki == "n":
        point += 3
    else:
        point += 2
    print("混一色")

# 清一色
if any(tile[i] > 0 for i in range(0, 9)) and \
   all(tile[i] == 0 for i in range(9, 34)):
    if naki == "n":
        point += 6
    else:
        point += 5
    print("清一色")

if any(tile[i] > 0 for i in range(9, 18)) and \
   all(tile[i] == 0 for i in range(0, 9)) and \
   all(tile[i] == 0 for i in range(18, 34)):
    if naki == "n":
        point += 6
    else:
        point += 5
    print("清一色")

if any(tile[i] > 0 for i in range(18, 27)) and \
   all(tile[i] == 0 for i in range(0, 18)) and \
   all(tile[i] == 0 for i in range(27, 34)):
    if naki == "n":
        point += 6
    else:
        point += 5
    print("清一色")

# 緑一色
ryu_tiles = [19, 20, 21, 23, 25, 32]
if any(tile[i] > 0 for i in ryu_tiles) and all(tile[i] == 0 for i in range(34) if i not in ryu_tiles):
    point += 13
    print("緑一色")

# 字一色
if any(tile[i] > 0 for i in range(27, 34)) and all(tile[i] == 0 for i in range(27)):
    point += 13
    print("字一色")
    
#大三元
required_tile = [31,32,33]
sangen_count = 0
for tile_index in required_tile:
    if tile[tile_index] >= 3:  # 3枚以上で刻子または槓子とみなす
        sangen_count += 1
if sangen_count == 3:  # 大三元の条件
        point = point +13
        print("大三元")


#四暗刻
if melds == 4 and pair == 1 and naki == "n":  # 四暗刻の条件
    point = point +13
    print("四暗刻")

print(f"総飜数: {point}")
