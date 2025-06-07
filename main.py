from templatematcher import TemplateMatcher  # TemplateMatcher をインポート
from PointCalculation import PointCalculation  # PointCalculation をインポート

All =0   # 全体の枚数を格納する変数
tile = [] # 各テンプレートのマッチ数を格納するリスト
tile2 = [0,2,0,2,0,0,0,0,0, #萬子
        0,0,0,0,2,0,2,0,0, #筒子
        0,0,0,0,2,0,0,0,2, #索子
        0,0,2,0, #東南西北
        0,0,0,]#白發中
if __name__ == "__main__":
    # 対象の画像のパス
    img_path = 'img3.png'

    # 1から36までのテンプレートファイルを処理
    for i in range(0, 34):
        # テンプレート画像のパスを動的に生成
        templ_path = f'tiles/tiles{i}.png'

        # インスタンスを作成
        matcher = TemplateMatcher(img_path=img_path, templ_path=templ_path, threshold=0.90)
        
        # テンプレートマッチングを実行
        matcher.perform_match()
        
        # マッチした箇所に赤枠を描画
        dst = matcher.draw_rectangles()
        
        # 結果を表示
        matcher.show_result(dst)
        
        # マッチしたテンプレートの枚数を表示
        print(f'{templ_path} の枚数: {matcher.z}')
        
        #マッチした枚数をそれぞれ格納
        tile.append(matcher.z)
        print(tile[i])
        
        #マッチしたテンプレートの枚数を格納
        All = All +matcher.z
print(f'全ての牌の枚数は {All}')


Calculation = PointCalculation(tile)
Calculation.check_tile_count()
Calculation.check_agari()
Calculation.check_yaku()
sum =Calculation.check_point()
print(f"合計点数: {sum}")