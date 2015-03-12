import numpy as np
import cv2

class Card(object): 
    def __init__(self, contour, img):
        self.Contour = contour 
        self.Img = img
        
    def warp_contour(self): 
        pts = self.Contour.reshape(4, 2)
        rect = np.zeros((4, 2), dtype = "float32")
        s = pts.sum(axis = 1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[0] - bl[0]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[0] - tl[0]) ** 2))
        heightA = np.sqrt(((tr[1] - br[1]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[1] - bl[1]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([
    	[0, 0],
    	[maxWidth - 1, 0],
    	[maxWidth - 1, maxHeight - 1],
    	[0, maxHeight - 1]], dtype = "float32")        
        M = cv2.getPerspectiveTransform(rect, dst)
        warp = cv2.warpPerspective(self.Img, M, (maxWidth, maxHeight))
        return warp

    def save_img(self, path): 
        warp = self.warp_contour( )
        cv2.imwrite(path, warp)
        
    def highlight_card_in_img(self):
        cv2.drawContours(self.Img, [self.Contour], -1, (0, 255, 0), 3)
        
        
