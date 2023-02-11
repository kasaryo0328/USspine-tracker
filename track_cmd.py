import cv2
import numpy as np

# Esc キー
ESC_KEY = 0x1b
# s キー
S_KEY = 0x73
# r キー
R_KEY = 0x72
# 特徴点の最大数
MAX_FEATURE_NUM = 500
# 反復アルゴリズムの終了条件
CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
# インターバル （1000 / フレームレート）
INTERVAL = 30
# ビデオデータ
VIDEO_DATA = r"C:\Users\ryohei\Desktop\ORITA210527\M202105271349160017.avi"




class Motion:
    # コンストラクタ
    def __init__(self):
        # 表示ウィンドウ
        cv2.namedWindow("motion")
        # マウスイベントのコールバック登録
        cv2.setMouseCallback("motion", self.onMouse)
        # 映像
        self.video = cv2.VideoCapture(VIDEO_DATA)
        print(self.video.isOpened())
        # インターバル
        self.interval = INTERVAL
        # 現在のフレーム（カラー）
        self.frame = None
        # 現在のフレーム（グレー）
        self.gray_next = None
        # 前回のフレーム（グレー）
        self.gray_prev = None
        # 現在template
        self.temp= None
        #過去のテンプレート
        self.temp_prev=None
        # tempの座標情報
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None
        self.tempsize = 20
        self.top_left = None
        self.bottom_right = None
        #特徴点
        self.features = None
        # 特徴点のステータス
        self.status = None


    # メインループ
    def run(self):
        frame_number=0

        # 最初のフレームの処理
        end_flag, self.frame = self.video.read()
        #print(self.frame.isOpened())
        self.gray_prev = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        while end_flag:
            # グレースケールに変換
            self.gray_next = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # テンプレートが登録されている場合にブロックマッチング,KLTトラッキング
            if self.temp is not None:
                # マッチング
                self.temp_prev = self.temp
                res = cv2.matchTemplate(self.gray_next,self.temp_prev,cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                self.top_left = min_loc
                self.bottom_right = (self.top_left[0] + self.tempsize, self.top_left[1] + self.tempsize)
                self.top=self.top_left[1]
                self.bottom=self.bottom_right[1]
                self.right=self.bottom_right[0]
                self.left=self.top_left[0]
                 # テンプレート更新
                self.refreshTemp()
                
                # 特徴点が登録されている場合にOpticalFlowを計算する
                if self.features is not None:
                    # オプティカルフローの計算、特徴点情報更新
                    features_prev = self.features
                    self.features, self.status, err = cv2.calcOpticalFlowPyrLK( \
                                                    self.temp_prev, \
                                                    self.temp, \
                                                    features_prev, \
                                                    None, \
                                                    winSize = (10, 10), \
                                                    maxLevel = 3, \
                                                    criteria = CRITERIA, \
                                                    flags = 0)

                # フレームに有効な特徴点を描画
                if self.temp is not None:
                    cv2.rectangle(self.frame,self.top_left, self.bottom_right, 255, 2)
                
                if self.features is not None:
                    for feature in self.features:
                        right = self.right+feature[0][0]
                        int_right = int(right)
                        top=self.top+feature[0][1]
                        int_top=int(top)
                        #cv2.circle(self.frame, (feature[0][0], feature[0][1]), 4, (15, 241, 255), -1, 8, 0)
                        cv2.circle(self.frame, (int_right, int_top), 4, (15, 241, 255), -1, 8, 0)
                        #print(feature[0][0]+self.left, ',',feature[0][1]+self.right,',',frame_number)
            cv2.imshow("motion",self.frame)

            # 次のループ処理の準備
            frame_number=frame_number+1
            self.gray_prev = self.gray_next
            end_flag, self.frame = self.video.read()
            #print(frame_number,self.bottom)
            if end_flag:
                self.gray_next = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # インターバル
            key = cv2.waitKey(self.interval)
            # "Esc"キー押下で終了
            if key == ESC_KEY:
                break
            # "s"キー押下で一時停止
            elif key == S_KEY:
                self.interval = 0
            elif key == R_KEY:
                self.interval = INTERVAL
        # 終了処理
        cv2.destroyAllWindows()
        self.video.release()


    # マウスクリックでテンプレート生成,
    def onMouse(self, event, x, y, flags, param):
        # 左クリック以外
        if event != cv2.EVENT_LBUTTONDOWN:
            return

        # 最初のテンプレート作成
        if self.temp is None:
            self.makeTemp(x, y)
            self.makeFeature()
            return
        return


    # テンプレートを作成
    def makeTemp(self, x, y):
        # 特徴点が未登録
        if self.temp is None:
            # ndarrayの作成し特徴点の座標を登録
            self.top=(y-(self.tempsize//2))
            self.left=(x-(self.tempsize//2))
            self.right=self.left+self.tempsize
            self.bottom=self.top+self.tempsize
            self.temp = self.gray_next[self.top:self.bottom,self.left:self.right]

    # template更新
    def refreshTemp(self):
        # 特徴点が未登録でない
        if self.temp is not None:
            self.temp = self.gray_next[self.top:self.bottom,self.left:self.right]
            return
    #特徴点作成
    def makeFeature(self):
        if self.features is None:
            featurepoint = cv2.goodFeaturesToTrack(self.temp,1,0.01,3)
            #cv2.cornerSubPix(self.temp, featurepoint, (10, 10), (-1, -1), CRITERIA)
            self.features = featurepoint

if __name__ == '__main__':
    Motion().run()