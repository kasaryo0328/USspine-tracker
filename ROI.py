import cv2
import Video

class ROI:
    def __init__(self,kernel_size, slide_size):
        self.kernel_size = kernel_size
        self.half_kernel = int(self.kernel_size//2)
        self.slide_size = slide_size
        self.kernel_sphere = []
        self.kernel_image = []
    
    def padding_for_ROI(self,target):
        self.image_padding = target.frame.copy()
        self.image_padding = cv2.copyMakeBorder(self.image_padding, self.half_kernel, self.half_kernel, self.half_kernel, self.half_kernel, cv2.BORDER_CONSTANT, 0)

    def get_ROI(self):
        self.kernel_image = []
        self.kernel_sphere = []
        height_image_padding,width_image_padding = self.image_padding.shape
        
        for y in range(self.half_kernel,height_image_padding - self.half_kernel, self.slide_size):
            for x in range(self.half_kernel,width_image_padding - self.half_kernel, self.slide_size):
                self.kernel_sphere.append((x,y))
                Roi = self.image_padding [y-self.half_kernel:y+self.half_kernel , x-self.half_kernel:x+self.half_kernel]
                self.kernel_image.append(Roi)
        
        