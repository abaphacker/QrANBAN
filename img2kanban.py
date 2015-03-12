import cv2
import detectCards as dc

if __name__ == '__main__':
        img = cv2.imread("/home/harry/python_workspace/kanban2.jpg")
        cards = dc.getCards(img)
        i = 0
        for card in cards:
            i = i + 1
            filename = "/home/harry/python_workspace/cards/card%s.png" % i 
            cv2.imwrite(filename,card)
        
        cv2.imshow('card', card)
        cv2.waitKey()
