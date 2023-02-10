import tkinter as tk            # ウィンドウ作成用
from tkinter import filedialog  # ファイルを開くダイアログ用
import os
from PIL import Image,ImageTk
import Video
import cv2
import numpy as np




class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.my_title = "USspine-tracker"  # タイトル
        self.back_color = "#FFFFFF"     # 背景色
        
        # ウィンドウの設定
        self.master.title(self.my_title)    # タイトル
        self.master.geometry("600x400")     # サイズ

        self.pil_image = None           # 表示する画像データ
        self.filename = None            # 最後に開いた動画ファイル名
 
        self.create_menu()   # メニューの作成
        self.create_widget() # ウィジェットの作成
        
        
    # -------------------------------------------------------------------------------
    # メニューイベント
    # -------------------------------------------------------------------------------
    def menu_open_clicked(self, event=None):
        # File → Open
        filename = tk.filedialog.askopenfilename(
            filetypes = [("Video file", ".mp4 .avi .mov .wmv")], # ファイルフィルタ
            initialdir = os.getcwd() # カレントディレクトリ
            )
        print (filename)
        # 動画ファイルを設定する
        self.set_video(filename)
        
    def menu_reload_clicked(self, event=None):
        # File → ReLoad
        self.set_video(self.filename)
    
    def menu_quit_clicked(self):
        # ウィンドウを閉じる
        self.master.destroy()
        
    # -------------------------------------------------------------------------------
    # create_menuメソッドを定義
    def create_menu(self):
        self.menu_bar = tk.Menu(self) # Menuクラスからmenu_barインスタンスを生成
 
        self.file_menu = tk.Menu(self.menu_bar, tearoff = tk.OFF)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="Open", command = self.menu_open_clicked, accelerator="Ctrl+O")
        self.file_menu.add_command(label="ReLoad", command = self.menu_reload_clicked, accelerator="Ctrl+R")
        self.file_menu.add_separator() # セパレーターを追加
        self.file_menu.add_command(label="Exit", command = self.menu_quit_clicked)

        self.menu_bar.bind_all("<Control-o>", self.menu_open_clicked) # ファイルを開くのショートカット(Ctrol-Oボタン)

        self.master.config(menu=self.menu_bar) # メニューバーの配置
      
      
    # -------------------------------------------------------------------------------
    #       widget生成
    # -------------------------------------------------------------------------------  
    def create_widget(self):
        print("make widget")

        # ステータスバー相当(親に追加)
        self.statusbar = tk.Frame(self.master)
        self.mouse_position = tk.Label(self.statusbar, relief = tk.SUNKEN, text="mouse position") # マウスの座標
        self.image_position = tk.Label(self.statusbar, relief = tk.SUNKEN, text="image position") # 画像の座標
        self.label_space = tk.Label(self.statusbar, relief = tk.SUNKEN)                           # 隙間を埋めるだけ
        self.image_info = tk.Label(self.statusbar, relief = tk.SUNKEN, text="image info")         # 画像情報
        self.mouse_position.pack(side=tk.LEFT)
        self.image_position.pack(side=tk.LEFT)
        self.label_space.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.image_info.pack(side=tk.RIGHT)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Canvas
        self.canvas = tk.Canvas(self.master, background= self.back_color)
        self.canvas.pack(expand=True,  fill=tk.BOTH)  # この両方でDock.Fillと同じ

        # マウスイベント
        self.master.bind("<Motion>", self.mouse_move)                       # MouseMove
        self.master.bind("<B1-Motion>", self.mouse_move_left)               # MouseMove（左ボタンを押しながら移動）
        self.master.bind("<Button-1>", self.mouse_down_left)                # MouseDown（左ボタン）
        self.master.bind("<Double-Button-1>", self.mouse_double_click_left) # MouseDoubleClick（左ボタン）
        self.master.bind("<MouseWheel>", self.mouse_wheel)                  # MouseWheel
    
    # -------------------------------------------------------------------------------
    # マウスイベント
    # -------------------------------------------------------------------------------

    def mouse_move(self, event):
        ''' マウスの移動時 '''
        # マウス座標
        self.mouse_position["text"] = f"mouse(x, y) = ({event.x: 4d}, {event.y: 4d})"
        
        if self.pil_image == None:
            return

        # 画像座標
        mouse_posi = np.array([event.x, event.y, 1]) # マウス座標(numpyのベクトル)
        mat_inv = np.linalg.inv(self.mat_affine)     # 逆行列（画像→Cancasの変換からCanvas→画像の変換へ）
        image_posi = np.dot(mat_inv, mouse_posi)     # 座標のアフィン変換
        x = int(np.floor(image_posi[0]))
        y = int(np.floor(image_posi[1]))
        if x >= 0 and x < self.pil_image.width and y >= 0 and y < self.pil_image.height:
            # 輝度値の取得
            value = self.pil_image.getpixel((x, y))
            self.image_position["text"] = f"image({x: 4d}, {y: 4d}) = {value}"
        else:
            self.image_position["text"] = "-------------------------"

    def mouse_move_left(self, event):
        ''' マウスの左ボタンをドラッグ '''
        if self.pil_image == None:
            return
        self.translate(event.x - self.__old_event.x, event.y - self.__old_event.y)
        self.redraw_image() # 再描画
        self.__old_event = event

    def mouse_down_left(self, event):
        ''' マウスの左ボタンを押した '''
        self.__old_event = event

    def mouse_double_click_left(self, event):
        ''' マウスの左ボタンをダブルクリック '''
        if self.pil_image == None:
            return
        self.zoom_fit(self.pil_image.width, self.pil_image.height)
        self.redraw_image() # 再描画

    def mouse_wheel(self, event):
        ''' マウスホイールを回した '''
        if self.pil_image == None:
            return

        if (event.delta < 0):
            # 上に回転の場合、縮小
            self.scale_at(0.8, event.x, event.y)
        else:
            # 下に回転の場合、拡大
            self.scale_at(1.25, event.x, event.y)
        
        self.redraw_image() # 再描画
    
    def set_video(self, filename):
        ''' 画像ファイルを開く '''
        if not filename or filename is None:
            return
        
        # 画像ファイルの再読込用に保持
        self.filename = filename
        self.video = Video.Video(self.filename)

        # PillowからNumPy(OpenCVの画像)へ変換
        self.cv_image = self.video.read_frame()
        self.pil_image = Image.fromarray(self.cv_image)
        #cv2.imshow("test",self.cv_image)

        # 画像の表示
        self.draw_image(self.pil_image)

        # ウィンドウタイトルのファイル名を設定
        self.master.title(self.my_title + " - " + os.path.basename(filename))
        # カレントディレクトリの設定
        os.chdir(os.path.dirname(filename))
        
    # -------------------------------------------------------------------------------
    # 描画
    # -------------------------------------------------------------------------------

    def draw_image(self, pil_image):
        
        #if pil_image == None:
            #return
        
        self.canvas.delete("all")

        # キャンバスのサイズ
        #canvas_width = self.canvas.winfo_width()
        #canvas_height = self.canvas.winfo_height()
        
        # 表示用画像を保持
        self.image = ImageTk.PhotoImage(image=pil_image)

        # 画像の描画
        self.canvas.create_image(
                0, 0,               # 画像表示位置(左上の座標)
                anchor='nw',        # アンカー、左上が原点
                image=self.image    # 表示画像データ
                )

    def redraw_image(self):
        ''' 画像の再描画 '''
        if self.pil_image == None:
            return
        self.draw_image(self.pil_image)
    

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Sub_Window1(self.newWindow)
        






class Sub_Window1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
    
    def create_widgets(self):
        print("make widget")

    def quit_window(self):
        self.master.destroy()
        
def main():
    root = tk.Tk()
    app = MainWindow(master=root)#Inherit
    app.mainloop()

if __name__ == "__main__":
    main()

    