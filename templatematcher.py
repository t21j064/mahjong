import cv2
import numpy as np
import matplotlib.pyplot as plt

class TemplateMatcher:
    def __init__(self, img_path, templ_path, threshold):
        """
        コンストラクタ
        :param img_path: 対象画像のパス
        :param templ_path: テンプレート画像のパス
        :param threshold: 類似度の閾値 (デフォルト: 0.7)
        """
        self.img = cv2.imread(img_path)
        self.templ = cv2.imread(templ_path)
        self.threshold = threshold
        self.result = None
        self.match_y = None
        self.match_x = None
        self.z = 0  # マッチしたテンプレートの枚数
    
    def perform_match(self):
       """
       テンプレートマッチングを実行し、結果を取得
       """
       # 正規化相互相関演算を実行
       self.result = cv2.matchTemplate(self.img, self.templ, cv2.TM_CCOEFF_NORMED)
       
       # 類似度が閾値以上の座標を取得
       threshold_indices = np.where(self.result >= self.threshold)
       points = list(zip(threshold_indices[1], threshold_indices[0]))  # (x, y) のリスト
       
       # テンプレートのサイズ
       w = self.templ.shape[1]
       h = self.templ.shape[0]

       # 矩形のリストを作成
       rects = []
       scores = []
       for (x, y) in points:
           rects.append([x, y, x + w, y + h])  # 矩形の形式 [x1, y1, x2, y2]
           scores.append(self.result[y, x])    # マッチングスコア

       # 非最大抑制を適用
       indices = cv2.dnn.NMSBoxes(rects, scores, self.threshold, 0.9)

       # 非最大抑制後の結果を取得
       if len(indices) > 0:
           indices = indices.flatten()  # 結果を1次元化
           final_points = [points[i] for i in indices]  # 残った座標を取得
           self.match_x, self.match_y = zip(*final_points) if final_points else ([], [])
       else:
           self.match_x, self.match_y = [], []

       # マッチしたテンプレートの枚数をカウント
       self.z = len(self.match_x)
    
    def draw_rectangles(self):
        """
        マッチした位置に赤い矩形を描画
        """
        # テンプレート画像のサイズ
        w = self.templ.shape[1]
        h = self.templ.shape[0]

        # 対象画像をコピー
        dst = self.img.copy()

        # マッチした箇所に赤枠を描画
        for x, y in zip(self.match_x, self.match_y):
            cv2.rectangle(dst, (x, y), (x + w, y + h), (0, 0, 225), 10)

        return dst

    def show_result(self, dst):
        """
        結果の画像を表示
        :param dst: 赤枠を描画した画像
        """
        plt.imshow(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
        plt.show()
    
    def print_count(self):
        """
        当てはまったテンプレートの枚数を表示
        """
        print(f'枚数　：{self.z}')