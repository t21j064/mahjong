import Agari
class Agari:
    def __init__(self, tehai):
        self.tehai = tehai

    def check_agari(self):
        # 雀頭候補を作成する
        head_list = []
        for index, hai in enumerate(self.tehai):
            if hai >= 2:
                head_list.append(index)

        # 雀頭候補を１つずつ取り出しループ
        for head in head_list:
            # 除外用に手配をコピー
            tehai_copy = self.tehai.copy()

            # 雀頭候補を除外
            tehai_copy[head] -= 2

            # 刻子候補を作成する
            kotsu_list = []
            for index, hai in enumerate(tehai_copy):
                if hai >= 3:
                    kotsu_list.append(index)

            # 刻子候補の全部分集合を作る
            kotsu_all_subset = [[]]
            for kotsu in kotsu_list:
                kotsu_all_subset_copy = kotsu_all_subset.copy()
                for kotsu_subset in kotsu_all_subset_copy:
                    kotsu_all_subset.append([kotsu] + kotsu_subset)

            # 刻子候補を１つ取り出しループ
            for kotsu_subset in kotsu_all_subset:
                # 除外用に手配をコピー
                tehai_copy2 = tehai_copy.copy()

                # 刻子を除外
                for kotsu in kotsu_subset:
                    tehai_copy2[kotsu] -= 3

                # 順子を除外(萬子)
                for i in range(0, 6):
                    hai_count = tehai_copy2[i]
                    tehai_copy2[i] -= hai_count
                    tehai_copy2[i + 1] -= hai_count
                    tehai_copy2[i + 2] -= hai_count

                # 順子を除外(索子)
                for i in range(9, 15):
                    hai_count = tehai_copy2[i]
                    tehai_copy2[i] -= hai_count
                    tehai_copy2[i + 1] -= hai_count
                    tehai_copy2[i + 2] -= hai_count

                # 順子を除外(筒子)
                for i in range(18, 24):
                    hai_count = tehai_copy2[i]
                    tehai_copy2[i] -= hai_count
                    tehai_copy2[i + 1] -= hai_count
                    tehai_copy2[i + 2] -= hai_count

                # 手牌が綺麗に全て除外されたかチェック
                result = all(hai == 0 for hai in tehai_copy2)

                if result:
                    return True

        return False
