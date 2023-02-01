import cv2

class Video:
    def __init__(self,path):
        self.path = path
        self.cap = cv2.VideoCapture(path)
        self.framenum = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.play_time = self.framenum / self.fps
        print("path = {}, width,height = ({},{}), fps,framenum,playtime = ({}/s,{} frames, {:1.1f} seconds)".format(self.path,self.width,self.height,self.fps,self.framenum,self.play_time))
    
    def read_frame(self):
        (self.ret,self.frame) = self.cap.read()
        self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
    
