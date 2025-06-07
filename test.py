def checkAgari(tehai):

    # 雀頭候補を作成する
    headList = []
    for index, hai in enumerate(tehai):
        if hai >= 2:
            headList.append(index)

    # 雀頭候補を１つずつ取り出しループ
    for head in headList:

        # 除外用に手配をコピー
        tehaiCopy = tehai.copy()

        # 雀頭候補を除外
        tehaiCopy[head] -= 2

        # 刻子候補を作成する
        kotsuList = []
        for index, hai in enumerate(tehaiCopy):
            if hai >= 3:
                kotsuList.append(index)

        # 刻子候補の全部分集合を作る
        kotsuAllSubset = [[]]
        for kotsu in kotsuList:
            kotsuAllSubsetCopy = kotsuAllSubset.copy()
            for kotsuSubset in kotsuAllSubsetCopy:
                kotsuAllSubset.append([kotsu] + kotsuSubset)

        # 刻子候補を１つ取り出しループ
        for kotsuSubset in kotsuAllSubset:

            # 除外用に手配をコピー
            tehaiCopy2 = tehaiCopy.copy()

            # 刻子を除外
            for kotsu in kotsuSubset:
                tehaiCopy2[kotsu] -= 3

            # 順子を除外(萬子)
            for i in range(0, 6):
                haiCount = tehaiCopy2[i]
                tehaiCopy2[i] -= haiCount
                tehaiCopy2[i + 1] -= haiCount
                tehaiCopy2[i + 2] -= haiCount

            # 順子を除外(索子)
            for i in range(9, 15):
                haiCount = tehaiCopy2[i]
                tehaiCopy2[i] -= haiCount
                tehaiCopy2[i + 1] -= haiCount
                tehaiCopy2[i + 2] -= haiCount

            # 順子を除外(筒子)
            for i in range(18, 24):
                haiCount = tehaiCopy2[i]
                tehaiCopy2[i] -= haiCount
                tehaiCopy2[i + 1] -= haiCount
                tehaiCopy2[i + 2] -= haiCount

            # 手牌が綺麗に全て除外されたかチェック
            result = True
            for hai in tehaiCopy2:
                if hai != 0:
                    result = False
            
            if result:
                print("あがり")
                return True

    return False
tehai = [1,0,0,0,0,0,0,0,1, #萬子
         1,0,0,0,0,0,0,0,1, #索子
         1,0,0,0,0,0,0,0,1, #筒子
         1,1,1,1, #東南西北
         1,1,2, #白發中
         0,0,0,]#赤　萬子　筒子　索子
checkAgari(tehai)