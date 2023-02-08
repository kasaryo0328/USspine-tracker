import tkinter as tk            # ウィンドウ作成用
from tkinter import filedialog  # ファイルを開くダイアログ用
import os
from PIL import Image,ImageTk
import Video
import cv2



class Application(tk.Frame):
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
    def create_widgets(self):
        print("make widget")
    
    
    def set_video(self, filename):
        ''' 画像ファイルを開く '''
        if not filename or filename is None:
            return
        
        # 画像ファイルの再読込用に保持
        self.filename = filename
        self.video = Video.Video(self.filename)

        # PillowからNumPy(OpenCVの画像)へ変換
        self.cv_image = self.video.read_frame()

        # 画像の表示
        self.draw_image(self.cv_image)

        # ウィンドウタイトルのファイル名を設定
        self.master.title(self.my_title + " - " + os.path.basename(filename))
        # カレントディレクトリの設定
        os.chdir(os.path.dirname(filename))
    

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
    app = Application(master=root)#Inherit
    app.mainloop()

if __name__ == "__main__":
    main()

    