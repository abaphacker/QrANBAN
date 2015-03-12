import numpy as np
import cv2
import card as c


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_rects(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    height, width = img.shape[:2]
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            #contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key = cv2.contourArea, reverse = True) #sort big to small
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                if cnt_len < (width*0.25):
                    cnt = cv2.approxPolyDP(cnt, 0.10*cnt_len, True)
                    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                        cnt = cnt.reshape(-1, 2)
                        max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                        if max_cos < 3.8:
                            #TODO: Pruefen ob mittelpunkt der Kontur bereits innnerhalb einer der Square-Konturen  liegt
                            if  not_already_known(squares,  cnt):
                                squares.append(cnt)
                                
    return squares

def not_already_known(squares,  cnt):
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    for sq in squares:
        if cv2.pointPolygonTest(sq,(x,y),False) > 0:
            return False
            
    return True

def getCards(img):
    squares = find_rects(img)
    cards = []
    card = 0
    for sq in squares:
        card = c.Card(sq,  img);
        cards.append(card)
    return cards
